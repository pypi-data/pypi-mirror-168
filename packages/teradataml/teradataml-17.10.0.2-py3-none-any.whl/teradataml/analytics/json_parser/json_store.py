"""
Unpublished work.
Copyright (c) 2021 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: pradeep.garre@teradata.com
Secondary Owner: PankajVinod.Purandare@teradata.com

This file implements the class _JsonStore, which stores the json data for analytic functions.
_JsonStore will be used to access the json data of analytic functions. so, one should refer to
_JsonStore to access the json data instead of parsing the json data again.
"""
import sys
from teradataml.analytics.json_parser.metadata import _AnlyFuncMetadata
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.exceptions import TeradataMlException
from teradataml.utils.validators import _Validators


class _JsonStore:
    """ An internal class for storing json data. """
    __data = {}
    version = None
    # Map to store function type, its corresponding lowest supported version
    # and parent JSON directory.
    func_info = {}
    # Map to store function type and corresponding version of JSON directory.
    func_type_json_version = {}
    # Functions to exclude from json store.
    _functions_to_exclude = {"NPath", "NaiveBayesPredict", "DecisionTreePredict"}

    @classmethod
    def add(cls, json_object):
        """
        DESCRIPTION:
            Function to add the json object to _JsonStore.

        PARAMETERS:
            json_object:
                Required Argument.
                Specifies the json object.
                Types: Object of type _AnlyFuncMetadata

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            # Add json data for XGBoost.
            _JsonStore.add(xg_boost_json_data)
        """
        # Validate whether the json object is of type _AnlyFuncMetadata or not.
        arg_info_matrix = [["json_object", json_object, False, _AnlyFuncMetadata]]
        _Validators._validate_function_arguments(arg_info_matrix)

        cls.__data[json_object.func_name] = json_object

    @classmethod
    def clean(cls):
        """
        DESCRIPTION:
            Function to clean the json store. This function does below:
            * Removes all the analytic functions attached to teradataml from _JsonStore.
            * Remove all json objects from _JsonStore.
            * unset the json store version.

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            # remove all json objects from _JsonStore.
            _JsonStore.clean()
        """
        for func_name in cls.__data:
            if getattr(sys.modules["teradataml"], func_name, None):
                delattr(sys.modules["teradataml"], func_name)
        cls.__data.clear()
        cls.version = None
        cls.func_info.clear()
        cls.func_type_json_version.clear()

    @classmethod
    def get_function_metadata(cls, analytic_function_name):
        """
        DESCRIPTION:
            Function to get the Analytic function metadata a.k.a json object.

        PARAMETERS:
            analytic_function_name:
                Required Argument.
                Specifies the analytic function name.
                Types: str

        RETURNS:
            Object of type _AnlyFuncMetadata

        RAISES:
            TeradataMlException.

        EXAMPLES:
            # Get json data for XGBoost.
            _JsonStore.get_function_metadata("XGBoost")
        """
        # Validate whether the analytic_function_name is of type str or not.
        arg_info_matrix = [["analytic_function_name", analytic_function_name, False, str]]
        _Validators._validate_function_arguments(arg_info_matrix)

        if analytic_function_name in cls.__data:
            return cls.__data[analytic_function_name]
        else:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.INVALID_FUNCTION_NAME,
                                     analytic_function_name),
                MessageCodes.INVALID_FUNCTION_NAME)

    @classmethod
    def _get_function_list(cls):
        """
        DESCRIPTION:
            Function to get the list of available analytic functions.

        PARAMETERS:
            None

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            _JsonStore._get_function_list()
        """
        return [*cls.__data] + list(cls._functions_to_exclude)
