#!/usr/bin/python
# ####################################################################
#
# Copyright (c) 2020 by Teradata Corporation. All rights reserved.
# TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Trupti Purohit (trupti.purohit@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
#
# Version: 1.0
# Represents remote user environment from Vantage Languages Ecosystem.
# ####################################################################

import functools
import inspect
import requests
from json.decoder import JSONDecodeError
import os
from pathlib import Path
import pandas as pd
import requests
from datetime import datetime
from sqlalchemy import func
from teradataml import configure
from concurrent.futures import ThreadPoolExecutor, wait
from teradataml.context.context import _get_user
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.garbagecollector import GarbageCollector
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.constants import TeradataConstants
from teradataml.common.utils import UtilFuncs
from teradataml.dbutils.filemgr import install_file
from teradataml.utils.validators import _Validators
from teradatasql import OperationalError as SqlOperationalError

def _get_ues_url(env_type="users", version="v1", **kwargs):
    """
    DESCRIPTION:
        Function to get the URL for inititating REST call to UES.

    PARAMETERS:
        env_type:
            Optional Argument.
            Specifies the type of resource in URL.
            Default Value: users
            Types: str

        version:
            Optional Argument.
            Specifies the UES API version.
            Default Value: v1
            Types: str
        
        api_name:
            Optional Argument.
            Specifies the name of the teradataml UES API to mention in the error message.
            Types: str

        kwargs:
            Specifies keyword arguments that can be passed to get the URL.

    RETURNS:
        str

    RAISES:
        TeradataMlException, RuntimeError

    EXAMPLES:
            >>> _get_ues_url("base_environments") # URL for listing base environments.
            >>> _get_ues_url() # URL to create/remove/list the user environment(s).
            >>> _get_ues_url(env_name="alice_env") # URL to delete/list files in an environment.
            >>> _get_ues_url(env_name="alice_env", files=True, api_name="install_file") # URL to install/replace file in environment.
            >>> _get_ues_url(env_name="alice_env", files=True, file_name="a.py") # URL to remove a file in environment.
            >>> _get_ues_url(env_name="alice_env", libs=True, api_name="libs") # URL to install/uninstall/update/list library in environment.
            >>> _get_ues_url(env_type="fm", claim_id="123-456", api_name=status) # URL for checking the task status.
            >>> _get_ues_url(env_type="fm", fm_type="export", claim_id="123-456") # URL for exporting a file.
            >>> _get_ues_url(env_type="fm", fm_type="import", api_name="install_file) # URL for generating end point to upload file.
            >>> _get_ues_url(env_name=self.env_name, files=True, is_property=True, api_name="files") # URL for listing down the files. 
    """
    api_name = kwargs.pop("api_name", inspect.stack()[1].function)

    # Raise error if user is not connected to Vantage.
    if _get_user() is None:
        error_msg = Messages.get_message(MessageCodes.FUNC_EXECUTION_FAILED,
                                         api_name,
                                         "Create context before using {}.".format(api_name))
        raise TeradataMlException(error_msg, MessageCodes.FUNC_EXECUTION_FAILED)

    if configure._ues_base_url is None:
        error_msg = Messages.get_message(MessageCodes.DEPENDENT_ARGUMENT,
                                         api_name, 'configure._ues_base_url')
        raise RuntimeError(error_msg)

    ues_url = "{}/user-environment-service/api/{}/{}".format(configure._ues_base_url, version, env_type)

    if env_type not in ("users", "fm"):
        return ues_url

    elif env_type == "fm":
        fm_type = kwargs.get("fm_type")
        if fm_type == "import":
            return "{}/import".format(ues_url)
        elif fm_type == "export":
            return "{}/export/{}".format(ues_url, kwargs["claim_id"])
        else:
            return "{}/users/{}/tasks/{}".format(ues_url, _get_user(), kwargs["claim_id"])

    # We will reach here to process "users" env type.
    ues_url = "{0}/{1}/environments".format(ues_url, _get_user())

    env_name, files, libs = kwargs.get("env_name"), kwargs.get("files", False), kwargs.get("libs", False)
    if env_name is not None:
        ues_url = "{0}/{1}".format(ues_url, env_name)

    if files:
        ues_url = "{0}/{1}".format(ues_url, "files")
        file_name = kwargs.get("file_name")
        if file_name is not None:
            ues_url = "{0}/{1}".format(ues_url, file_name)
    elif libs:
        ues_url = "{0}/{1}".format(ues_url, "libraries")

    return ues_url


def _process_ues_response(api_name, response, success_status_code=None):
    """
    DESCRIPTION:
        Function to process and validate the UES Response.

    PARAMETERS:
        api_name:
            Required Argument.
            Specifies the name of the teradataml UES API.
            Types: str

        response:
            Required Argument.
            Specifies the response recieved from UES.
            Types: requests.Response

        success_status_code:
            Optional Argument.
            Specifies the expected success status code for the corresponding UES API.
            Default Value: None
            Types: int

    RETURNS:
        dict, if status code of the response is same as success status code.

    RAISES:
        TeradataMlException.

    EXAMPLES:
            >>> _process_ues_response("list_base_envs", resp)
    """
    try:
        # Success status code ranges between 200-300.
        if (success_status_code is None and 200 <= response.status_code < 300) or \
                (success_status_code == response.status_code):
            return response.json()

        # teradataml API got an error response. Error response is expected as follows -
        # {
        #     "status": 404,
        #     "req_id": "1122.3.1",
        #     "error_code": "201",
        #     "error_description": "Environment not found."
        # }
        # Extract the fields and raise error accordingly.

        add_paranthesis = lambda msg: "({})".format(msg) if msg else msg

        data = response.json()
        request_id = add_paranthesis(data.get("req_id", ""))
        error_code = add_paranthesis(data.get("error_code", ""))
        error_description = "{}{} {}".format(request_id, error_code, data.get("error_description", ""))

        exception_message = "Request Failed - {}".format(error_description)

        error_msg = Messages.get_message(MessageCodes.FUNC_EXECUTION_FAILED,
                                         api_name,
                                         exception_message)
        raise TeradataMlException(error_msg, MessageCodes.FUNC_EXECUTION_FAILED)

    # teradataml API may not get a Json API response in some cases.
    # So, raise an error with the response received as it is.
    except JSONDecodeError:
        error_msg = Messages.get_message(MessageCodes.FUNC_EXECUTION_FAILED,
                                         api_name,
                                         response.text)
        raise TeradataMlException(error_msg, MessageCodes.FUNC_EXECUTION_FAILED)


def _get_auth_token():
    # TODO: Function will be implemented with ELE-4753.
    return {"X-Auth-Token": ""}


