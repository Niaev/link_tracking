"""Crawls through  the web to find links and scrapes webpages"""

# General imports
import re

# Web crawling imports
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup, Comment

def scrape_list(links):
    """Scrape a list of links to get page content

    Arguments:
    links {list} -- Containing links in strings

    Returns:
    {list} -- Containing dicts of pages of the links given
    """

    # List of page properties dictionaries
    ld = []

    # Scrape all valid links
    for l in links:
        try:
            c = Crawler(l)
            ld.append(c.scrape())
        except ValueError:
            pass
        except HTTPError:
            pass

    return ld

class Crawler:
    """Crawl webpages and track valid links

    The Crawler class receives an url and use urllib and bs4 to get 
    page information and with functions to track and scrape links.

    Instance Variables:
    url {str} -- Crawler primal URL
    http {str} -- URL HTTP protocol (HTTP or HTTPS)
    host {str} -- Hostname
    dir {str} -- self.url without the filename
    html {http.client.HTTPResponse} -- Response from access to self.url
    r {bs4.BeautifulSoup} -- Page source code
    links {list} -- All tracked valid links

    Raises:
    UnicodeEncodeError -- In case of encoding issues
    ValueError -- In case of an invalid URL
    HTTPError -- When URL is not accessible
    URLError -- When the domain doesn't exist or the service is 
                unavailable
    """

    def __init__(self, url):
        self.url = url
        url_splitted = url.split('//')
        self.dir = '/'.join(self.url.split('/')[:-1]) if '.' in self.url else self.url
        self.http = url_splitted[0]
        self.host = url_splitted[1].split('/')[0]

        # Fix bug of urllib trying to open links with '##'
        # r'^.*[#]+$'
        if re.match(r'^.*##$',self.url):
            print(self.url)
            self.url = self.url[:-2]

        try:
            self.html = urlopen(self.url)
        except UnicodeEncodeError as e:
            raise e
        except ValueError: 
            raise ValueError(f'Invalid URL: {self.url}')
        except HTTPError as e: 
            print(self.url)
            raise e
        except URLError: 
            raise URLError(f'Server unavailabe or incorrect domain name: {self.url}')
        else:
            self.r = BeautifulSoup(self.html.read(), 'html5lib')

    def track(self, include_self=False):
        """Crawl through the page source to find all valid links

        Arguments:
        include_self {bool} -- Defines if self.url needs to be included
                               in tracked links list - that will be 
                               self.links at the end of the function 
                               (default False)
        """

        # Tracked links list and adding `self.url` if requested
        links = []
        if include_self: links.append(self.url)

        # Get all `<a>` tags on the page source code
        a_tags = self.r.findAll('a')

        # Regex href link pattern
        p = r'href="([\w\.\/#-:;?=~]*)"'
        for a in a_tags:
            # Temporary condition - exclude tor links
            if '.onion' in str(a):
                continue
            
            # Search for the pattern in each `<a>`
            s = re.search(p,str(a))
            if s:
                # s is now the link itself
                s = s.group(1)
                
                # Adding just valid links
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
        """Scrape `self.url` page content

        Returns:
        {dict} -- Page dict, with 'url', 'title', 'description' and 
                  'content' as keys
        """

        # Page properties dictionary
        d = {
                'url': self.url,
                'title': self.r.title.string if hasattr(self.r.title, 'string') else self.url,
                'description': '',
                'content' : ''
        }

        # Try to find `<meta>` description tag
        try:
            description = self.r.find('meta',attras={'name':'description'})['content']
        except TypeError: 
            # In case of error, just proceed with empty string
            pass  
        else: d['description'] = description

        body = self.r.find('body')

        # Removing `<script>`, `<noscript>` and comments
        for script in body.findAll('script'):
            script.decompose()
        for noscript in body.findAll('noscript'):
            noscript.decompose()
        for element in body(text=lambda text: isinstance(text, Comment)):
            element.extract()

        d['content'] = body.text
        return d

    def scrape_links(self, scrap_self=False):
        """Scrape self.links to get page content

        Args:
        scrap_self {bool} -- Defines if self.url needs to be scraped 
                             (default False)

        Returns:
        {list} -- Containing dicts of pages
        """

        # List of page properties dictionaries
        ld = []

        # Scrape `self` if requested
        if scrap_self: ld.append(self.scrape())
        
        # If `self.links` exist, links were not tracked, yet
        if not hasattr(self,'links'):
            return None

        # Scrape all valid links
        sl = scrape_list(self.links)
        return ld + sl

    def track_with_depth(self, depth):
        """Track links, crawling through pages

        Crawl through the page source to find all valid links and crawl
        to the valid links pages by a given depth then return a full 
        list with all this links.

        Arguments:
        depth {int} -- Layers of crawling.

        Returns:
        {list} -- Containing links in strings
        """

        # If `self.links` exist, track
        if not hasattr(self,'links'):
            self.track()

        if depth == 0:
            return self.links

        links = self.links.copy()
        for link in self.links: 
            # For each link, access the page and track 
            try:
                c = Crawler(link)
            except HTTPError as e: 
                # Prevent from stopping the application because of 
                # Unavailable service
                if e.code == 503:
                    continue
            except UnicodeEncodeError: 
                # Prevent from stopping the application because of 
                # Special chars
                print('UNICODE ERROR -- GIVING UP')
                continue
            links.extend(c.track_with_depth(depth-1))

        return links
