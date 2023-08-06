"""
Unpublished work.
Copyright (c) 2021 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: pradeep.garre@teradata.com
Secondary Owner: PankajVinod.Purandare@teradata.com

This file implements several classes which executes analytic functions such as
SQLE functions and UAF functions on Vantage.
File implements classes for following:
    * _AnlyticFunctionExecutor
    * _SQLEFunctionExecutor
    * _TableOperatorExecutor
"""

from teradataml.common.constants import TeradataConstants, TeradataAnalyticFunctionTypes
from teradataml.analytics.json_parser import PartitionKind
from teradataml.analytics.analytic_query_generator import AnalyticQueryGenerator
from teradataml.analytics.json_parser.json_store import _JsonStore
from teradataml.options.display import display
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages, MessageCodes
from teradataml.common.wrapper_utils import AnalyticsWrapperUtils
from teradataml.common.utils import UtilFuncs
from teradataml.table_operators.table_operator_query_generator import TableOperatorQueryGenerator
from teradataml.utils.dtypes import _ListOf
from teradataml.utils.validators import _Validators
import time


class _AnlyticFunctionExecutor:
    """
    Class to hold the common attributes to execute analytic function.
    """
    def __init__(self, func_name, func_type):
        """
        DESCRIPTION:
            Constructor for the class.

        PARAMETERS:
            func_name:
                Required Argument.
                Specifies the name of the analytic function, which is exposed to user.
                Types: str

            func_type:
                Required Argument.
                Specifies whether the argument "func_name" is SQLE, UAF or Table Operator function.
                Types: str

        RAISES:
            TypeError OR ValueError OR TeradataMlException
        """
        self.func_name = func_name
        self._func_type = func_type

        # Input arguments passed, i.e., data members of the dynamic class to be generated.
        self._dyn_cls_data_members = {}

        # Output table arguments list
        self._func_output_args_sql_names = []
        self._func_output_args = []
        self._func_output_table_type = []

        # Generate lists for rest of the function arguments
        self._func_other_arg_sql_names = []
        self._func_other_args = []
        self._func_other_arg_json_datatypes = []
        self.sqlmr_query = None
        self._function_output_table_map = {}
        self._sql_specific_attributes = {}
        self._metadata = _JsonStore.get_function_metadata(self.func_name)
        self._mlresults = []
        self._awu = AnalyticsWrapperUtils()
        self.__build_time = None
        self._is_argument_dataframe = lambda object: type(object).__name__ == "DataFrame"

    @staticmethod
    def _validate_analytic_function_arguments(func_arg_name, func_arg_value, argument, additional_valid_types=None):
        """
        DESCRIPTION:
            Function to validate the analytic function arguments. This function does
            the following validations
                * Checks for missing mandatory argument.
                * Checks for the expected type for argument.
                * Checks for the expected values for argument.
                * Checks for empty value.

        PARAMETERS:
            func_arg_name:
                Required Argument.
                Specifies the name of the argument.
                Type: str

            func_arg_value:
                Required Argument.
                Specifies the value passed to argument 'func_arg_name' in analytic function.
                Type: str OR float OR int OR list

            argument:
                Required Argument.
                Specifies the argument object (_AnlyArgumentBase) containing argument
                information to be validated.
                Type: _AnlyFuncArgument OR _AnlyFuncInput

        RETURNS:
            None

        RAISES:
            ValueError OR TypeError

        EXAMPLES:
            self._validate_analytic_function_arguments("arg", 1, metadata.arguments)
        """
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        py_types = argument.get_python_type()
        if additional_valid_types:
            if isinstance(additional_valid_types, tuple):
                py_types = (py_types, ) + additional_valid_types
            else:
                py_types = (py_types, additional_valid_types)

        argument_info = [func_arg_name,
                         func_arg_value,
                         not argument.is_required(),
                         py_types
                         ]
        _Validators._validate_missing_required_arguments([argument_info])

        # Validate for empty string if argument accepts a column name for either input or output.
        if not argument.is_empty_value_allowed() or argument.is_output_column():
            argument_info.append(True)

        # Validate the permitted values.

        if isinstance(func_arg_value, str) and argument.get_permitted_values():
            if len(argument_info) == 4:
                argument_info.append(True)
            argument_info.append(argument.get_permitted_values())

        # Validate the function arguments.
        _Validators._validate_function_arguments([argument_info])

    def _execute_query(self, persist=False, volatile=False):
        """
        DESCRIPTION:
            Function to execute query on Vantage.

        PARAMETERS:
            persist:
                Optional Argument.
                Specifies whether to persist the result in a table or not.
                Default Value: False
                Type: bool

            volatile:
                Optional Argument.
                Specifies whether to create a volatile table or not.
                Default Value: False
                Type: bool

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            self._execute_query()
        """
        # Generate STDOUT table name and add it to the output table list.
        func_params = self.__get_generate_temp_table_params(persist=persist, volatile=volatile)
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(**func_params)

        __execute = UtilFuncs._create_table
        __execute_params = (sqlmr_stdout_temp_tablename, self.sqlmr_query, volatile)
        if func_params["table_type"] == TeradataConstants.TERADATA_VIEW:
            __execute = UtilFuncs._create_view
            __execute_params = (sqlmr_stdout_temp_tablename, self.sqlmr_query)

        try:
            __execute(*__execute_params)

            # Store the result table in map.
            if len(self._metadata.output_tables) > 0:
                self._function_output_table_map["output"] = sqlmr_stdout_temp_tablename
            else:
                self._function_output_table_map["result"] = sqlmr_stdout_temp_tablename

            if persist:
                # SQL is executed. So, print the table/view names.
                for output_attribute, table_name in self._function_output_table_map.items():
                    print("{} data stored in table '{}'".format(output_attribute, table_name))

        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)),
                                      MessageCodes.TDMLDF_EXEC_SQL_FAILED)

    def __get_generate_temp_table_params(self, persist=False, volatile=False):
        """
        DESCRIPTION:
            Function to get the required parameters to create either table or view.
            When function has output table arguments or argument persist is set to True,
            then function returns parameters to create table otherwise returns parameters
            to create view. If persist is set to True or volatile is set to True, in such cases,
            tables created are not GC'ed.

        PARAMETERS:
            persist:
                Optional Argument.
                Specifies whether to persist the output table or not.
                When set to True, output tables created are not garbage collected
                at the end of the session, otherwise they are garbage collected.
                Default Value: False
                Types: bool

            volatile:
                Optional Argument.
                Specifies whether to create the output table as volatile table or not.
                When set to True, output tables created are garbage collected
                at the end of the session, otherwise they are not garbage collected.
                Default Value: False
                Types: bool

        RETURNS:
            dict

        RAISES:
            None

        EXAMPLES:
            self.__get_generate_temp_table_params(True, True)
        """
        use_default_database = True
        db_object_type = TeradataConstants.TERADATA_VIEW
        prefix = "td_sqlmr_out_"
        gc_on_quit = True

        # If function produces output tables, i.e., function has output table arguments,
        # the 'db_object_type' should be "table" or if analytic function does not support
        # reading from a view created on output, then 'db_object_type' should be "table".
        if len(self._metadata.output_tables) > 0 or not self._metadata._is_view_supported:
            db_object_type = TeradataConstants.TERADATA_TABLE

        # If result is to be persisted or if the table is a volaile table then, db_object_type
        # should be "table" and it must not be Garbage collected.
        if persist or volatile:
            gc_on_quit = False
            db_object_type = TeradataConstants.TERADATA_TABLE
            prefix = "td_sqlmr_{}_out_".format("persist" if persist else "volatile")

        return {"use_default_database": use_default_database,
                "table_type": db_object_type,
                "prefix": prefix,
                "gc_on_quit": gc_on_quit}

    def _process_output_argument(self, persist=False, volatile=False, **kwargs):
        """
        DESCRIPTION:
            Function to process output argument(s) of analytic function.

        PARAMETERS:
            persist:
                Optional Argument.
                Specifies whether to persist the output table or not.
                When session is disconnected, if function is executed with persist
                set to False, then output tables are removed.
                When set to True, output tables created are not garbage collected
                at the end of the session, otherwise they are garbage collected.
                Default Value: False
                Types: bool

            volatile:
                Optional Argument.
                Specifies whether to create the output table as volatile table or not.
                When set to True, output tables created are garbage collected
                at the end of the session, otherwise they are not garbage collected.
                Default Value: False
                Types: bool

            kwargs:
                Specifies the keyword arguments passed to a function.

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            self._process_output_argument()
        """
        # Process the output_tables argument(s) of the metadata.
        for output_argument in self._metadata.output_tables:
            lang_name = output_argument.get_lang_name()

            # Generate the name of the table.
            func_params = self.__get_generate_temp_table_params(persist=persist, volatile=volatile)
            temp_table_name = UtilFuncs._generate_temp_table_name(**func_params)

            # By default, populate the output table lists irrespective of 'is_required'. However,
            # if the output table has a dependent argument, then check for the dependent argument
            # value and decide whether to populate output table lists or not.
            populate_output_tables = True
            dependent_argument = output_argument.get_is_required_dependent_argument()
            if dependent_argument is not None:
                # Dependent argument can be input_tables or arguments or output_tables.
                # Get the analytic function arguments based on the argument type and
                # check whether dependenncy is satisfied or not.
                for arg in getattr(self._metadata, dependent_argument.type):
                    if arg.get_sql_name() == dependent_argument.sql_name:
                        lang_name = arg.get_lang_name()
                        lang_name_val = kwargs.get(lang_name)
                        if not dependent_argument.is_required(lang_name_val):
                            populate_output_tables = False
                            break

            if populate_output_tables:
                self._func_output_args_sql_names.append(output_argument.get_sql_name())
                self._func_output_args.append(temp_table_name)
                self._function_output_table_map[lang_name] = temp_table_name

    def _process_other_argument(self, **kwargs):
        """
        DESCRIPTION:
            Function to process other arguments. This function does the following:
                * Checks the required arguments are passed or not.
                * Checks the type of the arguments are expected or not.
                * If argument accepts only specified values, function checks whether
                  the value passed is in the specified values or not.
                * If all the checks pass, it then populates the corresponding lists
                  with respective values.

        PARAMETERS:
            kwargs:
                Specifies the keyword arguments passed to a function.

        RETURNS:
            None.

        RAISES:
            ValueError OR TypeError OR TeradataMlException.

        EXAMPLES:
            self._process_other_arguments(arg1="string", arg2="db", arg3=2)
        """
        sequence_input_by_list = []

        # Before populate the corresponding lists, make sure to empty those so
        # duplicates wont be populated even analytic function execution happen twice.
        self._func_other_arg_sql_names = []
        self._func_other_args = []
        self._func_other_arg_json_datatypes = []

        # Store the table names and corresponding alternate alias names in a mapper.
        # Mapper to hold the table name and corresponding alias names as keys and
        # input table argument index as values.
        target_tables = {}
        for index, input_table in enumerate(self._metadata.input_tables):
            target_tables.update({t.lower(): index for t in
                                  UtilFuncs._as_list(input_table.get_sql_name())
                                  })
            target_tables.update({t.lower(): index for t in
                                  UtilFuncs._as_list(input_table.get_alternate_sql_name())
                                  })

        for argument in self._metadata.arguments:
            sql_name = argument.get_sql_name()
            arg_name = argument.get_lang_name()
            arg_value = kwargs.get(arg_name)

            self._validate_analytic_function_arguments(arg_name, arg_value, argument)

            # Perform the checks which are specific to argument(_AnlyFuncArgument) type.
            # Check lower bound and upper bound for number type of arguments.
            if isinstance(arg_value, (int, float)):

                lower_bound_inclusive = argument.get_lower_bound_type() == "INCLUSIVE"
                upper_bound_inclusive = argument.get_upper_bound_type() == "INCLUSIVE"
                _Validators._validate_argument_range(arg_value,
                                                     arg_name,
                                                     lbound=argument.get_lower_bound(),
                                                     ubound=argument.get_upper_bound(),
                                                     lbound_inclusive=lower_bound_inclusive,
                                                     ubound_inclusive=upper_bound_inclusive)

            if argument.is_column_argument() and not argument.get_target_table():
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.INVALID_JSON, "{}.json".format(self._metadata.sql_function_name),
                                         "Argument '{}' is specified as column argument but "
                                         "is Target table is not specified".format(sql_name)), MessageCodes.INVALID_JSON)

            # Additional Validations if argument is a Column name.
            if argument.is_column_argument() and argument.get_target_table():
                argument_target_table = UtilFuncs._as_list(argument.get_target_table())[0].lower()
                # If argument_target_table is either table name or alternate table name, then get
                # the table from the list of input tables. Once, table is retrieved, check if it
                # is a DataFrame or not. If it is not a DataFrame, get the DataFrame from the MLE Object.
                if argument_target_table in target_tables:
                    table_arg = self._metadata.input_tables[target_tables[argument_target_table]]
                    target_table_argument_name = table_arg.get_lang_name()

                    dataframe = kwargs.get(target_table_argument_name)
                    # Input table can be an object of MLE Functions too.
                    if not self._is_argument_dataframe(dataframe) and dataframe is not None:
                        dataframe = dataframe._mlresults[0]

                    # Validate column is existed or not in the table.
                    _Validators._validate_dataframe_has_argument_columns(
                        arg_value, arg_name, dataframe, target_table_argument_name)

            # SequenceInputBy arguments require special processing.
            if 500 <= argument.get_r_order_number() <= 510:
                quoted_value = UtilFuncs._teradata_collapse_arglist(arg_value, "")
                sequence_input_by_list.append("{}:{}".format(sql_name, quoted_value))
                continue

            if arg_value is not None and arg_value != argument.get_default_value():
                # TODO: Special handling required for few arguments. Will be implemented with ELE-4411.

                # Specific type of arguments required to be passed in a single quote.
                # Append quote if argument requires it.
                arg_value = self._quote_collapse_other_args(argument, arg_value)

                self._func_other_arg_sql_names.append(sql_name)
                self._func_other_args.append(arg_value)
                self._func_other_arg_json_datatypes.append(argument.get_data_type())

        if sequence_input_by_list:
            self._func_other_arg_sql_names.append("SequenceInputBy")
            sequence_input_by_arg_value = UtilFuncs._teradata_collapse_arglist(sequence_input_by_list, "'")
            self._func_other_args.append(sequence_input_by_arg_value)
            self._func_other_arg_json_datatypes.append("STRING")
            self._sql_specific_attributes["SequenceInputBy"] = sequence_input_by_arg_value

    def _create_dynamic_class(self):
        """
        DESCRIPTION:
            Function dynamically creates a class with name as analytic function name.

        RETURNS:
            class

        RAISES:
            None.

        EXAMPLE:
            self._create_dynamic_class()
        """
        # Constructor for the dynamic class.
        def constructor(self):
            """ Constructor for dynamic class """
            # Do Nothing...
            pass

        _function_output_table_map = self._function_output_table_map
        # __repr__ method for dynamic class.
        # Note that the self represents the dynamic class object. Not the
        # instance of _AnlyticFunctionExecutor. So, DataFrames will be available as
        # attributes of the object, which is created using dynamic class.
        def print_result(self):
            """ Function to be used for representation of InDB function type object. """
            repr_string = ""
            for key in _function_output_table_map:
                repr_string = "{}\n############ {} Output ############".format(repr_string, key)
                repr_string = "{}\n\n{}\n\n".format(repr_string, getattr(self,key))
            return repr_string
        self._dyn_cls_data_members["__repr__"] = print_result

        query = self.sqlmr_query
        build_time = None if self.__build_time is None else round(self.__build_time, 2)

        self._dyn_cls_data_members["show_query"] = lambda x: query
        self._dyn_cls_data_members["get_build_time"] = lambda x: build_time

        # To list attributes using dict()
        self._dyn_cls_data_members["__dict__"] = self._dyn_cls_data_members
        self._dyn_cls_data_members["_mlresults"] = self._mlresults

        # Dynamic class creation with In-DB function name.
        indb_class = type(self.func_name, (object,), self._dyn_cls_data_members)

        return indb_class()

    def _generate_query(self):
        """
        DESCRIPTION:
            An interface, which should be implemented by child class(es) to generate the
            query for analytic function.

        RETURNS:
            None

        RAISES:
            None.

        EXAMPLE:
            self._generate_query()
        """
        raise NotImplementedError("Function should be implemented in child class.")

    def _process_input_argument(self, **kwargs):
        """
        DESCRIPTION:
            An interface, which should be implemented by child class(es) to
            process input argument(s).

        PARAMETERS:
            kwargs:
                Specifies the keyword arguments passed to a function.

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            self._process_input_argument()
        """
        raise NotImplementedError("Function should be implemented in child class.")

    def _process_function_output(self, **kwargs):
        """
        DESCRIPTION:
            An interface, which should be implemented by child class(es) to
            process the output.

        PARAMETERS:
            kwargs:
                Specifies the keyword arguments passed to a function.

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            self._process_function_output()
        """
        raise NotImplementedError("Function should be implemented in child class.")

    def _execute_function(self,
                          skip_input_arg_processing=False,
                          skip_output_arg_processing=False,
                          skip_other_arg_processing=False,
                          skip_func_output_processing=False,
                          skip_dyn_cls_processing=False,
                          **kwargs):
        """
        DESCRIPTION:
            Function processes arguments and executes the analytic function.

        PARAMETERS:
            skip_input_arg_processing:
                Optional Argument.
                Specifies whether to skip input (data) argument processing or not.
                Default is to process the input (data) argument.
                When set to True, caller should make sure to process "input" argument and
                pass SQL argument and values as part of kwargs to this function.
                Default Value: False
                Types: bool

            skip_output_arg_processing:
                Optional Argument.
                Specifies whether to skip output argument processing or not.
                Default is to process the output arguments.
                When set to True, caller should make sure to process all output arguments and
                pass equivalent SQL argument and values as part of kwargs to this function.
                Default Value: False
                Types: bool

            skip_other_arg_processing:
                Optional Argument.
                Specifies whether to skip other argument processing or not.
                Default is to process the other arguments, i.e., kwargs.
                When set to True, caller should make sure to process all other arguments are
                processed internally by the function.
                Default Value: False
                Types: bool

            skip_func_output_processing:
                Optional Argument.
                Specifies whether to skip function output processing or not.
                Default is to process the same.
                When set to True, caller should make sure to process function output.
                Generally, when this argument is set to True, one must also
                set "skip_dyn_cls_processing" to True.
                Default Value: False
                Types: bool

            skip_dyn_cls_processing:
                Optional Argument.
                Specifies whether to skip dynamic class processing or not.
                Default is to process the dynamic class, where it creates a dynamic
                class and an instance of the same and returns the same.
                When set to True, caller should make sure to process dynamic class and
                return an instance of the same.
                Default Value: False
                Types: bool

            kwargs:
                Specifies the keyword arguments passed to a function.

        RETURNS:
            An object of class, with the name same as analytic function.

        RAISES:
            TeradataMlException, TypeError

        EXAMPLES:
            self._execute_function(arg1="string", arg2="db", arg3=2)
        """
        # kwargs may contain all additional arguments in 'generic_arguments'.
        # Hence update it to actual kwargs.
        kwargs.update(kwargs.pop("generic_arguments", {}))

        # Add all arguments to dynamic class as data members.

        start_time = time.time()
        persist = kwargs.pop("persist", False)
        volatile = kwargs.pop("volatile", False)

        # Validate local_order_column argument type and values.
        arg_info_matrix = [["persist", persist, True, bool], ["volatile", volatile, True, bool]]
        # Check for valid types and values.
        _Validators._validate_function_arguments(arg_info_matrix)

        if persist and volatile:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.CANNOT_USE_TOGETHER_WITH, "persist", "volatile"),
                MessageCodes.CANNOT_USE_TOGETHER_WITH)

        self._dyn_cls_data_members.update(kwargs)

        if not skip_input_arg_processing:
            self._process_input_argument(**kwargs)

        if not skip_output_arg_processing:
            self._process_output_argument(persist=persist, volatile=volatile, **kwargs)

        if not skip_other_arg_processing:
            self._process_other_argument(**kwargs)

        self._generate_query(volatile=volatile)

        # Print SQL-MR query if requested to do so.
        if display.print_sqlmr_query:
            print(self.sqlmr_query)

        self._execute_query(persist, volatile)

        if not skip_func_output_processing:
            self._process_function_output()

        # Set the build time.
        self.__build_time = time.time() - start_time

        if not skip_dyn_cls_processing:
            return self._create_dynamic_class()

    def _quote_collapse_other_args(self, argument, arg_value):
        """
        DESCRIPTION:
            Given a list as an argument this will single quote all the
            list elements and combine them into a single string separated by
            commas.
            Append single quote to the elements which are required to be quoted.

        PARAMETERS:
            argument:
                Required Argument.
                Specifies the argument object (_AnlyArgumentBase).
                Types: _AnlyFuncArgument

            arg_value:
                Required Argument.
                Specifies the arg_value to be quoted and combined.
                Types: list OR string OR int OR bool OR float

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            self._quote_collapse_other_args(argument, arg_value)
        """
        if isinstance(argument.get_data_type(), list):
            if isinstance(arg_value, (str, bool)):
                return UtilFuncs._teradata_collapse_arglist(arg_value, "'")
            else:
                return UtilFuncs._teradata_collapse_arglist(arg_value, "")
        else:
            if (argument.get_data_type().lower() in ("column", "columns", "column_names", "string", "boolean")):
                return UtilFuncs._teradata_collapse_arglist(arg_value, "'")
            else:
                return UtilFuncs._teradata_collapse_arglist(arg_value, "")

