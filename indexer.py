"""Organizes lists of links"""

# Database manipulation imports
import sqlite3

# Web crawling imports
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

class Indexer:
    """Class that receives a list of links to organize and index

    Instance Variables:
    links {list} -- Containing links in strings
    """

    def __init__(self, links):
        self.links = links
        self.remove_duplis()
        self.valid_links()

    def remove_duplis(self):
        """Remove duplicates in self.links"""
        self.links = list(set(self.links))
    
    def valid_links(self):
        """Maintains only valid links in self.links"""

        for i,link in enumerate(self.links):
            try:
                html = urlopen(link)
            except (ValueError, HTTPError, URLError) as e:
                self.links.pop(i)
    
    def order_scraped_links(self, pages):
        """Sort list of dictionaries pages by title

        Arguments:
        pages {list} -- Containing dicts of pages

        Returns:
        {list} -- List of pages sorted by title
        """
        
        return sorted(pages, key=lambda k: k['title'])

    def store_links(self, dbname, links=None, both=False):
        """Store given links or just self.links

        Arguments:
        dbname {str} -- Path to SQLite database file
        links {list} -- Containing links in strings (default None)
        both {bool} -- Defines if both self.links and links parameter
                       should be stored (default False)

        Raises:
        Exception -- When the given database doesn't have the "links" 
                     table
        """

        # Copy of links to store
        to_store = self.links.copy()

        # Handle given parameters
        if links and both:
            to_store.extend(links)
            self.remove_duplis()
            self.valid_links()
        elif links:
            to_store = links
            self.remove_duplis()
            self.valid_links()

        # Database connection
        db = sqlite3.connect(dbname)
        c = db.cursor()

        # Checking if connected database has links table
        c.execute('''SELECT name FROM sqlite_master
            WHERE type='table'
            ORDER BY name;''')
        tables = c.fetchall()
        has_links = False
        for table in tables:
            if 'links' in table:
                has_links = True
                break

        # Raise exception if it hasn't
        if not has_links:
            raise Exception('Given database don\'t have "links" table')

        # Store links if it's all ok
        for link in to_store:
            c.execute(f'''INSERT INTO links
                (link)
                VALUES
                (?);
            ''', (link,))       

        db.commit()
        db.close()

    def store_pages(self, dbname, pages):
        """Store given pages

        Arguments:
        dbname {str} -- Path to SQLite database file
        pages {list} -- Containing dicts of pages

        Raises:
        Exception -- When the given database doesn't have the "pages" 
                     table
        """

        # Order pages
        to_store = self.order_scraped_links(pages)

        # Database connection
        db = sqlite3.connect(dbname)
        c = db.cursor()

        # Checking if connected database has pages table
        c.execute('''SELECT name FROM sqlite_master
            WHERE type='table'
            ORDER BY name;''')
        tables = c.fetchall()
        has_pages = False
        for table in tables:
            if 'pages' in table:
                has_pages = True
                break

        # Raise exception if it hasn't
        if not has_pages:
            raise Exception('Given database don\'t have "pages" table')

        # Store pages if it's all ok
        for page in to_store:
            c.execute(f'''INSERT INTO pages
                (url, title, description, content)
                VALUES
                (?, ?, ?, ?);
            ''', (page['url'], page['title'], page['description'], page['content']))       

        db.commit()
        db.close()