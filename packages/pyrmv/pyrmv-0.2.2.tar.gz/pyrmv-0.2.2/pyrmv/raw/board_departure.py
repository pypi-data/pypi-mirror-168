from datetime import datetime
from requests import get
from typing import List, Union
from xmltodict import parse as xmlparse

from pyrmv.utility.find_exception import find_exception

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

# 2.24. Departure Board (departureBoard)
def board_departure(accessId: str,
        json: bool = True,
        id: str = None, # type: ignore
        extId: str = None, # type: ignore
        direction: str = None, # type: ignore
        date: Union[str, datetime] = None, # type: ignore
        time: Union[str, datetime] = None, # type: ignore
        duration: int = 60,
        maxJourneys: int = -1,
        products: int = None, # type: ignore
        operators: Union[str, list] = None, # type: ignore
        lines: Union[str, list] = None, # type: ignore
        filterEquiv: bool = True,
        attributes: Union[str, list] = None, # type: ignore
        platforms: int = None, # type: ignore
        passlist: bool = False,
        boardType: Literal["DEP", "DEP_EQUIVS", "DEP_MAST", "DEP_STATION"] = "DEP"
    ) -> dict:

    if json:
        headers = {"Accept": "application/json"}
    else:
        headers = {"Accept": "application/xml"}

    payload = {}

    for var, val in locals().items():
        if str(var) == "boardType":
            if val != None:
                payload["type"] = val
        elif str(var) not in ["json", "headers", "payload"]:
            if val != None:
                payload[str(var)] = val

    output = get("https://www.rmv.de/hapi/departureBoard", params=payload, headers=headers)

    find_exception(output.json())

    if json:
        return output.json()
    else:
        return xmlparse(output.content)