class _SQLEFunctionExecutor(_AnlyticFunctionExecutor):
    """ Class to hold the attributes and provide methods to enable function execution. """
    def __init__(self, func_name, func_type=TeradataAnalyticFunctionTypes.SQLE.value):
        """
        DESCRIPTION:
            Constructor for the class.

        PARAMETERS:
            func_name:
                Required Argument.
                Specifies the name of the analytic function, which is exposed to user.
                Types: str
            
            func_type:
                Optional Argument.
                Specifies the type of the analytic function.
                Types: str

        RAISES:
            TypeError OR ValueError OR TeradataMlException

        EXAMPLES:
            _SQLEFunctionExecutor("AdaBoost")
        """
        super().__init__(func_name, func_type)

        # Lists to hold Input Argument (Table) Information
        self._func_input_arg_sql_names = []
        self._func_input_table_view_query = []
        self._func_input_dataframe_type = []
        self._func_input_distribution = []
        self._func_input_partition_by_cols = []
        self._func_input_order_by_cols = []
        self._func_input_local_order = []

    def _generate_query(self, volatile=False):
        """
        DESCRIPTION:
            Function to generate the SQL query for SQLE analytic function.

        PARAMETERS:
            volatile:
                Optional Argument.
                Specifies whether to create a volatile table or not.
                Default Value: False
                Type: bool

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            self._generate_query()
        """
        self.__aqg_obj = AnalyticQueryGenerator(function_name=self._metadata.sql_function_name,
                                                func_input_arg_sql_names=self._func_input_arg_sql_names,
                                                func_input_table_view_query=self._func_input_table_view_query,
                                                func_input_dataframe_type=self._func_input_dataframe_type,
                                                func_input_distribution=self._func_input_distribution,
                                                func_input_partition_by_cols=self._func_input_partition_by_cols,
                                                func_input_order_by_cols=self._func_input_order_by_cols,
                                                func_other_arg_sql_names=self._func_other_arg_sql_names,
                                                func_other_args_values=self._func_other_args,
                                                func_other_arg_json_datatypes=self._func_other_arg_json_datatypes,
                                                func_output_args_sql_names=self._func_output_args_sql_names,
                                                func_output_args_values=self._func_output_args,
                                                engine="ENGINE_SQL",
                                                volatile_output=volatile,
                                                skip_config_lookup=True,
                                                func_input_local_order=self._func_input_local_order)

        # Invoke call to SQL-MR generation.
        self.sqlmr_query = self.__aqg_obj._gen_sqlmr_select_stmt_sql()

    def _process_input_argument(self, **kwargs):
        """
        DESCRIPTION:
            Function to process input argument(s).

        PARAMETERS:
            kwargs:
                Specifies the keyword arguments passed to a function.

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            self._process_input_argument()
        """
        for input_attribute in self._metadata.input_tables:
            input_table_arg = input_attribute.get_lang_name()
            partition_column_arg = "{}_partition_column".format(input_table_arg)
            order_column_arg = "{}_order_column".format(input_table_arg)
            local_order_column_arg = "local_order_{}".format(input_table_arg)
            hash_column_arg = "{}_hash_column".format(input_table_arg)

            # Get the argument values from kwargs
            input_table_arg_value = kwargs.get(input_table_arg)
            partition_column_arg_value = kwargs.get(partition_column_arg)
            order_column_arg_value = kwargs.get(order_column_arg)
            local_order_column_arg_value = kwargs.get(local_order_column_arg, False)
            hash_column_arg_value = kwargs.get(hash_column_arg)

            reference_class = None
            if input_attribute.is_reference_function_acceptable():
                reference_class = self._metadata.get_reference_function_class()

            # Validate the input table arguments.
            self._validate_analytic_function_arguments(
                input_table_arg, input_table_arg_value, input_attribute, additional_valid_types=reference_class)

            # If input is an object of reference Function, then get the DataFrame from it.
            if reference_class and isinstance(input_table_arg_value, reference_class):
                input_table_arg_value = input_table_arg_value._mlresults[0]

            # Don't fill the input lists if the value is None.
            if input_table_arg_value is None:
                continue

            # Validate local_order_column argument type and values.
            arg_info_matrix = [[local_order_column_arg, local_order_column_arg_value, True, bool, True]]
            # Check emptiness and types.
            _Validators._validate_missing_required_arguments(arg_info_matrix)
            _Validators._validate_function_arguments(arg_info_matrix)

            for arg in [partition_column_arg, order_column_arg, hash_column_arg]:
                arg_value = kwargs.get(arg)

                expected_types = (str, list)
                # For partition column, user can pass partition kind too.
                if "partition" in arg:
                    expected_types = (str, _ListOf(str), PartitionKind)
                arg_info_matrix = [[arg, arg_value, True, expected_types, True]]

                # Check for empty string and datatype.
                _Validators._validate_missing_required_arguments(arg_info_matrix)
                _Validators._validate_function_arguments(arg_info_matrix)

                # Set order column value to "NA_character_" if it is None.
                if not isinstance(arg_value, PartitionKind):
                    # Validate column existence in DataFrame only if user inputs a column(s).
                    _Validators._validate_dataframe_has_argument_columns(arg_value,
                                                                         arg,
                                                                         input_table_arg_value,
                                                                         input_table_arg
                                                                         )

            order_column_arg_value = UtilFuncs._teradata_collapse_arglist(order_column_arg_value, "\"")

            distribution, partition_column = self._get_distribution_and_partition_column(
                partition_column_arg_value, hash_column_arg_value, input_attribute)

            table_ref = AnalyticsWrapperUtils()._teradata_on_clause_from_dataframe(
                input_table_arg_value, False)

            self._func_input_arg_sql_names.append(input_attribute.get_sql_name())
            self._func_input_table_view_query.append(table_ref["ref"])
            self._func_input_dataframe_type.append(table_ref["ref_type"])
            self._func_input_order_by_cols.append(order_column_arg_value)
            self._func_input_distribution.append(distribution)
            self._func_input_partition_by_cols.append(partition_column)
            self._func_input_local_order.append(local_order_column_arg_value)

    def _get_distribution_and_partition_column(self, 
                                               partition_column_arg_value,
                                               hash_column_arg_value,
                                               input_attribute):
        """
        DESCRIPTION:
            Function to get the input distribution and partition column values to
            process input table argument.

        PARAMETERS:
            partition_column_arg_value:
                Required Argument.
                Specifies the partition column argument value.
                Types: str OR PartitionKind OR None.

            hash_column_arg_value:
                Required Argument.
                Specifies the hash column argument value.
                Types: str

            input_attribute:
                Required Argument.
                Specifies the input table attribute.
                Types: _AnlyFuncInput

        RETURNS:
            tuple, with first element represents distribution and second element
            represents partition_column.

        RAISES:
            None.

        EXAMPLES:
            self._get_distribution_and_partition_column(partition_column_arg_val, hash_column_arg_val)
        """
        # If user passes hash_column_argument, generate the Query based on HASH BY
        # irrespective of the value of partition_column.
        if hash_column_arg_value:
            return "HASH", UtilFuncs._teradata_collapse_arglist(hash_column_arg_value, "\"")

        # If user passes PartitionKind, generate Query based on distribution and partition type.
        if isinstance(partition_column_arg_value, PartitionKind):
            return self.__get_dist_partition_column_from_partition_kind(partition_column_arg_value)

        # If user pass a string or list of strings for partition_column, generate PARTITION BY
        # based on partition column value.
        if partition_column_arg_value is not None:
            return "FACT", UtilFuncs._teradata_collapse_arglist(partition_column_arg_value, "\"")
        # No partition_column is sourced to input. So, derive the default one.
        else:
            default = input_attribute._get_default_partition_column_kind()
            return self.__get_dist_partition_column_from_partition_kind(default)

    def __get_dist_partition_column_from_partition_kind(self, partition_kind):
        """
        DESCRIPTION:
            Function to get the distribution and partition column based on PartitionKind.

        PARAMETERS:
            partition_kind:
                Required Argument.
                Specifies the type of Partition.
                Types: PartitionKind

        RETURNS:
            tuple, with first element represents distribution and second element
            represents partition_column.

        RAISES:
            None.

        EXAMPLES:
            self.__get_dist_partition_column_from_partition_kind(PartitionKind.ONE)
        """
        if partition_kind in (PartitionKind.ANY, PartitionKind.ONE):
            return "FACT", partition_kind.value
        elif partition_kind == PartitionKind.DIMENSION:
            return PartitionKind.DIMENSION.value, None
        # Else is for PartitionKind.NONE.
        else:
            return "NONE", "NA_character_"

    # Below code is not being used. Kept here to refer again.
    '''
    def _get_input_distribution_and_partition_column(self, input_table, partition_column_arg_value):
        """
        DESCRIPTION:
            Function to get the input distribution and partition column values to
            process input table argument.

        PARAMETERS:
            input_table:
                Required Argument.
                Specifies the input table argument.
                Types: _AnlyFuncInput

            partition_column_arg_value:
                Required Argument.
                Specifies the partition column argument value.
                Types: str

        RETURNS:
            tuple, with first element represents distribution and second element
            represents partition_column.

        RAISES:
            None.

        EXAMPLES:
            self._get_input_distribution_and_partition_column(inp1, partition_column_arg)
        """
        # Initialise all the temporary variables and set those to False by default.
        is_dimension, is_partition_by_key, is_partition_by_any, is_partition_by_one = [False] * 4
        is_partition_by_one_only, is_partition_by_any_only = [False] * 2

        # Get the partition kind from input table.
        partition_kind = input_table._get_partition_column_required_kind()

        # Check whether associated input table requires to be partitioned
        # on any column or not.
        # Set some booleans based on what type of distribution is supported by
        # the argument.
        if partition_kind == PartitionKind.DIMENSION:
            is_dimension = True
        elif partition_kind == PartitionKind.DIMENSIONKEY:
            is_dimension, is_partition_by_key = True, True
        elif partition_kind == PartitionKind.DIMENSIONKEYANY:
            is_dimension, is_partition_by_any, is_partition_by_key = True, True, True
        elif partition_kind == PartitionKind.KEY:
            is_partition_by_key = True
        elif partition_kind == PartitionKind.ONE:
            is_partition_by_one, is_partition_by_key = True, True
        elif partition_kind == PartitionKind.ANY:
            is_partition_by_any, is_partition_by_key = True, True
        elif partition_kind == PartitionKind.ANYONLY:
            is_partition_by_any_only = True
        elif partition_kind == PartitionKind.ONEONLY:
            is_partition_by_one_only = True

        collapse_arg_list = lambda partition_column_arg_value: "NA_character_" if partition_column_arg_value is None\
            else UtilFuncs._teradata_collapse_arglist(partition_column_arg_value, "\"")

        default_partition_value = input_table._get_default_partition_by_value(partition_kind)

        # When distribution is of type dimension, no partition by column required.
        if is_dimension and not is_partition_by_key and not is_partition_by_any:
            distribution = "DIMENSION"
            partition_column = "NA_character_"
        # When partitioned by either key or any, distribution should be FACT.
        elif is_dimension and (is_partition_by_key or is_partition_by_any):
            # If the input is not None, then distribution should be FACT. Otherwise, DIMENSION.
            distribution = "DIMENSION"
            if (partition_column_arg_value is not None and is_partition_by_key):
                distribution = "FACT"

                # Quote if input value is not same as default value.
                if self._awu._is_default_or_not(partition_column_arg_value, default_partition_value):
                    partition_column = collapse_arg_list(partition_column_arg_value)
                else:
                    partition_column = default_partition_value

            elif partition_column_arg_value is not None and not is_partition_by_key and is_partition_by_any:
                distribution = "FACT"
                partition_column = "ANY"
            else:
                partition_column = "NA_character_"
        else:
            # When partitioned by either key or any, distribution should be FACT.
            if is_partition_by_any and not is_partition_by_key:
                distribution = "FACT"
                partition_column = "ANY"
            elif (is_partition_by_key and not is_partition_by_any and not is_partition_by_one) or\
                    (is_partition_by_key and is_partition_by_any):
                distribution = "FACT"
                # If partition value is default value, Enclose it with double quotes.
                if default_partition_value is not None or default_partition_value != "":
                    if self._awu._is_default_or_not(partition_column_arg_value, default_partition_value):
                        partition_column = collapse_arg_list(partition_column_arg_value)
                    else:
                        partition_column = default_partition_value
                else:
                    partition_column = UtilFuncs._teradata_collapse_arglist(partition_column_arg_value, "\"")
            elif is_partition_by_one:
                distribution = "FACT"
                # If partition value is 1, Enclose it with double quotes.
                if self._awu._is_default_or_not(partition_column_arg_value, "1"):
                    partition_column = collapse_arg_list(partition_column_arg_value)
                else:
                    partition_column = default_partition_value
            elif is_partition_by_any_only or is_partition_by_one_only:
                distribution = "FACT"
                partition_column = "{}".format(default_partition_value)
            else:
                distribution = "NONE"
                partition_column = "NA_character_"

        return distribution, partition_column
    '''

    def _process_function_output(self, **kwargs):
        """
        DESCRIPTION:
            Internal function to process the output tables. This function creates
            the required output DataFrames from the tables and a result list.

        PARAMETERS:
            kwargs:
                Specifies the keyword arguments passed to a function.

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            self._process_function_output()
        """
        for lang_name, table_name in self._function_output_table_map.items():
            out_table_name = UtilFuncs._extract_table_name(table_name)
            out_db_name = UtilFuncs._extract_db_name(table_name)
            df = self._awu._create_data_set_object(
                df_input=out_table_name, database_name=out_db_name, source_type="table")
            self._dyn_cls_data_members[lang_name] = df
            self._mlresults.append(df)

