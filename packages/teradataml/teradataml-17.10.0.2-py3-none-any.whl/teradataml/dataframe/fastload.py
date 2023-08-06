#!/usr/bin/python
# ##################################################################
#
# Copyright 2019 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Abhinav Sahu (abhinav.sahu@teradata.com)
# Secondary Owner: 
#
# ##################################################################

import re
import datetime
import warnings
import pandas as pd

from sqlalchemy import MetaData, Table, Column
from sqlalchemy.exc import OperationalError as sqlachemyOperationalError
from teradataml.dataframe import dataframe
from teradataml.context.context import *
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
from teradataml.common.constants import TeradataConstants, DriverEscapeFunctions
from teradataml.common.utils import UtilFuncs
from teradataml.common.garbagecollector import GarbageCollector
from teradataml.utils.validators import _Validators
from teradataml.dataframe.copy_to import copy_to_sql, \
                                        _validate_pti_copy_parameters, _create_table_object, \
                                        _create_pti_table_object, _extract_column_info, \
                                        _check_columns_insertion_compatible
from teradataml.dataframe.data_transfer import _DataTransferUtils


def fastload(df, table_name, schema_name=None, if_exists='replace', index=False, 
             index_label=None, primary_index=None, types=None, batch_size=None, 
             save_errors=False, open_sessions=None):
    """
    The fastload() API writes records from a Pandas DataFrame to Teradata Vantage 
    using Fastload. FastLoad API can be used to quickly load large amounts of data
    in an empty table on Vantage.
    1. Teradata recommends to use this API when number rows in the Pandas DataFrame
       is greater than 100,000 to have better performance. To insert lesser rows, 
       please use copy_to_sql for optimized performance. The data is loaded in batches.
    2. FastLoad API cannot load duplicate rows in the DataFrame if the table is a
       MULTISET table having primary index.
    3. FastLoad API does not support all Teradata Advanced SQL Engine data types. 
       For example, target table having BLOB and CLOB data type columns cannot be
       loaded.
    4. If there are any incorrect rows i.e. due to constraint violations, data type 
       conversion errors, etc., FastLoad protocol ignores those rows and inserts 
       all valid rows. 
    5. Rows in the DataFrame that failed to get inserted are categorized into errors 
       and warnings by FastLoad protocol and these errors and warnings are stored 
       into respective error and warning tables by FastLoad API. 
    6. If save_errors argument is True, the names of error and warning tables are 
       shown once the fastload operation is complete. These tables will be persisted
       using copy_to_sql.

    For additional information about FastLoad protocol through teradatasql driver, 
    please refer the FASTLOAD section of https://pypi.org/project/teradatasql/#FastLoad
    driver documentation for more information.

    PARAMETERS:
        df:
            Required Argument. 
            Specifies the Pandas DataFrame object to be saved in Vantage.
            Types: pandas.DataFrame

        table_name:
            Required Argument.
            Specifies the name of the table to be created in Vantage.
            Types: String

        schema_name:
            Optional Argument. 
            Specifies the name of the database schema in Vantage to write to.
            Types: String
            Default: None (Uses default database schema).

        if_exists:
            Optional Argument.
            Specifies the action to take when table already exists in Vantage.
            Types: String
            Possible values: {'fail', 'replace', 'append'}
                - fail: If table exists, raise TeradataMlException.
                - replace: If table exists, drop it, recreate it, and insert data.
                - append: If table exists, insert data. Create if does not exist.
            Default: replace

        index:
            Optional Argument.
            Specifies whether to save Pandas DataFrame index as a column or not.
            Types: Boolean (True or False)
            Default: False

        index_label: 
            Optional Argument.
            Specifies the column label(s) for Pandas DataFrame index column(s).
            Types: String or list of strings
            Default: None

        primary_index:
            Optional Argument.
            Specifies which column(s) to use as primary index while creating table 
            in Vantage. When set to None, No Primary Index (NoPI) tables are created.
            Types: String or list of strings
            Default: None
            Example:
                primary_index = 'my_primary_index'
                primary_index = ['my_primary_index1', 'my_primary_index2', 'my_primary_index3']

        types: 
            Optional Argument.
            Specifies the data types for requested columns to be saved in Vantage.
            Types: Python dictionary ({column_name1: type_value1, ... column_nameN: type_valueN})
            Default: None

            Note:
                1. This argument accepts a dictionary of columns names and their required 
                teradatasqlalchemy types as key-value pairs, allowing to specify a subset
                of the columns of a specific type.
                   i)  When only a subset of all columns are provided, the column types
                       for the rest are assigned appropriately.
                   ii) When types argument is not provided, the column types are assigned
                       as listed in the following table:
                       +---------------------------+-----------------------------------------+
                       |     Pandas/Numpy Type     |        teradatasqlalchemy Type          |
                       +---------------------------+-----------------------------------------+
                       | int32                     | INTEGER                                 |
                       +---------------------------+-----------------------------------------+
                       | int64                     | BIGINT                                  |
                       +---------------------------+-----------------------------------------+
                       | bool                      | BYTEINT                                 |
                       +---------------------------+-----------------------------------------+
                       | float32/float64           | FLOAT                                   |
                       +---------------------------+-----------------------------------------+
                       | datetime64/datetime64[ns] | TIMESTAMP                               |
                       +---------------------------+-----------------------------------------+
                       | Any other data type       | VARCHAR(configure.default_varchar_size) |
                       +---------------------------+-----------------------------------------+
                2. This argument does not have any effect when the table specified using
                   table_name and schema_name exists and if_exists = 'append'.

        batch_size:
            Optional Argument.
            Specifies the number of rows to be loaded in a batch. For better performance,
            recommended batch size is at least 100,000. batch_size must be a positive integer. 
            If this argument is None, there are two cases based on the number of 
            rows, say N in the dataframe 'df' as explained below:
            If N is greater than 100,000, the rows are divided into batches of 
            equal size with each batch having at least 100,000 rows (except the 
            last batch which might have more rows). If N is less than 100,000, the
            rows are inserted in one batch after notifying the user that insertion 
            happens with degradation of performance.
            If this argument is not None, the rows are inserted in batches of size 
            given in the argument, irrespective of the recommended batch size. 
            The last batch will have rows less than the batch size specified, if the 
            number of rows is not an integral multiples of the argument batch_size.
            Default Value: None
            Types: int            

        save_errors:
            Optional Argument.
            Specifies whether to persist the error/warning information in Vantage 
            or not. If save_errors is set to False, error/warnings are not persisted
            as tables. If argument is set to True, the error and warnings information
            are presisted and names of error and warning tables are returned. Otherwise,
            the function returns None for the names of the tables.
            Default Value: False
            Types: bool

        open_sessions:
            Optional Argument.
            Specifies the number of Teradata data transfer sessions to be opened for fastload operation.
            Note : If "open_sessions" argument is not provided, the default value is the smaller of 8 or the
                   number of AMPs available.
                   For additional information about number of Teradata data-transfer
                   sessions opened during fastload, please refer to:
                   https://pypi.org/project/teradatasql/#FastLoad
            Default Value: None
            Types: int

    RETURNS:
        A dict containing the following attributes:
            1. errors_dataframe: It is a Pandas DataFrame containing error messages
               thrown by fastload. DataFrame is empty if there are no errors.
            2. warnings_dataframe: It is a Pandas DataFrame containing warning messages 
               thrown by fastload. DataFrame is empty if there are no warnings.
            3. errors_table: Name of the table containing errors. It is None, if 
               argument save_errors is False.
            4. warnings_table: Name of the table containing warnings. It is None, if 
               argument save_errors is False.

    RAISES:
        TeradataMlException

    EXAMPLES:
        Saving a Pandas DataFrame using Fastload:
            >>> from teradataml.dataframe.fastload import fastload
            >>> from teradatasqlalchemy.types import *

            >>> df = {'emp_name': ['A1', 'A2', 'A3', 'A4'],
                'emp_sage': [100, 200, 300, 400],
                'emp_id': [133, 144, 155, 177],
                'marks': [99.99, 97.32, 94.67, 91.00]
                }

            >>> pandas_df = pd.DataFrame(df)

            # a) Default execution
            >>> fastload(df = pandas_df, table_name = 'my_table')

            # b) Save a Pandas DataFrame with primary_index
            >>> pandas_df = pandas_df.set_index(['emp_id'])
            >>> fastload(df = pandas_df, table_name = 'my_table_1', primary_index='emp_id')

            # c) Save a Pandas DataFrame using fastload() with index and primary_index
            >>> fastload(df = pandas_df, table_name = 'my_table_2', index=True,
                         primary_index='index_label')

            # d) Save a Pandas DataFrame using types, appending to the table if it already exists
            >>> fastload(df = pandas_df, table_name = 'my_table_3', schema_name = 'alice',
                         index = True, index_label = 'my_index_label', 
                         primary_index = ['emp_id'], if_exists = 'append',
                         types = {'emp_name': VARCHAR, 'emp_sage':INTEGER,
                        'emp_id': BIGINT, 'marks': DECIMAL})

            # e) Save a Pandas DataFrame using levels in index of type MultiIndex
            >>> pandas_df = pandas_df.set_index(['emp_id', 'emp_name'])
            >>> fastload(df = pandas_df, table_name = 'my_table_4', schema_name = 'alice',
                         index = True, index_label = ['index1', 'index2'], 
                         primary_index = ['index1'], if_exists = 'replace')

            # f) Save a Pandas DataFrame by opening spcified number of teradata data transfer sessions
            >>> fastload(df = pandas_df, table_name = 'my_table_5', open_sessions = 2)

    """
    # Deriving global connection using context.get_context()
    con = get_context()
    try:
        if con is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.CONNECTION_FAILURE), 
                                      MessageCodes.CONNECTION_FAILURE)

        if isinstance(df, dataframe.DataFrame):
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, 
                                      'df', "Pandas DataFrame"), MessageCodes.UNSUPPORTED_DATATYPE)

        dt_obj = _DataTransferUtils(df=df, table_name=table_name, schema_name=schema_name, if_exists=if_exists,
                                    index=index, index_label=index_label, primary_index=primary_index,
                                    types=types, batch_size=batch_size,
                                    save_errors=save_errors, api_name='fastload',
                                    use_fastload=True, open_sessions=open_sessions)
        # Validate DataFrame & related flags; Proceed only when True
        dt_obj._validate()

        # We have commented out the PTI related code for now as fastload fails to 
        # load data into PTI tables. Same has been reported to gosql team. We'll 
        # un-comment this once the issue is fixed.
        # Check if the table to be created must be a Primary Time Index (PTI) table.
        # If a user specifies the timecode_column parameter, and attempt to create
        # a PTI will be made.
