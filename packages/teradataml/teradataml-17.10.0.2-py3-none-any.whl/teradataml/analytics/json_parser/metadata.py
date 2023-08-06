"""
Unpublished work.
Copyright (c) 2021 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: pradeep.garre@teradata.com
Secondary Owner: PankajVinod.Purandare@teradata.com

This file implements _AnlyFuncMetadata for representing the metadata (json data)
of analytic function. All the functions/API's looking to extract the json data
should look at corresponding API's in _AnlyFuncMetadata.
"""
import json, os
from collections import OrderedDict
from pathlib import Path
from teradataml.analytics.json_parser.analytic_functions_argument import _AnlyFuncArgument,\
    _AnlyFuncInput, _AnlyFuncOutput, _DependentArgument
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.constants import TeradataAnalyticFunctionTypes
from teradataml.common.exceptions import TeradataMlException
from teradataml.analytics.json_parser import PartitionKind, SqleJsonFields as SJF
from teradataml.common.utils import UtilFuncs
from teradataml.utils.validators import _Validators


class _AnlyFuncMetadata:
    """ Class to hold the json data. """

    # A class variable to store the r function names and their function names.
    # Note that this is a class variable so it is accessable from all the objects
    # of _AnlyFuncMetadata.
    _reference_function_names = {
        "aa.glm": "GLM",
        "aa.forest": "DecisionForest",
        "aa.naivebayes.textclassifier.train": "NaiveBayesTextClassifier",
        "aa.svm.sparse.train": "SVMSparse"
    }

    def __init__(self, json_data, json_file, func_type=None):
        """
        DESCRIPTION:
            Constructor for the class.

        PARAMETERS:
            json_data:
                Required Argument.
                Specifies the json content of analytic function.
                Types: dict

            json_file:
                Required Argument.
                Specifies the absolute path of the json file.
                Types: str
            
            func_type:
                Optional Argument.
                Specifies the type of analytic function.
                Permitted Values: ['FASTPATH', 'TABLE_OPERATOR']
                Types: str
        """
        # Validate func_type.
        arg_info_matrix = []
        arg_info_matrix.append(
            ["func_type", func_type, False, 
             (str, type(None)), True, [TeradataAnalyticFunctionTypes.SQLE.value,
                                       TeradataAnalyticFunctionTypes.TABLEOPERATOR.value,
                                       None]])
        arg_info_matrix.append(["json_file", json_file, False, str, True])
        _Validators._validate_function_arguments(arg_info_matrix)

        self.short_description = json_data[SJF.SHORT_DESCRIPTION]
        self.long_description = json_data[SJF.LONG_DESCRIPTION]
        # Store Input Table data objects.
        self.__input_tables = []
        # Store Output Table data objects.
        self.__output_tables = []
        # Store rest of function argument objects.
        self.__arguments = []

        # JSON Object
        self.json_object = json_data

        self.sql_function_name = self.json_object["function_name"]
        self.func_name = self._get_function_name()

        self.func_type = json_data[SJF.FUNCTION_TYPE] if func_type is None else func_type
        self.__json_file = json_file

        # Variable to hold the name of the argument as key and the corresponding section as
        # value. This is used for checking duplicate arguments.
        self.__arguments_and_sections = {}

        # Call a function read JSON and collect arguments, input
        # and output table arguments.
        self.__parse_json()

        # TODO: Output schema is not required so not storing it for now. If we need it in
        #       future, then it can be enabled.
        # Store output schema of the function
        # self.standard_output_schema = self.json_object.get(SJF.OUTPUT_SCHEMA)
        self.__database_version = Path(self.__json_file).parts[-2]
        self._is_view_supported = self.json_object.get("supports_view", True)
        self.__is_driver_function = self.json_object.get("function_type", "").lower() == "driver"
        self.__function_params = OrderedDict()
        self.__refernce_function_name = self.json_object.get("ref_function_r_name")
        self.__r_function_name = self.json_object.get("function_r_name")
        # Lets store the r function name and the function names in a mapper.
        _AnlyFuncMetadata._reference_function_names[self.__r_function_name] = self.func_name

    def get_reference_function_class(self):
        """
        DESCRIPTION:
            Function to get the reference function class. This function checks if the function
            accepts any other function as input. If it accepts, it then returns the class of
            the referenced function.

        RETURNS:
            class OR None

        RAISES:
            None

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").get_reference_function_class()
        """
        reference_function = _AnlyFuncMetadata._reference_function_names.get(self.__refernce_function_name)
        if reference_function:
            return UtilFuncs._get_class(reference_function, supress_isinstance_check=True)

    def __get_argument_value(self, argument_properties, property, section, mandatory=True, default_value=None):
        """
        DESCRIPTION:
            Function to get the argument value from the json data. This function, checks
            the argument is a mandatory argument or not. If mandatory and not found in json
            data, raises an error otherwise either returns value or default value.

        PARAMETERS:
            argument_properties:
                Required Argument.
                Specifies json content of one of the below mentioned:
                    * Input argument.
                    * Output table.
                    * Input table.
                Types: dict

            property:
                Required Argument.
                Specifies the argument name to look in "argument_properties"
                Types: str

            section:
                Required Argument.
                Specifies the section of the json to which "property" belongs to.
                Types: str

            mandatory:
                Required Argument.
                Specifies whether "property" is a mandatory field in "argument_properties" or not.
                Default Value: True
                Types: bool

            default_value:
                Required Argument.
                Specifies the default value of "property".
                Types: str OR int OR float OR bool

        RETURNS:
            str OR bool OR int OR float OR list

        RAISES:
            TeradataMlException.

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").__get_argument_value(
            json_data, "defaultValue", "input_tables",  False)
        """
        if property not in argument_properties and mandatory:
            error_message = Messages.get_message(MessageCodes.MISSING_JSON_FIELD,
                                                 property,
                                                 section)

            raise TeradataMlException(error_message, MessageCodes.MISSING_JSON_FIELD)

        return argument_properties.get(property, default_value)

    def __parse_arguments(self):
        """
        DESCRIPTION:
            Function to parse and store the argument in json file. This function first validates
            whether argument is required for analytic function or not. If required, then arguments
            section in json data is parsed and object of _AnlyFuncArgument is created and stored.

        RETURNS:
            None

        RAISES:
            TeradataMlException.

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").__parse_arguments()
        """
        section = SJF.ARGUMENT_CLAUSES
        for argument in self.json_object.get(SJF.ARGUMENT_CLAUSES, []):

            is_argument_required = argument.get(SJF.USEINR, False)

            # Append argument to list if useInR is True.
            if is_argument_required:
                use_inR = is_argument_required

                sql_name = self.__get_argument_value(argument, SJF.NAME, section)

                lang_name = self.__get_pythonic_name_arg_name(
                    self.__get_argument_value(argument, SJF.R_NAME, section))

                is_required = self.__get_argument_value(argument, SJF.IS_REQUIRED, section)

                sql_description = self.__get_argument_value(argument, SJF.DESCRIPTION, section)

                r_description = self.__get_argument_value(argument, SJF.R_DESCRIPTION, section)

                datatype = self.__get_argument_value(argument, SJF.DATATYPE, section)

                r_order_num = self.__get_argument_value(argument, SJF.R_ORDER_NUM, section)

                # Look for default value. If default value is not available, the look for default values.
                # If default values found, the consider the first element as default value.
                default_value = self.__get_argument_value(argument, SJF.DEFAULT_VALUE, section, False)
                if isinstance(default_value, list):
                    default_value = default_value[0]

                # Json files can specify INFINITY as lower bound. So, convert it to appropriate
                # type in python.
                lower_bound = self.__get_argument_value(argument, SJF.LOWER_BOUND, section, False)
                lower_bound = UtilFuncs._get_negative_infinity() if lower_bound == SJF.INFINITY else lower_bound

                # Json files can specify INFINITY as upper bound. So, convert it to appropriate
                # type in python.
                upper_bound = self.__get_argument_value(argument, SJF.UPPER_BOUND, section, False)
                upper_bound = UtilFuncs._get_positive_infinity() if upper_bound == SJF.INFINITY else upper_bound

                r_default_value = self.__get_argument_value(argument, SJF.R_DEFAULT_VALUE, section, False)

                allows_lists = self.__get_argument_value(argument, SJF.ALLOWS_LISTS, section, False, False)

                allow_padding = self.__get_argument_value(argument, SJF.ALLOW_PADDING, section, False, False)

                r_formula_usage = self.__get_argument_value(argument, SJF.R_FORMULA_USAGE, section, False, False)

                allow_nan = self.__get_argument_value(argument, SJF.ALLOW_NAN, section, False, False)

                check_duplicate = self.__get_argument_value(argument, SJF.CHECK_DUPLICATE, section, False, False)

                is_output_column = self.__get_argument_value(argument, SJF.IS_OUTPUT_COLUMN, section, False, False)

                lower_bound_type = self.__get_argument_value(argument, SJF.LOWER_BOUND_TYPE, section, False)

                upper_bound_type = self.__get_argument_value(argument, SJF.UPPER_BOUND_TYPE, section, False)

                required_length = self.__get_argument_value(argument, SJF.REQUIRED_LENGTH, section, False, 0)

                match_length_of_argument = self.__get_argument_value(
                    argument, SJF.MATCH_LENGTH_OF_ARGUMENT, section, False, False)

                permitted_values = self.__get_argument_value(argument, SJF.PERMITTED_VALUES, section, False)

                target_table = self.__get_argument_value(argument, SJF.TARGET_TABLE, section, False)

                allowed_types = self.__get_argument_value(argument, SJF.ALLOWED_TYPES, section, False)

                allowed_type_groups = self.__get_argument_value(argument, SJF.ALLOWED_TYPE_GROUPS, section, False)

                alternate_sql_name = self.__get_argument_value(argument, SJF.ALTERNATE_NAMES, section, False)

                # Check for duplicate arguments.
                self.__validate_duplicate_argument(lang_name, SJF.ARGUMENT_CLAUSES)

                if sql_name.lower() == SJF.SEQUENCE_INPUT_BY or sql_name.lower() == SJF.UNIQUE_ID:

                    for j in range(len(self.__input_tables)):
                        r_order_num = (r_order_num * 10) + j

                        sql_name = self.__input_tables[j].get_sql_name()
                        datatype = "COLUMN_NAMES"

                        self.__arguments.append(_AnlyFuncArgument(default_value=default_value,
                                                                  permitted_values=permitted_values,
                                                                  lower_bound=lower_bound,
                                                                  lower_bound_type=lower_bound_type,
                                                                  upper_bound=upper_bound,
                                                                  upper_bound_type=upper_bound_type,
                                                                  allow_nan=allow_nan,
                                                                  required_length=required_length,
                                                                  match_length_of_argument=match_length_of_argument,
                                                                  sql_name=sql_name,
                                                                  is_required=is_required,
                                                                  sql_description=sql_description,
                                                                  lang_description=r_description,
                                                                  datatype=datatype,
                                                                  allows_lists=allows_lists,
                                                                  allow_padding=allow_padding,
                                                                  use_in_r=use_inR,
                                                                  r_formula_usage=r_formula_usage,
                                                                  r_default_value=r_default_value,
                                                                  target_table=target_table,
                                                                  check_duplicate=check_duplicate,
                                                                  allowed_types=allowed_types,
                                                                  allowed_type_groups=allowed_type_groups,
                                                                  r_order_num=r_order_num,
                                                                  is_output_column=is_output_column,
                                                                  alternate_sql_name=alternate_sql_name,
                                                                  lang_name=lang_name))
                else:
                    self.__arguments.append(_AnlyFuncArgument(default_value=default_value,
                                                              permitted_values=permitted_values,
                                                              lower_bound=lower_bound,
                                                              lower_bound_type=lower_bound_type,
                                                              upper_bound=upper_bound,
                                                              upper_bound_type=upper_bound_type,
                                                              allow_nan=allow_nan,
                                                              required_length=required_length,
                                                              match_length_of_argument=match_length_of_argument,
                                                              sql_name=sql_name,
                                                              is_required=is_required,
                                                              sql_description=sql_description,
                                                              lang_description=r_description,
                                                              datatype=datatype,
                                                              allows_lists=allows_lists,
                                                              allow_padding=allow_padding,
                                                              lang_name=lang_name,
                                                              use_in_r=use_inR,
                                                              r_formula_usage=r_formula_usage,
                                                              r_default_value=r_default_value,
                                                              target_table=target_table,
                                                              check_duplicate=check_duplicate,
                                                              allowed_types=allowed_types,
                                                              allowed_type_groups=allowed_type_groups,
                                                              r_order_num=r_order_num,
                                                              is_output_column=is_output_column,
                                                              alternate_sql_name=alternate_sql_name))

    def __parse_input_tables(self):
        """
        DESCRIPTION:
            Function to parse and store the input tables in json file. This function first validates
            whether input table is required for analytic function or not. If required, then input tables
            section in json data is parsed and object of _AnlyFuncInput is created and stored.

        RETURNS:
            None

        RAISES:
            TeradataMlException.

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").__parse_input_tables()
        """
        section = SJF.INPUT_TABLES
        for input_table_param in self.json_object.get(SJF.INPUT_TABLES, []):
            is_input_table_required = input_table_param.get(SJF.USEINR, False)

            # Append argument/input table to list if useInR is True.
            if is_input_table_required:
                use_InR = is_input_table_required

                r_order_num = self.__get_argument_value(input_table_param, SJF.R_ORDER_NUM, section)

                sql_name = self.__get_argument_value(input_table_param, SJF.NAME, section)

                is_required = self.__get_argument_value(input_table_param, SJF.IS_REQUIRED, section)

                sql_description = self.__get_argument_value(input_table_param, SJF.DESCRIPTION, section)

                r_description = self.__get_argument_value(input_table_param, SJF.R_DESCRIPTION, section)

                datatype = self.__get_argument_value(input_table_param, SJF.DATATYPE, section)

                required_input_kind = self.__get_argument_value(
                    input_table_param, SJF.REQUIRED_INPUT_KIND, section, False, None)

                partition_by_one = self.__get_argument_value(
                    input_table_param, SJF.PARTITION_BY_ONE, section, False, False)

                partition_by_one_inclusive = self.__get_argument_value(
                    input_table_param, SJF.PARTITION_BY_ONE_INCLUSIVE, section, False, False)

                is_ordered = self.__get_argument_value(input_table_param, SJF.IS_ORDERED, section, False, False)

                is_local_ordered = self.__get_argument_value(input_table_param, SJF.IS_LOCAL_ORDERED, section, False, False)

                hash_by_key = self.__get_argument_value(input_table_param, SJF.HASH_BY_KEY, section, False, False)

                allows_lists = self.__get_argument_value(input_table_param, SJF.ALLOWS_LISTS, section, False, False)

                lang_name = self.__get_pythonic_name_arg_name(
                    self.__get_argument_value(input_table_param, SJF.R_NAME, section))

                r_formula_usage = self.__get_argument_value(input_table_param, SJF.R_FORMULA_USAGE, section, False, False)

                alternate_sql_name = self.__get_argument_value(input_table_param, SJF.ALTERNATE_NAMES, section, False)

                # Check for duplicate arguments.
                self.__validate_duplicate_argument(lang_name, SJF.INPUT_TABLES)

                self.__input_tables.append(_AnlyFuncInput(required_input_kind=required_input_kind,
                                                          partition_by_one=partition_by_one,
                                                          partition_by_one_inclusive=partition_by_one_inclusive,
                                                          is_ordered=is_ordered,
                                                          hash_by_key=hash_by_key,
                                                          is_local_ordered=is_local_ordered,
                                                          sql_name=sql_name,
                                                          is_required=is_required,
                                                          sql_description=sql_description,
                                                          lang_description=r_description,
                                                          datatype=datatype,
                                                          allows_lists=allows_lists,
                                                          lang_name=lang_name,
                                                          use_in_r=use_InR,
                                                          r_formula_usage=r_formula_usage,
                                                          r_order_num=r_order_num,
                                                          alternate_sql_name=alternate_sql_name))

    def __parse_output_tables(self):
        """
        DESCRIPTION:
            Function to parse and store the output tables in json file. This function first validates
            whether output table is required for analytic function or not. If required, then output tables
            section in json data is parsed and object of _AnlyFuncOutput is created and stored.

        RETURNS:
            None

        RAISES:
            TeradataMlException.

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").__parse_output_tables()
        """
        section = SJF.OUTPUT_TABLES
        for output_table_param in self.json_object.get(SJF.OUTPUT_TABLES, []):
            is_output_table_required = output_table_param.get(SJF.USEINR, False)

            # Append argument/output table to list if useInR is true.
            if is_output_table_required:
                useInR = is_output_table_required

                sql_name = self.__get_argument_value(output_table_param, SJF.NAME, section)

                is_required = self.__get_argument_value(output_table_param, SJF.IS_REQUIRED, section)

                sql_description = self.__get_argument_value(output_table_param, SJF.DESCRIPTION, section)

                r_description = self.__get_argument_value(output_table_param, SJF.R_DESCRIPTION, section)

                datatype = self.__get_argument_value(output_table_param, SJF.DATATYPE, section)

                lang_name = self.__get_pythonic_name_arg_name(self.__get_argument_value(output_table_param,
                                                                                        SJF.R_NAME, section))

                r_order_num = self.__get_argument_value(output_table_param, SJF.R_ORDER_NUM, section)

                is_output_table = self.__get_argument_value(output_table_param, SJF.IS_OUTPUT_TABLE, section, False, False)

                allows_lists = self.__get_argument_value(output_table_param, SJF.ALLOWS_LISTS, section, False, False)

                alternate_sql_name = self.__get_argument_value(output_table_param, SJF.ALTERNATE_NAMES, section, False)

                # TODO: Additional dependencies needs to be implemented with ELE-4511.
                is_required_dependent_argument = self.__get_argument_value(
                    output_table_param, SJF.IS_REQUIRED_DEPENDENT, section, False)
                dependent_argument = None
                if is_required_dependent_argument:

                    argument_type = "input_tables"
                    if is_required_dependent_argument.get(SJF.DEPENDENT_ARGUMENT_TYPE) == "argument":
                        argument_type = "arguments"
                    elif is_required_dependent_argument.get(SJF.DEPENDENT_ARGUMENT_TYPE) == "input_table":
                        argument_type = "input_tables"

                    argument_name = is_required_dependent_argument.get(SJF.DEPENDENT_ARGUMENT_NAME)
                    operator = is_required_dependent_argument.get(SJF.OPERATOR)
                    right_operand = is_required_dependent_argument.get(SJF.DEPENDENT_ARGUMENT_VALUE)
                    dependent_argument = _DependentArgument(sql_name=argument_name,
                                                            operator=operator,
                                                            right_operand=right_operand,
                                                            type=argument_type)

                # TODO: Output schema is not being used any where in processing. So, skipping it for now.
                # output_schema = self.__get_argument_value(output_table_param, SJF.OUTPUT_SCHEMA, False)

                self.__output_tables.append(_AnlyFuncOutput(sql_name=sql_name,
                                                            is_required=is_required,
                                                            sql_description=sql_description,
                                                            lang_description=r_description,
                                                            lang_name=lang_name,
                                                            use_in_r=useInR,
                                                            r_order_num=r_order_num,
                                                            is_output_table=is_output_table,
                                                            datatype=datatype,
                                                            allows_lists=allows_lists,
                                                            output_schema=None,
                                                            alternate_sql_name=alternate_sql_name,
                                                            is_required_dependent_argument=dependent_argument))

    def __parse_json(self):
        try:
            # Parse all input tables.
            self.__parse_input_tables()

            # Parse all output tables.
            self.__parse_output_tables()

            # Parse all arguments.
            self.__parse_arguments()
        except Exception as err:
            teradataml_file_path = os.path.join(*Path(self.__json_file).parts[-6:])
            raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_JSON,
                                                           teradataml_file_path,
                                                           str(err)),
                                      MessageCodes.INVALID_JSON)

    def __get_analytic_function_args(self):
        """
        DESCRIPTION:
            Internal function to get the arguments of analytic function, which are required
            to generate function signature. This function iterates through every input
            table and argument, and does the below.
            * Check if argument formulates to an argument "formula" when exposed or not. If yes,
              then the argument should be the first argument and is extracted to a different variable.
            * Function arguments with rOrderNum <= 0 are not supposed to be exposed
              to end user. Ignore these arguments.

        RAISES:
            None

        RETURNS:
            tuple, first element specifies formula argument and second element specifies
            list of required arguments for analytic function.

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").__get_analytic_function_args()
        """
        new_args = []
        formula_args = []
        args = self.input_tables + self.arguments

        for arg in args:
            r_order_num = arg.get_r_order_number()
            is_argument_formula = isinstance(arg, _AnlyFuncArgument) and arg.is_argument_a_formula() \
                                  and arg.get_r_order_number() <= 0
            if is_argument_formula:
                formula_args.append(arg)
                continue

            if r_order_num <= 0:
                continue

            new_args.append(arg)
        return formula_args, new_args

    def __generate_function_parameters(self):
        """
        DESCRIPTION:
            Function to generate the analytic function argument names and their corresponding default values.
            Function arguments are generated by adhering to following:
            *  Signature includes only input as well as other arguments (SQL: Using clause
               arguments). So, process only those.
            *  Output arguments are ignored in the function signature. So, do not process Output arguments.
            *  Also, arguments pertaining to partition and order column are also generated for
               input tables.

        RAISES:
            None

        RETURNS:
            None

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").__generate_function_parameters()
        """
        formula_args, args = self.__get_analytic_function_args()

        # Formula should always appear as first argument. So, start with formula argument.
        if formula_args:
            self.__function_params["formula"] = None

        for arg in args:

            arg_name = arg.get_lang_name()
            default_value = arg.get_default_value()

            # Add argument and default value in the same order.
            self.__function_params[arg_name] = default_value

    def __process_partition_order_columns(self, arg):
        """
        DESCRIPTION:
            Function to generate the arguments which are related to partition columns
            and order columns arguments.
        
        PARAMETERS:
            arg:
                Required Argument.
                Specifies the object of analytic input argument.
                Types: _AnlyFuncInput

        RAISES:
            None

        RETURNS:
            None

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").__process_partition_order_columns(arg)
        """
        partition_column_kind = arg._get_partition_column_required_kind()
        partition_value = arg._get_default_partition_by_value(partition_column_kind)

        # If Function supports only PartitionByOne or PartitionByAny, don't expose
        # partition column to user.
        if arg._only_partition_by_one() or\
                arg._only_partition_by_any():
            pass
        elif partition_column_kind == PartitionKind.KEY or \
                partition_column_kind == PartitionKind.DIMENSIONKEY:
            self.__function_params["{}_partition_column".format(arg.get_lang_name())] = None
        elif partition_column_kind in [PartitionKind.ANY,
                                       PartitionKind.DIMENSIONKEYANY,
                                       PartitionKind.ONE]:
            self.__function_params['{}_partition_column'.format(arg.get_lang_name())] = partition_value

        # If function type is not a driver or argument is ordered, then add order
        # column also to arguments.
        if not self.__is_driver_function or arg.is_ordered():
            self.__function_params["{}_order_column".format(arg.get_lang_name())] = None
        
    def __process_hash_local_order_columns(self, arg):
        """
        DESCRIPTION:
            Generate the arguments related to LOCAL ORDER BY and HASH BY KEY.
        
        PARAMETERS:
            arg:
                Required Argument.
                Specifies the object of analytic input argument.
                Types: _AnlyFuncInput

        RAISES:
            None

        RETURNS:
            None

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").__process_hash_local_order_columns(arg)
        """
        # If the argument is local ordered, then add "is_local_ordered"
        # as argument.
        if arg.is_local_ordered():
            self.__function_params["{}_is_local_ordered".format(arg.get_lang_name())] = False
        # Let's check if function has HASH BY clause.
        if arg.hash_by_key():
            self.__function_params['{}_hash_column'.format(arg.get_lang_name())] = None        

    def get_function_parameters_string(self):
        """
        DESCRIPTION:
            Function to generate the function parameters in string format.

        RAISES:
            None

        RETURNS:
            str

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").get_function_parameters_string()
        """
        if not self.__function_params:
            self.__generate_function_parameters()

        # Along with function parameters, kwargs should be added to accept other parameters.
        return ", ".join(["{} = {}".format(param, '"{}"'.format(value) if isinstance(value, str) else value)
                          for param, value in self.__function_params.items()] + ["**generic_arguments"])

    @property
    def input_tables(self):
        """
        DESCRIPTION:
            Function to return input tables.

        RETURNS:
            list

        RAISES:
            None

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").input_tables
        """
        return self.__input_tables

    @property
    def output_tables(self):
        """
        DESCRIPTION:
            Function to return output tables.

        RETURNS:
            list

        RAISES:
            None

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").output_tables
        """
        return self.__output_tables

    @property
    def arguments(self):
        """
        DESCRIPTION:
            Function to return arguments.

        RETURNS:
            list

        RAISES:
            None

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").arguments
        """
        return self.__arguments

    @staticmethod
    def __get_anly_function_name_mapper():
        """
        Function to read mapper file teradataml/analytics/jsons/anly_function_name.json,
        which has a mapping between function name specified in json file and function to
        appear in user's context.
        """
        path = os.path.dirname(__file__)
        analytics_folder = os.path.dirname(path)
        return json.loads(
            UtilFuncs._get_file_contents(os.path.join(analytics_folder, "jsons", "anly_function_name.json")))

    def __validate_duplicate_argument(self, lang_name, section):
        """
        DESCRIPTION:
            Internal function to check the duplicates of arguments. No python function
            accepts duplicate parameters and since analytic functions are being formed at
            run time from json, there are chances that function may be constructed with
            duplicate arguments. This function validates whether arguments are duplicated or not.

        PARAMETERS:
            lang_name:
                Required Argument.
                Specifies the name of the argument which is mentioned in json file.
                Types: str

            section:
                Required Argument.
                Specifies the section of json file, to which argument belongs to.
                Types: str

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            _AnlyFuncMetadata(data, "abc.json").__validate_duplicate_argument("abc", "input_tables")
        """
        if lang_name not in self.__arguments_and_sections:
            self.__arguments_and_sections[lang_name] = section
        else:
            raise TeradataMlException(Messages.get_message(MessageCodes.DUPLICATE_PARAMETER,
                                                           lang_name,
                                                           section),
                                      MessageCodes.DUPLICATE_PARAMETER)

    @staticmethod
    def __get_pythonic_name_arg_name(r_name):
        """
        DESCRIPTION:
            Function to get the pythonic name for argument from the name specified
            in json. Conversion of a string to pythonic name does as below:
                * Strips out the trailing and leading spaces.
                * Converts the string to lower case.
                * Replaces the dot(.) with underscore.
                * Replaces the '_table' with '_data'.
                * Replaces the 'table_' with 'data_'.

        PARAMETERS:
            r_name:
                Required Argument.
                Specifies the name of the argument which is mentioned in json file.
                Types: str

        RETURNS:
            str

        RAISES:
            None

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json").__get_pythonic_name_arg_name("abc")
        """
        return r_name.strip().lower().replace(".", "_").replace("_table", "_data").replace("table_", "data_")

    def _get_function_name(self):
        """
        DESCRIPTION:
            Function to get the name of the function which is exposed to user.

        RETURNS:
            str

        RAISES:
            None

        EXAMPLES:
            _AnlyFuncMetadata(json_data, "/abc/Antiselect.json")._get_function_name()
        """
        # If teradataml/analytics/jsons/anly_function_name.json contains a mapping name, function name
        # should be corresponding mapping name. Else, same as function name.
        func_name = self.__get_anly_function_name_mapper().get(self.json_object["function_name"],
                                                               self.json_object["function_name"])

        # Few functions are expected to have a name starting with TD_,i.e., json file may
        # contain function name as TD_Xyz. Since we don't want the prefixed characters,
        # removing those.
        return func_name[3:] if func_name.startswith("TD_") else func_name

    def get_doc_string(self):
        """ This function will return a message asking the user to refer to reference guide. """
        return ("Refer to Teradata Package for Python Function Reference guide for "
                "Documentation. Reference guide can be found at: https://docs.teradata.com ."
                "Refer to the section with Database version: {}".format(self.__database_version))
