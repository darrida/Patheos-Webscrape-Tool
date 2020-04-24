# STANDARD
from pprint import pprint

# PyPI
import click
#from bs4 import BeautifulSoup as BS
import requests
#from tqdm import tqdm

# LOCAL
from interface_db import db_interface_sqlite as data
from interface_website import website_tools as tools
from interface_website import website_patheos as patheos





def main():
    #try:
    with data.database() as db:
        website_ids = db.query_table_ids_all('websites')#, last_date_ascending=True)
        #print(website_ids)
        for i in website_ids:
            website = db.query_websites(website_id=i)
            #print(website)
            if website.name == 'Patheos Blogs':
                print(website.name)
                #patheos.fetch_and_insert_categories(website_id=website.id)
                patheos.scrape_patheos(website.id)
            else:
                pass
    #except Exception:


def placeholder1():
    with data.database() as db:
        db.create_tables()
        db.insert_update_site_pages(0, 149)
        result = db.execute(f"SELECT number FROM site_pages WHERE site_id = 47")
        #print(result[0][0])
        for i in result:
            results = patheos.fetch_and_insert_blogs(i[0])
            print(f'Inserted: {results.inserted} | Not Inserted: {results.not_inserted} | Errors: {results.exceptions}')


def placeholder2():
    patheos.insert_website('Patheos Blogs', 'https://patheos.com/blogs')
    results = patheos.fetch_and_insert_categories('Patheos Blogs', 1)
    with data.database() as db:
        result = db.execute("SELECT name FROM categories")
        for i in result:
            results = patheos.fetch_and_insert_blogs(i[0])
            print(f'Inserted: {results.inserted} | Not Inserted: {results.not_inserted} | Errors: {results.exceptions}')