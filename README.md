# **link_tracking**

A simple Python script tool and package that uses web crawling concepts to find links and pages around the internet ans SQLite databases to store found data.

## **Using**

You can clone this Git repository and add it to your project to use **link_tracking** [as a package](#as-a-package) or to use the [`tracker.py`](#tracker-script) script.

```sh
$ git clone https://github.com/Niaev/link_tracking.git
```

**This package is not available at Python Package Index already.**

### **`tracker` script**

This script can be found in the root of this repository. The simple how to use:

```sh
$ python3 tracker.py SEEDS_FILE [depth]
```

* `SEEDS_FILE` - a file path, referring to a text file with a list of internet links. Example:

```
http://link-one.com/
https://link.org/two
...
```

* `DEPTH` - is an optional integer number (default is **2**), defining the link tracking depth - that is how many times it will enter in a child page link and search the link in there in a recursive way

The script will track links using your seeds and scrape its respective pages, then store in a SQLite database `data/pages.db`.

### **as a package**

It has two modules: `crawler` and `indexer`.

`crawler` has some functions and the `Crawler` class, responsible for web crawling.

```
Class that receives an url and use urllib and bs4 to get page 
information and with functions to track and scrape links
```

`indexer` has just the `Indexer` class, responsible for handling, organizing and storing the collected data;

```
Class that receives a list of links to organize and index
```

The code is well documented with docstrings and comments. A more deep documentation can be found in this repository wiki - **not yet available**.