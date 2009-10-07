'''
Created on 1/10/2009

@author: shiver
'''

from board import Board

import logging

class AvailableMap(Board):
    def __init__(self, board):
        self._logger = logging.getLogger('AvailableMap')
        
        # store the original board to use in generating the map
        self.__board = board
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
        startX, startY = self.getBlockStart(x, y)
        block = self.getBlock(startX, startY)
        
        combined = []
        for b in block:
            combined.extend(b)
            
        return combined
    
    def findValueInRow(self, y, value):
        found = {}
        
        #row = self.getRow(y)
        for x in xrange(self.getDimensions()):
            pos = self.getPosition(x, y)
            if value in pos:
                found[(x, y)] = value
                
        return found
    
    def findValueInColumn(self, x, value):
        found = {}
        
        #column = self.getColumn(x)
        for y in xrange(self.getDimensions()):
            pos = self.getPosition(x, y)
            if value in pos:
                found[(x, y)] = value
                
        return found
    
    def findValueInBlock(self, startX, startY, value):
        found = {}
        
        for y in xrange(startY, startY + 3):
            for x in xrange(startX, startX + 3):
                pos = self.getPosition(x, y)
                if value in pos:
                    found[(x, y)] = value
                
        return found
    
    def getUnassigned(self):
        return self._unassigned
        
    def calculate(self):    
        availableMap = []
        unassigned = 0
        for y in xrange(self.__board.getDimensions()):
            row = []
            for x in xrange(self.__board.getDimensions()):
                availableValues = []
                if self.__board.getPosition(x, y) in [0, '.']:
                    availableValues = self.__board.getAvailableValues(x, y)
                    unassigned += 1
                row.append(availableValues)
            availableMap.append(row)
            
        self._board = availableMap
        self._unassigned = unassigned 