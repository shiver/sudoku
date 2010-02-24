'''
Created on 1/10/2009

@author: Rob
'''

from Board import Board

import logging

class AvailableMap(Board):
    def __init__(self, board):
        self._logger = logging.getLogger('AvailableMap')

        # store the original board to use in generating the map
        self.__board = board
        self._exclusions = {}
        super(AvailableMap, self).__init__()
        self.calculate()

    def getCombineRow(self, y):
        """Returns all available values in a row as
        a single combined list
        """

        row = self.getRow(y)
        combined = []
        for r in row:
            combined.extend(r)

        return combined

    def getCombinedColumn(self, x):
        """Returns all available values in a column as
        a single combined list
        """

        column = self.getColumn(x)
        combined = []
        for r in column:
            combined.extend(r)

        return combined

    def getCombinedBlock(self, x, y):
        """Returns alls available values in a block as a
        single combined list
        """

        startX, startY = self.getBlockStart(x, y)
        block = self.getBlock(startX, startY)

        combined = []
        for b in block:
            combined.extend(b)

        return combined

    def findValueInRow(self, y, value):
        """Finds all instances of a value within the specified row.
        
        @param y: index of the row to search
        @param value: value to search for
        @return: a dict containing all instances of the value with the 
        key as a tuple indicating the position of the instance.
        """
        found = {}

        for x in xrange(self.getDimensions()):
            self._logger.debug('Fetching ' + str(x) + ', ' + str(y))
            pos = self.getPosition(x, y)
            if value in pos:
                found[(x, y)] = value

        return found

    def findValueInColumn(self, x, value):
        """Finds all instances of a value within the specified column.
        
        @param x: index of the column to search
        @param value: value to search for
        @return: a dict containing all instances of the value with the 
        key as a tuple indicating the position of the instance.
        """
        found = {}

        for y in xrange(self.getDimensions()):
            pos = self.getPosition(x, y)
            if value in pos:
                found[(x, y)] = value

        return found

    def findValueInBlock(self, startX, startY, value):
        """Finds all instances of a value within the specified block.
        
        @param x: index of starting row of the block
        @param y: index of starting column of the block
        @param value: value to search for
        @return: a dict containing all instances of the value with the 
        key as a tuple indicating the position of the instance.
        """
        found = {}

        for y in xrange(startY, startY + 3):
            for x in xrange(startX, startX + 3):
                pos = self.getPosition(x, y)
                if value in pos:
                    found[(x, y)] = value

        return found

    def getUnassigned(self):
        """Returns the number of positions in the board which are
        still unassigned.
        """

        return self._unassigned
    
    def getExclusions(self):
        """The exclusion dictionary which this method returns contains a
        x, y position key and a corresponding value list for are values not
        valid for the position.
        """
        
        return self._exclusions
    
    def addExclusion(self, x, y, value):
        """Indicates the value at the given location should be removed from the
        list of available values.
        """
        
        self.getExclusions()[(x, y)] = value
        
    def removeExclusions(self, x, y):
        """Removes all exclusions for a given location."""
        
        del self.getExclusions()[(x, y)]
        
    def removeExclusion(self, x, y, value):
        """Removes a specifically excluded value from the given location."""
        
        self.getExclusions()[(x, y)].remove(value)
        
    def isExcluded(self, x, y, value):
        """Returns True if the value is currently excluded from the given location"""
        
        if (self.getExclusions().has_key((x, y))):
            return value in self.getExclusions()[(x, y)]
        return False

    def calculate(self):
        """Recalculates the availableMap which indicates the possible 
        values for each position in the board.
        
        Note: This also updates the 'unassigned' value.
        """

        availableMap = []
        unassigned = 0
        for y in xrange(self.__board.getDimensions()):
            row = []
            for x in xrange(self.__board.getDimensions()):
                availableValues = []
                if self.__board.getPosition(x, y) in [0, '.']:
                    availableValues = self.__board.getAvailableValues(x, y)
                    
                    # Eliminate excluded values from the list of possible ones
                    for value in availableValues:
                        if self.isExcluded(x, y, value):
                            availableValues.remove(value)
                        
                    unassigned += 1
                row.append(availableValues)
            availableMap.append(row)

        self._board = availableMap
        self._unassigned = unassigned