#        is_pti = False
#        if timecode_column is not None:
#            is_pti = True
#            if primary_index is not None:
#                warnings.warn(Messages.get_message(MessageCodes.IGNORE_ARGS_WARN,
#                                                   'primary_index',
#                                                   'timecode_column',
#                                                   'specified'))
#        else:
#            ignored = []
#            if timezero_date is not None: ignored.append('timezero_date')
#            if timebucket_duration is not None: ignored.append('timebucket_duration')
#            if sequence_column is not None: ignored.append('sequence_column')
#            if seq_max is not None: ignored.append('seq_max')
#            if columns_list is not None and (
#                    not isinstance(columns_list, list) or len(columns_list) > 0): ignored.append('columns_list')
#            if primary_time_index_name is not None: ignored.append('primary_time_index_name')
#            if len(ignored) > 0:
#                warnings.warn(Messages.get_message(MessageCodes.IGNORE_ARGS_WARN,
#                                                   ignored,
#                                                   'timecode_column',
#                                                   'missing'))
      
        # Check and calculate batch size for optimized performance for FastLoad
        if batch_size is None:
            batch_size = _get_batchsize(df)
        else:
            # Validate argument batch_size type
            _Validators._validate_function_arguments([["batch_size", batch_size,
                                                      False, (int)]])
            if batch_size < 100000:
                warnings.warn("The batch_size provided is less than 100000. Teradata \
                              recommends using 100000 as minimum batch size for \
                              improved performance.")

        # If the table created must be a PTI table, then validate additional parameters
        # Note that if the required parameters for PTI are valid, then other parameters, though being validated,
        # will be ignored - for example, primary_index
