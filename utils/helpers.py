import os

def splitall(path):
    
    '''
    Splits a path string into all parts, because as.path.split splits it only
    in two parts.
    
    Parameters
    ----------
    path : string
        The path to be split.
    
    Returns
    -------
    The splitted path 
    '''
    
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts