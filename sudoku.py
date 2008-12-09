from random import *
import pdb
import sys

rows = ['123456789',
        '123456789',
        '123456789',
        '123456789',
        '123456789',
        '123456789',
        '123456789',
        '123456789',
        '123456789']

def get_block(x, y):
    block = ''
    
    s_x = 3
    if x <= 2:
        s_x = 0
    elif x >= 6:
        s_x = 6

    s_y = 3
    if y <= 2:
        s_y = 0
    elif y >= 6:
        s_y = 6

    try :
        for y in xrange(3):
            for x in xrange(3):
                block += rows[y+s_y][x+s_x]
    except:
        return block

    return block

def get_column(x, y):
    column = ''

    try:
        while y > 0:
            y -= 1
            column += rows[y][x]
    except:
        return column

    return column

def get_row(y):
    if len(rows) >= y+1:
        return rows[y]
    else:
        rows.append('')
        return rows[y]

def reset_row(y):
    rows[y] = ''

def append_row(y, num):
    rows[y] += num

def get_possible(a, b, c):
    valid = '123456789'
    p = ''

    for v in valid:
        if (not v in a) and (not v in b) and (not v in c):
            p += v

    #print 'p = ' + p + ' (' + a + ',' + b + ',' + c + ')'
    return p

def generate():
    x = 0
    y = 0
    reset_counter = 0

    while y < 9:
        x = 0
        block = get_block(x, y)
        column = get_column(x, y)
        row = get_row(y)
        
        while x < 9:
            p = get_possible(block, column, row)
            if len(p) == 0:
                #print 'Resetting!'
                reset_row(y)
                x = 0
                if reset_counter > 10:
                    y -= 1
                    reset_row(y)
                    
                row = get_row(y)
                column = get_column(x, y)
                block = get_block(x, y)

                reset_counter += 1
                
                if len(get_possible(block, column, row)) == 0:
                    print 'Failed twice!'
                    # give up and start over
                    rows = []
                    x = 0
                    y = 0
                    break
            else:
                append_row(y, p[randint(0, len(p)-1)])
                x += 1
                row = get_row(y)
                column = get_column(x, y)
                block = get_block(x, y)

        reset_counter = 0
                
        y += 1

def display():
    for y in xrange(0,len(rows)):
        if y in [3,6]:
            print '- ' * 11
        for x in xrange(0, len(rows[y])):
            if x in [3,6]:
                print '|',
            print rows[y][x],
        print ''
            




rows = []
generate()
display()
