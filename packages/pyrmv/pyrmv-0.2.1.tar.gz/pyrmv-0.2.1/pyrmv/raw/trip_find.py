from datetime import datetime
from requests import get
from typing import List, Union
from xmltodict import parse as xmlparse
from pyrmv.classes.Trip import Trip

from pyrmv.utility.find_exception import find_exception

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

# 2.12. Trip Search (trip) 
def trip_find(accessId: str,
        lang: Literal["de", "da", "en", "es", "fr", "hu", "it", "nl", "no", "pl", "sv", "tr"] = "en",
        json: bool = True,

        originId: str = None, # type: ignore
        originExtId: str = None, # type: ignore
        originCoordLat: Union[str, float] = None, # type: ignore
        originCoordLong: Union[str, float] = None, # type: ignore
        originCoordName: str = None, # type: ignore

        destId: str = None, # type: ignore
        destExtId: str = None, # type: ignore
        destCoordLat: Union[str, float] = None, # type: ignore
        destCoordLong: Union[str, float] = None, # type: ignore
        destCoordName: str = None, # type: ignore

        via: str = None, # type: ignore
        viaId: str = None, # type: ignore
        viaWaitTime: int = 0,

        avoid: str = None, # type: ignore
        avoidId: str = None, # type: ignore

        viaGis: str = None, # type: ignore

        changeTimePercent: int = 100,
        minChangeTime: int = None, # type: ignore
        maxChangeTime: int = None, # type: ignore
        addChangeTime: int = None, # type: ignore
        maxChange: int = None, # type: ignore

        date: Union[str, datetime] = None, # type: ignore
        time: Union[str, datetime] = None, # type: ignore
        
        searchForArrival: bool = False,

        numF: int = None, # type: ignore
        numB: int = None, # type: ignore

        context: str = None, # type: ignore

        poly: bool = False,
        polyEnc: Literal["DLT", "GPA", "N"] = "N",

        passlist: bool = False,
        products: int = None, # type: ignore
        operators: Union[str, list] = None, # type: ignore
        
        attributes: Union[str, list] = None, # type: ignore
        sattributes: Union[str, list] = None, # type: ignore
        fattributes: Union[str, list] = None, # type: ignore
        lines: Union[str, list] = None, # type: ignore
        lineids: Union[str, list] = None, # type: ignore

        avoidPaths: List[Literal["SW", "EA", "ES", "RA", "CB"]] = None, # type: ignore

        originWalk: Union[str, list] = None, # type: ignore
        originBike: Union[str, list] = None, # type: ignore
        originCar: Union[str, list] = None, # type: ignore
        originTaxi: Union[str, list] = None, # type: ignore
        originPark: Union[str, list] = None, # type: ignore
        originMeta: Union[str, list] = None, # type: ignore

        destWalk: Union[str, list] = None, # type: ignore
        destBike: Union[str, list] = None, # type: ignore
        destCar: Union[str, list] = None, # type: ignore
        destTaxi: Union[str, list] = None, # type: ignore
        destPark: Union[str, list] = None, # type: ignore
        destMeta: Union[str, list] = None, # type: ignore

        totalWalk: Union[str, list] = None, # type: ignore
        totalBike: Union[str, list] = None, # type: ignore
        totalCar: Union[str, list] = None, # type: ignore
        totalTaxi: Union[str, list] = None, # type: ignore
        totalMeta: Union[str, list] = None, # type: ignore

        gisProducts: str = None, # type: ignore

        includeIv: bool = False,
        ivOnly: bool = False,

        mobilityProfile: str = None, # type: ignore
        
        bikeCarriage: bool = False,
        bikeCarriageType: Literal["SINGLEBIKES", "SMALLGROUPS", "LARGEGROUPS"] = None, # type: ignore

        sleepingCar: bool = False,
        couchetteCoach: bool = False,
        showPassingPoints: bool = False,
        baim: bool = False,

        eco: bool = False,
        ecoCmp: bool = False,
        ecoParams: str = None, # type: ignore

        rtMode: Literal["FULL", "INFOS", "OFF", "REALTIME", "SERVER_DEFAULT"] = None, # type: ignore

        unsharp: bool = False,
        trainFilter: str = None, # type: ignore
        economic: bool = False,
        groupFilter: str = None, # type: ignore

        blockingList: str = None, # type: ignore
        blockedEdges: str = None, # type: ignore

        trainComposition: bool = False,
        includeEarlier: bool = False,
        withICTAlternatives: bool = False,
        tariff: bool = None, # type: ignore
        trafficMessages: bool = False,
        travellerProfileData: str = None, # type: ignore
        withFreq: bool = True
    ) -> dict:
    """The trip service calculates a trip from a specified origin to a specified destination. These might be
    stop/station IDs or coordinates based on addresses and points of interest validated by the location service or
    coordinates freely defined by the client.

    Read more about this in section 2.12. "Trip Search (trip)" of HAFAS ReST Documentation.  

    ### Args:
        * accessId (str): Access ID for identifying the requesting client. Get your key on [RMV website](https://opendata.rmv.de/site/start.html).
        * lang (Literal["de","da","en","es","fr","hu","it","nl","no","pl","sv","tr"], optional): The language of response. Defaults to "en".
        * json (bool, optional): Whether response should be retrieved as JSON. XML is returned if False. Only matters if raw_response is True. Defaults to True.
        * originId (str, optional): Specifies the station/stop ID of the origin for the trip. Such ID can be retrieved from stopByName() or stopByCoords(). Defaults to None.
        * originExtId (str, optional): Deprecated. Please use originId as it supports external IDs. Specifies the external station/stop ID of the origin for the trip. Such ID can be retrieved from stopByName() or stopByCoords(). Defaults to None.
        * originCoordLat (Union[str, float], optional): Latitude of station/stop coordinate of the trip's origin. The coordinate can be retrieved from stopByName() or stopByCoords(). Defaults to None.
        * originCoordLong (Union[str, float], optional): Longitude of station/stop coordinate of the trip's origin. The coordinate can be retrieved from stopByName() or stopByCoords(). Defaults to None.
        * originCoordName (str, optional): Name of the trip's origin if coordinate cannot be resolved to an address or poi. Defaults to None.
        * destId (str, optional): Specifies the station/stop ID of the destination for the trip. Such ID can be retrieved from stopByName() or stopByCoords(). Defaults to None.
        * destExtId (str, optional): Deprecated. Please use destId as it supports external IDs. Specifies the external station/stop ID of the destination for the trip. Such ID can be retrieved from stopByName() or stopByCoords(). Defaults to None.
        * destCoordLat (Union[str, float], optional): Latitude of station/stop coordinate of the trip's destination. The coordinate can be retrieved from stopByName() or stopByCoords(). Defaults to None.
        * destCoordLong (Union[str, float], optional): Longitude of station/stop coordinate of the trip's destination. The coordinate can be retrieved from stopByName() or stopByCoords(). Defaults to None.
        * destCoordName (str, optional): Name of the trip's destination if coordinate cannot be resolved to an address or poi. Defaults to None.
        * via (str, optional): Complex structure to provide multiple via points separated by semicolon. This structure is build like this: `viaId|waittime|viastatus|products|direct|sleepingCar|couchetteCoach|attributes`. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * viaId (str, optional): ID of a station/stop used as a via for the trip. Specifying a via station forces the trip search to look for trips which must pass through this station. Such ID can be retrieved from stopByName() or stopByCoords(). If `via` is used, `viaId` and `viaWaitTime ` are having no effect. Defaults to None.
        * viaWaitTime (int, optional): Defines the waiting time spent at via station in minutes. If `via` is used, `viaId` and `viaWaitTime` are having no effect. Defaults to 0.
        * avoid (str, optional): Complex structure to provide multiple points to be avoided separated by semicolon. This structure is build like this: `avoidId|avoidstatus` avoidId: id, extId or altId of the avoid, mandatory avoidstatus: one of NPAVM (do not run through if this is a meta station), NPAVO (do not run through), NCAVM (do not change if this is a meta station), NCAVO (do not change), optional but defaults to NCAVM Example: Just define three avoids by extId: `avoid="801234;801235;801236"`. Defaults to None.
        * avoidId (str, optional): ID of a station/stop to be avoided as transfer stop for the trip. Such ID can be retrieved from stopByName() or stopByCoords(). If `avoid` is used, `avoidId` has no effect. Defaults to None.
        * viaGis (str, optional): Complex structure to provide multiple GIS via locations separated by semicolon. This structure is build like this: `locationId|locationMode|transportMode|placeType|usageType|mode|durationOfStay`. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * changeTimePercent (int, optional): Configures the walking speed when changing from one leg of the journey to the next one. It extends the time required for changes by a specified percentage. A value of 200 doubles the change time as initially calculated by the system. In the response, change time is presented in full minutes. If the calculation based on changeTime-Percent does not result in a full minute, it is rounded using "round half up" method. Defaults to 100.
        * minChangeTime (int, optional): Minimum change time at stop in minutes. Defaults to None.
        * maxChangeTime (int, optional): Maximum change time at stop in minutes. Defaults to None.
        * addChangeTime (int, optional): This amount of minutes is added to the change time at each stop. Defaults to None.
        * maxChange (int, optional): Maximum number of changes. In range 0-11. Defaults to None.
        * date (str, optional): Sets the start date for which the departures shall be retrieved. Represented in the format `YYYY-MM-DD`. By default the current server date is used. Defaults to None.
        * time (str, optional): Sets the start time for which the departures shall be retrieved. Represented in the format `hh:mm[:ss]` in 24h nomenclature. Seconds will be ignored for requests. By default the current server time is used. Defaults to None.
        * searchForArrival (bool, optional): If set, the date and time parameters specify the arrival time for the trip search instead of the departure time. Defaults to False.
        * numF (int, optional): Minimum number of trips after the search time. Sum of numF and numB has to be less or equal 6. Read more about this in HAFAS ReST Documentation. In range 1-6. Defaults to None.
        * numB (int, optional): Minimum number of trips before the search time. Sum of numF and numB has to be less or equal 6. Read more about this in HAFAS ReST Documentation. In range 0-6. Defaults to None.
        * context (str, optional): Defines the starting point for the scroll back or forth operation. Use the scrB value from a previous result to scroll backwards in time and use the scrF value to scroll forth. Defaults to None.
        * poly (bool, optional): Enables/disables the calculation of the polyline for each leg of the trip except any GIS route. Defaults to False.
        * polyEnc (Literal["DLT", "GPA", "N"], optional): Defines encoding of the returned polyline. Possible values are "N" (no encoding / compression), "DLT" (delta to the previous coordinate), "GPA" (Google encoded polyline format). Defaults to "N".
        * passlist (bool, optional): Enables/disables the return of the passlist for each leg of the trip. Defaults to False.
        * products (str, optional): Decimal value defining the product classes to be included in the search. It represents a bitmask combining bit number of a product as defined in the HAFAS raw data. Defaults to None.
        * operators (Union[str, list], optional): Only trips provided by the given operators are part of the result. If the operator should not be part of the be trip, negate it by putting ! in front of it. Example: Filter for operator A and B: `operators=["A","B"]`. Defaults to None.
        * attributes (Union[str, list], optional): Filter trips by one or more attribute codes of a journey. If the attribute should not be part of the be trip, negate it by putting ! in front of it. Defaults to None.
        * sattributes (Union[str, list], optional): Filter trips by one or more station attribute codes of a journey. If the attribute should not be part of the be trip, negate it by putting ! in front of it. Defaults to None.
        * fattributes (Union[str, list], optional): Filter trips by one or more footway attribute codes of a journey. If the attribute should not be part of the be trip, negate it by putting ! in front of it. Defaults to None.
        * lines (Union[str, list], optional): Only journeys running the given line are part of the result. If the line should not be part of the be trip, negate it by putting ! in front of it. Defaults to None.
        * lineids (Union[str, list], optional): Only journeys running the given line (identified by its line ID) are part of the result. If the line should not be part of the be trip, negate it by putting ! in front of it. Defaults to None.
        * avoidPaths (List[Literal["SW", "EA", "ES", "RA", "CB"]], optional): Only path not having the given properties will be part of the result. "SW": Stairway; "EA": Elevator; "ES": Escalator; "RA": Ramp; "CB": Convey Belt. Example: Use paths without ramp and stairway: `avoidPaths="SW", "RA"`. Defaults to None.
        * originWalk (Union[str, list], optional): Enables/disables using footpaths in the beginning of a trip when searching from an address. To fine-tune the minimum and/or maximum distance to the next public transport station, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * originBike (Union[str, list], optional): Enables/disables using bike routes in the beginning of a trip when searching from an address. To fine-tune the minimum and/or maximum distance to the next public transport station or mode change point, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * originCar (Union[str, list], optional): Enables/disables using car in the beginning of a trip when searching from an address. To fine-tune the minimum and/or maximum distance to the next public transport station, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * originTaxi (Union[str, list], optional): Enables/disables using taxi rides in the beginning of a trip when searching from an address. To fine-tune the minimum and/or maximum distance to the next public transport station, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * originPark (Union[str, list], optional): Enables/disables using Park and Ride in the beginning of a trip when searching from an address. To fine-tune the minimum and/or maximum distance to the next public transport station, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * originMeta (Union[str, list], optional): Enables using one or more predefined individual transport meta profile at the beginning of a trip. Defaults to None.
        * destWalk (Union[str, list], optional): Enables/disables using footpaths at the end of a trip when searching to an address. To fine-tune the minimum and/or maximum distance to the next public transport station, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * destBike (Union[str, list], optional): Enables/disables using bike routes at the end of a trip when searching to an address. To fine-tune the minimum and/or maximum distance to the next public transport station, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * destCar (Union[str, list], optional): Enables/disables using car routes at the end of a trip when searching to an address. To fine-tune the minimum and/or maximum distance to the next public transport station, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * destTaxi (Union[str, list], optional): Enables/disables using taxi rides at the end of a trip when searching to an address. To fine-tune the minimum and/or maximum distance to the next public transport station, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * destPark (Union[str, list], optional): Enables/disables using Park and Ride at the end of a trip when searching to an address. To fine-tune the minimum and/or maximum distance to the next public transport station, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * destMeta (Union[str, list], optional): Enables using one or more predefined individual transport meta profile at the end of a trip. Defaults to None.
        * totalWalk (Union[str, list], optional): Enables/disables using footpaths for the whole trip. To fine-tune the minimum and/or maximum distance to the next public transport station, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * totalBike (Union[str, list], optional): Enables/disables using bike routes for the whole trip. To fine-tune the minimum and/or maximum distance to the next public transport station, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * totalCar (Union[str, list], optional): Enables/disables using car routes for the whole trip. To fine-tune the minimum and/or maximum distance to the next public transport station, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * totalTaxi (Union[str, list], optional): Enables/disables using taxi rides for the whole trip. To fine-tune the minimum and/or maximum distance to the next public transport station, provide these values as a list or as a string separated by comma. These values are expressed in meters. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * totalMeta (Union[str, list], optional): Enables using one or more predefined individual transport meta profile for a trip. Defaults to None.
        * gisProducts (str, optional): Filter on GIS product, e.g. specific sharing provider. Currently, only exclusion of certain providers is available by adding ! in front of the provider meta code. Defaults to None.
        * includeIv (bool, optional): Enables/disables search for individual transport routes. Defaults to False.
        * ivOnly (bool, optional): Enables/disables search for individual transport routes only. Defaults to False.
        * mobilityProfile (str, optional): Use a predefined filter by its name. The filters are defined in the HAFAS installation. If the filter should be negated, put a ! in front of its name. Defaults to None.
        * bikeCarriage (bool, optional): Enables/disables search for trips explicit allowing bike carriage. This will only work in combination with `maxChange=0` as those trips are always meant to be direct connections. Defaults to False.
        * bikeCarriageType (Literal["SINGLEBIKES", "SMALLGROUPS", "LARGEGROUPS"], optional): Filter for a specific bike carriage type. Defaults to None.
        * sleepingCar (bool, optional): Enables/disables search for trips having sleeping car. This will only work in combination with `maxChange=0` as those trips are always meant to be direct connections. Defaults to False.
        * couchetteCoach (bool, optional): Enables/disables search for trips having couchette coach. This will only work in combination with `maxChange=0` as those trips are always meant to be direct connections. Defaults to False.
        * showPassingPoints (bool, optional): Enables/disables the return of stops having no alighting and boarding in its passlist for each leg of the trip. Needs passlist enabled. Defaults to False.
        * baim (bool, optional): Enables/disables BAIM search and response. Defaults to False.
        * eco (bool, optional): Enables/disables eco value calculation. Defaults to False.
        * ecoCmp (bool, optional): Enables/disables eco comparison. Defaults to False.
        * ecoParams (str, optional): Provide additional eco parameters. Defaults to None.
        * rtMode (Literal["FULL", "INFOS", "OFF", "REALTIME", "SERVER_DEFAULT"], optional): Set the realtime mode to be used. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * unsharp (bool, optional): Enables/disables unsharp search mode. Read more about this in section 2.12.2.1. "Trip Search (trip)" of HAFAS ReST Documentation. Defaults to False.
        * trainFilter (str, optional): Filters a trip search for a certain train. First hit will be taken. Defaults to None.
        * economic (bool, optional): Enables/disables economic search mode. Read more about this in section 2.12.2.2. "Trip Search (trip)" of HAFAS ReST Documentation. Defaults to False.
        * groupFilter (str, optional): Use a predefined group filter to query for certain modes. Defaults to None.
        * blockingList (str, optional): Defines a section of a route of a journey not to be used within the trip search. Each route section is defined by a tuple of the following style: `<train name>|<departure id>|<arrival id>|<departure time>|<arrival time>|<departure date>|<arrival date>` A set of tuples can be separated by semicolon. Defaults to None.
        * blockedEdges (str, optional): List of edges within the public transport network that should be excluded from the result. Each edge is defined by a tuple of the following style: `start location ID|end locationID|bidirectional|blockOnlyIfInOutAllowed` A set of tuples can be separated by semicolon. Defaults to None.
        * trainComposition (bool, optional): Enables/disables train composition data. Defaults to False.
        * includeEarlier (bool, optional): Disables search optimization in relation of duration. Defaults to False.
        * withICTAlternatives (bool, optional): Enables/disables the search for alternatives with individualized change times (ICT). Defaults to False.
        * tariff (bool, optional): Enables/disables the output of tariff data. The default is configurable via provisioning. Defaults to None.
        * trafficMessages (bool, optional): Enables/disables the output of traffic messages. The default is configurable via provisioning. Defaults to False.
        * travellerProfileData (str, optional): Traveller profile data. Structure depends on set up. Defaults to None.
        * withFreq (bool, optional): Enables/disables the calculation of frequency information. Defaults to True.

    ### Returns:
        * dict: Output from RMV. Dict will contain "errorCode" and "errorText" if exception occurs.
    """    

    if json:
        headers = {"Accept": "application/json"}
    else:
        headers = {"Accept": "application/xml"}

    payload = {}

    for var, val in locals().items():
        if str(var) == "date":
            if val != None:
                if isinstance(val, datetime):
                    payload[str(var)] = val.strftime("%Y-%m-%d")
                else:
                    payload[str(var)] = val
        elif str(var) == "time":
            if val != None:
                if isinstance(val, datetime):
                    payload[str(var)] = val.strftime("%H:%M")
                else:
                    payload[str(var)] = val
        elif str(var) not in ["json", "headers", "payload", "raw_response"]:
            if val != None:
                payload[str(var)] = val

    output = get("https://www.rmv.de/hapi/trip", params=payload, headers=headers)

    find_exception(output.json())

    if json:
        return output.json()
    else:
        return xmlparse(output.content)