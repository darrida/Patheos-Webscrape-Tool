# PyPI
from bs4 import BeautifulSoup as BS
import requests
from tqdm import tqdm

# LOCAL
from interface_db import db_interface_sqlite as data



class insert_results:
    def __init__(self, inserted=0, not_inserted=0, exceptions=0):
        self.inserted = inserted
        self.not_inserted = not_inserted
        self.exceptions = exceptions

        
def parse_html(url: str) -> str:
    """Process and return the parsed html of any webpage.

    Arguments:
        url (str): webpage address to be processed

    Return
        str: [potentially large] string of parsed html

    """
    response = requests.get(url)
    return BS(response.content, 'html.parser')


def check_url_new(table: str, url: str) -> bool:
    """Check a URL against a database table to see if it already exists.
    
    Arguments:
        url (str): webpage page address to check against database table
        table (str): database table to check against

    Return
        bool: True if url exists in given table; False if it doesn't exist.
    
    """
    with data.database() as db:
        existing_url = db.execute(f'SELECT url FROM {table} WHERE url = \'{url}\'')
        if len(existing_url) == 0:
            return True
        else: 
            return False        


# this should probably be deleted, or put in some initialization file
def create_db():
    with data.database() as db:
        db.create_tables()
        websites   = db.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'websites\'')
        categories = db.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'categories\'')
        blogs      = db.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'blogs\'')
        posts      = db.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'posts\'')
    try:
        assert websites[0][0] == 'websites'
    except AssertionError:
        print('ASSERTION ERROR: Error querying \'websites\'')
    try:
        assert categories[0][0] == 'categories'
    except AssertionError:
        print('ASSERTION ERROR: Error querying \'categories\'')
    try:
        assert blogs[0][0] == 'blogs'
    except AssertionError:
        print('ASSERTION ERROR: Error querying \'blogs\'')
    try:
        assert posts[0][0] == 'posts'
    except AssertionError:
        print('ASSERTION ERROR: Error querying \'posts\'')