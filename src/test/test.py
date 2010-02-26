'''
Created on 2/10/2009

@author: Rob
'''

def testIt():
    startX = 0
    startY = 0
    for y in xrange(startY, startY + 3):
        for x in xrange(startX, startX + 3):
            print(str(x) + ", " + str(y))
            
testIt()