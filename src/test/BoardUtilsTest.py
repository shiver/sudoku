'''
Created on 24/02/2010

@author: Rob
'''

from board.board import Board
from board.boardutils import * 

import unittest

class Test(unittest.TestCase):
    
    def setUp(self):
        self.SIMPLE_SUDOKU = """\n*-----------*\n|...|...|...|\n|...|...|...|\n|...|...|...|\n|---+---+---|\n|...|.8.|..5|\n|.2.|...|...|\n|...|463|...|\n|---+---+---|\n|...|...|...|\n|...|...|...|\n|...|...|...|\n*-----------*"""
        self.SUDOKU_STRING = """...............................8...5.2..........463.............................."""

    def tearDown(self):
        pass
    
    def testSimpleSudokuClipboardToString(self):            
        board = Board()
        result = simpleSudokuClipboardToString(self.SIMPLE_SUDOKU)
        assert(self.SUDOKU_STRING == result)
        
    def testBoardToSimpleSudokuClipboard(self):
        board = Board()
        board.boardFromString(self.SUDOKU_STRING)
        result = boardToSimpleSudokuClipboard(board)
        assert(self.SIMPLE_SUDOKU == result)
        
    