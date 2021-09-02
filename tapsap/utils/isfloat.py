# islist
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

def isfloat(variable) -> bool:
    """

    A function for determining if a value float.
    
    Args:
        variable: A variable to test if it is a float.

    Returns:
        isfloat (bool): A true false statement if the value is a float.
    """
    try:
        float(variable)
        return True
    except ValueError:
        return False
