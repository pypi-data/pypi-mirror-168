#!/usr/bin/python
# ##################################################################
#
# Copyright 2020 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Trupti Purohit (trupti.purohit@teradata.com)
# Secondary Owner: Gouri Patwardhan (gouri.patwardhan@teradata.com)
#
# Function Version: 1.0
#
# Description: Base class for Teradata's Table Operators
# ##################################################################

import docker
import os
import tarfile
from pathlib import Path
import teradataml.dataframe as tdmldf
from teradataml.common.constants import OutputStyle, TeradataConstants
from teradataml.common.wrapper_utils import AnalyticsWrapperUtils
from teradataml.common.utils import UtilFuncs
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils

from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.options.configure import configure
from teradataml.utils.validators import _Validators
from teradatasqlalchemy import (BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, FLOAT, NUMBER)
from teradatasqlalchemy import (TIMESTAMP, DATE, TIME)
from teradatasqlalchemy import (CHAR, VARCHAR, CLOB)
from teradatasqlalchemy import (BYTE, VARBYTE, BLOB)
from teradatasqlalchemy import (PERIOD_DATE, PERIOD_TIME, PERIOD_TIMESTAMP)
from teradatasqlalchemy import (INTERVAL_YEAR, INTERVAL_YEAR_TO_MONTH, INTERVAL_MONTH, INTERVAL_DAY,
                                INTERVAL_DAY_TO_HOUR, INTERVAL_DAY_TO_MINUTE, INTERVAL_DAY_TO_SECOND,
                                INTERVAL_HOUR, INTERVAL_HOUR_TO_MINUTE, INTERVAL_HOUR_TO_SECOND,
                                INTERVAL_MINUTE, INTERVAL_MINUTE_TO_SECOND, INTERVAL_SECOND)
from teradataml.context.context import _get_current_databasename, get_context