class UserEnv:

    def __init__(self, env_name, base_env, desc=None):
        """
        DESCRIPTION:
            Represents remote user environment from Vantage Languages Ecosystem.
            The object of the class can be created either by using create_env() function which will
            create a new remote user environment and returns an object of UserEnv class or
            by using get_env() function which will return an object representing the existing remote user environment.

        PARAMETERS:
            env_name:
                Required Argument.
                Specifies the name of the remote user environment.
                Types: str

            base_env:
                Required Argument.
                Specifies base environment interpreter which is used to create remote user environment.
                Types: str

            desc:
                Optional Argument.
                Specifies description associated with the remote user environment.
                Types: str

        RETURNS:
            Instance of the class UserEnv.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create a new environment and get instance of UserEnv class.
            env1 = create_env('testenv', 'python_3.7.9', 'Test environment')

            # Get an object for existing user environment.
            env2 = get_env('testenv')
        """

        # Make sure the initialization happens only using either create_env() or get_env().
        if inspect.stack()[1][3] not in ['create_env', 'get_env']:
            raise TeradataMlException(Messages.get_message(
                MessageCodes.USE_FUNCTION_TO_INSTANTIATE).format("A teradataml UserEnv object","create_env() and get_env() functions from teradataml.scriptmgmt.lls_utils"),
                                      MessageCodes.USE_FUNCTION_TO_INSTANTIATE)

        self.env_name = env_name
        self.base_env = base_env
        self.desc = desc

        # Initialize variables to store files and libraries from the remote user environment.
        self.__files = None
        self.__libs = None

        # This variable will be used to detect if files from the remote user environment are changed by
        # install_file or remove_file functions.
        self.__files_changed = None

        # This variable will be used to detect if libraries from the remote user environment are changed by
        # install_lib, remove_lib or update_lib functions in teradataml.
        # Updates from only current session are recorded by this variable.
        self.__libs_changed = None

        # This variable will be set to False when remove() method is called to indicate that.
        self.__exists = True

        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["env_name", self.env_name, False, (str), True])
        self.__arg_info_matrix.append(["base_env", self.base_env, False, (str), True])
        self.__arg_info_matrix.append(["desc", self.desc, True, (str), False])

        # Argument validation.
        _Validators._validate_function_arguments(self.__arg_info_matrix)

        # Map to store the claim id and corresponding file.
        self.__claim_ids = {}

    def install_file(self, file_path, replace=False):
        """
        DESCRIPTION:
            Function installs or replaces a file from client machine to the remote user environment created in
            Vantage Languages Ecosystem.
            * If the size of the file is more than 10 MB, the function installs the
              file asynchronusly and returns claim-id to check the installation status using status().
            * If the size of the file is less than or equal to 10 MB, the function installs the
              file synchronusly and returns the status of installation.

        PARAMETERS:
            file_path:
                Required Argument.
                Specifies absolute or relative path of the file (including file name) to be installed in the
                remote user environment.
                Types: str

            replace:
                Optional Argument.
                Specifies if the file should be forcefully replaced in remote user environment.
                * When set to True,
                   * If the file already exists in remote user environment, it will be replaced with the file
                     specified by argument "file_path".
                   * If the file does not already exist in remote user environment, then the specified file will
                     be installed.
                * Argument is ignored when file is uploaded asynchronously.
                Default Value: False
                Types: bool

        RETURNS:
            True, if the file size is less than or equal to 10 MB and operation is successful.
            str(claim-id), if the file size is greater than 10 MB.

        RAISES:
            TeradataMlException.

        EXAMPLES:
            # Create remote user environment.
            >>> env = create_env('testenv', 'python_3.7.9', 'Test environment')
            User environment testenv created.

            # Example 1: Install the file mapper.py in the 'testenv' environment.
            >>> import os, teradataml
            >>> file_path = os.path.join(os.path.dirname(teradataml.__file__), "data", "scripts", "mapper.py")
            >>> env.install_file(file_path = file_path)
            File 'mapper.py' installed successfully in the remote user environment 'testenv'.

            # Example 2: Replace the file mapper.py.
            >>> file_path = os.path.join(os.path.dirname(teradataml.__file__), "data", "scripts", "mapper.py")
            >>> env.install_file(file_path = file_path, replace=True)
            File 'mapper.py' replaced successfully in the remote user environment 'testenv'.

            # Example 3: Install the file 'large_file' asynchronusly with 'large_file' found in
                         temp folder and check the status of installation.
            # Note:
            #     Running this example creates a file 'large_file' with size
            #     approximately 11MB in the temp folder.
            >>> import tempfile, os
            >>> def create_large_file():
            ...     file_name = os.path.join(tempfile.gettempdir(),"large_file")
            ...     with open(file_name, 'xb') as fp:
            ...         fp.seek((1024 * 1024 * 11) - 1)
            ...         fp.write(b'\0')
            ...
            >>> create_large_file()
            >>> claim_id = env.install_file(file_path = os.path.join(tempfile.gettempdir(),"large_file"))
            File installation is initiated. Check the status using status() with the claim id 76588d13-6e20-4892-9686-37768adcfadb.
            >>> env.status(claim_id)
                                            Claim Id              File/Libs    Method Name               Stage             Timestamp Additional Details
            0   76588d13-6e20-4892-9686-37768adcfadb             large_file   install_file       File Uploaded  2022-07-13T10:34:02Z               None
            >>> env.status(claim_id, stack=True)
                                            Claim Id              File/Libs    Method Name               Stage             Timestamp Additional Details
            0   76588d13-6e20-4892-9686-37768adcfadb             large_file   install_file  Endpoint Generated  2022-07-13T10:34:00Z               None
            1   76588d13-6e20-4892-9686-37768adcfadb             large_file   install_file       File Uploaded  2022-07-13T10:34:02Z               None
            2   76588d13-6e20-4892-9686-37768adcfadb             large_file   install_file      File Installed  2022-07-13T10:34:08Z               None

            >>> os.remove(os.path.join(tempfile.gettempdir(),"large_file")) # Remove the file created using function 'create_large_file'.

            # Remove the environment.
            >>> remove_env('testenv')
            User environment 'testenv' removed.
        """
        # Install/Replace file on Vantage
        __arg_info_matrix = []
        __arg_info_matrix.append(["file_path", file_path, False, (str), True])
        __arg_info_matrix.append(["replace", replace, True, (bool)])

        # Argument validation.
        _Validators._validate_function_arguments(__arg_info_matrix)

        # Check if file exists or not.
        _Validators._validate_file_exists(file_path)

        try:
            # If file size is more than 10 MB, upload the file to cloud and export it to UES.
            if UtilFuncs._get_file_size(file_path) > configure._ues_max_file_upload_size:
                res = self.__install_file_from_cloud(file_path)
            else:
                res = self.__install_file_from_local(file_path, replace)
            self.__files_changed = True
            return res

        except (TeradataMlException, RuntimeError):
            raise

        except Exception as emsg:
            # TODO: Exception message code will be changed with ELE-4998.
            msg_code = MessageCodes.FUNC_EXECUTION_FAILED
            error_msg = Messages.get_message(msg_code, "install_file", str(emsg))
            raise TeradataMlException(error_msg, msg_code)

    def __install_file_from_local(self, file_path, replace):
        """
        DESCRIPTION:
            Internal function to install or replace a file from client machine to the remote
            user environment created in Vantage Languages Ecosystem.

        PARAMETERS:
            file_path:
                Required Argument.
                Specifies absolute or relative path of the file (including file name) to be installed in the
                remote user environment.
                Types: str

            replace:
                Required Argument.
                Specifies if the file should be forcefully replaced in remote user environment.
                When set to True,
                    * If the file already exists in remote user environment, it will be replaced with the file
                      specified by argument "file_path".
                    * If the file does not already exist in remote user environment, then the specified file will
                      be installed.
                Types: bool

        RETURNS:
            True, if the operation is successful.

        RAISES:
            TeradataMlException.

        EXAMPLES:
            # Create remote user environment.
            >>> env = create_env('testenv', 'python_3.7.9', 'Test environment')
            User environment testenv created.
            >>> env.__install_file_from_local("abc.py")
            File 'abc.py' is installed successfully in 'testenv' environment.
        """
        file_name = os.path.basename(file_path)

        # Prepare the payload.
        files = {
            'env-file': (file_name, UtilFuncs._get_file_contents(file_path, read_in_binary_mode=True)),
            'env-name': (None, self.env_name),
            'env-user': (None, _get_user()),
        }

        http_req = requests.post
        success_msg = "installed"
        success_status_code = 201
        if replace:
            http_req = requests.put
            success_msg = "replaced"
            success_status_code = 200

        # UES accepts multiform data. Specifying the 'files' attribute makes 'requests'
        # module to send it as multiform data.
        resp = http_req(_get_ues_url(env_name=self.env_name, files=True, api_name="install_file"),
                        headers=_get_auth_token(),
                        files=files
                        )

        # Process the response.
        _process_ues_response(api_name="install_file", response=resp, success_status_code=success_status_code)

        print("File '{}' {} successfully in the remote user environment '{}'.".format(
            file_name, success_msg, self.env_name))

        return True

    @staticmethod
    def __upload_file_to_cloud(file_path):
        """
        DESCRIPTION:
            Internal function to upload a file to the cloud environment.

        PARAMETERS:
            file_path:
                Required Argument.
                Specifies absolute or relative path of the file (including file name) to be uploaded
                to the cloud.
                Types: str

        RETURNS:
            str, if the operation is successful.

        RAISES:
            TeradataMlException.

        EXAMPLES:
            # Create remote user environment.
            >>> env = create_env('testenv', 'python_3.7.9', 'Test environment')
            User environment testenv created.
            >>> env.__upload_file_to_cloud("abc.txt")
        """
        # Prepare the payload for UES to get the URL and claim-id.
        payload = {"user": _get_user(), "file": os.path.basename(file_path)}

        response = requests.post(_get_ues_url(env_type="fm", fm_type="import", api_name="install_file"),
                                 json=payload,
                                 headers=_get_auth_token()
                                 )
        data = _process_ues_response("install_file", response)

        # Get the URL to upload file to cloud and the claim-id from response.
        cloud_storage_url, claim_id = data["url"], data["claim_id"]

        # Initiate file upload to cloud.
        response = requests.put(cloud_storage_url,
                                data=UtilFuncs._get_file_contents(file_path, read_in_binary_mode=True)
                                )

        # Since the API is not for UES, it is better to validate and raise error separately.
        if response.status_code != 200:
            raise Exception("File upload failed with status code - {}".format(response.status_code))

        return claim_id

    def __install_file_from_cloud(self, file_path):
        """
        DESCRIPTION:
            Internal Function to export file from cloud environment to the remote user
            environment created in Vantage Languages Ecosystem.

        PARAMETERS:
            file_path:
                Required Argument.
                Specifies absolute or relative path of the file (including file name) to
                be installed in the remote user environment.
                Types: str

        RETURNS:
            str, if the operation is successful.

        RAISES:
            TeradataMlException.

        EXAMPLES:
            # Create remote user environment.
            >>> env = create_env('testenv', 'python_3.7.9', 'Test environment')
            User environment testenv created.
            >>> env.__install_file_from_cloud("abc.py")
            File installation is initiated. Check the status using 'status' API with the claim id abc-xyz.
            abc-xyz
        """
        # Upload file to cloud.
        claim_id = self.__upload_file_to_cloud(file_path)

        # Initiate file export from cloud to UES file system. Note that, the corresponding call to
        # UES is an asynchronous call.
        data = {"user": _get_user(),
                "environment": self.env_name,
                "claim_id": claim_id
                }
        response = requests.put(_get_ues_url(env_type="fm",
                                             fm_type="export",
                                             claim_id=claim_id,
                                             api_name="install_file"),
                                json=data)

        # Validate the response.
        _process_ues_response("install_file", response)

        # Print a message to user console.
        print("File installation is initiated. Check the status"
              " using status() with the claim id {}.".format(claim_id))

        # Store the claim id locally to display the file/library name in status API.
        self.__claim_ids[claim_id] = {"action": "install_file", "value": file_path}

        return claim_id

    def remove_file(self, file_name):
        """
        DESCRIPTION:
            Function removes the specified file from the remote user environment.

        PARAMETERS:
            file_name:
                Required Argument.
                Specifies the file name to be removed. If the file has an extension, specify the filename with extension.
                Types: str

        RETURNS:
            True, if the operation is successful.

        RAISES:
            TeradataMlException, RuntimeError

        EXAMPLES:
            # Create a Python 3.7.3 environment with given name and description in Vantage.
            >>> env = create_env('testenv', 'python_3.7.9', 'Test environment')
            User environment 'testenv' created.
            # Install the file "mapper.py" using the default text mode in the remote user environment.
            >>> import os, teradataml
            >>> file_path = os.path.join(os.path.dirname(teradataml.__file__), "data", "scripts", "mapper.py")
            >>> env.install_file(file_path = file_path)
                File 'mapper.py' replaced successfully in the remote user environment 'testenv'.

            # Example 1: Remove file from remote user environment.
            >>> env.remove_file('mapper.py')
            File 'mapper.py' removed successfully from the remote user environment 'testenv'.

            # Remove the environment.
            >>> remove_env('testenv')
            User environment 'testenv' removed.
        """
        __arg_info_matrix = []
        __arg_info_matrix.append(["file_name", file_name, False, (str), True])

        # Argument validation.
        _Validators._validate_missing_required_arguments(__arg_info_matrix)
        _Validators._validate_function_arguments(__arg_info_matrix)

        try:
            response = requests.delete(_get_ues_url(env_name=self.env_name, files=True,
                                                    file_name=file_name),
                                       headers=_get_auth_token())
            _process_ues_response(api_name="remove_file", response=response)
            print("File '{0}' removed successfully from the remote user environment '{1}'.".
                  format(file_name, self.env_name))
            # Files are changed, change the flag.
            self.__files_changed = True
            return True

        except (TeradataMlException, RuntimeError):
            raise
        except Exception as err:
            msg_code = MessageCodes.FUNC_EXECUTION_FAILED
            error_msg = Messages.get_message(msg_code, "remove_file", err)
            raise TeradataMlException(error_msg, msg_code)


    @property
    def files(self):
        """
        DESCRIPTION:
            A class property that returns list of files installed in remote user environment.

        PARAMETERS:
            None

        RETURNS:
            Files present in remote user environment.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create a remote user environment.
            >>> env = create_env('testenv', 'python_3.7.9', 'Test environment')
            User environment testenv created.

            >>> env.install_file(file_path = 'data/scripts/mapper.py')
            File mapper.py installed successfully in the remote user environment testenv.

            # List files installed in the user environment.
            >>> env.files
                    file	size	last_updated_dttm
            0	mapper.py	233	    2020-08-06T21:59:22Z
        """
        # Fetch the list of files from remote user environment only when they are not already fetched in this object
        # or files are changed either by install or remove functions.
        if self.__files is None or self.__files_changed:
            self._set_files()

        if len(self.__files) == 0:
            print("No files found in remote user environment {}.".format(self.env_name))
        else:
            return self.__files

    def _set_files(self):
        """
        DESCRIPTION:
            Function fetches the list of files installed in a remote user environment using
            the REST call to User Environment Service.

        PARAMETERS:
            None

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> self._set_files()
        """

        try:
            response = requests.get(_get_ues_url(env_name=self.env_name, files=True, api_name="files"),
                                    headers=_get_auth_token())
            response = _process_ues_response(api_name="files", response=response)

            data = response.get("data", [])

            if len(data) > 0:
                self.__files = pd.DataFrame.from_records(data)
            else:
                self.__files = pd.DataFrame(columns=["file", "size", "last_updated_dttm"])

            # Latest files are fetched; reset the flag.
            self.__files_changed = False

        except (TeradataMlException, RuntimeError):
            raise

        except Exception as err:
            msg_code = MessageCodes.FUNC_EXECUTION_FAILED
            error_msg = Messages.get_message(msg_code, "files", err)
            raise TeradataMlException(error_msg, msg_code)


    def _set_libs(self):
        """
        DESCRIPTION:
            Function lists the installed libraries in the remote user environment using
            the REST call to User Environment Service and sets the '__libs' data member.

        PARAMETERS:
            None

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            self._set_libs()
        """
        try:
            response = requests.get(_get_ues_url(env_name=self.env_name, libs=True, api_name="libs"),
                                    headers=_get_auth_token())
            ues_response = _process_ues_response(api_name="libs", response=response)
            data = ues_response.get("data", [])

            if len(data) > 0:
                # Return result as Pandas dataframe.
                df = pd.DataFrame.from_records(data["python"])
                self.__libs = df

            # Latest libraries are fetched; reset the flag.
            self.__libs_changed = False

        except (TeradataMlException, RuntimeError):
            raise
        except Exception as emsg:
            msg_code = MessageCodes.FUNC_EXECUTION_FAILED
            error_msg = Messages.get_message(msg_code, "libs", emsg)
            raise TeradataMlException(error_msg, msg_code)

    @property
    def libs(self):
        """
        DESCRIPTION:
            A class property that returns list of libraries installed in the remote user environment.

        PARAMETERS:
            None

        RETURNS:
            Pandas DataFrame containing libraries and their versions.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create a remote user environment.
            >>> env = create_env('test_env', 'python_3.7.9', 'Test environment')
            User environment test_env created.

            # View existing libraries installed.
            >>> env.libs
                base_language	library	    version
            0	python	        pip	        20.1.1
            1	python	        setuptools	47.1.0

            # Install additional Python libraries.
            >>> env.install_lib('numpy','nltk>=3.3,<3.5')
            Libraries installed successfully in the remote user environment test_env.

            # List libraries installed.
            >>> env.libs
            base_language  library	    version
            0	python	        nltk	    3.4.5
            1	python	        numpy	    1.19.4
            2	python	        pip	        20.1.1
            3	python	        setuptools	47.1.0
            4	python	        six	        1.15.0
        """
        # Fetch the list of libraries from remote user environment only when they are not
        # already fetched in this object or libraries are changed either by
        # install_lib/uninstall_lib/update_lib functions.
        if self.__libs is None or self.__libs_changed:
            self._set_libs()

        return self.__libs

    def __manage(self, file_contents, option="INSTALL"):
        """
        DESCRIPTION:
            Function installs, removes and updates Python libraries from
            remote user environment.

        PARAMETERS:
            file_contents:
                Required Argument.
                Specifies the contents of the file in binary format.
                Types: binary

            option:
                Required Argument.
                Specifies the action intended to be performed on the libraries.
                Permitted Values: INSTALL, UNINSTALL, UPDATE
                Types: str
                Default Value: INSTALL

        RETURNS:
            True, if the operation is successful.

        RAISES:
            TeradataMlException, SqlOperationalError

        EXAMPLES:
            self.__manage(b'pandas' ,"INSTALL")
            self.__manage(b'pandas', "UNINSTALL")
            self.__manage(b'pandas', "UPDATE")
        """
        # Common code to call XSP manage_libraries with options "INSTALL", "UNINSTALL", "update"
        # This internal method will be called by install_lib, uninstall_lib and update_lib.
        __arg_info_matrix = []
        __arg_info_matrix.append(["option", option, False, (str), True, ["INSTALL", "UNINSTALL", "UPDATE"]])

        # Validate arguments
        _Validators._validate_missing_required_arguments(__arg_info_matrix)
        _Validators._validate_function_arguments(__arg_info_matrix)

        try:
            # Prepare the payload.
            # Update the action to 'UPGRADE' for the post call as the UES accepts 'UPGRADE'.
            action = "UPGRADE" if option == "UPDATE" else option

            files = {
                'env-file': ("requirements.txt", file_contents),
                'env-name': (None, self.env_name),
                'env-user': (None, _get_user()),
                'action' : (None, action)
            }

            # Get the API name (install_lib or uninstall_lib or update_lib) which calls 
            # __manage_libraries which ends up calling this function.
            api_name = inspect.stack()[2].function

            # UES accepts multiform data. Specifying the 'files' attribute makes 'requests'
            # module to send it as multiform data.
            resp = requests.post(_get_ues_url(env_name=self.env_name, libs=True, api_name=api_name),
                                 headers=_get_auth_token(), files=files)

            # Process the response.
            resp = _process_ues_response(api_name="{}_lib".format(option.lower()), response=resp)
            # Set the flag to indicate that libraries are changed in remote user environment.
            self.__libs_changed = True
            return(resp.get("claim_id", ""))

        except (TeradataMlException, RuntimeError):
            raise
        except Exception as emsg:
            msg_code = MessageCodes.FUNC_EXECUTION_FAILED
            error_msg = Messages.get_message(msg_code, "{}_lib".format(option.lower()), str(emsg))
            raise TeradataMlException(error_msg, msg_code)

    def __validate(self, libs=None, libs_file_path=None):
        """
        DESCRIPTION:
            Function performs argument validations.

        PARAMETERS:
            libs:
                Optional Argument.
                Specifies the add-on library name(s).
                Types: str OR list of Strings(str)

            libs_file_path:
                Optional Argument.
                Specifies file path with extension.
                Types: str

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            __validate_requirement_filename(libs_file_path = 'data/requirements.txt')
            __validate_requirement_filename(libs="numpy")
            __validate_requirement_filename(libs=['pandas','numpy'])
        """
        __arg_info_matrix = []
        __arg_info_matrix.append(["libs", libs, True, (str, list), True])
        __arg_info_matrix.append(["libs_file_path", libs_file_path, True, str, True])

        # Argument validation.
        _Validators._validate_missing_required_arguments(__arg_info_matrix)
        _Validators._validate_function_arguments(__arg_info_matrix)
        _Validators._validate_mutually_exclusive_arguments(libs, "libs", libs_file_path, "libs_file_path")

        if libs_file_path is not None:
            # If user has specified libraries in a file.
            _Validators._validate_file_exists(libs_file_path)

            # Verify only files with .txt extension are allowed.
            _Validators._validate_file_extension(libs_file_path, ".txt")
            _Validators._check_empty_file(libs_file_path)

    def __manage_libraries(self, libs=None, libs_file_path=None, action="INSTALL"):
        """
        DESCRIPTION:
            Internal function to perform argument validation, requirement text file
            generation and executing XSP call to get the results.

        PARAMETERS:
            libs:
                Optional Argument.
                Specifies the add-on library name(s).
                Types: str OR list of Strings(str)

            libs_file_path:
                Optional Argument.
                Specifies the absolute/relative path of the text file (including file name)
                which supplies a list of libraries to be installed in remote user
                environment. Path specified should include the filename with extension.
                Note:
                    1. The file must have an ".txt" extension.
                    2. Either libs or libs_file_path argument must be specified.
                Types: str

            action:
                Optional Argument.
                Specifies if libraries are to be installed or uninstalled or updated
                from remote user environment.
                Default Value: 'INSTALL'
                Types: str

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            __manage_libraries(libs_file_path="/data/requirement.txt", action="INSTALL")
            __manage_libraries(libs="pandas", action="UNINSTALL")
            __manage_libraries(libs=["pandas","numpy","joblib==0.13.2"], action="UPDATE")
        """
        # Argument validation.
        self.__validate(libs, libs_file_path)

        # If file is provided, store the file_name and also extracts it contents
        if libs_file_path is not None:
            value = libs_file_path
            file_contents = UtilFuncs._get_file_contents(libs_file_path, read_in_binary_mode=True)
        else:
            # If libs are provided as string or list, convert the contents to binary.
            file_contents = libs
            # When library names are provided in a list, create a string.
            if isinstance(libs, list):
                file_contents = '\n'.join(libs)
            # Store it with comma separated values if it is a list.
            value = ', '.join(libs) if isinstance(libs, list) else libs
            # Convert to binary.
            file_contents = file_contents.encode('ascii')

        try:
            claim_id = self.__manage(file_contents, action)
            print("Request to {} libraries initiated successfully in the remote user environment {}. "
                  "Check the status using status() with the claim id '{}'.".format(
                  action.lower(), self.env_name, claim_id))
            # Populate the details for status API.
            self.__claim_ids[claim_id] = {"action": "{}_lib".format(action.lower()), "value": value}
            return (claim_id)
        except:
            raise

    def install_lib(self, libs=None, libs_file_path=None):
        """
        DESCRIPTION:
            Function installs Python libraries in the remote user environment.

        PARAMETERS:
            libs:
                Optional Argument.
                Specifies the add-on library name(s).
                Types: str OR list of Strings(str)

            libs_file_path:
                Optional Argument.
                Specifies the absolute/relative path of the text file (including file name)
                which supplies a list of libraries to be installed in remote user environment.
                Path specified should include the filename with extension.
                The file should contain library names and version number(optional) of libraries.
                The file should contain library names and version number(optional) of libraries.
                Note:
                    This file format should adhere to the specification of the requirements file
                    used to install Python libraries with pip install command.
                Sample text file contents:
                    numpy
                    joblib==0.13.2
                Note:
                    1. The file must have an ".txt" extension.
                    2. Either libs or libs_file_path argument must be specified.
                Types: str

        RETURNS:
            claim_id, to track status.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create remote user environment.
            >>> env = create_env('testenv', 'python_3.7.9', 'Test environment')
            User environment testenv created.

            # Example 1: Install single Python library.
            >>> env.install_lib('numpy')
            Request to install libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id '4b062b0e-6e9f-4996-b92b-5b20ac23b0f9'.

            # Check the status.
            >>> env.status('4b062b0e-6e9f-4996-b92b-5b20ac23b0f9')
                                           Claim Id File/Libs  Method Name     Stage             Timestamp Additional Details
            0  4b062b0e-6e9f-4996-b92b-5b20ac23b0f9     numpy  install_lib  Finished  2022-07-13T11:09:40Z               None
            >>>

            # Verify if libraries are installed.
            >>> env.libs
                  library version
            0       numpy  1.21.6
            1         pip  20.1.1
            2  setuptools  47.1.0

            # Example 2: Install libraries by passing them as list of library names.
            >>> env.install_lib(["pandas",
            ...                   "joblib==0.13.2",
            ...                   "scikit-learn",
            ...                   "numpy>=1.17.1",
            ...                   "nltk>=3.3,<3.5"])
            Request to install libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id '90aae7df-5efe-4b5a-af26-150aab35f1fb'.

            # Check the status.
            >>> env.status('90aae7df-5efe-4b5a-af26-150aab35f1fb')
                                           Claim Id                                                           File/Libs  Method Name     Stage             Timestamp Additional Details
            0  90aae7df-5efe-4b5a-af26-150aab35f1fb pandas, joblib==0.13.2, scikit-learn, numpy>=1.17.1, nltk>=3.3,<3.5  install_lib  Finished  2022-07-13T11:09:40Z               None

            # Verify if libraries are installed with specific version.
            >>> env.libs
                        library version
            0            joblib  0.13.2
            1              nltk   3.4.5
            2             numpy  1.21.6
            3            pandas   1.3.5
            4               pip  20.1.1
            5   python-dateutil   2.8.2
            6              pytz  2022.1
            7      scikit-learn   1.0.2
            8             scipy   1.7.3
            9        setuptools  47.1.0
            10              six  1.16.0
            11    threadpoolctl   3.1.0


            # Example 3: Install libraries by creating requirement.txt file.
            # Create a requirement.txt file with below contents.
            -----------------------------------------------------------
            pandas
            joblib==0.13.2
            scikit-learn
            numpy>=1.17.1
            nltk>=3.3,<3.5
            -----------------------------------------------------------

            # Install libraries specified in the file.
            >>> env.install_lib(libs_file_path="requirement.txt")
            Request to install libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id 'f11c7f28-f958-4cae-80a8-926733954bdc'.

            # Check the status.
            >>> env.status('8709b464-f144-4c37-8918-ef6a98ecf295', stack=True)
                                           Claim Id         File/Libs  Method Name     Stage             Timestamp Additional Details
            0  f11c7f28-f958-4cae-80a8-926733954bdc  requirements.txt  install_lib   Started  2022-07-13T11:23:23Z               None
            1  f11c7f28-f958-4cae-80a8-926733954bdc  requirements.txt  install_lib  Finished  2022-07-13T11:25:37Z               None
            >>>

            # Verify if libraries are installed with specific version.
            >>> env.libs
                        library version
            0            joblib  0.13.2
            1              nltk   3.4.5
            2             numpy  1.21.6
            3            pandas   1.3.5
            4               pip  20.1.1
            5   python-dateutil   2.8.2
            6              pytz  2022.1
            7      scikit-learn   1.0.2
            8             scipy   1.7.3
            9        setuptools  47.1.0
            10              six  1.16.0
            11    threadpoolctl   3.1.0
        """
        claim_id = self.__manage_libraries(libs, libs_file_path, "INSTALL")
        return (claim_id)

    def uninstall_lib(self, libs=None, libs_file_path=None):
        """
        DESCRIPTION:
            Function uninstalls Python libraries from remote user environment.

        PARAMETERS:
            libs:
                Optional Argument.
                Specifies the add-on library name(s).
                Types: str OR list of Strings(str)

            libs_file_path:
                Optional Argument.
                Specifies the absolute/relative path of the text file (including file name)
                which supplies a list of libraries to be uninstalled from the remote user
                environment. Path specified should include the filename with extension.
                The file should contain library names and version number(optional) of libraries.
                Note:
                    This file format should adhere to the specification of the requirements file
                    used to uninstall Python libraries with pip uninstall command.
                Sample text file contents:
                    numpy
                    joblib==0.13.2
                Note:
                    1. The file must have an ".txt" extension.
                    2. Either libs or libs_file_path argument must be specified.
                Types: str

        RETURNS:
            claim_id, to track status.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create remote user environment.
            >>> testenv = create_env('testenv', 'python_3.7.9', 'Test environment')
            User environment testenv created.

            # Example 1: Install and uninstall a single Python library.
            >>> testenv.install_lib('numpy')
            Request to install libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id '407e644d-3630-4085-8a0b-169406f52340'.

            # Check the status.
            >>> testenv.status('407e644d-3630-4085-8a0b-169406f52340')
                                           Claim Id File/Libs  Method Name     Stage             Timestamp Additional Details
            0  407e644d-3630-4085-8a0b-169406f52340     numpy  install_lib  Finished  2022-07-13T11:32:33Z               None
            >>>

            # Verify installed library.
            >>> testenv.libs
                  library version
            0       numpy  1.21.6
            1         pip  20.1.1
            2  setuptools  47.1.0

            # Uninstall single Python library.
            >>> testenv.uninstall_lib('numpy')
            Request to uninstall libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id '16036846-b9d7-4c5b-be92-d7cf14aa2016'.

            # Check the status.
            >>> testenv.status('16036846-b9d7-4c5b-be92-d7cf14aa2016')
                                           Claim Id File/Libs    Method Name     Stage             Timestamp Additional Details
            0  16036846-b9d7-4c5b-be92-d7cf14aa2016     numpy  uninstall_lib  Finished  2022-07-13T11:33:42Z               None
            >>>

            # Verify library is uninstalled.
            >>> testenv.libs
                library	    version
            0	pip	        20.1.1
            1	setuptools	47.1.0

            # Example 2: Install and uninstall list of Python libraries.
            >>> testenv.install_lib(["pandas", "scikit-learn"])
            Request to install libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id 'a91af321-cf57-43cc-b864-a67fa374cb42'.

            # Check the status
            >>> testenv.status('a91af321-cf57-43cc-b864-a67fa374cb42', stack=True)
                                           Claim Id             File/Libs  Method Name     Stage             Timestamp Additional Details
            0  a91af321-cf57-43cc-b864-a67fa374cb42  pandas, scikit-learn  install_lib   Started  2022-07-13T11:34:38Z               None
            1  a91af321-cf57-43cc-b864-a67fa374cb42  pandas, scikit-learn  install_lib  Finished  2022-07-13T11:36:40Z               None
            >>>

            # Verify libraries are installed along with its dependant libraries.
            >>> testenv.libs
                        library version
            0            joblib   1.1.0
            1             numpy  1.21.6
            2            pandas   1.3.5
            3               pip  20.1.1
            4   python-dateutil   2.8.2
            5              pytz  2022.1
            6      scikit-learn   1.0.2
            7             scipy   1.7.3
            8        setuptools  47.1.0
            9               six  1.16.0
            10    threadpoolctl   3.1.0

            # Uninstall libraries by passing them as a list of library names.
            >>> testenv.uninstall_lib(["pandas", "scikit-learn"])
            Request to uninstall libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id '8d6bb524-c047-4aae-8597-b48ab467ef37'.

            # Check the status.
            >>> testenv.status('8d6bb524-c047-4aae-8597-b48ab467ef37', stack=True)
                                           Claim Id             File/Libs    Method Name     Stage             Timestamp Additional Details
            0  8d6bb524-c047-4aae-8597-b48ab467ef37  pandas, scikit-learn  uninstall_lib   Started  2022-07-13T11:46:55Z               None
            1  8d6bb524-c047-4aae-8597-b48ab467ef37  pandas, scikit-learn  uninstall_lib  Finished  2022-07-13T11:47:20Z               None
            >>>

            # Verify if the specified libraries are uninstalled.
             >>> testenv.libs
                       library version
            0           joblib   1.1.0
            1            numpy  1.21.6
            2              pip  20.1.1
            3  python-dateutil   2.8.2
            4             pytz  2022.1
            5            scipy   1.7.3
            6       setuptools  47.1.0
            7              six  1.16.0
            8    threadpoolctl   3.1.0

            # Example 3: Install and uninstall libraries specified in
            #            requirement text file.

            # Install libraries by creating requirement.txt file.
            # Create a requirement.txt file with below contents.
            -----------------------------------------------------------
            pandas
            joblib==0.13.2
            scikit-learn
            numpy>=1.17.1
            nltk>=3.3,<3.5
            -----------------------------------------------------------

            # Install libraries specified in the file.
            >>> testenv.install_lib(libs_file_path="requirements.txt")
            Request to install libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id 'c3669eea-327c-453f-b068-6b5f3f4768a5'.

            # Check the status.
            >>> testenv.status('c3669eea-327c-453f-b068-6b5f3f4768a5', stack=True)
                                           Claim Id         File/Libs  Method Name     Stage             Timestamp Additional Details
            0  c3669eea-327c-453f-b068-6b5f3f4768a5  requirements.txt  install_lib   Started  2022-07-13T11:48:46Z               None
            1  c3669eea-327c-453f-b068-6b5f3f4768a5  requirements.txt  install_lib  Finished  2022-07-13T11:50:09Z               None
            >>>

            # Verify libraries are installed along with its dependant libraries.
                        library version
            0            joblib   1.1.0
            1             numpy  1.21.6
            2            pandas   1.3.5
            3               pip  20.1.1
            4   python-dateutil   2.8.2
            5              pytz  2022.1
            6      scikit-learn   1.0.2
            7             scipy   1.7.3
            8        setuptools  47.1.0
            9               six  1.16.0
            10    threadpoolctl   3.1.0

            # Uninstall libraries specified in the file.
            >>> testenv.uninstall_lib(libs_file_path="requirements.txt")
            Request to uninstall libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id '95ebfc7b-2910-4aab-be80-3e47f84737bd'.

            # Check the status.
            >>> testenv.status('95ebfc7b-2910-4aab-be80-3e47f84737bd', stack=True)
                                           Claim Id         File/Libs    Method Name     Stage             Timestamp Additional Details
            0  95ebfc7b-2910-4aab-be80-3e47f84737bd  requirements.txt  uninstall_lib   Started  2022-07-13T11:52:03Z               None
            1  95ebfc7b-2910-4aab-be80-3e47f84737bd  requirements.txt  uninstall_lib  Finished  2022-07-13T11:52:39Z               None
            >>>

            # Verify if the specified libraries are uninstalled.
             >>> testenv.libs
                       library version
            0           joblib   1.1.0
            1            numpy  1.21.6
            2              pip  20.1.1
            3  python-dateutil   2.8.2
            4             pytz  2022.1
            5            scipy   1.7.3
            6       setuptools  47.1.0
            7              six  1.16.0
            8    threadpoolctl   3.1.0
        """
        claim_id = self.__manage_libraries(libs, libs_file_path, "UNINSTALL")
        return(claim_id)

    def update_lib(self, libs=None, libs_file_path=None):
        """
        DESCRIPTION:
            Function updates Python libraries if already installed,
            otherwise installs the libraries in remote user environment.

        PARAMETERS:
            libs:
                Optional Argument.
                Specifies the add-on library name(s).
                Types: str OR list of Strings(str)

            libs_file_path:
                Optional Argument.
                Specifies the absolute/relative path of the text file (including file name)
                which supplies a list of libraries to be updated from the remote user
                environment. Path specified should include the filename with extension.
                The file should contain library names and version number(optional) of libraries.
                Note:
                    This file format should adhere to the specification of the requirements file
                    used to update Python libraries with pip command.
                Sample text file contents:
                    numpy
                    joblib==0.13.2
                Note:
                    1. The file must have an ".txt" extension.
                    2. Either libs or libs_file_path argument must be specified.
                Types: str

        RETURNS:
            claim_id, to track status.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create remote user environment.
            >>> testenv = create_env('testenv', 'python_3.7.9', 'Test environment')
            User environment testenv created.

            # Example 1: Update a single Python library.
            # Install a Python library.
            >>> testenv.install_lib(["joblib==0.13.2"])
            Request to install libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id 'f44443a9-42c3-4fd3-b4a2-735d1bfb7c27'.

            # Check the status.
            >>> testenv.status('f44443a9-42c3-4fd3-b4a2-735d1bfb7c27')
                                           Claim Id       File/Libs  Method Name     Stage             Timestamp Additional Details
            0  f44443a9-42c3-4fd3-b4a2-735d1bfb7c27  joblib==0.13.2  install_lib  Finished  2022-07-13T11:54:31Z               None
            >>>

            # Verify joblib library is installed with specified version.
            >>> testenv.libs
                  library version
            0      joblib  0.13.2
            1         pip  20.1.1
            2  setuptools  47.1.0

            # Update joblib libary to the new version specified.
            >>> testenv.update_lib("joblib==0.14.1")
            Request to update libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id '8bfe55fc-efaa-44c7-9137-af24b6bb9ef8'.

            # Check the status.
            >>> testenv.status('8bfe55fc-efaa-44c7-9137-af24b6bb9ef8')
                                           Claim Id       File/Libs Method Name     Stage             Timestamp Additional Details
            0  8bfe55fc-efaa-44c7-9137-af24b6bb9ef8  joblib==0.14.1  update_lib  Finished  2022-07-13T11:55:29Z               None
            >>>

            # Verify joblib library version is updated with specified version.
            >>> testenv.libs
                  library version
            0      joblib  0.14.1
            1         pip  20.1.1
            2  setuptools  47.1.0

            # Example 2: Update multiple Python libraries.
            >>> testenv.update_lib(["joblib==0.14.1","numpy==1.19.5"])
            Request to update libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id '28e0e03e-469b-440c-a939-a0e8a901078f'.

            # Check the status.
            >>> testenv.status('28e0e03e-469b-440c-a939-a0e8a901078f')
                                           Claim Id                      File/Libs Method Name     Stage             Timestamp Additional Details
            0  28e0e03e-469b-440c-a939-a0e8a901078f  joblib==0.14.1, numpy==1.19.5  update_lib  Finished  2022-07-13T11:56:34Z               None
            >>>

            # Verify if numpy is installed with the specific version.
            >>> testenv.libs
                  library version
            0      joblib  0.14.1
            1       numpy  1.19.5
            2         pip  20.1.1
            3  setuptools  47.1.0

            # Example 3: update libraries specified in the requirements text file.
            # Create a requirement.txt file with below contents.
            -----------------------------------------------------------
            numpy==1.21.6
            -----------------------------------------------------------
            >>> testenv.update_lib(libs_file_path="requirement.txt")
            Request to update libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id 'd3301da5-f5cb-4248-95dc-a59e77fe9db5'.

            # Verify if numpy is updated to the specific version.
            >>> testenv.libs
                  library version
            0      joblib  0.14.1
            1       numpy  1.21.6
            2         pip  20.1.1
            3  setuptools  47.1.0

            # Example 4: Downgrade Python libraries. Downgrade the Python library joblib to 0.13.2.
            >>> testenv.update_lib(["joblib==0.13.2"])
            Request to update libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id 'ca669e5b-bd2c-4037-ae65-e0147954b85d'.

            # Check the status.
            >>> testenv.status('ca669e5b-bd2c-4037-ae65-e0147954b85d', stack=True)
                                           Claim Id       File/Libs Method Name     Stage             Timestamp Additional Details
            0  ca669e5b-bd2c-4037-ae65-e0147954b85d  joblib==0.13.2  update_lib   Started  2022-07-13T11:57:41Z               None
            1  ca669e5b-bd2c-4037-ae65-e0147954b85d  joblib==0.13.2  update_lib  Finished  2022-07-13T11:57:47Z               None
            >>>

            # Listing the available libraries.
            >>> testenv.libs
                  library version
            0      joblib  0.14.1
            1         pip  20.1.1
            2  setuptools  47.1.0

            # As higher version of the package is not automatically uninstalled, we need to uninstall the higher version
            # to use the lower version.
            >>> testenv.uninstall_lib("joblib")
            Request to uninstall libraries initiated successfully in the remote user environment testenv.
            Check the status using status() with the claim id 'e32d69d9-452b-4600-be4b-1d5c60647a54'.

            >>> testenv.status('e32d69d9-452b-4600-be4b-1d5c60647a54', stack=True)
                                           Claim Id File/Libs    Method Name     Stage             Timestamp Additional Details
            0  e32d69d9-452b-4600-be4b-1d5c60647a54    joblib  uninstall_lib   Started  2022-07-13T11:59:14Z               None
            1  e32d69d9-452b-4600-be4b-1d5c60647a54    joblib  uninstall_lib  Finished  2022-07-13T11:59:17Z               None
            >>>

            # Verify if joblib package is downgraded to the required version.
            >>> testenv.libs
                  library version
            0         pip  20.1.1
            1  setuptools  47.1.0
        """
        claim_id = self.__manage_libraries(libs, libs_file_path, "UPDATE")
        return (claim_id)

    def refresh(self):
        """
        DocString -- TODO
        """
        # Function will refresh self._files and self._libs by calling below methods.
        # self._get_libs()
        # self._get_files()
        raise NotImplementedError("To be implemented - VLA-201")

    def remove(self):
        """
        DocString -- TODO
        """
        raise NotImplementedError("To be implemented - VLA-201")

    def status(self, claim_ids=None):
        """
        DESCRIPTION:
            Function to check the status of the operations performed by the library/file
            management methods of UserEnv. Status of the following operations can be checked:
              * File installation, when installed asynchronously. Applicable for the files
                with size greater than 10 MB.
              * Install/Uninstall/Update of the libraries in user environment.

        PARAMETERS:
            claim_ids:
                Optional Argument.
                Specifies the unique identifier(s) of the asynchronous process
                started by the UserEnv management methods.
                If user do not pass claim_ids, then function gets the status
                of all the asynchronus process'es in the current session.
                Types: str OR list of Strings (str)

        RETURNS:
            Pandas DataFrame.

        RAISES:
            None

        EXAMPLES:
            # Create a remote user environment.
            >>> env = create_env('test_env', 'python_3.7.9', 'Test environment')
            User environment test_env created.

            # Example 1: Install the file 'large_file' asynchronusly with 'large_file' found in
                         temp folder and check the latest status of installation.
            # Note:
            #     Running this example creates a file 'large_file' with size
            #     approximately 41MB in the temp folder.
            >>> import tempfile, os
            >>> def create_large_file():
            ...     file_name = os.path.join(tempfile.gettempdir(),"large_file")
            ...     with open(file_name, 'xb') as fp:
            ...         fp.seek((1024 * 1024 * 41) - 1)
            ...         fp.write(b'\0')
            ...
            >>> claim_id = env.install_file('large_file')
                File installation is initiated. Check the status using status() with the claim id 53e44892-1952-45eb-b828-6635c0447b59.
            >>> env.status(claim_id)
                                           Claim Id                                                       File/Libs   Method Name               Stage             Timestamp Additional Details
            0  53e44892-1952-45eb-b828-6635c0447b59  TeradataToolsAndUtilitiesBase__ubuntu_x8664.17.10.19.00.tar.gz  install_file  Endpoint Generated  2022-07-27T18:20:34Z               None
            1  53e44892-1952-45eb-b828-6635c0447b59  TeradataToolsAndUtilitiesBase__ubuntu_x8664.17.10.19.00.tar.gz  install_file       File Uploaded  2022-07-27T18:20:35Z               None
            2  53e44892-1952-45eb-b828-6635c0447b59  TeradataToolsAndUtilitiesBase__ubuntu_x8664.17.10.19.00.tar.gz  install_file      File Installed  2022-07-27T18:20:38Z               None
            >>>

            # Example 2: Install the library 'teradataml' asynchronusly and check the status of installation.
            >>> claim_id = env.install_lib('teradataml')
                Request to install libraries initiated successfully in the remote user environment test_env. Check the status using status() with the claim id '349615e2-9257-4a70-8304-ac76f50712f8'.
            >>> env.status(claim_id)
                                           Claim Id   File/Libs  Method Name     Stage             Timestamp Additional Details
            0  349615e2-9257-4a70-8304-ac76f50712f8  teradataml  install_lib   Started  2022-07-13T10:37:40Z               None
            1  349615e2-9257-4a70-8304-ac76f50712f8  teradataml  install_lib  Finished  2022-07-13T10:39:29Z               None
            >>>

            # Example 3: update the library 'teradataml' to 17.10.0.0 asynchronusly and check the status of installation.
            >>> claim_id = env.update_lib('teradataml==17.10.0.0')
            Request to update libraries initiated successfully in the remote user environment test_env. Check the status using status() with the claim id '29d06296-7444-4851-adef-ca1f921b1dd6'.
            >>> env.status(claim_id)
                                           Claim Id              File/Libs Method Name     Stage             Timestamp Additional Details
            0  29d06296-7444-4851-adef-ca1f921b1dd6  teradataml==17.10.0.0  update_lib   Started  2022-07-13T10:47:39Z               None
            1  29d06296-7444-4851-adef-ca1f921b1dd6  teradataml==17.10.0.0  update_lib  Finished  2022-07-13T10:49:52Z               None
            >>>

            # Example 4: uninstall the library 'teradataml' and check the complete status of all the asynchronous process'es.
            >>> claim_id = env.uninstall_lib('teradataml')
            Request to uninstall libraries initiated successfully in the remote user environment test_env. Check the status using status() with the claim id '5cd3b3f7-f3b8-4bfd-8abe-7c811a6728db'.
            >>> env.status()
                                           Claim Id                                                       File/Libs    Method Name               Stage             Timestamp Additional Details
            0  53e44892-1952-45eb-b828-6635c0447b59  TeradataToolsAndUtilitiesBase__ubuntu_x8664.17.10.19.00.tar.gz   install_file  Endpoint Generated  2022-07-27T18:20:34Z               None
            1  53e44892-1952-45eb-b828-6635c0447b59  TeradataToolsAndUtilitiesBase__ubuntu_x8664.17.10.19.00.tar.gz   install_file       File Uploaded  2022-07-27T18:20:35Z               None
            2  53e44892-1952-45eb-b828-6635c0447b59  TeradataToolsAndUtilitiesBase__ubuntu_x8664.17.10.19.00.tar.gz   install_file      File Installed  2022-07-27T18:20:38Z               None
            3  29d06296-7444-4851-adef-ca1f921b1dd6                                           teradataml==17.10.0.0     update_lib             Started  2022-07-13T10:47:39Z               None
            4  29d06296-7444-4851-adef-ca1f921b1dd6                                           teradataml==17.10.0.0     update_lib            Finished  2022-07-13T10:49:52Z               None
            5  349615e2-9257-4a70-8304-ac76f50712f8                                           teradataml               install_lib             Started  2022-07-13T10:37:40Z               None
            6  349615e2-9257-4a70-8304-ac76f50712f8                                           teradataml               install_lib            Finished  2022-07-13T10:39:29Z               None
            7  5cd3b3f7-f3b8-4bfd-8abe-7c811a6728db                                           teradataml             uninstall_lib             Started  2022-07-13T10:37:40Z               None
            8  5cd3b3f7-f3b8-4bfd-8abe-7c811a6728db                                           teradataml             uninstall_lib            Finished  2022-07-13T10:39:29Z               None

        """
        __arg_info_matrix = []
        __arg_info_matrix.append(["claim_ids", claim_ids, True, (list, str), True])

        # Validate arguments
        _Validators._validate_function_arguments(__arg_info_matrix)

        # If user do not pass any claim_ids, get the status for all the claim-ids
        # created in the current session.
        if claim_ids is None:

            # If there are no claim_ids in the current session, print a message and return.
            if not self.__claim_ids:
                print("No file/library management operations found.")
                return

            # Get all the claim_ids.
            claim_ids = self.__claim_ids.keys()
        else:
            # If user pass a single claim_id as string, convert to list.
            claim_ids = UtilFuncs._as_list(claim_ids)

        # Define the order of columns in output DataFrame.
        columns = ['Claim Id', 'File/Libs', 'Method Name', 'Stage', 'Timestamp', 'Additional Details']
        return pd.DataFrame.from_records(self.__process_claim_ids(claim_ids=claim_ids),
                                         columns=columns)

    def __process_claim_ids(self, claim_ids):
        """
        DESCRIPTION:
            Function processes the claim IDs of asynchronous process using
            their 'claim_ids' parallelly to get the status.

        PARAMETERS:
            claim_ids:
                Required Argument.
                Specifies the unique identifier(s) of the asynchronous process
                started by the UserEnv management methods.
                Types: str OR list of Strings (str)

        RETURNS:
            list

        RAISES:
            None

        EXAMPLES:
            # Create a remote user environment.
            >>> env.__process_claim_ids(['123-456-789', 'abc-xyz'])
        """
        # Create thread pool executor to get the status parallelly.
        executor = ThreadPoolExecutor(max_workers=10)

        # executor.submit returns a future object. Store all the futures in a list.
        futures = [executor.submit(self.__get_claim_id_status, claim_id) for claim_id in claim_ids]

        # Wait forever, till all the futures complete.
        wait(futures)

        # Add all the results to a list.
        return functools.reduce(lambda x, y: x+y, (future.result() for future in futures))

    def __get_claim_id_status(self, claim_id):
        """
        DESCRIPTION:
            Function to get the status of asynchronus process using the claim_id.

        PARAMETERS:
            claim_id:
                Required Argument.
                Specifies the unique identifier of the asynchronous process
                started by the UserEnv management methods.
                Types: str

        RETURNS:
            Pandas DataFrame.

        RAISES:
            None

        EXAMPLES:
            # Create a remote user environment.
            >>> env.__get_claim_id_status('123-456')
        """
        # Get the claim_id details.
        claim_id_details = {"Claim Id": claim_id,
                            "Method Name": self.__claim_ids.get(claim_id, {}).get("action", "Unknown"),
                            "File/Libs": self.__claim_ids.get(claim_id, {}).get("value", "Unknown")}

        try:
            response = requests.get(_get_ues_url(env_type="fm", claim_id=claim_id, api_name="status"), headers=_get_auth_token())
            data = _process_ues_response(api_name="status", response=response)

            # if claim_id is for install_file - 'data' looks as below:
            #      [
            #         {'timestamp': '2022-06-29T17:03:49Z', 'stage': 'Endpoint Generated'},
            #         {'timestamp': '2022-06-29T17:03:50Z', 'stage': 'File Uploaded'},
            #         {'timestamp': '2022-06-29T17:03:52Z', 'stage': 'File Installed'}
            #      ]

            # if claim_id is for install_lib/uninstall_lib/update_lib - 'data' looks as below:
            #     [
            #         {
            #             "timestamp": "2022-07-07T09:43:04Z",
            #             "stage": "Started"
            #         },
            #         {
            #             "timestamp": "2022-07-07T09:43:06Z",
            #             "stage": "Finished",
            #             "details": "WARNING: Skipping numpysts as it is not installed."
            #                        "WARNING: Skipping pytest as it is not installed."
            #         }
            #      ]

            # Create a lamda function to extract the data.
            get_details = lambda data: {"Additional Details": data.pop("details", None),
                                        "Stage": data.pop("stage", None),
                                        "Timestamp": data.pop("timestamp", None),
                                        **claim_id_details}

            return [get_details(sub_step) for sub_step in data]

        except Exception as e:
            # For any errors, construct a row with error reason in 'additional_details' column.
            record = {"Additional Details": str(e), "Timestamp": None, "Stage": "Errored"}
            record.update(claim_id_details)
            return [record]

    def __repr__(self):
        """
        Returns the string representation for class instance.
        """
        repr_string = "Environment Name: {}\n".format(self.env_name)
        repr_string = repr_string + "Base Environment: {}\n".format(self.base_env)
        repr_string = repr_string + "Description: {}\n".format(self.desc)

        if self.__files is not None:
            repr_string_files = "############ Files installed in User Environment ############"
            repr_string = "{}\n\n{}\n\n{}".format(repr_string, repr_string_files, self.__files)

        if self.__libs is not None:
            repr_string_libs = "############ Libraries installed in User Environment ############"
            repr_string = "{}\n\n{}\n\n{}".format(repr_string, repr_string_libs, self.__libs)

        return repr_string
