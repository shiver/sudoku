'''
Created on 17/02/2010

@author: Rob
'''

from solver.EasySolver import EasySolver
from board.Board import Board

import unittest

class Test(unittest.TestCase):
    def setUp(self):
        self.NAKED_SINGLES = '79....3.......69..8...3..76.....5..2..54187..4..7.....61..9...8..23.......9....54'

    def tearDown(self):
        pass

    def testFindNakedSingles(self):
        board = Board()
        board.boardFromString(self.NAKED_SINGLES)
        easySolver = EasySolver(board)
        singles = easySolver.findNakedSingles()
        
        # Check we found all the expected results
        assert(len(singles) == 4)
        
        # Validate the value of the single found
        assert((0, 8) in singles)
        assert(singles[(0, 8)] == '3')
        assert((0, 7) in singles)
        assert(singles[(0, 7)] == '5')
        assert((4, 3) in singles)
        assert(singles[(4, 3)] == '6')
        assert((6, 6) in singles)
        assert(singles[(6, 6)] == '2')
        
    def testAssignNakedSingles(self):
        board = Board();
        board.boardFromString(self.NAKED_SINGLES)
        
        # Create a copy of the original board
        originalBoard = Board(board)
        
        easySolver = EasySolver(board)
        result = easySolver.assignNakedSingles()
        
        # Make sure all were assigned
        assert(result == 4)
        
        # Make sure that the board now has the naked singles assigned
        assert(board.getPosition(0, 8) == '3')
        assert(board.getPosition(0, 7) == '5')
        assert(board.getPosition(4, 3) == '6')
        assert(board.getPosition(6, 6) == '2')
        
        # Ensure the only changes to the board are the assigned singles
        assert(board != originalBoard)
        for y in xrange(board.getDimensions()):
            for x in xrange(board.getDimensions()):
                # Don't bother checking fields we know have changed
                if not (x, y) in [(0, 8), (0, 7), (4, 3), (6, 6)]:                         
                    assert(board.getPosition(x, y) ==
                       originalBoard.getPosition(x, y))
                    
    def testFindHiddenSingles(self):
        board = Board()
        board.boardFromString(self.NAKED_SINGLES)
        
        easySolver = EasySolver(board)
        singles = easySolver.findHiddenSingles()
        
        # Check we found all the expected results
        assert(len(singles) == 6)
        
        # Validate the value of the single found
        assert((5, 5) in singles)
        assert(singles[(5, 5)] == '3')
        assert((7, 6) in singles)
        assert(singles[(7, 6)] == '3')
        assert((3, 6) in singles)
        assert(singles[(3, 6)] == '5')
        assert((2, 0) in singles)
        assert(singles[(2, 0)] == '6')
        assert((8, 7) in singles)
        assert(singles[(8, 7)] == '7')
        assert((4, 1) in singles)
        assert(singles[(4, 1)] == '7')
        
    def testAssignHiddenSingles(self):
        board = Board();
        board.boardFromString(self.NAKED_SINGLES)
        
        # Create a copy of the original board
        originalBoard = Board(board)
        
        easySolver = EasySolver(board)
        result = easySolver.assignHiddenSingles()
        
        # Make sure all were assigned
        assert(result == 6)
        
        # Make sure that the board now has the singles assigned
        assert(board.getPosition(5, 5) == '3')
        assert(board.getPosition(7, 6) == '3')
        assert(board.getPosition(3, 6) == '5')
        assert(board.getPosition(2, 0) == '6')
        assert(board.getPosition(8, 7) == '7')
        assert(board.getPosition(4, 1) == '7')
        
        # Ensure the only changes to the board are the assigned singles
        assert(board != originalBoard)
        for y in xrange(board.getDimensions()):
            for x in xrange(board.getDimensions()):
                # Don't bother checking fields we know have changed
                if not (x, y) in [(5, 5), (7, 6), (3, 6), (2, 0), (8, 7), (4, 1)]:                         
                    assert(board.getPosition(x, y) ==
                       originalBoard.getPosition(x, y))
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()