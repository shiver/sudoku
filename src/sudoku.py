#!/usr/bin/python

'''
Created on 1/10/2009

@author: Rob
'''

from board.board import Board
from solver.easysolver import EasySolver
from board.boardutils import *

import logging

IMPOSSIBLE_STRING = '1.......2.9.4...5...6...7...5.9.3.......7.......85..4.7.....6...3...9.8...2.....1'
HARD_STRING = '6.5..2..8...1...7..9.5..6....2736.8....485....3.9217....4..3.9..5...4...3..8..1.2'
EASY_STRING = '79....3.......69..8...3..76.....5..2..54187..4..7.....61..9...8..23.......9....54'

logger = logging.getLogger('sudoku')
logging.basicConfig(level=logging.INFO)

board = Board()
board.boardFromString(HARD_STRING)
logger.info('\n' + boardToString(board))
easySolver = EasySolver(board)

assigned = -1
while assigned != 0:
    if easySolver.getAvailableMap().getUnassigned() == 0:
        break
    
    assigned = 0
    assignedNakedSingles = 0
    assignedHiddenSingles = 0
        
    assignedNakedSingles += easySolver.assignNakedSingles()
    logger.info('Found ' + str(assignedNakedSingles) + ' naked singles')
    assignedHiddenSingles = easySolver.assignHiddenSingles()
    logger.info('Found ' + str(assignedNakedSingles) + ' hidden singles')
    assignedLockedCandidates1 = easySolver.assignLockedCandidates1()
    logger.info('Found ' + str(assignedLockedCandidates1) + ' locked candidates')
    
    assigned += assignedNakedSingles
    assigned += assignedHiddenSingles
    assigned += assignedLockedCandidates1
    
logger.info('\n' + boardToString(easySolver.getBoard()))