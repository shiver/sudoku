#!/usr/bin/python
import sys
import random
import math
import pdb

BOARD_DIMENSIONS = 9
# [1,2,3,4,5,6,7,8,9]
VALID_VALUES = range(1, BOARD_DIMENSIONS + 1)
BLANK_BOARD = [[0 for x in xrange(BOARD_DIMENSIONS)] for y in xrange(BOARD_DIMENSIONS)]
HARD_STRING = '1.......2.9.4...5...6...7...5.9.3.......7.......85..4.7.....6...3...9.8...2.....1'
EASY_STRING = '79....3.......69..8...3..76.....5..2..54187..4..7.....61..9...8..23.......9....54'


DEBUG=False

class InvalidBoard(Exception):
    def __init__(self, board):
        super(InvalidBoard, self).__init__('The board is invalid')

def getBlankBoard():
    return [[0 for x in xrange(9)] for y in xrange(9)]
    
def createBoard(availableValues):
    board = getBlankBoard()
    for y in xrange(BOARD_DIMENSIONS):
        for x in xrange(BOARD_DIMENSIONS):
            unused = getAvailableValues(board, x, y)
            try:
                board[y][x] = random.choice(unused)
            except IndexError:
                if DEBUG:
                    print('Invalid board:')
                    displayBoard(board)
                raise InvalidBoard(board)
    return board

def getAvailableValues(board, x, y):
    if DEBUG:
        print('(' + str(x) + ', ' + str(y) + ')')

    available = []
    used = []

    row = getRow(board, y)
    if DEBUG:
        print('Row:')
        displayRow(row)
    for v in row:
        used.append(v)

    column = getColumn(board, x)
    if DEBUG:
        print('Column:')
        displayColumn(column)
    for v in column:
        used.append(v)
        
    block = getBlock(board, x, y)
    if DEBUG:
        print('Block:')
        displayBlock(block)
    for v in block:
        used.append(v)

    for v in VALID_VALUES:
        if not str(v) in used:
            available.append(str(v))

    if DEBUG:
        print('Available:')
        displayRow(available)
    
    return available

def getRow(board, rowIndex):
    return board[rowIndex]

def setRow(board, rowIndex, row):
    board[rowIndex] = row

def getColumn(board, columnIndex):
    column = []
    for rowIndex in xrange(BOARD_DIMENSIONS):
        column.append(board[rowIndex][columnIndex])
        
    return column

def setColumn(board, columnIndex, column):
    for rowIndex in xrange(BOARD_DIMENSIONS):
        board[rowIndex][columnIndex] = column[rowIndex]

    return board

def getBlock(board, rowIndex, columnIndex):
    startRowIndex, startColumnIndex = getBlockStart(board, rowIndex, columnIndex)

    block = []
    for y in xrange(startColumnIndex, startColumnIndex + 3):
        for x in xrange(startRowIndex, startRowIndex + 3):
            block.append(board[y][x])

    return block

def setBlock(board, rowIndex, columnIndex, block):
    startRowIndex, startColumnIndex = getBlockStart(board, rowIndex, columnIndex)

    index = 0
    for y in xrange(startColumnIndex, startColumnIndex + 3):
        for x in xrange(startRowIndex, startRowIndex + 3):
            board[y][x] = block[index]
            index += 1

    return block

def getBlockStart(board, rowIndex, columnIndex):
    startRowIndex = (rowIndex / (BOARD_DIMENSIONS / 3)) * (BOARD_DIMENSIONS / 3)
    startColumnIndex = (columnIndex / (BOARD_DIMENSIONS / 3)) * (BOARD_DIMENSIONS / 3)

    return startRowIndex, startColumnIndex

def stringToBoard(boardString):
    dimension = math.sqrt(len(boardString))
    if dimension == int(dimension):
        dimension = int(dimension)
        board = []
        index = 0
        for y in xrange(dimension):
            row = []
            for x in xrange(dimension):
                if not boardString[index] in [0, '.']:
                    row.append(str(boardString[index]))
                else:
                    row.append(0)
                index += 1
            board.append(row)

        return board

def solveBoard(board):
    unassigned = -1
    while unassigned != 0:
        if unassigned == -1:
            unassigned = 0
            
        availableMap, unassigned = getAvailableMap(board)
        assigned = assignSingles(board, availableMap)
        availableMap, unassigned = getAvailableMap(board)
        eliminateHiddenSinglesRows(board, availableMap)
        assigned += assignSingles(board, availableMap)
        availableMap, unassigned = getAvailableMap(board)

        print(str(assigned) + ' assigned\n')
        if assigned == 0:
            break

    if DEBUG:
        print(availableMap + '\n')

    return board

def getAvailableMap(board):
    dimension = len(board)

    availableMap = []
    unassigned = 0
    for y in xrange(dimension):
        row = []
        for x in xrange(dimension):
            availableValues = []
            if board[y][x] in [0, '.']:
                availableValues = getAvailableValues(board, x, y)
                unassigned += 1
            row.append(availableValues)
        availableMap.append(row)
        
    return availableMap, unassigned


def assignSingles(board, availableMap):
    dimension = len(board)

    assigned = 0
    for y in xrange(dimension):
        for x in xrange(dimension):
            if len(availableMap[y][x]) == 1:
                board[y][x] = availableMap[y][x][0]
                assigned += 1
                # TODO: add DEBUG
                print(availableMap[y][x][0] \
                      + ' set at (' + str(x) \
                      + ', ' + str(y) + ')')

    if DEBUG:
        print(str(assigned) + ' assigned\n')

    return assigned

def eliminateHiddenSinglesRows(board, availableMap):
    dimension = len(availableMap)

    assigned = 0
    for y in xrange(dimension):
        # Row
        row = getRow(availableMap, y)
        combined = []
        for r in row:
            combined.extend(r)

        unique = []
        for v in VALID_VALUES:
            if (combined.count(str(v))) == 1:
                unique.append(str(v))

        for u in unique:
            for i in xrange(dimension):
                if u in row[i]:
                    row[i] = [u]

        setRow(availableMap, y, row)

def eliminateHiddenSinglesColumns(board, availableMap):
    dimension = len(availableMap)

    assigned = 0
    for x in xrange(dimension):
        # Column
        column = getColumn(availableMap, x)
        combined = []
        for c in column:
            combined.extend(c)

        unique = []
        for v in VALID_VALUES:
            if combined.count(v) == 1:
                unique.append(v)

def displayBoard(board):
    for row in board:
        for column in row:
            sys.stdout.write(str(column) + ' ')
        sys.stdout.write('\n')

    sys.stdout.write('\n')

def displayBlock(block):
    for i in xrange(9):
        sys.stdout.write(str(block[i]) + ' ')
        if (i + 1) % 3 == 0:
            sys.stdout.write('\n')

    sys.stdout.write('\n')

def displayRow(row):
    for v in row:
        sys.stdout.write(str(v))
        
    sys.stdout.write('\n\n')

def displayColumn(column):
    for v in column:
        print(str(v))
        
    sys.stdout.write('\n')


def generate():
    failures = 0
    while True:
        try:
            displayBoard(createBoard(VALID_VALUES))
            if DEBUG:
                print(str(failures) + ' failure(s)')
            break
        except InvalidBoard:
            failures += 1
            pass

#generate()
board = stringToBoard(EASY_STRING)
displayBoard(board)
solveBoard(board)
displayBoard(board)
