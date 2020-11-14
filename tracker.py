# imports
## link_tracking modules
from crawler import Crawler, scrape_list
from indexer import Indexer
## others
import sys
import os

# parameters handling
if len(sys.argv) == 1: 
    print('No parameters were given')
    sys.exit()
elif len(sys.argv) == 2 and sys.argv[1] != 'help!':
    depht = 2
    seeds_file = sys.argv[1]
elif len(sys.argv) == 3:
    depht = int(sys.argv[2])
    seeds_file = sys.argv[1]
elif len(sys.argv) == 2 and sys.argv[1] == 'help!':
    print('''

# about

link_tracking is a web crawling tool that requires a list of seed links to start crawling and find new links and contents, that are cured and indexed

# how to use

it's simple to use. just execute it and then you can give parameters

    $ python3 tracker.py SEEDS_FILE [DEPHT]

SEEDS_FILE is the path of a text file with a few links in it, one link by line
DEPHT is a optional parameter. it is an integer number that defined de depht of the crawling inside each seed link. the default DEPHT is 5

or you can type help! as a parameter to get this message in your terminal

            ''')
    sys.exit()

# reading seeds file
try:
    with open(seeds_file, 'r') as f:
        seeds = f.read().split('\n')[0:-1]
except FileNotFoundError:
    print('seeds file was not found')
    sys.exit()

# links list
l = []

# main crawler instance
crawler = Crawler(seeds[0])

# crawling seeds with given depht
for seed in seeds:
    c = Crawler(seed)
    c.links = c.track_with_depht(depht)
    # update main links list with tracked links
    l.extend(c.links)

# main indexer instance with all tracked links
indexer = Indexer(l)
crawler.links = indexer.links

# get links page content and sort contents
pages = crawler.scrape_links()
pages = indexer.order_scraped_links(pages)

# storing links and pages on sqlite database data/pages.db
indexer.store_links('data/pages.db')
indexer.store_pages('data/pages.db',pages)