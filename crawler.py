# imports
## crawling
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup, Comment
## others
import re

def scrape_list(links):
    """
        Scrape a list of links to get page content, description and title, then return a list of dictionaries
        with this elements
    """
    ld = []

    for l in links:
        try:
            c = Crawler(l)
            ld.append(c.scrape())
        except ValueError:
            pass
        except HTTPError:
            pass

    return ld


class Crawler():
    """
        Class that receives an url and use urllib and bs4 to get page information and with
        functions to track and scrape links
    """

    def __init__(self, url):
        """
            Set class attributes
        """
        self.url = url
        self.http = url.split('//')[0]

        try:
            self.html = urlopen(self.url)
        except ValueError: raise ValueError('Invalid URL')
        except HTTPError as e: raise e
        except URLError: raise URLError('Server unavailabe or incorrect domain name')
        else:
            self.r = BeautifulSoup(self.html.read(), 'html5lib')

    def track(self, include_self=False):
        """
            Crawl through the page source to find all valid links
        """
        a_tags = self.r.findAll('a')

        p = r'href="([\w\.\/#-:;?=~]*)"'
        links = []
        if include_self: links.append(self.url)
        for a in a_tags:
            s = re.search(p,str(a))
            if s:
                s = s.group(1)
                m = re.match(r'[#/]',s)
                if re.match(r'[#]',s):
                    links.append(f"{self.url}{s}")
                elif re.match(r'//',s):
                    links.append(f"{self.http}{s}")
                elif re.match(r'/',s):
                    links.append(f"{self.http[0:-1]}{s}")
                elif re.match(r'https{0,1}://',s):
                    links.append(s)

        self.links = links

    def scrape(self):
        """
            Scrape page content, description and title, then return a dictionary with this scraped elements
        """
        d = {
                'url': self.url,
                'title': self.r.title.string if hasattr(self.r.title, 'string') else self.url,
                'description': '',
                'content' : ''
        }

        try:
            description = self.r.find('meta',attras={'name':'description'})['content']
        except TypeError: pass
        else: d['description'] = description

        body = self.r.find('body')
        for script in body.findAll('script'):
            script.decompose()
        for noscript in body.findAll('noscript'):
            noscript.decompose()
        for element in body(text=lambda text: isinstance(text, Comment)):
            element.extract()

        d['content'] = body.text
        return d

    def scrape_links(self, scrap_self=False):
        """
            Scrape self.links to get page content, description and title, then return a list of dictionaries
            with this elements
        """
        ld = []

        if scrap_self:
            ld.append(self.scrape())
        
        if not hasattr(self,'links'):
            return None # Links were not tracked, yet

        sl = scrape_list(self.links)
        
        return ld + sl
