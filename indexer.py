# general imports
import re

# database manipulation imports
import sqlite3

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
            try:
                html = urlopen(link)
            except (ValueError, HTTPError, URLError) as e:
                self.links.pop(i)
    
    def order_scraped_links(self, pages):
        '''
            Orders list of dictionaries pages
        '''
        
        return sorted(pages, key=lambda k: k['title'])

    def store_links(self, dbname, links=None, both=False):
        '''
            Store given links or just `self.links`
        '''

        # copy of links to store
        to_store = self.links.copy()

        # handle given parameters
        if links and both:
            to_store.extend(links)
            self.remove_duplis()
            self.valid_links()
        elif links:
            to_store = links
            self.remove_duplis()
            self.valid_links()

        # database connection
        db = sqlite3.connect(dbname)
        c = db.cursor()

        # checking if connected database has links table
        c.execute('''SELECT name FROM sqlite_master
            WHERE type='table'
            ORDER BY name;''')
        tables = c.fetchall()
        has_links = False
        for table in tables:
            if 'links' in table:
                has_links = True
                break

        # raise exception if it hasn't
        if not has_links:
            raise Exception('Given database don\'t have "links" table')

        # store links if it's all ok
        for link in to_store:
            c.execute(f'''INSERT INTO links
                (link)
                VALUES
                (?);
            ''', (link,))       

        db.commit()
        db.close()

    def store_pages(self, dbname, pages):
        '''
            Store given pages
        '''

        # order pages
        to_store = self.order_scraped_links(pages)

        # database connection
        db = sqlite3.connect(dbname)
        c = db.cursor()

        # checking if connected database has pages table
        c.execute('''SELECT name FROM sqlite_master
            WHERE type='table'
            ORDER BY name;''')
        tables = c.fetchall()
        has_pages = False
        for table in tables:
            if 'pages' in table:
                has_pages = True
                break

        # raise exception if it hasn't
        if not has_pages:
            raise Exception('Given database don\'t have "pages" table')

        # store pages if it's all ok
        for page in to_store:
            c.execute(f'''INSERT INTO pages
                (url, title, description, content)
                VALUES
                (?, ?, ?, ?);
            ''', (page['url'], page['title'], page['description'], page['content']))       

        db.commit()
        db.close()