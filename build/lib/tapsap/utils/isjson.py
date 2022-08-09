# isjson
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import json

def isjson(variable) -> bool:
    """

    A function for determining if a value is a json object.
    
    Args:
        variable: A variable to test if it is a json object.

    Returns:
        isjson (bool): A true false statement if the value is a json object.
    """
    try:
        json.loads(variable)
    except ValueError:
        return False
    return True