'''
Created on 8/10/2009

@author: Rob
'''

from solver import Solver
from foundutils import *

import logging

class ModerateSolver(Solver):
    def __init__(self, board):
        super(ModerateSolver, self).__init__(board)
        self._logger = logging.getLogger('ModerateSolver')

    def findLockedCandidates1(self):
        """
        Find candidates in a block which are locked to either
        a single row or column. When this occurs we are able to remove 
        the candidates in the same row from the remaining two blocks.
        
        Returns a list containing block starting coordinates and 
        """

        lockedCandidates = []
        checked_blocks = []
        availableMap = self.getAvailableMap()

        for y in xrange(availableMap.getDimensions()):
            for x in xrange(availableMap.getDimensions()):
                startX, startY = availableMap.getBlockStart(x, y)

                if not (startX, startY) in checked_blocks:
                    checked_blocks.append((startX, startY))
                    # We haven't checked this block yet
                    for value in availableMap.getValidValues():
                        # Cycle through each possible value and record the number
                        # and position of each time the value is found.
                        foundInBlock = availableMap.findValueInBlock(
                                        startX, startY, value)

                        if len(foundInBlock) > 0:
                            # Check if all instances of the value fall in the
                            # same row. 
                            rowIndex = self._getLockedRow(foundInBlock)
                            if not rowIndex is None:
                                # Found locked candidates.
                                row = availableMap.getRow(rowIndex)
                                # Remove all 'other' instances of the value
                                # from row and replace the original in the
                                # availableMap.
                                #subtractFound(row, foundInBlock)
                                lockedCandidate = LockedCandidate()
                                lockedCandidate.blockStart = (startX, startY)
                                lockedCandidate.type = 0
                                lockedCandidate.index = rowIndex
                                lockedCandidate.value = value
                                
                                lockedCandidates.append(lockedCandidate)
                                availableMap.setRow(rowIndex, row)

        self._logger.debug(str(lockedCandidates) +
                           ' locked candidates found')
        return lockedCandidates

    def assignLockedCandidates1(self):
        """Excludes available values based on the locked candidates found.
        NOTE: This method does recalculate the available map.
        """
        
        lockedCandidates = self.findLockedCandidates1()
        availableMap = self.getAvailableMap()
        excluded = 0
        
        for locked in lockedCandidates:
            if locked.type == LockedCandidate.ROW:
                # This is a locked candidate in a row
                for x in xrange(self.getBoard().getDimensions()):
                    if not (self.getBoard().getBlockStart(x, locked.index) == 
                        locked.blockStart):
                        # We only exclude values which fall outside the 
                        # originating block
                        if locked.value in availableMap.getAvailableValues(x, 
                                                                locked.index):
                            availableMap.addExclusion(x, locked.index, 
                                                      locked.value)
                            excluded += 1
        
        self.getAvailableMap().calculate()
        return excluded

    def _getLockedRow(self, values):
        """
        Checks the position of each value and determines
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
    
class LockedCandidate(object):
    """A class used to store information about locked candidates.
    """
    
    ROW = 0
    COLUMN = 1
    BLOCK = 2
    INVALID = -1
    
    blockStart = (INVALID, INVALID)
    type = INVALID
    index = INVALID
    value = INVALID
