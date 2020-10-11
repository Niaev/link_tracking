# general imports
import re

# web crawling imports
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

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
        self.remove_duplis()
        self.valid_links()

    def remove_duplis(self):
        '''
            Remove duplicates in `self.links`
        '''
        self.links = list(set(self.links))
    
    def valid_links(self):
        '''
            Maintains only valid links in `self.links` by removing invalid ones
        '''

        for i,link in enumerate(self.links):
            print(i)
            try:
                html = urlopen(link)
            except (ValueError, HTTPError, URLError) as e:
                self.links.pop(i)
    
    def order_scraped_links(self, pages):
        '''
            Orders list of dictionaries pages
        '''
        
        return sorted(pages, key=lambda k: k['title'])