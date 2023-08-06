from requests import get
from typing import List, Union
from xmltodict import parse as xmlparse

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

# 2.25. Arrival Board (arrivalBoard)
def boardArrival(accessId: str,
        json: bool = True
    ) -> dict:

    if json:
        headers = {"Accept": "application/json"}
    else:
        headers = {"Accept": "application/xml"}

    payload = {}

    for var, val in locals().items():
        if str(var) not in ["json", "headers", "payload"]:
            if val != None:
                payload[str(var)] = val

    output = get("https://www.rmv.de/hapi/arrivalBoard", params=payload, headers=headers)

    if json:
        return output.json()
    else:
        return xmlparse(output.content)