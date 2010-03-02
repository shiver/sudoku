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
                            result = self._getLocked(foundInBlock)
                            if not result is None:
                                # Found locked candidates. 
                                lockedCandidate = LockedCandidate()
                                lockedCandidate.blockStart = (startX, startY)
                                lockedCandidate.type = result['type']
                                lockedCandidate.index = result['index']
                                lockedCandidate.value = value
                                
                                lockedCandidates.append(lockedCandidate)
                                ##availableMap.setRow(index, row)

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
            if locked.type == LockedCandidate.COLUMN:
                for y in xrange(self.getBoard().getDimensions()):
                    if not (self.getBoard().getBlockStart(locked.index, y) == 
                        locked.blockStart):
                        # We only exclude values which fall outside the 
                        # originating block
                        if locked.value in availableMap.getAvailableValues(
                                                locked.index, y):
                            availableMap.addExclusion(locked.index, y, 
                                                      locked.value)
                            excluded += 1
        self.getAvailableMap().calculate()
        return excluded

    def _getLocked(self, values):
        """Checks the position of each value and determines
        if they all fall in the same row or column.
        
        @returns: index of the row or column which the values fall in
        if they are locked. Otherwise None
        """

        # To be locked we should only have 3 or fewer values to check
        if len(values) > 3:
            return None
        
        columns = {}
        rows = {}
        
        for column, row in values.iterkeys():
            if columns.has_key(column):
                columns[column] += 1
            else:
                columns[column] = 1
                
            if rows.has_key(row):
                rows[row] += 1
            else:
                rows[row] = 1
                
        for key, value in columns.iteritems():
            if value == len(values):
                return dict(index=key, type=LockedCandidate.COLUMN)
            
        for key, value in rows.iteritems():
            if value == len(values):
                return dict(index=key, type=LockedCandidate.ROW)
        
        return None
        
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
