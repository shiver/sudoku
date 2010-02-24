'''
Created on 1/10/2009

@author: Rob
'''

def simpleSudokuClipboardToString(boardString):
        """Creates a board from a Simple Sudoku clipboard format."""

        import string
        
        rows = boardString.split('\n')
        if (len(rows[0]) == 0): rows = rows[1:]
        clean_rows = list()
        for i in xrange(len(rows)):
            if not (i % 4 == 0):
                new_row = rows[i].strip()
                new_row = new_row.replace('|', '')
                if (len(new_row) > 0):
                    clean_rows.append(new_row)
        result = string.join(clean_rows, '')
        return result
    
def boardToSimpleSudokuClipboard(board):
    """Converts a board to a Simple Sudoku clipboard format.
    Also useful for a prettier style of display.
    """
    
    out = '\n'
    out += '*-----------*'
    for y in xrange(board.getDimensions()):
        if (y != 0): out += '|' 
        out += '\n'
        if (y != 0 and y % 3 == 0): out += '|---+---+---|\n'
        for x in xrange(board.getDimensions()):
            if (x % 3 == 0): 
                out += '|'
            
            out += board.getPosition(x, y)
        
    out += '|\n*-----------*'   
            
    return out
            

def boardToSimpleSudoku(board):
    """Converts a board to Simple Sudoku file format"""

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
    """Converts a board to a string"""
    
    bstr = ''
    for y in xrange(board.getDimensions()):
        row = board.getRow(y)
        for x in row:
            bstr += str(x) + ' '
        bstr += '\n'

    return bstr

def blockToString(block):
    """Converts a block to a string"""
    
    bstr = ''
    for i in xrange(len(block)):
        bstr += str(block[i]) + ' '
        if (i + 1) % 3 == 0:
            bstr += '\n'

    return bstr

def rowToString(row):
    """Converts a row to a string"""
    bstr = ''
    for v in row:
        bstr += str(v)

    return bstr

def columnToString(column):
    """Converts a column to a string"""
    
    bstr = ''
    for v in column:
        bstr += str(v) + '\n'

    return bstr
