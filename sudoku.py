import sys
import random
import pdb

BOARD_DIMENSIONS = 9
# [1,2,3,4,5,6,7,8,9]
VALID_VALUES = range(1, BOARD_DIMENSIONS + 1)
BLANK_BOARD = [[0 for x in xrange(BOARD_DIMENSIONS)] for y in xrange(BOARD_DIMENSIONS)]

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
    available = []

    used = []

    row = getRow(board, y)
    if DEBUG: displayRow(row)
    for v in row:
        used.append(v)

    column = getColumn(board, x)
    if DEBUG: displayColumn(column)
    for v in column:
        used.append(v)
        
    block = getBlock(board, x, y)
    if DEBUG: displayBlock(block)
    for v in block:
        used.append(v)

    for v in VALID_VALUES:
        if not v in used:
            available.append(v)


    if DEBUG:
        print('Available:')
        displayRow(available)
    
    return available

def getRow(board, rowIndex):
    return board[rowIndex]

def getColumn(board, columnIndex):
    column = []
    for row in xrange(BOARD_DIMENSIONS):
        column.append(board[row][columnIndex])
        
    return column

def getBlock(board, rowIndex, columnIndex):
    startRowIndex = (rowIndex / (BOARD_DIMENSIONS / 3)) * (BOARD_DIMENSIONS / 3)
    startColumnIndex = (columnIndex / (BOARD_DIMENSIONS / 3)) * (BOARD_DIMENSIONS / 3)

    block = []
    for y in xrange(startColumnIndex, startColumnIndex + 3):
        for x in xrange(startRowIndex, startRowIndex + 3):
            block.append(board[y][x])

    return block

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
        sys.stdout.write(v)
        
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

generate()