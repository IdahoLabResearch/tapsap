# filter_xl
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from tapsap.utils.isjson import isjson
from tapsap.utils import isfloat, isint, islist
import json


def filter_xl(variable) -> bool:
    """

    A function for filtering a value that is coming in from an excel file.
    For example, if the input is a float, but read as a string, then the result in a class should be float.
    
    Args:
        variable (str): A variable to test the type of value.

    Returns:
        result (any): The result of the string filter from xlsx.
    """
    if isjson(variable):
        return json.loads(variable)
    elif islist(variable):
        if len(variable) == 2:
            return []
        else:
            return json.loads(variable)
    elif isint(variable):
        return int(variable)
    elif isfloat(variable):
        return float(variable)
    else:
        return variable