#        if is_pti:
#            _validate_pti_copy_parameters(df, timecode_column, timebucket_duration,
#                                          timezero_date, primary_time_index_name, columns_list,
#                                          sequence_column, seq_max, types, index, index_label)

        # Check if destination table exists
        table_exists = dt_obj._table_exists(con)

        # Raise an exception when the table not exists and if_exists='fail'
        dt_obj._check_table_exists(is_table_exists=table_exists)

        # Let's create the SQLAlchemy table object to recreate the table
        if not table_exists or if_exists.lower() == 'replace':
            dt_obj._create_or_replace_table(con, table_exists=table_exists)

            fl_dict = _insert_from_dataframe(dt_obj, table_name, batch_size)
            
        # Check column compatibility for insertion when table exists and if_exists = 'append'
        if table_exists and if_exists.lower() == 'append':
            # Create table object
            table = UtilFuncs._get_sqlalchemy_table(table_name,
                                                    schema_name=schema_name)

            cols = _extract_column_info(df, index=index, index_label=index_label)
            if table is not None:
                dt_obj._check_columns_compatibility(table_obj=table, cols=cols)

            stag_table_name = ''
            try:
                # Create staging table and use FastLoad to load data.
                # Then copy all the rows from staging table to target table using insert_into sql.
                stag_table_name = UtilFuncs._generate_temp_table_name(prefix="fl_stag",
                                                                      gc_on_quit=False,
                                                                      quote=False,
                                                                      table_type=TeradataConstants.TERADATA_TABLE)

                # Get the table name without schema name for further steps
                stag_table_name = stag_table_name.split('.')[-1].replace('"', '')
                # Create staging table object
                dt_obj._create_table(con, table_name=stag_table_name)

                # Insert data to staging table using faslload
                fl_dict = _insert_from_dataframe(dt_obj, stag_table_name, batch_size)

                # Insert data from staging table to target data.
                df_utils._insert_all_from_table(table_name,
                                                dt_obj._get_fully_qualified_table_name(table_name=stag_table_name),
                                                cols[0], schema_name)
            except:
                raise
            finally:
                if stag_table_name:
                    UtilFuncs._drop_table(dt_obj._get_fully_qualified_table_name(stag_table_name))

    except (TeradataMlException, ValueError, TypeError):
        raise
    except Exception as err:
        raise TeradataMlException(Messages.get_message(MessageCodes.FASTLOAD_FAILS), 
                                  MessageCodes.FASTLOAD_FAILS) from err
    return fl_dict

