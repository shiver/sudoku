'''
Created on 25/02/2010

@author: Rob
'''
from board.Board import Board
from board.AvailableMap import AvailableMap
from board.HTMLBoard import HTMLBoard

import unittest

class Test(unittest.TestCase):

    def setUp(self):
        self.BOARD = '79....3.......69..8...3..76.....5..2..54187..4..7.....61..9...8..23.......9....54'

    def tearDown(self):
        pass

    def testGetHTMLAvailableMap(self):
        board = Board()
        board.boardFromString(self.BOARD)
        availableMap = AvailableMap(board)
        htmlBoard = HTMLBoard(availableMap)        
        print(htmlBoard.getHTML())
        
    def testGetHTMLBoard(self):
        board = Board()
        board.boardFromString(self.BOARD)
        htmlBoard = HTMLBoard(board)        
        print(htmlBoard.getHTML())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetHTML']
    unittest.main()