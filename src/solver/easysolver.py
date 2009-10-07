'''
Created on 1/10/2009

@author: shiver
'''

from solver import Solver

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
        
