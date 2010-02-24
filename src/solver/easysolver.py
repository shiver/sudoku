'''
Created on 1/10/2009

@author: Rob
'''

from Solver import Solver
from FoundUtils import *

import logging

class EasySolver(Solver):
    def __init__(self, board):
        super(EasySolver, self).__init__(board)
        self._logger = logging.getLogger('EasySolver')
    
    def findNakedSingles(self):
        nakedSingles = {}
        counter = 0
        
        for y in xrange(self.getAvailableMap().getDimensions()):
            for x in xrange(self.getAvailableMap().getDimensions()):
                avail = self.getAvailableMap().getPosition(x, y)
                if len(avail) == 1:
                    nakedSingles[(x, y)] = avail[0]
                    counter += 1
        
        self._logger.debug(str(counter) + ' naked singles found')
        self._logger.debug(nakedSingles)     
        
        return nakedSingles
    
    def assignNakedSingles(self):
        nakedSingles = self.findNakedSingles()
        self.assignValues(nakedSingles)
        self.getAvailableMap().calculate()
        return len(nakedSingles)
    
    def findHiddenSingles(self):
        validValues = self.getAvailableMap().getValidValues()
        hiddenSingles = {}
        checked_rows = []
        checked_columns = []
        checked_blocks = []
        
        for y in xrange(self.getAvailableMap().getDimensions()):  
            for x in xrange(self.getAvailableMap().getDimensions()):                    
                
                startX, startY = self.getAvailableMap().getBlockStart(x, y)
                
                for v in validValues:
                    if not (y, v) in checked_rows:
                        found = self.getAvailableMap().findValueInRow(y, v)
                        if found.values().count(v) == 1:
                            hiddenSingles[self.getKeyFromDict(found, v)] = v
                        checked_rows.append((y, v))
                    if not (x, v) in checked_columns:
                        found = self.getAvailableMap().findValueInColumn(x, v)
                        if found.values().count(v) == 1:
                            hiddenSingles[self.getKeyFromDict(found, v)] = v
                        checked_columns.append((x, v))
                    if not (startX, startY, v) in checked_blocks:
                        found = self.getAvailableMap().findValueInBlock(startX, startY, v)
                        if found.values().count(v) == 1:
                            hiddenSingles[self.getKeyFromDict(found, v)] = v
                        checked_blocks.append((startX, startY, v)) 
                    
        self._logger.debug(str(hiddenSingles) + ' hidden singles found')
        return hiddenSingles
    
    def getKeyFromDict(self, dict, value):
        #TODO: this needs work and possibly a totally different solution
        
        for key, v in dict.iteritems():
            if v == value:
                return key
                
    def assignHiddenSingles(self):
        hiddenSingles = self.findHiddenSingles()
        self.assignValues(hiddenSingles)
        self.getAvailableMap().calculate()
        return len(hiddenSingles)
        
    
    # TODO: Locked candidates need to be in the ModerateSolver
    def findLockedCandidates1(self):
        """Find candidates in a block which are found either
        in a single row or column.
        """

        lockedCandidates = 0
        checked_blocks = []
        availableMap = self.getAvailableMap()

        for y in xrange(availableMap.getDimensions()):
            for x in xrange(availableMap.getDimensions()):
                startX, startY = availableMap.getBlockStart(x, y)

                if not (startX, startY) in checked_blocks:
                    self._logger.debug(str(startX) + ', ' + str(startY))
                    checked_blocks.append((startX, startY))
                    # We haven't checked this block yet
                    for value in availableMap.getValidValues():
                        # Cycle through each possible value and record the number
                        # and position of each time the value is found.
                        self._logger.debug('checking ' + str(value))
                        foundInBlock = availableMap.findValueInBlock(
                                        startX, startY, value)

                        if len(foundInBlock) > 0:
                            # Check if all instances of the value fall in the
                            # same row. 
                            rowIndex = self._getLockedRow(foundInBlock)
                            if not rowIndex is None:
                                # Found locked candidates.
                                row = availableMap.getRow(rowIndex)
                                foundInRow = availableMap.findValueInRow(
                                                rowIndex, value)
                                # Remove all 'other' instances of the value
                                # from row and replace the original in the
                                # availableMap.
                                subtractFound(foundInRow, foundInBlock)
                                lockedCandidates += subtractFoundFromRow(row, foundInRow)
                                availableMap.setRow(rowIndex, row)

        self._logger.debug(str(lockedCandidates) +
                           ' locked candidates found')
        return lockedCandidates

    def assignLockedCandidates1(self):
        lockedCandidates = self.findLockedCandidates1()
        #self.assignValues(lockedCandidates)
        self.getAvailableMap().calculate()
        return lockedCandidates

    def _getLockedRow(self, values):
        """Checks the position of each value and determines
        if they all fall in the same row.
        
        @returns: index of the row which the values fall in
        if they are locked. Otherwise None
        """

        prev = None
        for key in values.iterkeys():
            if prev is None:
                # Take record of the first row index we come across
                prev = key[1]
            else:
                # Make sure that all subsequent rows match
                if not key[1] == prev:
                    return None

        # We only get here if all the rows matched 
        return prev
    
