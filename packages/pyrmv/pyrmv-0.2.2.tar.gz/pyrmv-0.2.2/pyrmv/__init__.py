"""
## PythonRMV

Small module that makes your journey with RMV REST API somehow easier. Based fully on official RMV API reference and HAFAS documentation.

## Usage

```py
import pyrmv

# Set API key
access_id = "Something"

# Get origin's and destination's location
origin = pyrmv.stop_by_name(access_id, "Frankfurt Hauptbahnhof", max_number=3)[0]
destination = pyrmv.stop_by_coords(access_id, 50.099613, 8.685449, max_number=3)[0]

# Find a trip by locations got
trip = pyrmv.trip_find(access_id, origin_id=origin.id, dest_id=destination.id)
```
"""

__name__ = "pyrmv"
__version__ = "0.2.2"
__license__ = "MIT License"
__author__ = "Profitroll"

from . import raw
from . import errors
from . import utility
from . import classes
from .methods import *