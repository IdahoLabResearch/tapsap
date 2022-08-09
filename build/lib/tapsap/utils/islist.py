# islist
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

def islist(variable) -> bool:
    """

    A function for determining if a value includes brackets '['.
    
    Args:
        variable: A variable to test if it is a list.

    Returns:
        islist (bool): A true false statement if the value is a list.
    """
    if '[' in variable:
        return True
    else:
        return False
