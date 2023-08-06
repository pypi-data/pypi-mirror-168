"""
Unpublished work.
Copyright (c) 2021 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: pradeep.garre@teradata.com, gouri.patwardhan@teradata.com
Secondary Owner: PankajVinod.Purandare@teradata.com

This file implements the helper methods and classes which are required to
process In-DB Functions.
"""

from teradataml.options.configure import configure
from teradataml.analytics.json_parser.json_store import _JsonStore
from teradataml.analytics.json_parser.metadata import _AnlyFuncMetadata
from teradataml.common.constants import TeradataAnalyticFunctionTypes
import json, os
from teradataml import _version


def _get_json_data_from_tdml_repo():
    """
    DESCRIPTION:
        An internal function to parse the json files stored in teradataml repo. This function,
        first checks whether the version of json store is same as database version.
        If both versions are same, it then returns an empty list, i.e., the framework
        will neither parse the json files nor generate the SQLE functions. Otherwise cleans
        the json store and parses the json files in the corresponding directory and adds
        the json data to json store.

    PARAMETERS:
        None.

    RAISES:
        None.

    RETURNS:
        An iterator of _AnlyFuncMeta object OR list

    EXAMPLES:
        >>> _get_json_data_from_tdml_repo()
    """

    # Check if the json store version is matched with Vantage database version. If
    # both versions are matched, then the json store has data available so no need
    # to parse again.
    if configure.database_version != _JsonStore.version:

        # Json store version is different from database version. So, json's should
        # be parsed again. Before parsing the json, first clean the json store.
        _JsonStore.clean()

        # Set the json store version to current database version.
        _JsonStore.version = configure.database_version

        # Load the mapping information for all analytic functions which are version dependent into _JsonStore.
        _load_anlyfuncs_jsons_versions_info()

        json_file_directories = __get_json_files_directory()

        # For the corresponding database version, if teradataml does not have any json
        # files, then return an empty list. So framework will not attach any SQLE function
        # to teradataml.
        if not json_file_directories:
            return []

        # Read the directory, parse the json file and add the _AnlyFuncMeta object to json store
        # and yield the same.
        for json_file_directory in json_file_directories:
            for json_file in os.listdir(json_file_directory):

                file_path = os.path.join(json_file_directory, json_file)
                with open(file_path, encoding="utf-8") as fp:
                    json_data = json.load(fp)
                    metadata = _AnlyFuncMetadata(json_data, file_path)

                    # Functions which do not need to participate in IN-DB Framework
                    # should not be stored in _JsonStore.
                    if metadata.func_name in _JsonStore._functions_to_exclude:
                        continue
                    _JsonStore.add(metadata)
                    yield metadata

    # If both database version and json store version are same, return an empty list so that
    # framework will not attach any SQLE function to teradataml.
    else:
        return []


def _load_anlyfuncs_jsons_versions_info():
    """
    DESCRIPTION:
        Function populates following information for analytic functions:
            * Lowest supported version.
            * Parent directory containing JSONs.
            * Nearest matching JSON directory for a particular database version.

    PARAMETERS:
        None

    RETURNS:
        None

    RAISES:
        None

    EXAMPLES:
        >>> _load_anlyfuncs_jsons_versions_info()
    """
    # Get the directory of teradataml module.
    module_directory = os.path.dirname(_version.__file__)

    # Populate the information about the lowest supported version and parent directory of JSONs
    # for all available analytic functions whose JSONs are version dependent.
    _JsonStore.func_info[TeradataAnalyticFunctionTypes.SQLE.value] = [16.20, os.path.join(module_directory,
                                                                      "analytics", "jsons", "sqle")]
    _JsonStore.func_info[TeradataAnalyticFunctionTypes.TABLEOPERATOR.value] = [17.00, os.path.join(module_directory,
                                                                               "table_operators", "jsons")]

    # Get the closest matching JSON directory out of all directories corresponding
    # to JSONs of different version.
    db_version = float(_JsonStore.version[:5])
    for func in _JsonStore.func_info:
        func_base_version, parent_dir = _JsonStore.func_info[func]
        if db_version >= func_base_version:
            closest_version = _get_closest_version_json_dir(parent_dir, db_version)
            if closest_version:
                _JsonStore.func_type_json_version[func] = closest_version


def __get_json_files_directory():
    """
    DESCRIPTION:
        An internal function to get the corresponding directory name, which
        contains the json files.

    PARAMETERS:
        None.

    RAISES:
        None.

    RETURNS:
        list

    EXAMPLES:
        >>> __get_json_files_directory()
    """
    # If function has version specific JSON directory, return it by using mapping information in
    # _Jsonstore else return common JSON directory.
    for func_type in _JsonStore.func_type_json_version:
        yield os.path.join(_JsonStore.func_info[func_type][1], _JsonStore.func_type_json_version[func_type])


def _get_closest_version_json_dir(parent_dir, database_version):
    """
    DESCRIPTION:
        Internal function to get the nearest matching JSON directory for a database
        version from the available JSON directories for the functions.

    PARAMETERS:
        parent_dir:
            Required Argument.
            Specifies the parent dirctory for JSONs of all teradataml version.
            Types: str

        database_version:
            Required Argument.
            Specifies the database version.
            Types: float

    RAISES:
        None.

    RETURNS:
        str

    EXAMPLES:
        >>> _get_closest_version_json_dir("path_to_teradataml/teradataml/analytics/jsons/sqle", 17.10)
    """
    # Get the exact matching JSON directory name for current database version.
    # If matching directory exists, return it.
    matching_dir = format(database_version, '.2f')
    if matching_dir in os.listdir(parent_dir):
        return matching_dir

    # If exact matching JSON directory is not found,
    # return the directory corresponding to the closest lower version.
    lower_versions = (json_dir for json_dir in os.listdir(parent_dir) if float(json_dir) <= database_version)

    # If generator generates non-empty list, return max of all versions from that list,
    # else while an empty list is passed to max() it throws ValueError, so return None.
    try:
        return max(lower_versions)
    except ValueError:
        return None
