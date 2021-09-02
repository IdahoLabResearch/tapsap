# isint
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

def isint(variable) -> bool:
    """

    A function for determining if a value int.
    
    Args:
        variable: A variable to test if it is a int.

    Returns:
        isint (bool): A true false statement if the value is a int.
    """
    try:
        float(variable)
    except ValueError:
        return False
    else:
        if float(variable).is_integer():
            if '.' in variable:
                return False
            else:
                return True
        else:
            return False
