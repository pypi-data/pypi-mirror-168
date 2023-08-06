"""
Unpublished work.
Copyright (c) 2021 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: pradeep.garre@teradata.com
Secondary Owner: PankajVinod.Purandare@teradata.com

This file implements json file related argument names.
"""
from enum import Enum


class PartitionKind(Enum):
    ONE = "1"
    ANY = "ANY"
    DIMENSION = "DIMENSION"
    NONE = "NONE"
    # DIMENSIONKEY = "DIMENSIONKEY"
    # DIMENSIONKEYANY = "DIMENSIONKEYANY"
    # KEY = "KEY"
    # ONEONLY = "ONEONLY"
    # ANYONLY = "ANYONLY"

class JsonFields:
    ALLOWS_LISTS = "allowsLists"
    DATATYPE = "datatype"
    BOOL_TYPE = "BOOLEAN"
    INT_TYPE = ["INTEGER", "LONG"]
    FLOAT_TYPE = ["DOUBLE", "DOUBLE PRECISION", "FLOAT"]
    INPUT_TABLES = "input_tables"
    OUTPUT_TABLES = "output_tables"
    ARGUMENT_CLAUSES = "argument_clauses"
    R_NAME = "rName"
    NAME = "name"
    FUNCTION_TDML_NAME = "function_tdml_name"
    R_FOMULA_USAGE = "rFormulaUsage"
    R_ORDER_NUM = "rOrderNum"
    TDML_SEQUENCE_COLUMN_NAME = "sequence_column"
    USEINR = "useInR"
    IS_REQUIRED = "isRequired"
    DESCRIPTION = "description"
    R_DESCRIPTION = "rDescription"
    DEFAULT_VALUE = "defaultValue"
    DEFAULT_VALUES = "defaultValues"
    LOWER_BOUND = "lowerBound"
    UPPER_BOUND = "upperBound"
    R_DEFAULT_VALUE = "rDefaultValue"
    ALLOW_PADDING = "allowPadding"
    R_FORMULA_USAGE = "rFormulaUsage"
    ALLOW_NAN = "allowNaN"
    CHECK_DUPLICATE = "checkDuplicate"
    IS_OUTPUT_COLUMN = "isOutputColumn"
    LOWER_BOUND_TYPE = "lowerBoundType"
    UPPER_BOUND_TYPE = "upperBoundType"
    REQUIRED_LENGTH = "requiredLength"
    MATCH_LENGTH_OF_ARGUMENT = "matchLengthofArgument"
    PERMITTED_VALUES = "permittedValues"
    TARGET_TABLE = "targetTable"
    ALLOWED_TYPES = "allowedTypes"
    ALLOWED_TYPE_GROUPS = "allowedTypeGroups"
    ALTERNATE_NAMES = "alternateNames"
    IS_OUTPUT_TABLE = "isOutputTable"
    OUTPUT_SCHEMA = "outputSchema"
    REQUIRED_INPUT_KIND = "requiredInputKind"
    PARTITION_BY_ONE = "partitionByOne"
    PARTITION_BY_ONE_INCLUSIVE = "partitionByOneInclusive"
    IS_ORDERED = "isOrdered"
    IS_LOCAL_ORDERED = "isLocalOrdered"
    HASH_BY_KEY = "hashByKey"
    SEQUENCE_INPUT_BY = "sequenceinputby"
    UNIQUE_ID = "UniqueId"
    INFINITY = "Infinity"
    SHORT_DESCRIPTION = "short_description"
    LONG_DESCRIPTION = "long_description"
    STRING = "String"
    COLUMN_NAMES = "COLUMN_NAMES"
    FUNCTION_TYPE = "function_type"
    SUPPORTS_VOLATILE_TABLE = "SupportVolatileTable"
    IS_REQUIRED_DEPENDENT = "isRequiredDependent"
    DEPENDENT_ARGUMENT_NAME = "argumentName"
    DEPENDENT_ARGUMENT_TYPE = "argumentType"
    OPERATOR = "operator"
    DEPENDENT_ARGUMENT_VALUE = "argumentValue"


class SqleJsonFields(JsonFields):
    pass