'''
Created on 25/02/2010

@author: Rob
'''

from Board import Board
from AvailableMap import AvailableMap

from types import ListType
from string import Template
import os

class HTMLBoard(Board):
    """The HTMLBoard class' main goal is to provide assistance during debugging.
    Being able to see a visual representation of the combined Board and 
    AvailableMap makes it far easier to test new functionality and fix bugs.
    """
    
    def __init__(self, board, availableMap=None):
        super(HTMLBoard, self).__init__(board)
        if availableMap is None:
            self._availableMap = AvailableMap(board)
        else:
            self._availableMap = availableMap
        
    def _createCell(self, value):
        """Creates and returns an HTML element using the supplied values.
        
        value - Can be either a list() or a single string value.
        """
        
        cellString = """<div class="cell">"""
        replacement = dict(x1='', x2='', x3='', x4='', x5='', x6='', x7='',
                           x8='', x9='')
        
        if isinstance(value, ListType):
            # A list of values indicates we are dealing with an AvailableMap
            
            if len(value) <= 4:
                # With only 4 values or less, we place values at each of the 
                # four corners, starting with the top left.
                # 
                # E.g:
                # 1.2
                # ...
                # 3.4
                
                cellString += """<div class="insidecell">
                                    <span>$x1</span>
                                    <span>&nbsp;</span>
                                    <span>$x2</span>
                                </div>
                                <div class="insidecell">
                                &nbsp;
                                </div>
                                <div class="insidecell">
                                    <span>$x3</span>
                                    <span>&nbsp;</span>
                                    <span>$x4</span>
                                </div>"""                     
            elif len(value) <= 6:
                # With 5 or 6 values we place values in two columns of 3.
                #
                # E.g:
                # 1.2
                # 3.4
                # 5.6
                
                cellString += """<div class="insidecell">
                                    <span>$x1</span>
                                    <span>&nbsp;</span>
                                    <span>$x2</span>
                                </div>
                                <div class="insidecell">
                                    <span>$x3</span>
                                    <span>&nbsp;</span>
                                    <span>$x4</span>
                                </div>
                                <div class="insidecell">
                                    <span>$x5</span>
                                    <span>&nbsp;</span>
                                    <span>$x6</span>
                                </div>""" 
            elif len(value) > 6:
                # More than 6 values and we use all available spaces in the cell
                #
                # E.g:
                # 123
                # 456
                # 789
                cellString += """<div class="insidecell">
                                    <span>$x1</span>
                                    <span>$x2</span>
                                    <span>$x3</span>
                                    
                                </div>
                                <div class="insidecell">
                                    <span>$x4</span>
                                    <span>$x5</span>
                                    <span>$x6</span>
                                </div>
                                <div class="insidecell">
                                    <span>$x7</span>
                                    <span>$x8</span>
                                    <span>$x9</span>
                                </div>"""              
            template = Template(cellString)
            for i in xrange(len(value)):
                replacement['x' + str(i + 1)] = value[i]
            cellString = template.substitute(replacement)    
        else:
            # Dealing with a regular Board so each cell only has a single value
            cellString +=   """<div class="insidecell">
                                    <span class="single">""" + value + """</span>
                                </div>"""
        
        cellString += """</div>"""
        return cellString
         
    def getHTML(self, includeAvailableMap=True):
        """Returns a HTML string representation of a combined Board and 
        AvailableMap.
        
        includeAvailableMap - If False, will only generate Board values
        """
         
        htmlString = """<style type="text/css">
                            div.cell {
                                border-style: solid;
                                border-width: 1px;
                                float: left;
                                width: 60px;
                                height: 60px;
                                text-align: center;
                            }
                            
                            div.insidecell {
                            }
                            
                            span.single {
                                font-size: 3em;
                            }
                        </style>"""
                        
        for y in xrange(self.getDimensions()):
            for x in xrange(self.getDimensions()):
                value = self.getPosition(x, y)
                if value is Board.EMPTY_VALUE and includeAvailableMap:
                    value = self._availableMap.getPosition(x, y)
                htmlString += self._createCell(value)
            
            htmlString += """<div style="clear:both"></div>"""
                
        return htmlString
    
    def write(self, filename, includeAvailableMap=True, forceOverwrite=False):
        """Writes an HTML representation of a Board to the specified file.
        
        filename - full path location of the file to be created.
        includeAvailableMap - If False, will only generate Board values.
        forceOverwrite - If the specified file already exists, will attempt to
                        overwrite it.
                        
        Returns True if the file was successfully written.
        """
        
        if os.path.exists(filename) and not forceOverwrite:
            return False
        
        with open(filename, 'w') as file:
            file.write(self.getHTML(includeAvailableMap))
            
        return True
            