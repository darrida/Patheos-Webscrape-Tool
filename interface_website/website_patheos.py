# Standard
import sys
import math
import time
import datetime

# PyPI
from bs4 import BeautifulSoup as BS
import requests

# LOCAL
from interface_db import db_interface_sqlite as data
from interface_db import table_classes as table
from interface_website import website_tools as tools


# Global Variables
results = tools.insert_results()


def scrape_patheos(website_id):    
    #print(website_id)
    with data.database() as db:
        category_ids = db.query_table_ids_all('categories', 'website_id', website_id)#, last_date_ascending=True)
        print(category_ids)
        for i in category_ids:
            with data.database() as db:
                category = db.query_categories(category_id=i)
                print(category.name)
                blog_ids = db.query_table_ids_all('blogs', 'category_id', category.id)#, last_date_ascending=True)
                for i in blog_ids:
                    scrape_blog_initialize(i)
            with data.database() as db:
                db.update_date_category(category)


def scrape_blog_initialize(blog_id):
    with data.database() as db:
        blog = db.query_blogs(blog_id=blog_id)
        total_blogs = db.execute(f"""SELECT COUNT(*) FROM blogs WHERE category_id = {blog.category_id}""")[0][0]
    total_pages = number_of_blog_pages(blog_id=blog.id)
    resume_page = find_page_resume_scrape(blog.id)
    
    page_number = resume_page
    total = 0
    continue_on = True
    while continue_on == True:
        base_url = blog.url + '/page/' + str(page_number)
        #print(base_url)
        results_l = scrape_posts_on_page(base_url)
        if results_l != 404:
            for i in results_l:
                try:
                    post = table.post(i, blog.id)
#                     post = scrape_post(post, 'no')
                    if tools.check_url_new('posts', i) == True:
                        post = scrape_post(post, 'no')
                        if post.title == None:
                            print('no title')
                        with data.database() as db:
                            db.insert_post(post)
                            db.commit()
                            results.inserted += 1
                    else:
                        # <placeholder for logging>
                        results.not_inserted += 1
                    total += 1
                    sys.stdout.write('\r' + 'BLOG: (' + str(blog.id) + '/' + str(total_blogs) + ') '  + blog.name 
                                          + ' | PAGE: ' + str(page_number) + '/' + str(total_pages) 
                                          + ' | TOTAL PROCESSED: ' + str(total) 
                                          + ' | INSERTED: ' + str(results.inserted)
                                          + ' | NOT INSERTED: ' + str(results.not_inserted))
                except AttributeError:
                    with data.database() as db:
                        url_error = table.url_error(i, 'post', blog_id)
                        db.insert_error_url(url_error)
        else:
            continue_on = False
        page_number += 1
        sys.stdout.write('\r' + 'BLOG: (' + str(blog.id) + '/' + str(total_blogs) + ') '  + blog.name 
                              + ' | PAGE: ' + str(page_number) + '/' + str(total_pages) 
                              + ' | TOTAL PROCESSED: ' + str(total) 
                              + ' | INSERTED: ' + str(results.inserted)
                              + ' | NOT INSERTED: ' + str(results.not_inserted))
    with data.database() as db:
        db.update_date_blog(blog)


def insert_website(website_name: str, website_url: str) -> data.website:
    website = table.website(name = website_name, url = website_url)
    #results = tools.insert_results()
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


def fetch_and_insert_categories(website_id: int) -> tools.insert_results:
    category = table.category()
    results = tools.insert_results()
    with data.database() as db:
        website = db.query_websites(website_id=website_id)
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


def fetch_and_insert_blogs(category_name: str) -> tools.insert_results:
    blog = table.blog()
    results = tools.insert_results()
    with data.database() as db:
        category = db.query_categories(category_name)
        #print(f'{category.name}', category.url)
        parsed_html = tools.parse_html(category.url)
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


def number_of_blog_pages(name=None, blog_id=None) -> int:
    with data.database() as db:
        blog = db.query_blogs(name=name, blog_id=blog_id)
        base_page_url = blog.url + '/page/'
        try:
            result = db.execute(f"SELECT number FROM site_pages WHERE site_id = {blog.id}")[0][0]
            valid_page = result if result > 1 else 1
        except IndexError:
            valid_page = 1
        original_number = valid_page
        p = valid_page
        search_increment_list = [1000, 100, 10, 5, 1, 0]
        search_list_index = 0
        while search_increment_list[search_list_index] != 0:                            # Continue processing until the increment number = 0
            try:
                search_increment = search_increment_list[search_list_index]
                url = base_page_url + str(p)
                url_test = requests.get(url)
                if url_test.status_code != 404:                                         # While request.get is successful, continue incrementing
                    valid_page = p
                    p += search_increment
                else:                                                                   # When request.get gets 404 error, move to smaller increment
                    search_list_index += 1
                    p = (p - search_increment) + search_increment_list[search_list_index]
            except IndexError:
                search_increment = 0
            db.insert_update_site_pages(valid_page, blog.id)
            #sys.stdout.write('\r' 'PAGES: ' + str(valid_page))
    return valid_page #- original_number


def scrape_posts_on_page(blog_page_url: str) -> list:
    page_post_urls_l = []
    response = requests.get(blog_page_url)
    if response.status_code != 404:
        parsed_content = BS(response.content, 'html.parser')
        for post_url in parsed_content.find_all('h2', attrs={"class":"entry-title"}):
            post_a = post_url.find('a')
            post_href = post_a['href']
            page_post_urls_l.append(post_href)
    else:
        return 404
    return page_post_urls_l


# def scrape_post(url: str, blog_id: str, unicode_escape_yes_no='no') -> object:  # post class
def scrape_post(post: object, unicode_escape_yes_no='no') -> object:  # post class
    tags = []
    #post = table.post(url=url, blog_id=blog_id)
    response = requests.get(post.url)
    if response.status_code != 404:
        parsed_html = BS(response.content, 'html.parser')
        post.title = parsed_html.find("h1", {"class" : "entry-title"}).text
        for g_basic in parsed_html.find_all("div", {"class": "main-post"}):
            post.author = g_basic.find("span", {"itemprop": "author"}).text
            post.date = g_basic.find("span", {"itemprop": "datePublished dateModified"}).text
        post.content = parsed_html.find("div", {"class": "story-block"}).text
        post.content_html = None
        for items in parsed_html.find_all("ul", {"class": "list-inline related-topics"}):
            for g_tags in items.find_all("li")[0:]:
                if g_tags.find('a'):
                    tag = g_tags.find('a').text
                    tags.append(tag)
        post.tags = tags
        if unicode_escape_yes_no == "yes":
            post.title = post.title.encode('unicode_escape')
            post.content = post.content.encode('utf8')
    return post


def find_page_resume_scrape(blog_id):
    with data.database() as db:
        number_of_posts = db.execute(f'SELECT COUNT(*) FROM posts WHERE blog_id = {blog_id}')[0][0]
        number_of_pages = math.floor(number_of_posts / 10)
    return number_of_pages
