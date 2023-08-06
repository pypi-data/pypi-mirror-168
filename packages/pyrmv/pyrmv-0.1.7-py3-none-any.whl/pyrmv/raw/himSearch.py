from requests import get
from typing import Dict, Union
from xmltodict import parse as xmlparse
from datetime import datetime

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

# 2.37. HIM Search (himsearch)
def himSearch(accessId: str,
        json: bool = True,
        dateB: str = None,
        dateE: str = None,
        timeB: str = None,
        timeE: str = None,
        weekdays: Dict[str, bool] = None,
        himIds: Union[str, list] = None,
        hierarchicalView: bool = False,
        operators: Union[str, list] = None,
        categories: Union[str, list] = None,
        channels: Union[str, list] = None,
        companies: Union[str, list] = None,
        lines: Union[str, list] = None,
        lineids: Union[str, list] = None,
        stations: Union[str, list] = None,
        fromstation: str = None,
        tostation: str = None,
        bothways: bool = None,
        trainnames: Union[str, list] = None,
        metas: Union[str, list] = None,
        himcategory: str = None,
        himtags: Union[str, list] = None,
        regions: Union[str, list] = None,
        himtext: Union[str, list] = None,
        himtexttags: Union[str, list] = None,
        additionalfields: Union[str, list] = None,
        poly: bool = False,
        searchmode: Literal["MATCH", "NOMATCH", "TFMATCH"] = None,
        affectedJourneyMode: Literal["ALL", "OFF"] = None,
        affectedJourneyStopMode: Literal["ALL", "IMP", "OFF"] = None,
        orderBy: Union[str, list] = None,
        minprio: Union[str, int] = None,
        maxprio: Union[str, int] = None
    ) -> dict:
    """The himSearch will return a list of HIM messages if matched by the given criteria as well as affected
    products if any.

    Read more about this in section 2.37. "HIM Search (himsearch)" of HAFAS ReST Documentation.  

    ### Args:
        * accessId (str): _description_
        * json (bool, optional): _description_. Defaults to True.
        * dateB (str, optional): _description_. Defaults to None.
        * dateE (str, optional): _description_. Defaults to None.
        * timeB (str, optional): _description_. Defaults to None.
        * timeE (str, optional): _description_. Defaults to None.
        * weekdays (Dict[str, bool], optional): _description_. Defaults to None.
        * himIds (Union[str, list], optional): _description_. Defaults to None.
        * hierarchicalView (bool, optional): _description_. Defaults to False.
        * operators (Union[str, list], optional): _description_. Defaults to None.
        * categories (Union[str, list], optional): _description_. Defaults to None.
        * channels (Union[str, list], optional): _description_. Defaults to None.
        * companies (Union[str, list], optional): _description_. Defaults to None.
        * lines (Union[str, list], optional): _description_. Defaults to None.
        * lineids (Union[str, list], optional): _description_. Defaults to None.
        * stations (Union[str, list], optional): _description_. Defaults to None.
        * fromstation (str, optional): _description_. Defaults to None.
        * tostation (str, optional): _description_. Defaults to None.
        * bothways (bool, optional): _description_. Defaults to None.
        * trainnames (Union[str, list], optional): _description_. Defaults to None.
        * metas (Union[str, list], optional): _description_. Defaults to None.
        * himcategory (str, optional): _description_. Defaults to None.
        * himtags (Union[str, list], optional): _description_. Defaults to None.
        * regions (Union[str, list], optional): _description_. Defaults to None.
        * himtext (Union[str, list], optional): _description_. Defaults to None.
        * himtexttags (Union[str, list], optional): _description_. Defaults to None.
        * additionalfields (Union[str, list], optional): _description_. Defaults to None.
        * poly (bool, optional): _description_. Defaults to False.
        * searchmode (Literal[&quot;MATCH&quot;, &quot;NOMATCH&quot;, &quot;TFMATCH&quot;], optional): _description_. Defaults to None.
        * affectedJourneyMode (Literal[&quot;ALL&quot;, &quot;OFF&quot;], optional): _description_. Defaults to None.
        * affectedJourneyStopMode (Literal[&quot;ALL&quot;, &quot;IMP&quot;, &quot;OFF&quot;], optional): _description_. Defaults to None.
        * orderBy (Union[str, list], optional): _description_. Defaults to None.
        * minprio (Union[str, int], optional): _description_. Defaults to None.
        * maxprio (Union[str, int], optional): _description_. Defaults to None.

    ### Returns:
        * dict: Output from RMV. Dict will contain "errorCode" and "errorText" if exception occurs.
    """    

    if json:
        headers = {"Accept": "application/json"}
    else:
        headers = {"Accept": "application/xml"}

    payload = {}

    for var, val in locals().items():
        if str(var) in ["dateB", "dateE"]:
            if val != None:
                if isinstance(val, datetime):
                    payload[str(var)] = val.strftime("%Y-%m-%d")
                else:
                    payload[str(var)] = val
        elif str(var) in ["timeB", "timeE"]:
            if val != None:
                if isinstance(val, datetime):
                    payload[str(var)] = val.strftime("%H:%M")
                else:
                    payload[str(var)] = val
        elif str(var) not in ["json", "headers", "payload"]:
            if val != None:
                payload[str(var)] = val

    output = get("https://www.rmv.de/hapi/himsearch", params=payload, headers=headers)

    if json:
        return output.json()
    else:
        return xmlparse(output.content)