def _insert_from_dataframe(dt_obj, table_name, batch_size):
    """
    This is an internal function used to to sequentially extract column info from DataFrame,
    iterate rows, and insert rows manually. Used for Insertions to Tables with Pandas index.
    This uses DBAPI's escape functions for Fastload which is a batch insertion method.

    PARAMETERS:
        dt_obj:
            Object of _DataTransferUtils class.
            Types: object

        table_name:
            Name of the table.
            Types: String

        batch_size:
            Specifies the number of rows to be inserted in a batch.
            Types: Int

    RETURNS:
        dict

    RAISES:
        Exception

    EXAMPLES:
        _insert_from_dataframe(dt_obj, table_name, batch_size=100)
    """
    conn = get_connection().connection
    # Create a cursor from connection object
    cur = conn.cursor()

    error_tablename = ""
    warn_tablename = ""

    try:
#        if is_pti:
#            # This if for non-index columns.
#            col_names = _reorder_insert_list_for_pti(col_names, timecode_column, sequence_column)

        is_multi_index = isinstance(dt_obj.df.index, pd.MultiIndex)

        # The Fastload functionality is provided through several escape methods using
        # teradatasql; like: {fn teradata_try_fastload}, {fn teradata_get_errors}, etc.
        # - {fn teradata_nativesql}: This escape method is to specify to use native
        # SQL escape calls.
        # - {fn teradata_autocommit_off}: This escape method is to turn off auto-commit.
        # For FastLoad it is required that it should not execute any transaction
        # management SQL commands when auto-commit is on.
        # - {fn teradata_try_fastload}: This escape method tries to use FastLoad
        # for the INSERT statement, and automatically executes the INSERT as a regular
        # SQL statement when the INSERT is not compatible with FastLoad.
        # - {fn teradata_require_fastload}: This escape method requires FastLoad
        # for the INSERT statement, and fails with an error when the INSERT is not
        # compatible with FastLoad.
        # - {fn teradata_get_errors}: This escape method returns in one string all
        # data errors observed by FastLoad for the most recent batch. The data errors
        # are obtained from FastLoad error table 1, for problems such as constraint
        # violations, data type conversion errors, and unavailable AMP conditions.
        # - {fn teradata_get_warnings}: This escape method returns in one string all
        # warnings generated by FastLoad for the request. The warnings are obtained
        # from FastLoad error table 2, for problems such as duplicate rows.
        # - {fn teradata_logon_sequence_number}: This escape method returns the string
        # form of an integer representing the Logon Sequence Number(LSN) for the
        # FastLoad. Returns an empty string if the request is not a FastLoad.

        # Quoted, schema-qualified table name.
        table = dt_obj._get_fully_qualified_table_name(table_name)

        # Form the INSERT query for fastlod.
        ins = dt_obj._form_insert_query(table)

        #  Turn off autocommit before the Fastload insertion
        dt_obj._process_escape_functions(cur, escape_function= \
                                        DriverEscapeFunctions.AUTOCOMMIT_OFF)

        # Initialize dict template for saving error/warning information
        err_dict = {key:[] for key in ['batch_no', 'error_message']}
        warn_dict = {key:[] for key in ['batch_no', 'error_message']}

        batch_number = 1
        num_batches = int(dt_obj.df.shape[0]/batch_size)

        for i in range(0, dt_obj.df.shape[0], batch_size):
            # Add the remaining rows to last batch after second last batch
            if (batch_number == num_batches) :
                last_elem = dt_obj.df.shape[0]
            else :
                last_elem = i + batch_size

            pdf = dt_obj.df.iloc[i:last_elem]
            insert_list = []
            # Iterate rows of DataFrame per batch size to convert it to list of lists.
            for row_index, row in enumerate(pdf.itertuples(index=True)):
                insert_list2 = []
                for col_index, x in enumerate(pdf.columns):
                    insert_list2.append(row[col_index+1])
                if dt_obj.index is True:
                    insert_list2.extend(row[0]) if is_multi_index else insert_list2.append(row[0])
                insert_list.append(insert_list2)
            # Execute insert statement
            cur.execute (ins, insert_list)

            # Get error and warning information
            err, _ = dt_obj._process_fastexport_errors_warnings(ins)
            if len(err) != 0:
                err_dict['batch_no'].extend([batch_number] * len(err))
                err_dict['error_message'].extend(err)

            print("Processed {} rows in batch {}.".format(pdf.shape[0], batch_number))

            # If shape of DataFrame equal to last_elem of last batch.
            if last_elem == dt_obj.df.shape[0]:
                break

            batch_number += 1

        # Get logon sequence number to be used for error/warning table names
        logon_seq_number = dt_obj._process_escape_functions(cur, escape_function= \
                                                            DriverEscapeFunctions.LOGON_SEQ_NUM,
                                                            insert_query=ins)

        # Commit the rows
        conn.commit()

        # Get error and warning information, if any.
        # Errors/Warnings like duplicate rows are added here.
        _, warn = dt_obj._process_fastexport_errors_warnings(ins)
        if len(warn) != 0:
            warn_dict['batch_no'].extend(['batch_summary'] * len(warn))
            warn_dict['error_message'].extend(warn)

        # Get error and warning informations for error and warning tables, persist
        # error and warning tables to Vantage if user has specified save_error as True
        # else show it as pandas dataframe on console.
        pd_err_df = dt_obj._get_pandas_df_from_errors_warnings(err_dict)
        if not pd_err_df.empty:
            msg_type = "err"
            error_tablename = dt_obj._create_error_warnings_table(pd_err_df, msg_type, logon_seq_number[0][0])

        pd_warn_df = dt_obj._get_pandas_df_from_errors_warnings(warn_dict)
        if not pd_warn_df.empty:
            msg_type = "warn"
            warn_tablename = dt_obj._create_error_warnings_table(pd_warn_df, msg_type, logon_seq_number[0][0])

    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()

    return {"errors_dataframe": pd_err_df, "warnings_dataframe": pd_warn_df,
            "errors_table": error_tablename, "warnings_table": warn_tablename}

