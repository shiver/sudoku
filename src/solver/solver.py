'''
Created on 1/10/2009

@author: shiver
'''

from board.availablemap import AvailableMap

import logging

class Solver(object):
    
    def __init__(self, board):
        self._availableMap = AvailableMap(board)
        self._board = board
        self._logger = logging.getLogger('Solver')
        
    def getAvailableMap(self):
        return self._availableMap
    
    def getBoard(self):
        return self._board

    def assignValues(self, values):
        for pos, value in values.iteritems():
            x = pos[0]
            y = pos[1]
            self._board.setPosition(x, y, value)