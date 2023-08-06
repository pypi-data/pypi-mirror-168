from typing import List, Union
from pyrmv.classes.Stop import Stop
from pyrmv.raw.stop_by_coords import stop_by_coords as raw_stop_by_coords

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

def stop_by_coords(
    
        access_id: str,
        coords_lat: Union[str, float],
        coords_lon: Union[str, float],

        lang: Literal["de", "da", "en", "es", "fr", "hu", "it", "nl", "no", "pl", "sv", "tr"] = "en",
        radius: Union[int, float] = 1000,
        max_number: int = 10,
        stop_type: Literal["S", "P", "SP", "SE", "SPE"] = "S",
        selection_mode: Literal["SLCT_N", "SLCT_A"] = None, # type: ignore
    ) -> List[Stop]:
    """Method returns a list of stops around a given center coordinate.
    The returned results are ordered by their distance to the center coordinate.  

    More detailed request is available as raw.stop_by_coords(), however returns dict instead of List[Stop].

    ### Args:
        * access_id (`str`): Access ID for identifying the requesting client. Get your key on [RMV website](https://opendata.rmv.de/site/start.html).
        * coords_lat (`Union[str, float]`): Latitude of centre coordinate.
        * coords_lon (`Union[str, float]`): Longitude of centre coordinate.
        * lang (`Literal["de","da","en","es","fr","hu","it","nl","no","pl","sv","tr"]`, **optional**): The language of response. Defaults to "en".
        * radius (`Union[int, float]`, **optional**): Search radius in meter around the given coordinate if any. Defaults to 1000.
        * max_number (`int`, **optional**): Maximum number of returned stops. Defaults to 10.
        * stop_type (`Literal["S", "P", "SP", "SE", "SPE"]`, **optional**): Type filter for location types. Defaults to "S".
        * selection_mode (`Literal["SLCT_N", "SLCT_A"]`, **optional**): Selection mode for locations. Defaults to None.

    ### Returns:
        * dict: Output from RMV. Dict will contain "errorCode" and "errorText" if exception occurs.
    """    

    stops = []
    stops_raw = raw_stop_by_coords(
        accessId=access_id,
        originCoordLat=coords_lat,
        originCoordLong=coords_lon,
        lang=lang,
        radius=radius,
        maxNo=max_number,
        stopType=stop_type,
        locationSelectionMode=selection_mode
    )

    for stop in stops_raw["stopLocationOrCoordLocation"]:
        if "StopLocation" in stop:
            stops.append(Stop(stop["StopLocation"]))
        elif "CoordLocation" in stop:
            stops.append(Stop(stop["CoordLocation"]))

    return stops