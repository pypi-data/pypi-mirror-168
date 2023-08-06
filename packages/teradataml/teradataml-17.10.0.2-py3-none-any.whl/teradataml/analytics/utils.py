from teradataml.analytics.json_parser.json_store import _JsonStore
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.messages import Messages
from teradataml.context.context import get_connection

def display_analytic_functions():
    """
    DESCRIPTION:
        Display list of analytic functions available to use on the Teradata Vantage system, user is connected to.

    PARAMETERS:
        None

    RETURNS:
        None

    RAISES:
        TeradataMlException.

    EXAMPLES:
        >>> from teradataml import create_context, display_analytic_functions

        # Example 1: Displaying a list of available analytic functions
        >>> connection_name = create_context(host = host, username=user, password=password)
        >>> display_analytic_functions()
        List of available SQLE analytic functions:
         1: Antiselect
         2: Attribution
         3: DecisionForestPredict
         4: DecisionTreePredict
         5: GLMPredict
         6: MovingAverage
         7: NaiveBayesPredict
         8: NaiveBayesTextClassifierPredict
         9: NGrams
         10: NPath
         ...

         # Example 2: When no analytic functions are available on the cluster.
         >>> display_analytic_functions()
         No analytic functions available with connected Teradata Vantage system.
    """

    if get_connection() is None:
        error_code = MessageCodes.INVALID_CONTEXT_CONNECTION
        error_msg = Messages.get_message(error_code)
        raise TeradataMlException(error_msg, error_code)
    else:
        functions = _JsonStore._get_function_list()
        if len(functions) > 0:
            print("List of available SQLE analytic functions:")
            functions = enumerate(sorted(functions, key=lambda function_name: function_name.lower()), 1)
            for key, value in functions:
                print(" {}: {}".format(key, value))
        else:
            print("No analytic functions available with connected Teradata Vantage system.")