class TableOperator:

    def __init__(self,
                 data=None,
                 script_name=None,
                 files_local_path=None,
                 delimiter="\t",
                 returns=None,
                 quotechar=None,
                 data_partition_column=None,
                 data_hash_column=None,
                 data_order_column=None,
                 is_local_order=False,
                 sort_ascending=True,
                 nulls_first=True):
        """
        DESCRIPTION:
            Table Operators are a type of User-Defined Function, only available when connected to a
            Vantage.

        PARAMETERS:
            data:
                Optional Argument.
                Specifies a teradataml DataFrame containing the input data for the script.

            script_name:
                Required Argument.
                Specifies the name of the user script.
                Types: str

            files_local_path:
                Required Argument.
                Specifies the absolute local path where the user script and all supporting files
                like model files, input data file reside.
                Types: str

            delimiter:
                Optional Argument.
                Specifies a delimiter to use when reading columns from a row and
                writing result columns.
                The delimiter is a single character chosen from the set of punctuation characters.
                Types: str

            returns:
                Required Argument.
                Specifies the output column definition.
                Types: Dictionary specifying column name to teradatasqlalchemy type mapping.
                Default: None

            data_hash_column:
                Optional Argument.
                Specifies the column to be used for hashing.
                The rows in the data are redistributed to AMPs based on the hash value of the
                column specified. The user-installed script file then runs once on each AMP.
                If there is no data_hash_column, then the entire result set,
                delivered by the function, constitutes a single group or partition.
                Types: str
                Note:
                    "data_hash_column" can not be specified along with "data_partition_column",
                    "is_local_order" and "data_order_column".

            data_partition_column:
                Optional Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Default Value: ANY
                Types: str OR list of Strings (str)
                Notes:
                    1) "data_partition_column" can not be specified along with "data_hash_column".
                    2) "data_partition_column" can not be specified along with "is_local_order = True".

            is_local_order:
                Optional Argument.
                Specifies a boolean value to determine whether the input data is to be ordered locally
                or not. 'sort_ascending' specifies the order in which the values in a group, or partition,
                are sorted. This argument is ignored, if data_order_column is None.
                When set to 'True', qualified rows are ordered locally in preparation to be input
                to the function.
                Default Value: False
                Types: bool
                Note:
                    "is_local_order" can not be specified along with "data_hash_column".
                    When "is_local_order" is set to 'True', "data_order_column" should be specified,
                    and the columns specified in "data_order_column" are used for local ordering.

            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                This argument is used with in both cases: "is_local_order = True"
                and "is_local_order = False".
                Types: str OR list of Strings (str)
                Note:
                    "data_order_column" can not be specified along with "data_hash_column".

            sort_ascending:
                Optional Argument.
                Specifies a boolean value to determine if the input data is to be sorted on
                the data_order_column column in ascending or descending order.
                When this is set to 'True' data is sorted in ascending order,
                otherwise data is sorted in descending order.
                This argument is ignored, if data_order_column is None.
                Default Value: True
                Types: bool

            nulls_first:
                Optional Argument.
                Specifies a boolean value to determine whether NULLS from input data are listed
                first or last during ordering.
                When this is set to 'True' NULLS are listed first, otherwise NULLS are listed last.
                This argument is ignored, if data_order_column is None.
                Default Value: True
                Types: bool

        RETURNS:
             An instance of TableOperator class.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Apply class extends this base class.
            apply_obj = Apply(data=barrierdf,
                              script_name='mapper.py',
                              files_local_path= '/root/data/scripts/',
                              apply_command='python3 mapper.py',
                              data_order_column="Id",
                              is_local_order=False,
                              nulls_first=False,
                              sort_ascending=False,
                              env_name = "test_env",
                              returns={"word": VARCHAR(15), "count_input": VARCHAR(2)},
                              style='csv',
                              delimiter=',')
        """
        self.result = None
        self._tblop_query = None
        self.data = data
        self.script_name = script_name
        self.files_local_path = files_local_path
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.returns = returns
        self.data_partition_column = data_partition_column
        self.data_hash_column = data_hash_column
        self.data_order_column = data_order_column
        self.is_local_order = is_local_order
        self.sort_ascending = sort_ascending
        self.nulls_first = nulls_first

        # Datatypes supported in returns clause of a table operator.
        self._supported_returns_datatypes = (BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, FLOAT, NUMBER,
                             TIMESTAMP, DATE, TIME, CHAR, VARCHAR, CLOB, BYTE, VARBYTE,
                             BLOB, PERIOD_DATE, PERIOD_TIME, PERIOD_TIMESTAMP, INTERVAL_YEAR,
                             INTERVAL_YEAR_TO_MONTH, INTERVAL_MONTH, INTERVAL_DAY, INTERVAL_DAY_TO_HOUR,
                             INTERVAL_DAY_TO_MINUTE, INTERVAL_DAY_TO_SECOND, INTERVAL_HOUR,
                             INTERVAL_HOUR_TO_MINUTE, INTERVAL_HOUR_TO_SECOND, INTERVAL_MINUTE,
                             INTERVAL_MINUTE_TO_SECOND, INTERVAL_SECOND
                             )

        # Create AnalyticsWrapperUtils instance which contains validation functions.
        # This is required for is_default_or_not check.
        # Rest all validation is done using _Validators.
        self.__awu = AnalyticsWrapperUtils()

        self.awu_matrix = []
        self.awu_matrix.append(["data", self.data, True, (tdmldf.dataframe.DataFrame)])
        self.awu_matrix.append(["data_partition_column", self.data_partition_column, True, (str, list), True])
        self.awu_matrix.append(["data_hash_column", self.data_hash_column, True, (str, list), True])
        self.awu_matrix.append(["data_order_column", self.data_order_column, True, (str, list), True])
        self.awu_matrix.append(["is_local_order", self.is_local_order, True, (bool)])
        self.awu_matrix.append(["sort_ascending", self.sort_ascending, True, (bool)])
        self.awu_matrix.append(["nulls_first", self.nulls_first, True, (bool)])
        self.awu_matrix.append(["script_name", self.script_name, True, (str), True])
        self.awu_matrix.append(["files_local_path", self.files_local_path, True, (str), True])
        self.awu_matrix.append(["delimiter", self.delimiter, True, (str), False])
        self.awu_matrix.append(["quotechar", self.quotechar, True, (str), False])

        # Perform the function validations.
        self.__validate()

    def __validate(self):
        """
        Function to validate Table Operator Function arguments, which verifies missing
        arguments, input argument and table types. Also processes the
        argument values.
        """
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        _Validators._validate_missing_required_arguments(self.awu_matrix)

        # Validate argument types
        _Validators._validate_function_arguments(self.awu_matrix,
                                                 skip_empty_check={"quotechar": ["\n", "\t"],
                                                                   "delimiter": ["\n"]})

        if self.data is not None:
            # Either hash or partition can be used.
            if all([self.data_hash_column, self.data_partition_column]):
                raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                                               "data_hash_column", "data_partition_column"),
                                          MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

            # Either hash or local order by can be used.
            elif all([self.data_hash_column, self.is_local_order]):
                raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                                               "data_hash_column", "is_local_order = True"),
                                          MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

            # Either hash or order by can be used.
            elif all([self.data_hash_column, self.data_order_column]):
                raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                                               "data_hash_column", "data_order_column"),
                                          MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

            # Either local order by or partition by can be used.
            if all([self.is_local_order, self.data_partition_column]):
                raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                                               "is_local_order=True",
                                                               "data_partition_column"),
                                          MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

            # local order by requires column name.
            if self.is_local_order and self.data_order_column is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING,
                                                               "data_order_column",
                                                               "is_local_order=True"),
                                          MessageCodes.DEPENDENT_ARG_MISSING)

            if self.__awu._is_default_or_not(self.data_partition_column, "ANY"):
                _Validators._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column",
                                                                    self.data, "data", True)

            _Validators._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column",
                                                                    self.data, "data", False)

            _Validators._validate_dataframe_has_argument_columns(self.data_hash_column, "data_hash_column",
                                                                    self.data, "data", False)

        # Check for length of the arguments "delimiter" and "quotechar".
        if self.delimiter is not None:
            _Validators._validate_str_arg_length('delimiter', self.delimiter, 'EQ', 1)

        if self.quotechar is not None:
            _Validators._validate_str_arg_length('quotechar', self.quotechar, 'EQ', 1)

        # The arguments 'quotechar' and 'delimiter' cannot take newline character.
        if self.delimiter == '\n':
            raise TeradataMlException(Messages.get_message(MessageCodes.NOT_ALLOWED_VALUES,
                                                           "\n", "delimiter"),
                                      MessageCodes.NOT_ALLOWED_VALUES)
        if self.quotechar == '\n':
            raise TeradataMlException(Messages.get_message(MessageCodes.NOT_ALLOWED_VALUES,
                                                           "\n", "quotechar"),
                                      MessageCodes.NOT_ALLOWED_VALUES)

        # The arguments 'quotechar' and 'delimiter' cannot have the same value.
        if self.delimiter == self.quotechar:
            raise TeradataMlException(Messages.get_message(MessageCodes.ARGUMENT_VALUE_SAME,
                                                           "delimiter", "quotechar"),
                                      MessageCodes.ARGUMENT_VALUE_SAME)


    def _execute(self, output_style='VIEW'):
        """
        Function to execute Table Operator queries.
        Create DataFrames for the required Table Operator output.
        """
        table_type = TeradataConstants.TERADATA_VIEW
        if output_style == OutputStyle.OUTPUT_TABLE.value:
            table_type = TeradataConstants.TERADATA_TABLE

        # Generate STDOUT table name and add it to the output table list.
        tblop_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_tblop_out_",
                                                                          use_default_database=True, gc_on_quit=True,
                                                                          quote=False,
                                                                          table_type=table_type
                                                                          )

        try:
            if output_style == OutputStyle.OUTPUT_TABLE.value:
                UtilFuncs._create_table(tblop_stdout_temp_tablename, self._tblop_query)
            else:
                UtilFuncs._create_view(tblop_stdout_temp_tablename, self._tblop_query)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)),
                                      MessageCodes.TDMLDF_EXEC_SQL_FAILED)


        self.result = self.__awu._create_data_set_object(
            df_input=UtilFuncs._extract_table_name(tblop_stdout_temp_tablename), source_type="table",
            database_name=UtilFuncs._extract_db_name(tblop_stdout_temp_tablename))

        return self.result

    def _returns_clause_validation(self):
        """
        DESCRIPTION:
            Function validates 'returns' clause for a table operator query.

        PARAMETERS:
            None.

        RETURNS:
            None

        RAISES:
            Error if argument is not of valid datatype.

        EXAMPLES:
            self._returns_clause_validation()
        """
        # Validate keys and datatypes in returns.
        if self.returns is not None:
            awu_matrix_returns = []
            for key in self.returns.keys():
                awu_matrix_returns.append(["keys in returns", key, False, (str), True])
                awu_matrix_returns.append(["values in returns", self.returns[key], False, self._supported_returns_datatypes])
            _Validators._validate_function_arguments(awu_matrix_returns)

    def setup_test_env(self, docker_image_location):
        """
                DESCRIPTION:
                    Function enables user to load already downloaded sandbox image.
                    This will enable users to run the Python scripts on client machine outside of
                    Open Analytics Framework.

                PARAMETERS:
                    docker_image_location:
                        Required Argument.
                        Specifies the location of image on user's system.
                        Types: str
                        Note:
                            For location to download docker image refer teradataml User Guide.

                RETURNS:
                    None.

                RAISES:
                    TeradataMlException

                EXAMPLES:
                    # Load example data.
                    load_example_data("Script", ["barrier"])

                    # Example - The script mapper.py reads in a line of text input ("Old Macdonald Had A Farm") from csv and
                    # splits the line into individual words, emitting a new row for each word.

                    # Create teradataml DataFrame objects.
                    >>> barrierdf = DataFrame.from_table("barrier")

                    # Create remote user environment.
                    >>> test_env = create_env('test_env', 'python_3.7.9', 'Demo environment');
                    User environment test_env created.

                    # Create an Apply object that allows user to execute script using Open Analytics Framework.
                    >>> apply_obj = Apply(data=barrierdf,
                                script_name='mapper.py',
                                files_local_path='data/scripts',
                                apply_command='python mapper.py',
                                delimiter=',',
                                env_name = "test_env",
                                data_partition_column="Id",
                                returns={"word": VARCHAR(15), "count_input": VARCHAR(2)}
                                )

                    # Run user script locally within docker container and using data from csv.
                    # This helps the user to fix script level issues outside of Open Analytics Framework.
                    # Setup the environment by providing local path to docker image file.
                    >>> apply_obj.setup_test_env(docker_image_location='/tmp/sto_sandbox_docker_image.tar'))
                    Loading image from /tmp/sto_sandbox_docker_image.tar. It may take few minutes.
                    Image loaded successfully.
        """
        self.awu_matrix_setup=[]
        self.awu_matrix_setup.append((["docker_image_location", docker_image_location, False, (str), True]))

        # Validate missing arguments
        _Validators._validate_missing_required_arguments(self.awu_matrix_setup)

        # Validate argument types
        _Validators._validate_function_arguments(self.awu_matrix_setup)

        # Load image from user provided location
        client = docker.from_env()
        if not Path(docker_image_location).exists():
            raise TeradataMlException(
                Messages.get_message(MessageCodes.INPUT_FILE_NOT_FOUND).format(docker_image_location),
                MessageCodes.INPUT_FILE_NOT_FOUND)
        else:
            try:
                print("Loading image from {0}. It may take few minutes.".format(docker_image_location))
                with open(docker_image_location, 'rb') as f:
                    client.images.load(f)
                print("Image loaded successfully.")
            except:
                raise

        # Set _latest_sandbox_exists to True - which indicates sandbox image for STO exists on the system
        configure._latest_sandbox_exists = True


    def test_script(self, supporting_files=None, input_data_file=None, script_args="", **kwargs):
        """
        DESCRIPTION:
            Function enables user to run script in docker container environment outside Vantage.
            Input data for user script is read from file.

        PARAMETERS:
            supporting_files:
                Optional Argument
                Specifies a file or list of supporting files like model files to be copied to the container.
                Types: string or list of str

            input_data_file:
                Required Argument.
                Specifies the absolute local path of input data file.
                If set to None, read data from AMP, else from file passed in the argument 'input_data_file'.
                Types: str

            script_args:
                Optional Argument.
                Specifies command line arguments required by the user script.
                Types: str

            kwargs:
                Optional Argument.
                Specifies the arguments used for reading data from all AMPs.
                Keys can be:
                    1. data_row_limit:
                        Specifies the number of rows to be taken from all amps when reading from a table or view
                        on Vantage.
                        Default Value: 1000
                        Types: int
                    2. password:
                        Specifies the password to connect to vantage where the data resides.
                        Types: str
                Types: dict
                Note: When data is read from file, if these arguments are passed, they will be ignored.

        RETURNS:
            Output from user script.

        RAISES:
            TeradataMlException

        EXAMPLES:
            Refer to help(Script)
        """
        self.awu_matrix_test=[]
        self.awu_matrix_test.append((["supporting_files", supporting_files, True, (str, list), True]))
        self.awu_matrix_test.append((["input_data_file", input_data_file, True, (str), True]))
        self.awu_matrix_test.append((["script_args", script_args, True, (str), False]))

        data_row_limit = kwargs.pop("data_row_limit", 1000)

        self.awu_matrix_test.append((["data_row_limit", data_row_limit, True, (int), True]))

        # Validate argument types
        _Validators._validate_function_arguments(self.awu_matrix_test)

        self.__validate()

        if data_row_limit <= 0:
            raise ValueError(Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT).
                             format("data_row_limit", "greater than"))

        # Either of 'input_data_file' or 'password' argument is required.
        password = kwargs.pop("password", None)
        if not (input_data_file or (self.data and password)):
            raise TeradataMlException(Messages.get_message(
                MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT, "input_data_file",
                "Script/Apply data and password"), MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

        if not self.script_name and self.files_local_path:
            raise TeradataMlException(Messages.get_message(MessageCodes.MISSING_ARGS,
                "script_name and files_local_path"), MessageCodes.MISSING_ARGS)

        docker_image_name = "stosandbox:1.0"
        client = docker.from_env()

        # Check if sandbox image exists on system
        if not client.images.list(docker_image_name):
            raise RuntimeError("STO sandbox image not found. Please run setup_sto_env.")

        try:
            # Create container
            container = client.containers.run(docker_image_name
                                              , stdin_open=True
                                              , tty=True
                                              , detach=True
                                              )

            path_in_docker_container = "/home/tdatuser"

            if script_args:
                script_args = "--script-args='{}'".format(script_args)

            files_to_copy = [self.script_name]

            if supporting_files is not None:
                if isinstance(supporting_files, str):
                    if supporting_files == "":
                        raise ValueError(Messages.get_message(MessageCodes.LIST_SELECT_NONE_OR_EMPTY, 'supporting_files'))
                    else:
                        files_to_copy.append(supporting_files)
                elif isinstance(supporting_files, list) and (len(supporting_files) == 0 or
                                                             any(file in [None, "None", ""] for file in supporting_files)):
                    raise ValueError(Messages.get_message(MessageCodes.LIST_SELECT_NONE_OR_EMPTY, 'supporting_files'))
                else:
                    files_to_copy.extend(supporting_files)

            if input_data_file is not None:
                files_to_copy.append(input_data_file)
                input_file_name = os.path.basename(input_data_file)

            for file in files_to_copy:
                file_path = os.path.join(self.files_local_path, file)
                if not Path(file_path).exists():
                    raise TeradataMlException(Messages.get_message(MessageCodes.INPUT_FILE_NOT_FOUND).format(file_path),
                                                MessageCodes.INPUT_FILE_NOT_FOUND)
                try:
                    self.__copy_to_docker_container(file_path, path_in_docker_container, container)
                except Exception as exp:
                    raise TeradataMlException(Messages.get_message(
                         MessageCodes.SANDBOX_CONTAINER_ERROR).format(str(exp)),
                         MessageCodes.SANDBOX_CONTAINER_ERROR)

            if input_data_file is not None:
                exec_cmd = ("python3 /home/tdatuser/script_executor.py file --script-type=py " 
                            "--user-script-path={0}/{1} --data-file-path={0}/{2} {3}".format(
                    path_in_docker_container, self.script_name, input_file_name, script_args))
            else:
                if self.data.shape[0] > data_row_limit:
                    raise ValueError(
                        Messages.get_message(MessageCodes.DATAFRAME_LIMIT_ERROR, 'data_row_limit', 'data_row_limit', data_row_limit))
                db_host = get_context().url.host
                user_name = get_context().url.username
                if not self.data._table_name:
                    self.data._table_name = df_utils._execute_node_return_db_object_name(
                                                self.data._nodeid, self.data._metaexpr)
                temp_db_name = '"{}"'.format(_get_current_databasename())
                table_name = self.data._table_name.replace(temp_db_name, "")
                table_name = table_name.replace("\"", "")
                if table_name and table_name[0] == '.':
                    table_name = table_name[1:]

                db_name = "--db-name='{}'".format(_get_current_databasename())

                if self.delimiter:
                    delimiter = "--delimiter='{}'".format(self.delimiter)

                exec_cmd = ("python3 /home/tdatuser/script_executor.py db --script-type=py "
                    "--user-script-path={}/{} --db-host={} --user={} --passwd={} --table={} "
                    "{} {} {}".format(path_in_docker_container, self.script_name, db_host,
                    user_name, password, table_name, db_name, script_args, delimiter))
            try:
                # Run user script
                exec_cmd_output = container.exec_run(exec_cmd)
                return exec_cmd_output.output.decode()
            except Exception as exp:
                raise TeradataMlException(Messages.get_message(
                     MessageCodes.SANDBOX_CONTAINER_ERROR).format(str(exp)),
                     MessageCodes.SANDBOX_CONTAINER_ERROR)
        finally:
            # Cleanup container
            container.stop()
            container.remove()

    def __copy_to_docker_container(self, local_file_path, path_in_docker_container, container):
        """
        DESCRIPTION:
            Function to copy files to docker container.

        PARAMETERS:
            local_file_path:
                Required Argument.
                Specifies the path to the file to be copied.
                Types: str

            path_in_docker_container:
                Required Argument.
                Specifies destination path in the docker container where file will be copied to.
                Types: str

            container:
                Required Argument.
                Specifies container id.
                Types: str

            RETURNS:
                None.

            RAISES:
                TeradataMLException.

        """
        # Create tar file
        tar_file_path = "{}.tar".format(local_file_path)
        file_name = os.path.basename(local_file_path)
        tar = tarfile.open(tar_file_path, mode='w')
        try:
            tar.add(local_file_path, arcname=file_name)
        finally:
            tar.close()
        data = open(tar_file_path, 'rb').read()

        # Copy file to docker container
        copy_status = container.put_archive(path_in_docker_container, data)
        os.remove(tar_file_path)

        if copy_status:
            return

    def __repr__(self):
        """
        Returns the string representation for the class instance.
        """
        if self.result is None:
            repr_string = "Result is empty. Please run execute_script first."
        else:
            repr_string = "############ STDOUT Output ############"
            repr_string = "{}\n\n{}".format(repr_string, self.result)
        return repr_string
