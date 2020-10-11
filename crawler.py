# general imports
import re

# web crawling imports
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup, Comment

def scrape_list(links):
    '''
        Scrape a list of links to get page content, description and 
        title, then return a list of dictionaries with this elements
    '''

    # list of page properties dictionaries
    ld = []

    # scrape all valid links
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
    '''
        Class that receives an url and use urllib and bs4 to get page 
        information and with functions to track and scrape links

        ### Attributes

        * url
            * `str`
            * crawler primal url
        * http
            * `str`
            * url HTTP protocol (HTTP or HTTPS)
        * host
            * `str`
            * hostname
        * dir
            * `str`
            * `self.url` without filename
        * html
            * `http.client.HTTPResponse`
            * based in `self.url`
        * r
            * `bs4.BeautifulSoup`
            * uses `self.html` as markup and `html5lib` as parser
        * links
            * `list`
            * all tracked valid links

        ### Methods

        * track:
            * Crawl through the page source to find all valid links
        * scrape:
            * Scrape `self.url` page content, description and title, then 
            return a dictionary with this scraped elements
        * scrape_links:
            * Scrape self.links to get page content, description and 
            title, then return a list of dictionaries with this
            elements
        * track_with_depht:
            * Crawl through the page source to find all valid links
            and crawl to the valid links pages by a given depht
            then return a full list with all this links
    '''

    def __init__(self, url):

        self.url = url
        url_splitted = url.split('//')
        self.dir = '/'.join(self.url.split('/')[:-1]) if '.' in self.url else self.url
        self.http = url_splitted[0]
        self.host = url_splitted[1].split('/')[0]

        try:
            self.html = urlopen(self.url)
        except ValueError: 
            raise ValueError(f'Invalid URL: {self.url}')
        except HTTPError as e: 
            raise e
        except URLError: 
            raise URLError(f'Server unavailabe or incorrect domain name: {self.url}')
        else:
            self.r = BeautifulSoup(self.html.read(), 'html5lib')

    def track(self, include_self=False):
        '''
            Crawl through the page source to find all valid links
        '''

        # tracked links list and adding `self.url` if requested
        links = []
        if include_self: links.append(self.url)

        # get all `<a>` tags on the page source code
        a_tags = self.r.findAll('a')

        # regex href link pattern
        p = r'href="([\w\.\/#-:;?=~]*)"'
        for a in a_tags:
            # search for the pattern in each `<a>`
            s = re.search(p,str(a))
            if s:
                # s is now the link itself
                s = s.group(1)
                # adding just valid links
                if re.match(r'[#]',s):
                    links.append(f'{self.url}{s}')
                elif re.match(r'\./',s):
                    links.append(f'{self.dir}{s[1:]}')
                elif re.match(r'//',s):
                    links.append(f'{self.http}{s}')
                elif re.match(r'/',s):
                    links.append(f'{self.http}//{self.host}{s}')
                elif re.match(r'https{0,1}://',s):
                    links.append(s)

        self.links = links

    def scrape(self):
        '''
            Scrape `self.url` page content, description and title, then 
            return a dictionary with this scraped elements
        '''

        # page properties dictionary
        d = {
                'url': self.url,
                'title': self.r.title.string if hasattr(self.r.title, 'string') else self.url,
                'description': '',
                'content' : ''
        }

        # try to find `<meta>` description tag
        try:
            description = self.r.find('meta',attras={'name':'description'})['content']
        except TypeError: pass  # in case of error, just proceed with empty string
        else: d['description'] = description

        body = self.r.find('body')

        # removing `<script>`, `<noscript>` and comments (purifying page content)
        for script in body.findAll('script'):
            script.decompose()
        for noscript in body.findAll('noscript'):
            noscript.decompose()
        for element in body(text=lambda text: isinstance(text, Comment)):
            element.extract()

        d['content'] = body.text
        return d

    def scrape_links(self, scrap_self=False):
        '''
            Scrape self.links to get page content, description and 
            title, then return a list of dictionaries with this
            elements
        '''

        # list of page properties dictionaries
        ld = []

        # scrape `self` if requested
        if scrap_self: ld.append(self.scrape())
        
        # if `self.links` exist, links were not tracked, yet
        if not hasattr(self,'links'):
            return None

        # scrape all valid links
        sl = scrape_list(self.links)
        return ld + sl

    def track_with_depht(self, depht):
        '''
            Crawl through the page source to find all valid links
            and crawl to the valid links pages by a given depht
            then return a full list with all this links
        '''

        # if `self.links` exist, track
        if not hasattr(self,'links'):
            self.track()

        if depht == 0:
            return self.links

        links = self.links.copy()
        for link in self.links: 
            # for each link, access the page and track 
            c = Crawler(link)
            links.extend(c.track_with_depht(depht-1))

        return links