class _TableOperatorExecutor(_SQLEFunctionExecutor):
    """ Class to hold the attributes and provide methods to enable execution for Table Operators. """
    def __init__(self, func_name):
        """
        DESCRIPTION:
            Constructor for the class.

        PARAMETERS:
            func_name:
                Required Argument.
                Specifies the name of the analytic function, which is exposed to the user.
                Types: str

        RAISES:
            TypeError OR ValueError OR TeradataMlException

        EXAMPLES:
            _TableOperatorExecutor("write_nos")
        """
        super().__init__(func_name, TeradataAnalyticFunctionTypes.TABLEOPERATOR.value)

        # Lists to hold Input Argument (Table) Information
        self.__func_input_order_by_type = []
        self.__func_input_sort_ascending = []
        self.__func_input_nulls_first = []

    def _generate_query(self, **kwargs):
        """
        DESCRIPTION:
            Function to generate the SQL query for TABLE OPERATOR function.

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            self._generate_query()
        """
        self.__aqg_obj = TableOperatorQueryGenerator(function_name=self.func_name,
                                                     func_input_arg_sql_names=self._func_input_arg_sql_names,
                                                     func_input_table_view_query=self._func_input_table_view_query,
                                                     func_input_dataframe_type=self._func_input_dataframe_type,
                                                     func_input_distribution=self._func_input_distribution,
                                                     func_input_partition_by_cols=self._func_input_partition_by_cols,
                                                     func_input_order_by_cols=self._func_input_order_by_cols,
                                                     func_other_arg_sql_names=self._func_other_arg_sql_names,
                                                     func_other_args_values=self._func_other_args,
                                                     func_other_arg_json_datatypes=self._func_other_arg_json_datatypes,
                                                     func_output_args_sql_names=self._func_output_args_sql_names,
                                                     func_output_args_values=self._func_output_args,
                                                     func_input_order_by_type=self.__func_input_order_by_type,
                                                     func_input_sort_ascending=self.__func_input_sort_ascending,
                                                     func_input_nulls_first=self.__func_input_nulls_first,
                                                     engine="ENGINE_SQL")

        # Invoke call to SQL-MR generation.
        self.sqlmr_query = self.__aqg_obj._gen_table_operator_select_stmt_sql()

    def _process_input_argument(self, **kwargs):
        """
        DESCRIPTION:
            Function to process input argument(s).

        PARAMETERS:
            kwargs:
                Specifies the keyword arguments passed to a function.

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            self._process_input_argument()
        """
        super()._process_input_argument(**kwargs)
        # Iterating over multiple input arguments if present.
        for index, input_attribute in enumerate(self._metadata.input_tables):
            # Extracting input argument name and value.
            input_table_arg = input_attribute.get_lang_name()
            input_table_arg_value = kwargs.get(input_table_arg)
            # No need to process further if no input argument.
            # Validation of this input is done in the parent class.
            if input_table_arg_value is None:
                continue
            
            # Extracting argument names for partition, hash and is local ordered.
            partition_column_arg = "{}_partition_column".format(input_table_arg)
            hash_column_arg = "{}_hash_column".format(input_table_arg)
            is_local_ordered_arg = "local_order_{}".format(input_table_arg)
            order_column_arg = "{}_order_column".format(input_table_arg)
            # Extracting argument values for partition, hash and is local ordered.
            partition_column_value = kwargs.get(partition_column_arg, None)
            hash_column_value = kwargs.get(hash_column_arg, None)
            is_local_ordered_value = kwargs.get(is_local_ordered_arg, False)
            order_column_value = kwargs.get(order_column_arg, "NA_character_")
            
            self._validate_hash_local_ordered_arguments(partition_column_arg, partition_column_value,
                                                        hash_column_arg, hash_column_value,
                                                        is_local_ordered_arg, is_local_ordered_value,
                                                        order_column_arg, order_column_value,
                                                        input_table_arg, input_table_arg_value)
            
            if is_local_ordered_value:
                self.__func_input_order_by_type.append("LOCAL")
                if hash_column_value is None:
                    self._func_input_distribution[index] = "NONE"      
                else:
                    self._func_input_distribution[index] = "HASH"
                    self._func_input_partition_by_cols[index] = hash_column_value
            else:
                self.__func_input_order_by_type.append(None)
                if partition_column_value is None:
                    self._func_input_distribution[index] = "NONE"
        
    def _validate_hash_local_ordered_arguments(self, partition_column_arg, partition_column_value,
                                               hash_column_arg, hash_column_value,
                                               is_local_ordered_arg, is_local_ordered_value,
                                               order_column_arg, order_column_value,
                                               input_table_arg, input_table_arg_value):
        """
        DESCRIPTION:
            Function to validate the hash and local order function arguments. This function does
            the following validations
                * Check if Hash Column value is not empty string.
                * Check if "is local order" value is of type boolean.
                * Hash and order by can be used together as long as is_local_order = True.
                * Either hash or partition can be used.
                * Either local order by or partition by can be used.

        PARAMETERS:
            partition_column_arg:
                Required Argument.
                Specifies the name of the partition by column argument.
                Type: str
            
            partition_column_value:
                Required Argument.
                Specifies the value of the partition by column argument.
                Type: str
            
            hash_column_arg:
                Required Argument.
                Specifies the name of the hash by column argument.
                Type: str
            
            hash_column_value:
                Required Argument.
                Specifies the value of the hash by column argument.
                Type: str
            
            is_local_ordered_arg:
                Required Argument.
                Specifies the name of the is local ordered argument.
                Type: str
            
            is_local_ordered_value:
                Required Argument.
                Specifies the value of the is local ordered argument.
                Type: bool
            
            order_column_arg:
                Required Argument.
                Specifies the name of the order by column argument.
                Type: str
            
            order_column_value:
                Required Argument.
                Specifies the value of the ordere by column argument.
                Type: str
            
            input_table_arg:
                Required Argument.
                Specifies the name of the input table provided to the function.
                Types: str

            input_table_arg_value:
                Required Argument.
                Specifies the value of the input table provided to the function.
                Types: DataFrame

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            self._validate_hash_local_ordered_arguments("data", DataFrame.from_table("ibm_stock")), **kwargs)
        """
        # Check for empty string and types(str or list) for hash column values.
        # Check for types for is local ordered values.

        _Validators._validate_function_arguments([[hash_column_arg, hash_column_value, True, (str, list), True],
                                                  [is_local_ordered_arg, is_local_ordered_value, True, bool, False]])

        # Validate column existence in DataFrame.
        _Validators._validate_dataframe_has_argument_columns(hash_column_value,
                                                             hash_column_arg,
                                                             input_table_arg_value,
                                                             input_table_arg
                                                             )
        
        # Hash and order by can be used together as long as is_local_order = True.
        if all([hash_column_value,
                order_column_value]) and not is_local_ordered_value:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.CANNOT_USE_TOGETHER_WITH,
                                        "{}' and '{}".format(hash_column_arg, order_column_arg),
                                        "{}=False".format(is_local_ordered_arg)),
                MessageCodes.CANNOT_USE_TOGETHER_WITH)

        # Either hash or partition can be used.
        _Validators._validate_mutually_exclusive_arguments(hash_column_value,
                                                           hash_column_arg,
                                                           partition_column_value,
                                                           partition_column_arg,
                                                           skip_all_none_check=True)

        # Either local order by or partition by can be used.
        _Validators._validate_mutually_exclusive_arguments(is_local_ordered_value,
                                                           is_local_ordered_arg,
                                                           partition_column_value,
                                                           partition_column_arg,
                                                           skip_all_none_check=True)

        # local order by requires column name.
        if is_local_ordered_value and order_column_value is None:
            message = Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING,
                                            order_column_arg, "{}=True".format(is_local_ordered_arg))
            raise TeradataMlException(message, MessageCodes.DEPENDENT_ARG_MISSING)

    def _quote_collapse_other_args(self, argument, arg_value):
        """
        DESCRIPTION:
            Given a list as an argument this will single quote all the
            list elements and combine them into a single string separated by
            commas.
            Append single quote to the elements which are required to be quoted.

        PARAMETERS:
            argument:
                Required Argument.
                Specifies the argument object (_AnlyArgumentBase).
                Types: _AnlyFuncArgument

            arg_value:
                Required Argument.
                Specifies the arg_value to be quoted and combined.
                Types: list OR string OR int OR bool OR float

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            self._quote_collapse_other_args(argument, arg_value)
        """
        arg_dtype = UtilFuncs._as_list(argument.get_data_type())
        for arg in arg_dtype:
            if arg.lower() in ("column", "columns", "column_names", "string", "boolean") and isinstance(arg_value,(str, bool)):
                return UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_collapse_arglist(arg_value, "\'"), "'")
            else:
                return UtilFuncs._teradata_collapse_arglist(arg_value, "'")