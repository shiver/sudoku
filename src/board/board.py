'''
Created on 30/09/2009

@author: Rob
'''

from boardutils import *

import logging
import random
import math

class InvalidBoard(Exception):
    def __init__(self, board):
        super(InvalidBoard, self).__init__('The board is invalid')

class Board(object):
    DEFAULT_DIMENSIONS = 9
    DEFAULT_VALUES = [str(i) for i in range(1, DEFAULT_DIMENSIONS + 1)]
    EMPTY_VALUE = '.'

    def __init__(self, board=None, dimensions=DEFAULT_DIMENSIONS, availableValues=DEFAULT_VALUES):
        self._logger = logging.getLogger('Board')
        self._dimensions = dimensions
        self._validValues = [str(i) for i in range(1, self._dimensions + 1)]

        if board is None:
            self.clear()
        else:
            self._board = board._getUniqueBoard()
        
    def _getUniqueBoard(self):
        """Returns a unique board which is used for copying the values from an already existing board"""
        newBoard = []
        for i in xrange(self.getDimensions()):
            newBoard.append(list(self._board[i]))
            
        return newBoard
            

    def getBoard(self):
        """Returns the internal board which contains the currently set values"""
        return self._board

    def clear(self):
        """Sets all values on the board to EMPTY_VALUE
        
        EMPTY_VALUE defaults to '.'
        """

        self._board = [[self.EMPTY_VALUE for x in xrange(self._dimensions)] for y in xrange(self._dimensions)]

    def getValidValues(self):
        """Returns a list of values which are valid for the current board"""

        return self._validValues

    def generate(self, availableValues):
        """Generates a new board filled with random values"""

        self.clear()

        for y in xrange(self._dimensions):
            for x in xrange(self._dimensions):
                unused = self.getAvailableValues(self._board, x, y)
                try:
                    self._board[y][x] = random.choice(unused)
                except IndexError:
                    self._logger.debug('Invalid board:')
                    self._logger.debug(boardToString(self._board))
                    raise InvalidBoard(self._board)

    def setPosition(self, x, y, value):
        """Sets the value of the board at the specified position
        
        @param x: The 0 based index of the column
        @param y: The 0 based index of the row
        @param value: The value to set
        """
        self._board[y][x] = value

    def getPosition(self, x, y):
        """Returns the value at the specified position
        
        @param x:
        @param y:
        """
        return self._board[y][x]

    def getDimensions(self):
        """Returns the dimensions of the current board"""
        return self._dimensions

    def getRow(self, y):
        """Returns a list containing the values found at the specified index
        
        @param y: The 0 based index of the row to fetch 
        """

        return self._board[y]

    def setRow(self, y, row):
        """Overwrites the row at the specified index
        
        @param y: The 0 based index of the row to overwrite
        @param row: A list containing the values to set
        """
        self._board[y] = row

    def getColumn(self, x):
        """Returns a list containing the values found at the specified index
        
        @param x: The 0 based index of the column to fetch
        """
        column = []
        for yIndex in xrange(self._dimensions):
            column.append(self._board[yIndex][x])

        return column

    def setColumn(self, x, column):
        """Overwrites the column at the specified index
        
        @param x: The 0 based index of the column to overwrite
        @param column: A list containing the values to set
        """
        for yIndex in xrange(self._dimensions):
            self.__board[yIndex][x] = column[yIndex]

    def getBlock(self, x, y):
        """Returns a list containing the values found in a block
        which the specified location falls in. 
        
        @param x: The 0 based index of a position which falls 
        within the required block
        @param y: The 0 based index of a position which falls
        within the required block
        """
        startX, startY = self.getBlockStart(x, y)

        block = []
        for y in xrange(startY, startY + 3):
            for x in xrange(startX, startX + 3):
                block.append(self._board[y][x])

        return block

    def setBlock(self, x, y, block):
        """Overwrites a block found at the specified location
        
        @param x: the 0 based index of a position which falls
        within the required block
        @param y: the 0 based index of a position which falls
        within the required block
        @param block: a list containing the values with which
        the block will be overwritten
        """
        startX, startY = self.getBlockStart(x, y)

        index = 0
        for y in xrange(startY, startY + 3):
            for x in xrange(startX, startX + 3):
                self._board[y][x] = block[index]
                index += 1

    def getBlockStart(self, x, y):
        """Retrieves a tuple containing starting location
        of a block which contains the supplied position.
        """
        startX = (x / (self._dimensions / 3)) * (self._dimensions / 3)
        startY = (y / (self._dimensions / 3)) * (self._dimensions / 3)

        return startX, startY

    def getAvailableValues(self, x, y):
        """Determines the values that are valid for the specified
        location
        """
        self._logger.debug('(' + str(x) + ', ' + str(y) + ')')

        available = []
        used = []

        row = self.getRow(y)

        self._logger.debug('Row:')
        self._logger.debug(rowToString(row))
        for v in row:
            used.append(v)

        column = self.getColumn(x)
        self._logger.debug('Column:')
        self._logger.debug(columnToString(column))
        for v in column:
            used.append(v)

        block = self.getBlock(x, y)
        self._logger.debug('Block:')
        self._logger.debug(blockToString(block))
        for v in block:
            used.append(v)

        for v in self.getValidValues():
            if not v in used:
                available.append(v)

        self._logger.debug('Available:')
        self._logger.debug(rowToString(available))

        return available

    def boardFromString(self, boardString):
        """Sets the board using the values found in the string"""

        dimensions = math.sqrt(len(boardString))
        if dimensions == int(dimensions):
            dimensions = int(dimensions)
            board = []
            index = 0
            for y in xrange(dimensions):
                row = []
                for x in xrange(dimensions):
                    if not boardString[index] in [0, '.']:
                        row.append(str(boardString[index]))
                    else:
                        row.append(self.EMPTY_VALUE)
                    index += 1
                board.append(row)

            self._board = board
            
