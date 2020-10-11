# general imports
import re

class Indexer():
    '''
        Class that receives a list of links to organize and index

        ### Attributes

        * links
            * `list`
            * list of links
        
    '''

    def __init__(self, links):

        self.links = links