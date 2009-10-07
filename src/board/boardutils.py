'''
Created on 1/10/2009

@author: shiver
'''

def boardToSimpleSudoku(board):
    """Converts a board to Simple Sudoku format"""

    ss = ''
    for y in xrange(board.getDimensions()):
        for x in xrange(board.getDimensions()):
            if board.getPosition(x, y) in [0, '.']:
                ss += 'X'
            else:
                ss += board.getPosition(x, y)
        ss += '\n'

    ss += '\n'

    return ss

def boardToString(board):
    bstr = ''
    for y in xrange(board.getDimensions()):
        row = board.getRow(y)
        for x in row:
            bstr += str(x) + ' '
        bstr += '\n'

    return bstr

def blockToString(block):
    bstr = ''
    for i in xrange(len(block)):
        bstr += str(block[i]) + ' '
        if (i + 1) % 3 == 0:
            bstr += '\n'

    return bstr

def rowToString(row):
    bstr = ''
    for v in row:
        bstr += str(v)

    return bstr

def columnToString(column):
    bstr = ''
    for v in column:
        bstr += str(v) + '\n'

    return bstr
