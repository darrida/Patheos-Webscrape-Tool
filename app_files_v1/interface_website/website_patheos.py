# PyPI
from bs4 import BeautifulSoup as BS
import requests
from tqdm import tqdm

# LOCAL
from interface_db import db_interface_sqlite as data
from interface_website import website_tools as tools


def insert_website(website_name: str, website_url: str) -> data.website:
    website = data.website(name = website_name, url = website_url)
    results = tools.insert_results()
    with data.database() as db:
        print(f'Inserting {website_name} - {website_url}')
        result = db.insert_website(website)
        if type(result) == str:
            print(result)
        else:
            print(f'Insert successful. Name: {result.name}, URL: {result.url}')
        #new_website = db.query_websites(website_name)
        #print(f'Inserted or exists: {result.name} - {result.url}')
 #       if check_url_new('categories', category.url) == True:
 #           db.insert_category(category)
 #           results.inserted += 1
 #       else:
 #           # <placeholder for logging>
 #           results.not_inserted += 1
 #   return results

# with data.database() as db:
#     result = db.execute("SELECT * FROM websites")
# pprint(result)


def fetch_and_insert_categories(website_name: str) -> tools.insert_results:
    category = data.category()
    results = tools.insert_results()
    with data.database() as db:
        website = db.query_websites(website_name)
        print(f'Pulling categories for {website.name}')
        parsed_html = tools.parse_html(website.url)
        for item in parsed_html.find_all('div', attrs={"class":"related-content clearfix related-content-sm decorated channel-list"}):
            category.url = item.find('a')['href']
            category.name = category.url.rsplit("/")[3]
            category.website_id = website.id
            if tools.check_url_new('categories', category.url) == True:
                db.insert_category(category)
                results.inserted += 1
            else:
                # <placeholder for logging>
                results.not_inserted += 1
    return results



# results = fetch_and_insert_categories('Patheos Blogs')
# print(results.inserted, 
#       results.not_inserted, 
#       results.exceptions)


# with data.database() as db:
#     result = db.execute("SELECT * FROM categories")
# pprint(result[:2])


def fetch_and_insert_blogs(category_name: str) -> tools.insert_results:
    blog = data.blog()
    results = tools.insert_results()
    with data.database() as db:
        category = db.query_categories(category_name)
        print(category.url)
        print(f'{category.name}', end=' ')
        parsed_html = tools.parse_html(category.url)
        #pprint(parsed_html)
        for item in parsed_html.find_all('div', attrs={"class":"author-info"}):
            for title_html in item.find_all('div', attrs={"class":"title"}):
                title_html_a = title_html.find('a')
                blog.name = title_html_a.get_text()
                blog.url = title_html_a['href']
            for by_line_html in item.find_all('div', attrs={"class":"by-line"}):
                blog.author = by_line_html.find('a').get_text()
            blog.category_id = category.id
            if tools.check_url_new('blogs', blog.url) == True:
                db.insert_blog(blog)
                results.inserted += 1
            else:
                # <placeholder for logging>
                results.not_inserted += 1
    return results




# results = fetch_and_insert_blogs('patheos-partner-blogs')
# print(results.inserted, 
#       results.not_inserted, 
#       results.exceptions)


# with data.database() as db:
#     result = db.execute("SELECT * FROM blogs where name = 'ReImagine'")
#     print(result)