'''
Created on 10/10/2009

@author: Rob
'''

"""
This module contains helper methods to be used on Found Values.

Found Values are stored in a dictionary object.
The key is a tuple holding the x and y positional
information, while the value is set to the value which was 
searched for and found.

eg: found = {(0, 0): 1, (1, 0): 1}
""" 

def getFoundColumns(foundValues):
    """Returns a list of all the column indexes"""
    columns = []
    for pos, value in foundValues.iteritems():
        columns.append(pos[0])
        
    return columns

def getFoundRows(foundValues):
    """Returns a list of all the row indexes"""
    rows = []
    for pos, value in foundValues.iteritems():
        rows.append(pos[1])
        
    return rows

def subtractFound(original, remove):
    """Subtracts one set of Found Values from another and returns the
    result.
    
    @param original: the original Found Values
    @param remove: the Found Values to remove
    @return: original without the removed Found Values
    """
    
    for key in remove.iterkeys():
        try:
            del original[key]
        except KeyError:
            continue
        
def subtractFoundFromRow(row, remove):
    """
    """
    count = 0
    for pos, value in remove.iteritems():
        x = pos[0]
        try:
            row[x].remove(value)
            count += 1
        except KeyError:
            continue
        
    return count
        