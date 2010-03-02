'''
Created on 18/02/2010

@author: Rob
'''

from solver.easysolver import EasySolver
from board.board import Board
from board.boardutils import boardToSimpleSudokuClipboard,\
    simpleSudokuClipboardToString
from solver.moderatesolver import ModerateSolver
from board.htmlboard import HTMLBoard

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
        self.LOCKED_CANDIDATES1_2 = """
             *-----------*
             |...|...|...|
             |...|.2.|...|
             |...|...|...|
             |---+---+---|
             |...|4..|...|
             |...|6.8|...|
             |...|3..|...|
             |---+---+---|
             |...|...|...|
             |...|...|...|
             |...|..5|...|
             *-----------*"""
            
        self.OUT_PATH = 'c:\\users\\rob\\projects\\sudoku\\debug\\'

    def tearDown(self):
        pass

    def testFindLockedCandidates1_Row(self):
        board = Board()
        board.boardFromString(
                simpleSudokuClipboardToString(self.LOCKED_CANDIDATES1_1))
        solver = ModerateSolver(board)
        availableMap = solver.getAvailableMap()
        
        # Check before the locked candidates have been found
        assert('2' in availableMap.getPosition(6, 3))
        assert('2' in availableMap.getPosition(7, 3))
        assert('5' in availableMap.getPosition(0, 4))
        assert('5' in availableMap.getPosition(2, 4))
        
        htmlBoard = HTMLBoard(solver.getBoard(), solver.getAvailableMap())
        assert(htmlBoard.write(self.OUT_PATH + 'locked_candidates1_row_before.html', 
                               forceOverwrite=True))
        
        solver.assignLockedCandidates1()
        
        # Make sure the excluded values are no longer returned
        assert(not ('2' in availableMap.getPosition(6, 3)))
        assert(not ('2' in availableMap.getPosition(7, 3)))
        assert(not ('5' in availableMap.getPosition(0, 4)))
        assert(not ('5' in availableMap.getPosition(2, 4)))
        
        assert(htmlBoard.write(self.OUT_PATH + 'locked_candidates1_row_after.html', 
                               forceOverwrite=True))
        
    def testFindLockedCandidates1_Column(self):
        board = Board()
        board.boardFromString(
                simpleSudokuClipboardToString(self.LOCKED_CANDIDATES1_2))
        solver = ModerateSolver(board)
        availableMap = solver.getAvailableMap()
        
        # Check before the locked candidates have been found
        assert('2' in availableMap.getPosition(5, 6))
        assert('2' in availableMap.getPosition(5, 7))
        assert('5' in availableMap.getPosition(4, 0))
        assert('5' in availableMap.getPosition(4, 2))
        
        htmlBoard = HTMLBoard(solver.getBoard(), solver.getAvailableMap())
        assert(htmlBoard.write(self.OUT_PATH + 'locked_candidates1_column_before.html', 
                               forceOverwrite=True))
        
        solver.assignLockedCandidates1()
        
        # Make sure the excluded values are no longer returned
        assert(not ('2' in availableMap.getPosition(5, 6)))
        assert(not ('2' in availableMap.getPosition(5, 7)))
        assert(not ('5' in availableMap.getPosition(4, 0)))
        assert(not ('5' in availableMap.getPosition(4, 2)))
        
        assert(htmlBoard.write(self.OUT_PATH + 'locked_candidates1_column_after.html', 
                               forceOverwrite=True))
                       
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()