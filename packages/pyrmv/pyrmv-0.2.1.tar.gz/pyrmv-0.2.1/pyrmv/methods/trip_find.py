from datetime import datetime
from typing import List, Union
from pyrmv.classes.Trip import Trip
from pyrmv.raw.trip_find import trip_find as raw_trip_find

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

def trip_find(
    
        access_id: str,
        lang: Literal["de", "da", "en", "es", "fr", "hu", "it", "nl", "no", "pl", "sv", "tr"] = "en",

        origin_id: str = None, # type: ignore
        origin_id_ext: str = None, # type: ignore
        origin_coord_lat: Union[str, float] = None, # type: ignore
        origin_coord_lon: Union[str, float] = None, # type: ignore
        origin_coord_name: str = None, # type: ignore

        destination_id: str = None, # type: ignore
        destination_id_ext: str = None, # type: ignore
        destination_coord_lat: Union[str, float] = None, # type: ignore
        destination_coord_lon: Union[str, float] = None, # type: ignore
        destination_coord_name: str = None, # type: ignore

        via: str = None, # type: ignore
        via_id: str = None, # type: ignore
        via_gis: str = None, # type: ignore
        via_wait_time: int = 0,

        avoid: str = None, # type: ignore
        avoid_id: str = None, # type: ignore

        change_time_percent: int = 100,
        change_time_min: int = None, # type: ignore
        change_time_max: int = None, # type: ignore
        change_time_add: int = None, # type: ignore
        change_max: int = None, # type: ignore

        date: Union[str, datetime] = None, # type: ignore
        time: Union[str, datetime] = None, # type: ignore
        
        search_arrival: bool = False,

        trips_after_time: int = None, # type: ignore
        trips_before_time: int = None, # type: ignore

        context: str = None, # type: ignore

        passlist: bool = False,
        operators: Union[str, list] = None, # type: ignore
        
        lines: Union[str, list] = None, # type: ignore
        lineids: Union[str, list] = None, # type: ignore

        iv_include: bool = False,
        iv_only: bool = False,
        
        bike_carriage: bool = False,

        passing_points: bool = False,

        real_time_mode: Literal["FULL", "INFOS", "OFF", "REALTIME", "SERVER_DEFAULT"] = None, # type: ignore

        include_earlier: bool = False,
        ict_alternatives: bool = False,
        tariff: bool = None, # type: ignore
        messages: bool = False,
        frequency: bool = True
    ) -> List[Trip]:
    """The trip service calculates a trip from a specified origin to a specified destination. These might be
    stop/station IDs or coordinates based on addresses and points of interest validated by the location service or
    coordinates freely defined by the client.

    Read more about this in section 2.12. "Trip Search (trip)" of HAFAS ReST Documentation.  

    ### Args:
        * access_id (`str`): Access ID for identifying the requesting client. Get your key on [RMV website](https://opendata.rmv.de/site/start.html).
        * lang (`Literal["de","da","en","es","fr","hu","it","nl","no","pl","sv","tr"]`, **optional**): The language of response. Defaults to "en".
        * origin_id (`str`, **optional**): Specifies the station/stop ID of the origin for the trip. Such ID can be retrieved from stop_by_name() or stop_by_coords(). Defaults to None.
        * origin_id_ext (`str`, **optional**): Deprecated. Please use originId as it supports external IDs. Specifies the external station/stop ID of the origin for the trip. Such ID can be retrieved from stop_by_name() or stop_by_coords(). Defaults to None.
        * origin_coord_lat (`Union[str, float]`, **optional**): Latitude of station/stop coordinate of the trip's origin. The coordinate can be retrieved from stop_by_name() or stop_by_coords(). Defaults to None.
        * origin_coord_lon (`Union[str, float]`, **optional**): Longitude of station/stop coordinate of the trip's origin. The coordinate can be retrieved from stop_by_name() or stop_by_coords(). Defaults to None.
        * origin_coord_name (`str`, **optional**): Name of the trip's origin if coordinate cannot be resolved to an address or poi. Defaults to None.
        * destination_id (`str`, **optional**): Specifies the station/stop ID of the destination for the trip. Such ID can be retrieved from stop_by_name() or stop_by_coords(). Defaults to None.
        * destination_id_ext (`str`, **optional**): Deprecated. Please use destId as it supports external IDs. Specifies the external station/stop ID of the destination for the trip. Such ID can be retrieved from stop_by_name() or stop_by_coords(). Defaults to None.
        * destination_coord_lat (`Union[str, float]`, **optional**): Latitude of station/stop coordinate of the trip's destination. The coordinate can be retrieved from stop_by_name() or stop_by_coords(). Defaults to None.
        * destination_coord_lon (`Union[str, float]`, **optional**): Longitude of station/stop coordinate of the trip's destination. The coordinate can be retrieved from stop_by_name() or stop_by_coords(). Defaults to None.
        * destination_coord_name (`str`, **optional**): Name of the trip's destination if coordinate cannot be resolved to an address or poi. Defaults to None.
        * via (`str`, **optional**): Complex structure to provide multiple via points separated by semicolon. This structure is build like this: `viaId|waittime|viastatus|products|direct|sleepingCar|couchetteCoach|attributes`. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * via_id (`str`, **optional**): ID of a station/stop used as a via for the trip. Specifying a via station forces the trip search to look for trips which must pass through this station. Such ID can be retrieved from stop_by_name() or stop_by_coords(). If `via` is used, `via_id` and `via_wait_time ` are having no effect. Defaults to None.
        * via_gis (`str`, **optional**): Complex structure to provide multiple GIS via locations separated by semicolon. This structure is build like this: `locationId|locationMode|transportMode|placeType|usageType|mode|durationOfStay`. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * via_wait_time (`int`, **optional**): Defines the waiting time spent at via station in minutes. If `via` is used, `via_id` and `via_wait_time` are having no effect. Defaults to 0.
        * avoid (`str`, **optional**): Complex structure to provide multiple points to be avoided separated by semicolon. This structure is build like this: `avoidId|avoidstatus` avoidId: id, extId or altId of the avoid, mandatory avoidstatus: one of NPAVM (do not run through if this is a meta station), NPAVO (do not run through), NCAVM (do not change if this is a meta station), NCAVO (do not change), optional but defaults to NCAVM Example: Just define three avoids by extId: `avoid="801234;801235;801236"`. Defaults to None.
        * avoid_id (`str`, **optional**): ID of a station/stop to be avoided as transfer stop for the trip. Such ID can be retrieved from stop_by_name() or stop_by_coords(). If `avoid` is used, `avoid_id` has no effect. Defaults to None.
        * change_time_percent (`int`, **optional**): Configures the walking speed when changing from one leg of the journey to the next one. It extends the time required for changes by a specified percentage. A value of 200 doubles the change time as initially calculated by the system. In the response, change time is presented in full minutes. If the calculation based on changeTime-Percent does not result in a full minute, it is rounded using "round half up" method. Defaults to 100.
        * change_time_min (`int`, **optional**): Minimum change time at stop in minutes. Defaults to None.
        * change_time_max (`int`, **optional**): Maximum change time at stop in minutes. Defaults to None.
        * change_time_add (`int`, **optional**): This amount of minutes is added to the change time at each stop. Defaults to None.
        * change_max (`int`, **optional**): Maximum number of changes. In range 0-11. Defaults to None.
        * date (`str`, **optional**): Sets the start date for which the departures shall be retrieved. Represented in the format `YYYY-MM-DD`. By default the current server date is used. Defaults to None.
        * time (`str`, **optional**): Sets the start time for which the departures shall be retrieved. Represented in the format `hh:mm[:ss]` in 24h nomenclature. Seconds will be ignored for requests. By default the current server time is used. Defaults to None.
        * search_arrival (`bool`, **optional**): If set, the date and time parameters specify the arrival time for the trip search instead of the departure time. Defaults to False.
        * trips_after_time (`int`, **optional**): Minimum number of trips after the search time. Sum of `trips_after_time` and `trips_before_time` has to be less or equal 6. Read more about this in HAFAS ReST Documentation. In range 1-6. Defaults to None.
        * trips_before_time (`int`, **optional**): Minimum number of trips before the search time. Sum of `trips_after_time` and `trips_before_time` has to be less or equal 6. Read more about this in HAFAS ReST Documentation. In range 0-6. Defaults to None.
        * context (`str`, **optional**): Defines the starting point for the scroll back or forth operation. Use the scrB value from a previous result to scroll backwards in time and use the scrF value to scroll forth. Defaults to None.
        * passlist (`bool`, **optional**): Enables/disables the return of the passlist for each leg of the trip. Defaults to False.
        * operators (`Union[str, list]`, **optional**): Only trips provided by the given operators are part of the result. If the operator should not be part of the be trip, negate it by putting ! in front of it. Example: Filter for operator A and B: `operators=["A","B"]`. Defaults to None.
        * lines (`Union[str, list]`, **optional**): Only journeys running the given line are part of the result. If the line should not be part of the be trip, negate it by putting ! in front of it. Defaults to None.
        * lineids (`Union[str, list]`, **optional**): Only journeys running the given line (identified by its line ID) are part of the result. If the line should not be part of the be trip, negate it by putting ! in front of it. Defaults to None.
        * iv_include (`bool`, **optional**): Enables/disables search for individual transport routes. Defaults to False.
        * iv_only (`bool`, **optional**): Enables/disables search for individual transport routes only. Defaults to False.
        * bike_carriage (`bool`, **optional**): Enables/disables search for trips explicit allowing bike carriage. This will only work in combination with `change_max=0` as those trips are always meant to be direct connections. Defaults to False.
        * passing_points (`bool`, **optional**): Enables/disables the return of stops having no alighting and boarding in its passlist for each leg of the trip. Needs passlist enabled. Defaults to False.
        * real_time_mode (`Literal["FULL", "INFOS", "OFF", "REALTIME", "SERVER_DEFAULT"]`, **optional**): Set the realtime mode to be used. Read more about this in HAFAS ReST Documentation. Defaults to None.
        * include_earlier (`bool`, **optional**): Disables search optimization in relation of duration. Defaults to False.
        * ict_alternatives (`bool`, **optional**): Enables/disables the search for alternatives with individualized change times (ICT). Defaults to False.
        * tariff (`bool`, **optional**): Enables/disables the output of tariff data. The default is configurable via provisioning. Defaults to None.
        * messages (`bool`, **optional**): Enables/disables the output of traffic messages. The default is configurable via provisioning. Defaults to False.
        * frequency (`bool`, **optional**): Enables/disables the calculation of frequency information. Defaults to True.

    ### Returns:
        * List[Trip]: List of Trip objects. Empty list if none found.
    """    

    trips = []
    trips_raw = raw_trip_find(

        accessId=access_id,
        lang=lang,

        originId=origin_id,
        originExtId=origin_id_ext,
        originCoordLat=origin_coord_lat,
        originCoordLong=origin_coord_lon,
        originCoordName=origin_coord_name,

        destId=destination_id,
        destExtId=destination_id_ext,
        destCoordLat=destination_coord_lat,
        destCoordLong=destination_coord_lon,
        destCoordName=destination_coord_name,

        via=via,
        viaId=via_id,
        viaGis=via_gis,
        viaWaitTime=via_wait_time,

        avoid=avoid,
        avoidId=avoid_id,

        changeTimePercent=change_time_percent,
        minChangeTime=change_time_min,
        maxChangeTime=change_time_max,
        addChangeTime=change_time_add,
        maxChange=change_max,

        date=date,
        time=time,
        
        searchForArrival=search_arrival,

        numF=trips_after_time,
        numB=trips_before_time,

        context=context,

        passlist=passlist,
        operators=operators,
        
        lines=lines,
        lineids=lineids,

        includeIv=iv_include,
        ivOnly=iv_only,
        
        bikeCarriage=bike_carriage,

        showPassingPoints=passing_points,

        rtMode=real_time_mode,

        includeEarlier=include_earlier,
        withICTAlternatives=ict_alternatives,
        tariff=tariff,
        trafficMessages=messages,
        withFreq=frequency
    )

    for trip in trips_raw["Trip"]:
        trips.append(Trip(trip))

    return trips