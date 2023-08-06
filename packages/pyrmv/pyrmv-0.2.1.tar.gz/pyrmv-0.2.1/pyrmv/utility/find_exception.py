from pyrmv.errors.api_errors import ApiAuthError, ApiFormatError, ApiParamError, ApiQuotaError, ApiTooManyRequests
from pyrmv.errors.int_errors import IntError, IntGatewayError, IntTimeoutError
from pyrmv.errors.ps_errors import PsIncorrectParamError
from pyrmv.errors.sot_errors import SotAllTrainsFilteredError, SotAlreadyArrivedError, SotCancelledError, SotNotStartedError, SotStayOnTripError
from pyrmv.errors.svc_errors import SvcContextError, SvcDatetimeError, SvcDatetimePeriodError, SvcLocationArrivalError, SvcLocationDepartureError, SvcLocationEqualError, SvcLocationError, SvcLocationNearError, SvcLocationViaError, SvcNoMatchError, SvcNoResultError, SvcProductError, SvcSearchError
from pyrmv.errors.unknown_error import UnknownError

def find_exception(data: dict):
    """Scan returned dict for errorCode from RMV.
    Raises different exceptions if errorCode is not None. 

    ### Args:
        * data (dict): Response from RMV as a dict.

    ### Raises:
        * Any: Formatted as "errorCode -> errorText" if ApiParamError and UnknownError or as a single massage for others.
    """    
    if "errorCode" in data:

        if data["errorCode"] == "API_AUTH":
            raise ApiAuthError()

        elif data["errorCode"] == "API_QUOTA":
            raise ApiQuotaError()

        elif data["errorCode"] == "API_TOO_MANY_REQUESTS":
            raise ApiTooManyRequests()
            
        elif data["errorCode"] == "API_PARAM":
            raise ApiParamError(errorCode=data["errorCode"], errorText=data["errorText"])

        elif data["errorCode"] == "API_FORMAT":
            raise ApiFormatError()

        elif data["errorCode"] == "SVC_LOC":
            raise SvcLocationError()

        elif data["errorCode"] == "SVC_LOC_ARR":
            raise SvcLocationArrivalError()

        elif data["errorCode"] == "SVC_LOC_DEP":
            raise SvcLocationDepartureError()

        elif data["errorCode"] == "SVC_LOC_VIA":
            raise SvcLocationViaError()

        elif data["errorCode"] == "SVC_LOC_EQUAL":
            raise SvcLocationEqualError()

        elif data["errorCode"] == "SVC_LOC_NEAR":
            raise SvcLocationNearError()

        elif data["errorCode"] == "SVC_DATATIME":
            raise SvcDatetimeError()

        elif data["errorCode"] == "SVC_DATATIME_PERIOD":
            raise SvcDatetimePeriodError()

        elif data["errorCode"] == "SVC_PROD":
            raise SvcProductError()

        elif data["errorCode"] == "SVC_CTX":
            raise SvcContextError()

        elif data["errorCode"] == "SVC_NO_RESULT":
            raise SvcNoResultError()

        elif data["errorCode"] == "SVC_FAILED_SEARCH":
            raise SvcSearchError()

        elif data["errorCode"] == "SVC_NO_MATCH":
            raise SvcNoMatchError()

        elif data["errorCode"] == "INT_ERR":
            raise IntError()

        elif data["errorCode"] == "INT_GATEWAY":
            raise IntGatewayError()

        elif data["errorCode"] == "INT_TIMEOUT":
            raise IntTimeoutError()

        elif data["errorCode"] == "SOT_AT_DEST":
            raise SotAlreadyArrivedError()

        elif data["errorCode"] == "SOT_BEFORE_START":
            raise SotNotStartedError()

        elif data["errorCode"] == "SOT_CANCELLED":
            raise SotCancelledError()

        elif data["errorCode"] == "SOT_ALL_TRAINS_FILTERED":
            raise SotAllTrainsFilteredError()

        elif data["errorCode"] == "SOT_STAY_IN_CURRENT_CONNECTION":
            raise SotStayOnTripError()

        elif data["errorCode"] == "PARTIALSEARCH_INCORRECT_PARAM":
            raise PsIncorrectParamError()

        else:
            raise UnknownError(errorCode=data["errorCode"], errorText=data["errorText"])