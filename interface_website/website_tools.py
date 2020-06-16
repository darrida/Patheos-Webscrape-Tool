# PyPI
from bs4 import BeautifulSoup as BS
import requests

# LOCAL
#from interface_db import db_interface_sqlite as data
from interface_db import orm_peewee_classes as data



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