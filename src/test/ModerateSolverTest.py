'''
Created on 18/02/2010

@author: Rob
'''

from solver.EasySolver import EasySolver
from board.Board import Board
from board.BoardUtils import boardToSimpleSudokuClipboard,\
    simpleSudokuClipboardToString
from solver.ModerateSolver import ModerateSolver

import unittest

class Test(unittest.TestCase):
    def setUp(self):
        self.LOCKED_CANDIDATES1_1 = """
             *-----------*
             |...|...|...|
             |...|...|...|
             |...|...|...|
             |---+---+---|
             |...|.8.|..5|
             |.2.|...|...|
             |...|463|...|
             |---+---+---|
             |...|...|...|
             |...|...|...|
             |...|...|...|
             *-----------*
            """

    def tearDown(self):
        pass

    def testFindLockedCandidates1(self):
        board = Board()
        board.boardFromString(simpleSudokuClipboardToString(self.LOCKED_CANDIDATES1_1))
        solver = ModerateSolver(board)
        availableMap = solver.getAvailableMap()
        
        # Check before the locked candidates have been found
        assert('2' in availableMap.getPosition(6, 3))
        assert('2' in availableMap.getPosition(7, 3))
        assert('5' in availableMap.getPosition(0, 4))
        assert('5' in availableMap.getPosition(2, 4))
        
        solver.assignLockedCandidates1()
        
        # Make sure the excluded values are no longer returned
        assert(not ('2' in availableMap.getPosition(6, 3)))
        assert(not ('2' in availableMap.getPosition(7, 3)))
        assert(not ('5' in availableMap.getPosition(0, 4)))
        assert(not ('5' in availableMap.getPosition(2, 4)))
                       
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()