from pyrmv.classes.Stop import Stop
from datetime import datetime
from isodate import parse_duration

class Url():

    def __init__(self, data: dict) -> None:
        self.name = data["name"]
        self.url = data["url"]

    def __str__(self) -> str:
        return f"{self.name}: {self.url}"

class Channel():

    def __init__(self, data: dict) -> None:
        self.name = data["name"]
        url = []
        for link in url:
            url.append(Url(link))
        self.url = url
        self.time_start = datetime.strptime(data["validFromTime"], "%H:%M:%S")
        self.date_start = datetime.strptime(data["validFromDate"], "%Y-%m-%d")
        self.time_end = datetime.strptime(data["validToTime"], "%H:%M:%S")
        self.date_end = datetime.strptime(data["validToDate"], "%Y-%m-%d")

    def __str__(self) -> str:
        return f"{self.name}: from {self.time_start} {self.date_start} until {self.time_end} {self.date_end}"


class Message():

    def __init__(self, data: dict) -> None:

        self.affected_stops = []
        for stop in data["affectedStops"]["StopLocation"]:
            self.affected_stops.append(Stop(stop))

        self.valid_from_stop = Stop(data["validFromStop"])
        self.valid_to_stop = Stop(data["validToStop"])

        self.channels = []
        for channel in data["channel"]:
            self.channels.append(Channel(channel))

        self.id = data["id"]
        self.active = data["act"]
        self.head = data["head"]
        self.lead = data["lead"]
        self.text = data["text"]
        self.company = data["company"]
        self.category = data["category"]
        self.priority = data["priority"]
        self.products = data["products"]
        self.icon = data["icon"]
        self.time_start = datetime.strptime(data["sTime"], "%H:%M:%S")
        self.date_start = datetime.strptime(data["sDate"], "%Y-%m-%d")
        self.time_end = datetime.strptime(data["eTime"], "%H:%M:%S")
        self.date_end = datetime.strptime(data["eDate"], "%Y-%m-%d")
        self.date_start_alt = data["altStart"]
        self.date_end_alt = data["altEnd"]
        self.time_modified = datetime.strptime(data["modTime"], "%H:%M:%S")
        self.date_modified = datetime.strptime(data["modDate"], "%Y-%m-%d")
        self.daily_start = datetime.strptime(data["dailyStartingAt"], "%H:%M:%S")
        self.daily_duration = parse_duration(data["dailyDuration"])

        if "baseType" in data:
            self.base_type = data["baseType"]
        else:
            self.base_type = None

    def __str__(self) -> str:
        return f"{self.base_type} message with priority {self.products} valid from {self.time_start.time()} {self.date_start.date()} until {self.time_end.time()} {self.date_end.date()}: {self.head} - {self.lead}"