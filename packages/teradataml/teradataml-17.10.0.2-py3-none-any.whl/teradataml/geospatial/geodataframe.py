# ##################################################################
#
# Copyright 2021 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner:
#
# This file implements teradataml GeoDataFrame.
# teradataml GeoDataFrame allows user to access table on Vantage
# containing Geometry or Geospatial data.
#
# ##################################################################
import sqlalchemy
from teradataml.common.constants import GeospatialConstants, TeradataTypes
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.messages import Messages
from teradataml.common.utils import UtilFuncs
from teradataml.common.exceptions import TeradataMlException
from teradataml.dataframe.dataframe import DataFrame
from teradataml.geospatial.geodataframecolumn import GeoDataFrameColumn
from teradataml.utils.validators import _Validators
from teradatasqlalchemy import (GEOMETRY, MBR, MBB)

class GeoDataFrame(DataFrame):
    """
    The teradataml GeoDataFrame enables data manipulation, exploration, and
    analysis on tables, views, and queries on Teradata Vantage that contains
    Geospatial data.
    """
    def __init__(self, table_name=None, index=True, index_label=None,
                 query=None, materialize=False):
        """
        Constructor for teradataml GeoDataFrame.

        PARAMETERS:
            table_name:
                Optional Argument.
                The table name or view name in Teradata Vantage referenced by this DataFrame.
                Types: str

            index:
                Optional Argument.
                True if using index column for sorting, otherwise False.
                Default Value: True
                Types: bool

            index_label:
                Optional Argument.
                Column/s used for sorting.
                Types: str OR list of Strings (str)

            query:
                Optional Argument.
                SQL query for this Dataframe. Used by class method from_query.
                Types: str

            materialize:
                Optional Argument.
                Whether to materialize DataFrame or not when created.
                Used by class method from_query.

                One should use enable materialization, when the query passed
                to from_query(), is expected to produce non-deterministic
                results, when it is executed multiple times. Using this option
                will help user to have deterministic results in the resulting
                teradataml GeoDataFrame.
                Default Value: False (No materialization)
                Types: bool

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            df = DataFrame("mytab")
            df = DataFrame("myview")
            df = DataFrame("myview", False)
            df = DataFrame("mytab", True, "Col1, Col2")

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL
        """
        self.__geom_column = None
        # Call super(), to process the inputs.
        super().__init__(table_name=table_name, index=index,
                         index_label=index_label, query=query,
                         materialize=materialize)

    def _check_geom_column(self, metaexpr=None):
        """
        DESCRIPTION:
            Internal function to whether the metaexpr contains a geospatial
            type column or not.

        PARAMETERS:
            metaexpr:
                Required Argument.
                Specifies the teradataml DataFrame/teradataml GeoDataFrame
                metaexpr to validate for geospatial content.
                Types: _MetaExpression

        RETURNS:
            boolean.
            True if Geospatial data type column exists, False otherwise.

        RAISES:
            None.

        EXAMPLES:
            self._check_geom_column(metaexpr)
        """
        if metaexpr is None:
            metaexpr = self._metaexpr.c
        for col in metaexpr.c:
            if isinstance(col.type, (GEOMETRY, MBR, MBB)):
                return True
        return False

    def __getattr__(self, name):
        """
        Returns an attribute of the GeoDataFrame.

        PARAMETERS:
            name:
                Required Argument.
                Specifies the name of the attribute.
                Types: str

        RETURNS:
            Return the value of the named attribute of object (if found).

        EXAMPLES:
            df = GeoDataFrame('table')

            # You can access a column from the teradataml GeoDataFrame.
            df.c1

        RAISES:
            Attribute Error when the named attribute is not found.
        """

        # Look in the underlying _MetaExpression for columns
        for col in self._metaexpr.c:
            if col.name == name:
                return col

        # If "name" is present in any of the following 'GeospatialConstants'
        #   1. GeospatialConstants.PROPERTY_TO_NO_ARG_SQL_FUNCTION_NAME
        #   2. GeospatialConstants.METHOD_TO_ARG_ACCEPTING_SQL_FUNCTION_NAME
        #   3. GeospatialConstants.METHOD_TO_NO_ARG_SQL_FUNCTION_NAME
        # that means, it's a function that operates on Geometry Data.
        #
        # Look for such function names.
        if name in GeospatialConstants.PROPERTY_TO_NO_ARG_SQL_FUNCTION_NAME.value:
            # Geospatial functions which are exposed as property of teradataml
            # GeoDataFrame.
            return self.__process_geometry(func_name=name, all_geom=False,
                                           property=True)

        if name in GeospatialConstants.METHOD_TO_ARG_ACCEPTING_SQL_FUNCTION_NAME.value \
                or name in GeospatialConstants.METHOD_TO_NO_ARG_SQL_FUNCTION_NAME.value:
            # Geospatial functions which are exposed as method of teradataml
            # GeoDataFrame.
            return lambda *args, **kwargs: \
                self.__process_geometry(name, *args, **kwargs)

        # TODO - Raise error or Keep it open ended to accept SQL Function names.
        raise AttributeError("'GeoDataFrame' object has no attribute %s" % name)

    def __process_geometry(self, func_name, *args, **kwargs):
        """
        Function helps to execute the Geospatial function on the column(s)
        containing geometry data.

        PARAMETERS:
            func_name:
                Required Argument.
                Specifies the name of the function to execute.
                Types: string

            all_geom:
                Optional Argument.
                Specifies whether to execute the function on all geometry
                columns in the GeoDataFrame or not.
                When set to 'True', geospatial function specified in
                "func_name", is executed on all the columns containing
                geometry data, i.e., geospatial data.
                When set to 'False', geospatial function specified in
                "func_name", is executed only on the column represented
                by the 'GeoDataFrame.geometry' property.
                Default Value: False
                Types: bool

            property:
                Optional Argument.
                Specifies whether the function being executed should be treated
                as GeoDataFrame property or not.
                When set to 'True', geospatial function specified in
                "func_name", is treated as property, otherwise treated as
                method.
                Default Value: False
                Types: bool

            *args:
                Positional arguments passed to the method, i.e., geospatial
                function.

            **kwargs:
                Keyword arguments passed to the method, i.e., geospatial
                function.

        RETURNS:
            DataFrame or GeoDataFrame

        RAISES:
            None.

        EXAMPLES:
            self.__process_geometry(fname, all_geom, False, *c, **kwargs)
        """
        property = kwargs.pop("property", False)
        all_geom = kwargs.pop("all_geom", False)
        assign_args = {}
        if not all_geom:
            # Function will be run only on column represented by
            # 'GeoDataFrame.geometry' property.
            new_col = "{}_{}_geom".format(func_name, self.geometry.name)
            if property:
                # If property is set to True, then no need to pass **kwargs and
                # no need to invoke the call with parenthesis '()'.
                assign_args[new_col] = self.geometry[func_name]
            else:
                # Pass *args and **kwargs as function accepts arguments.
                assign_args[new_col] = self.geometry[func_name](*args, **kwargs)
        else:
            # Function will be run on all column(s) containing geometry data.
            # Columns containing geometry data can be following types:
            #   1. ST_GEOMETRY
            #   2. MBR
            #   3. MBB
            for col in self._metaexpr.c:
                if col.type in [GEOMETRY, MBR, MBB]:
                    new_col = "{}_{}".format(func_name, col.name)
                    if property:
                        # If property is set to True, then no need to pass
                        # **kwargs and no need to invoke the call with
                        # parenthesis '()'.
                        assign_args[new_col] = self[col.name][func_name]
                    else:
                        # Pass *args and **kwargs as function accepts arguments.
                        assign_args[new_col] = self[col.name][func_name](*args,
                                                                         **kwargs)

        return self.assign(**assign_args)

    @property
    def geometry(self):
        """
        DESCRIPTION:
            Returns a GeoColumnExpression for a column containing geometry data.
            If GeoDataFrame contains, multiple columns containing geometry data,
            then it returns reference to only one of them.
            Columns containing geometry data can be of following types:
                1. ST_GEOMETRY
                2. MBB
                3. MBR
            Refer 'GeoDataFrame.tdtypes' to view the Teradata column data types.

            Note:
                This property is used to execute any geospatial operation on
                GeoDataFrame, i.e., any geospatial function executed on
                GeoDataFrame, is executed on the geomtry column referenced by
                this property.

        RETURNS:
            GeoDataFrameColumn

        EXAMPLES:
            >>> load_example_data("geodataframe", ["sample_cities", "sample_streets"])
            >>> cities = GeoDataFrame("sample_cities")
            >>> streets = GeoDataFrame("sample_streets")
            >>> city_streets = cities.join(streets, how="cross", lsuffix="l", rsuffix="r")
            >>> city_streets
               l_skey  r_skey   city_name                                 city_shape  street_name              street_shape
            0       0       1  Oceanville            POLYGON ((1 1,1 3,6 3,6 0,1 1))  Main Street  LINESTRING (2 2,3 2,4 1)
            1       0       1  Oceanville            POLYGON ((1 1,1 3,6 3,6 0,1 1))   Coast Blvd  LINESTRING (12 12,18 17)
            2       1       1     Seaside  POLYGON ((10 10,10 20,20 20,20 15,10 10))   Coast Blvd  LINESTRING (12 12,18 17)
            3       1       1     Seaside  POLYGON ((10 10,10 20,20 20,20 15,10 10))  Main Street  LINESTRING (2 2,3 2,4 1)
            >>>

            # Check the name of the column containing geometry data, where
            # 'geometry' property references.
            >>> city_streets.geometry.name
            'city_shape'
            >>>

            # Check all the column types.
            >>> city_streets.tdtypes
            l_skey                                    INTEGER()
            r_skey                                    INTEGER()
            city_name       VARCHAR(length=40, charset='LATIN')
            city_shape                               GEOMETRY()
            street_name     VARCHAR(length=40, charset='LATIN')
            street_shape                             GEOMETRY()
            >>>
            >>>

            # Set the 'geometry' property to refer 'street_shape' column.
            >>> city_streets.geometry = city_streets.street_shape
            >>> city_streets.geometry.name
            'street_shape'
            >>>

            # Check whether the geometry referenced by 'geometry' property are 3D
            # or not.
            >>> city_streets.is_3D
               l_skey  r_skey   city_name                                 city_shape  street_name              street_shape  is_3D_street_shape_geom
            0       1       1     Seaside  POLYGON ((10 10,10 20,20 20,20 15,10 10))  Main Street  LINESTRING (2 2,3 2,4 1)                        0
            1       1       1     Seaside  POLYGON ((10 10,10 20,20 20,20 15,10 10))   Coast Blvd  LINESTRING (12 12,18 17)                        0
            2       0       1  Oceanville            POLYGON ((1 1,1 3,6 3,6 0,1 1))   Coast Blvd  LINESTRING (12 12,18 17)                        0
            3       0       1  Oceanville            POLYGON ((1 1,1 3,6 3,6 0,1 1))  Main Street  LINESTRING (2 2,3 2,4 1)                        0
            >>>

            # Use the geometry property to execute multiple geospatial functions
            # in conjunctions with GeoDataFrame.assign()
            # Get the geometry type.
            >>> geom_type = city_streets.geometry.geom_type
            # Check if geometry is simple or not.
            >>> is_simple = city_streets.geometry.is_simple
            # Check if geometry is valid or not.
            >>> is_valid = city_streets.geometry.is_valid
            >>>
            # Call GeoDataFrame.assign() and pass the above GeoDataFrameColumn, i.e.,
            # ColumnExpressions as input.
            >>> city_streets.assign(geom_type = geom_type,
            ...                     is_simple = is_simple,
            ...                     is_valid = is_valid
            ...                     )
               l_skey  r_skey   city_name                                 city_shape  street_name              street_shape      geom_type  is_simple  is_valid
            0       0       1  Oceanville            POLYGON ((1 1,1 3,6 3,6 0,1 1))  Main Street  LINESTRING (2 2,3 2,4 1)  ST_LineString          1         1
            1       0       1  Oceanville            POLYGON ((1 1,1 3,6 3,6 0,1 1))   Coast Blvd  LINESTRING (12 12,18 17)  ST_LineString          1         1
            2       1       1     Seaside  POLYGON ((10 10,10 20,20 20,20 15,10 10))   Coast Blvd  LINESTRING (12 12,18 17)  ST_LineString          1         1
            3       1       1     Seaside  POLYGON ((10 10,10 20,20 20,20 15,10 10))  Main Street  LINESTRING (2 2,3 2,4 1)  ST_LineString          1         1
            >>>
        """
        # Check if attribute __geom_column is already set or not.
        if self.__geom_column is not None:
            return self.__geom_column
        else:
            # No geom column identified, iterate over the columns
            # and set the attribute and return the same.
            for col in self._metaexpr.c:
                if isinstance(col.type, (GEOMETRY, MBR, MBB)):
                    self.__geom_column = col
                    return col

    @geometry.setter
    def geometry(self, column):
        """
        DESCRIPTION:
            Sets the geometry property to new geometry column.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column used for setting the 'geometry'
                property. Column passed to the function must contain the
                geometry data, i.e., column should be of type GEOMETRY, MBR,
                or MBB.
                Types: str or GeoDataFrameColumn

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Set the property by passing the column name.
            df.geometry = "geom_column"

            # Set the property by passing the GeoDataFrameColumn.
            df.geometry = df.geom_column
        """
        awu_matrix = []
        awu_matrix.append(["column", column, False, (str, GeoDataFrameColumn),
                           True])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        if isinstance(column, str):
            column = getattr(self, column)

        supported_types = (GEOMETRY, MBR, MBB)
        if not isinstance(column.type, supported_types):
            err_fmt = Messages.get_message(MessageCodes.INVALID_COLUMN_DATATYPE)
            err_ = err_fmt.format(column.name, "column", "Supported",
                                  supported_types)
            raise TeradataMlException(err_, MessageCodes.INVALID_COLUMN_DATATYPE)

        self.__geom_column = column

    def _create_dataframe_from_node(self, nodeid, metaexpr, index_label, undropped_columns=None):
        """
        DESCRIPTION:
            This function overrides the parent method, that creates the
            dataframe from node, i.e., using '_Parent_from_node' function.

            Parent class always returns a teradataml DataFrame, but for
            GeoDataFrame, we will return teradataml DataFrame or teradataml
            GeoDataFrame, based on whether the resultant DataFrame contains
            geometry column or not.

        PARAMETERS:
            nodeid:
                Required Argument.
                Specifies the nodeid for the DataFrame or GeoDataFrame.
                Types: str

            metaexpr:
                Required Argument.
                Specifies the metadata for the resultant object.
                Types: _MetaExpression

            index_label:
                Required Argument.
                Specifies list specifying index column(s) for the DataFrame.
                Types: str OR list of Strings (str)

            undropped_columns:
                Optional Argument.
                Specifies list of index column(s) to be retained as columns for printing.
                Types: list

        RETURNS:
            teradataml DataFrame or teradataml GeoDataFrame

        RAISES:
            None

        EXAMPLES:
            self._create_dataframe_from_node(new_nodeid, new_meta,
                                             self._index_label, undropped_columns)
        """
        # TODO: <DEPENDENT_ON_GEOMETRY_DATATYPES_SUPPORT_IN_teradatasqlalchemy>
        #   1. Add the test cases.
        #       a. Run teradataml DataFrame functions, that will result in
        #           dropping the geometry datatype columns.
        #       b. Run GeoDataFrame.assign() with "drop_columns=True" and
        #           run geospatial function on a column, a function that will
        #           not return the Geometry data type column.
        #       All other cases, this should return the object of this class.
        if not self._check_geom_column(metaexpr):
            # If generated metaexpr does not contain a geometry column
            # then we should return the teradataml DataFrame.
            return DataFrame._from_node(nodeid, metaexpr, index_label, undropped_columns)
        else:
            # Return the teradataml GeoDataFrame.
            return self._from_node(nodeid, metaexpr, index_label, undropped_columns)

    def _get_metadata_from_metaexpr(self, metaexpr):
        """
        Private method for setting _metaexpr and retrieving column names and types.

        PARAMETERS:
            metaexpr - Parent meta data (_MetaExpression object).

        RETURNS:
            None

        RAISES:
            None

        EXAMPLE:
            self._get_metadata_from_metaexpr(metaexpr)
        """
        self._metaexpr = self._generate_child_metaexpr(metaexpr)
        self._column_names_and_types = []
        self._td_column_names_and_types = []
        self._td_column_names_and_sqlalchemy_types = {}
        for col in self._metaexpr.c:
            if isinstance(col.type, sqlalchemy.sql.sqltypes.NullType):
                tdtype = TeradataTypes.TD_NULL_TYPE.value
            else:
                tdtype = "{}".format(col.type)

            self._column_names_and_types.append((str(col.name), UtilFuncs._teradata_type_to_python_type(col.type)))
            self._td_column_names_and_types.append((str(col.name), tdtype))
            self._td_column_names_and_sqlalchemy_types[(str(col.name)).lower()] = col.type

            # Set the Geometry column, which will be used as "geometry"
            # property.
            if self.__geom_column is None and \
                    isinstance(col.type, (GEOMETRY, MBR, MBB)):
                self.__geom_column = col

        if self.__geom_column is None:
            error_code = MessageCodes.NO_GEOM_COLUMN_EXIST
            raise TeradataMlException(Messages.get_message(error_code), error_code)


    def _generate_child_metaexpr(self, metaexpr):
        """
        Internal function that generates the metaexpression by converting
        _SQLColumnExpression to GeoDataFrameColumn.

        PARAMETERS:
            metaexpr:
                Required Arguments.
                Specifies the metaexpression to update.
                Types: _MetaExpression

        RETURNS:
            _MetaExpression

        RAISES:
            None.

        EXAMPLES:
            self._metaexpr = self._generate_child_metaexpr(metaexpr)
        """
        metaexpr.c = [GeoDataFrameColumn(col.expression)
                      if not isinstance(col, GeoDataFrameColumn) else col
                      for col in metaexpr.c]
        return metaexpr


