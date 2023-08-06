from requests import get
from typing import List, Union
from xmltodict import parse as xmlparse
from pyrmv.classes.Stop import Stop

from pyrmv.utility.find_exception import find_exception

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

# 2.3. Location Search by Name (location.name)
def stop_by_name(accessId: str,
        inputString: str,
        lang: Literal["de", "da", "en", "es", "fr", "hu", "it", "nl", "no", "pl", "sv", "tr"] = "en",
        json: bool = True,
        raw_response: bool = False,
        maxNo: int = 10,
        stopType: Literal["A", "ALL", "AP", "P", "S", "SA", "SP"] = "ALL",
        locationSelectionMode: Literal["SLCT_N", "SLCT_A"] = None, # type: ignore
        products: int = None, # type: ignore
        coordLat: Union[str, float] = None, # type: ignore
        coordLong: Union[str, float] = None, # type: ignore
        radius: Union[int, float] = 1000,
        refineId: str = None, # type: ignore
        meta: str = None, # type: ignore
        stations: Union[str, list] = None, # type: ignore
        sattributes: Union[str, list] = None, # type: ignore
        filterMode: Literal["DIST_PERI", "EXCL_PERI", "SLCT_PERI"] = "DIST_PERI"
    ) -> Union[dict, List[Stop]]:
    """The location.name service can be used to perform a pattern matching of a user input and to retrieve a list
    of possible matches in the journey planner database. Possible matches might be stops/stations, points of
    interest and addresses.  

    The result is a list of possible matches (locations) where the user might pick one entry to perform a trip
    request with this location as origin or destination or to ask for a departure board or arrival board of this
    location (stops/stations only).  

    Read more about this in section 2.3. "Location Search by Name (location.name)" of HAFAS ReST Documentation.  

    ### Args:
        * accessId (str): Access ID for identifying the requesting client. Get your key on [RMV website](https://opendata.rmv.de/site/start.html).
        * inputString (str): Search for that token.
        * lang (Literal["de","da","en","es","fr","hu","it","nl","no","pl","sv","tr"], optional): The language of response. Defaults to "en".
        * json (bool, optional): Whether response should be retrieved as JSON. XML is returned if False. Only matters if raw_response is True. Defaults to True.
        * raw_response (bool, optional): Whether response should be returned as `dict` instead of `List[Stop]`. Defaults to False.
        * maxNo (int, optional): Maximum number of returned stops. In range 1-1000. Defaults to 10.
        * stopType (Literal["A", "ALL", "AP", "P", "S", "SA", "SP"], optional): Type filter for location types. Defaults to "ALL".
        * locationSelectionMode (str, optional): Selection mode for locations. "SLCT_N": Not selectable, "SLCT_A": Selectable. Defaults to None.
        * products (int, optional): Decimal value defining the product classes to be included in the search. It represents a bitmask combining bit number of a product as defined in the HAFAS raw data. Defaults to None.
        * coordLat (Union[str, float], optional): Latitude of centre coordinate. Defaults to None.
        * coordLong (Union[str, float], optional): Longitude of centre coordinate. Defaults to None.
        * radius (Union[int, float], optional): Search radius in meter around the given coordinate if any. Defaults to 1000.
        * refineId (str, optional): In case of an refinable location, this value takes the ID of the refinable one of a previous result. Defaults to None.
        * meta (str, optional): Filter by a predefined meta filter. If the rules of the predefined filter should not be negated, put ! in front of it. Defaults to None.
        * stations (Union[str, list], optional): Filter for stations. Matches if the given value is prefix of any station in the itinerary. Multiple values are separated by comma. Defaults to None.
        * sattributes (Union[str, list], optional): Filter locations by one or more attribute codes. Multiple attribute codes are separated by comma. If the attribute should not be part of the be location data, negate it by putting ! in front of it. Defaults to None.
        * filterMode (Literal["DIST_PERI", "EXCL_PERI", "SLCT_PERI"], optional): Filter modes for nearby searches. Defaults to "DIST_PERI".

    ### Returns:
        * dict: Output from RMV. Dict will contain "errorCode" and "errorText" if exception occurs.
    """    

    if json:
        headers = {"Accept": "application/json"}
    else:
        headers = {"Accept": "application/xml"}

    payload = {}

    for var, val in locals().items():
        if str(var) == "inputString":
            if val != None:
                payload["input"] = val
        elif str(var) not in ["json", "headers", "payload", "raw_response"]:
            if val != None:
                payload[str(var)] = val

    output = get("https://www.rmv.de/hapi/location.name", params=payload, headers=headers)

    find_exception(output.json())

    if raw_response:
        if json:
            return output.json()
        else:
            return xmlparse(output.content)
    else:
        stops = []
        for stop in output.json()["stopLocationOrCoordLocation"]:
            if "StopLocation" in stop:
                stops.append(Stop(stop["StopLocation"]))
            elif "CoordLocation" in stop:
                stops.append(Stop(stop["CoordLocation"]))
        return stops