def _get_batchsize(df):
    """
    This internal function calculates batch size which should be more than 100000 
    for better fastload performance.

    PARAMETERS:
        df:
            The Pandas DataFrame object for which the batch size has to be calculated.
            Types: pandas.DataFrame

    RETURNS:
        Batch size i.e. number of rows to be inserted in a batch.

    RAISES:
        N/A

    EXAMPLES:
        _get_batchsize(df)
    """
    return df.shape[0] if df.shape[0] <= 100000 else round(df.shape[0]/int(df.shape[0]/100000))

def _create_table_for_fastload(df, con, table_name, schema_name=None, primary_index=None, 
                               is_pti=False, primary_time_index_name=None, timecode_column=None,
                               timezero_date=None, timebucket_duration=None, sequence_column=None,
                               seq_max=None, columns_list=[], types=None, index=False,
                               index_label=None):
    """
    PARAMETERS:
        df:
            Specifies the Pandas DataFrame object to be saved.
            Types: pandas.DataFrame
                
        con:
            A SQLAlchemy connectable (engine/connection) object
            Types: Teradata connection object

        table_name:
            Specifies the name of the table to be created in Vantage.
            Types: String

        schema_name:
            Specifies the name of the database schema in Teradata Vantage to write to.
            Types: String

        index:
            Specifies whether to save Pandas DataFrame index as a column or not.
            Types: Boolean (True or False)
            
        index_label: 
            Specifies the column label(s) for Pandas DataFrame index column(s).
            Types: String or list of strings
            
        primary_index:
            Specifies which column(s) to use as primary index while creating Teradata 
            table in Vantage. When None, No Primary Index Teradata tables are created.
            Types: String or list of strings

        types: 
            Specifies required data-types for requested columns to be saved in Vantage.
            Types: Python dictionary ({column_name1: type_value1, ... column_nameN: type_valueN})
                   
    RETURNS:
        Table object

    RAISES:
        TeradataMlException, sqlalchemy.OperationalError

    EXAMPLES:
        _create_table_for_fastload(df, con, table_name, schema_name, primary_index, 
                                   is_pti, primary_time_index_name, timecode_column, 
                                   timezero_date, timebucket_duration, sequence_column,
                                   seq_max, columns_list, types, index, index_label)
    """
    if is_pti:
        table = _create_pti_table_object(df=df, con=con, table_name=table_name,
                                         schema_name=schema_name, temporary=False,
                                         primary_time_index_name=primary_time_index_name,
                                         timecode_column=timecode_column, timezero_date=timezero_date,
                                         timebucket_duration=timebucket_duration,
                                         sequence_column=sequence_column, seq_max=seq_max,
                                         columns_list=columns_list, set_table=False,
                                         types=types, index=index, index_label=index_label)

        UtilFuncs._create_table_using_table_object(table)

