from typing import OrderedDict


def weekdays_bitmask(data: OrderedDict[str, bool]) -> str:
    """Convert ordered dict with weekdays to a bitmask.

    ### Args:
        * data (OrderedDict[str, bool]): OrderedDict formatted as follows: OrderedDict(Monday=bool, Tuesday=bool, Wednesday=bool, Thursday=bool, Friday=bool, Saturday=bool, Sunday=bool)

    ### Returns:
        * str: _description_
    """    
    output = ""
    if len(data) != 7:
        raise ValueError("OrderedDict must be formatted as follows: OrderedDict(Monday=bool, Tuesday=bool, Wednesday=bool, Thursday=bool, Friday=bool, Saturday=bool, Sunday=bool)")
    for day in data:
        if data[day]:
            output += "1"
        else:
            output += "0"
    return output