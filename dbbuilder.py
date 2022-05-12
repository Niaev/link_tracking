"""Builds SQLite database file"""

# imports
import sqlite3, os

def build(filename):
    os.system('mkdir data')

    # database connection
    db = sqlite3.connect(f'data/{filename}.db')
    c = db.cursor()

    # create links table
    c.execute('''CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY,
            link TEXT
        );''')

    # create pages table
    c.execute('''CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY,
            url TEXT,
            title TEXT,
            description TEXT,
            content TEXT
        );''')

    # show tables
    c.execute('''SELECT name FROM sqlite_master
        WHERE type='table'
        ORDER BY name;''')
    f = c.fetchall()
    print('tables created:')
    for table in f:
        print(f'  - {table[0]}')
    print('')

    # show columns from the crated tables
    c.execute('''PRAGMA table_info(links);''')
    f = c.fetchall()
    print('links')
    for column in f:
        print(f'  - {column[1]}')
    print('')

    c.execute('''PRAGMA table_info(pages);''')
    f = c.fetchall()
    print('pages')
    for column in f:
        print(f'  - {column[1]}')
    print('')

    print('database created')

    db.close()

if __name__ == '__main__':
    build('pages')