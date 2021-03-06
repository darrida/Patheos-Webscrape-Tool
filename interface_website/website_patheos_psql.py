# Standard
import sys
import math
import time
import datetime

# PyPI
from bs4 import BeautifulSoup as BS
import requests
import psycopg2
import peewee

# LOCAL
#from interface_db import db_interface_postgres as data
from interface_website import website_tools as tools
from interface_db import orm_peewee_classes as data


# Global Variables
results = tools.insert_results()


def scrape_patheos(website: data.website, print_progress: bool):    
    categories = data.category.select().where(data.category.website_id==website.id).order_by(data.category.last_date)
    for category in categories:
        print(category.name)
        blogs = data.blog.select().where(data.blog.category_id==category.id).order_by(data.blog.last_date)
        blog_out_of_category = 1
        for blog in blogs:
            scrape_blog_initialize(blog, blog_out_of_category, print_progress)
            blog_out_of_category +=1
        nrows = (data.category
                 .update(last_date=datetime.datetime.utcnow(),
                         last_user='user')
                 .where(data.category.id==category.id).execute())
        if nrows < 1:
            print(f'\n{blog.name}, {blog.id}, date not updated.')
        #query.execute()


def scrape_blog_initialize(blog: data.blog, blog_out_of_category: int, print_progress: bool):
    total_blogs = len(data.blog.select().where(data.blog.category_id==blog.category_id))

    total_pages = number_of_blog_pages(blog)
    resume_page = find_page_resume_scrape(blog.id)
    page_number = resume_page

    total = 0
    continue_on = True
    while continue_on == True:
        base_url = blog.url + '/page/' + str(page_number)
        results_l = scrape_posts_on_page(base_url)
        if results_l != 404:
            for i in results_l:
                try:
                    post = data.post(url=i, blog_id=blog.id)
                    try:
                        post = scrape_post(post, 'no')
                        if post.title == None:
                            print('no title')
                        post.save()
                        results.inserted += 1
                    except peewee.IntegrityError as e:
                        # <logging placeholder>
                        results.not_inserted += 1
                    except peewee.InternalError as e:
                        print(f'INTERNALERROR: {e}')
                        results.exceptions += 1
                    total += 1
                    if print_progress:
                        sys.stdout.write('\r' + 'BLOG: (' + str(blog_out_of_category) + '/' + str(total_blogs) + ') '  + blog.name 
                                          + ' | PAGE: ' + str(page_number) + '/' + str(total_pages) 
                                          + ' | TOTAL PROCESSED: ' + str(total) 
                                          + ' | INSERTED: ' + str(results.inserted)
                                          + ' | NOT INSERTED: ' + str(results.not_inserted)
                                          + ' | ERROR: ' + str(results.exceptions))
                except peewee.IntegrityError as e:
                    print(f'\nINTEGRITYERROR: {e}\n{i}')
                    url_error = data.url_error_list(url=i, url_type='post', parent_id=blog.id, exception=f'peewee.IntegrityError: {e}')
                    nrow = url_error.save()
                    results.exceptions += 1
                    if nrow > 0:
                        print('Status: Logged')
                except AttributeError as e:
                    print(f'\nATTRIBUTEERROR: {e}\n{i}')
                    url_error = data.url_error_list(url=i, url_type='post', parent_id=blog.id, exception=f'AttributeError: {e}')
                    nrow = url_error.save()
                    results.exceptions += 1
                    if nrow > 0:
                        print('Status: Logged')
        else:
            continue_on = False
        page_number += 1
        if print_progress:
            sys.stdout.write('\r' + 'BLOG: (' + str(blog_out_of_category) + '/' + str(total_blogs) + ') '  + blog.name 
                              + ' | PAGE: ' + str(page_number) + '/' + str(total_pages) 
                              + ' | TOTAL PROCESSED: ' + str(total) 
                              + ' | INSERTED: ' + str(results.inserted)
                              + ' | NOT INSERTED: ' + str(results.not_inserted)
                              + ' | ERROR: ' + str(results.exceptions))
    nrows = (data.blog
            .update(last_date=datetime.datetime.utcnow(),
                    last_user='user')
            .where(data.blog.id==blog.id).execute())
    if nrows < 1:
        print(f'\n{blog.name}, {blog.id}, last_date not updated')


def insert_website(website_name: str, website_url: str) -> data.website:
    website = data.website(name = website_name, url = website_url)
    print(f'Inserting {website_name} - {website_url}')
    result = website.save()
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


def fetch_and_insert_categories(website: data.website) -> tools.insert_results:
    results = tools.insert_results()
    print(f'Pulling categories for {website.name}')
    parsed_html = tools.parse_html(website.url)
    for item in parsed_html.find_all('div', attrs={"class":"related-content clearfix related-content-sm decorated channel-list"}):
        category = data.category()
        category.url = item.find('a')['href']
        category.name = category.url.rsplit("/")[3]
        category.context = 'na'
        category.website_id = int(website.id)
        try:
            category.save()
            results.inserted += 1
        except peewee.IntegrityError as e:    # Related to unique constraint preventing insertion. Desired result | Skipped
            # <logging placeholder>
            results.not_inserted += 1
        except peewee.InternalError as e:
            # <logging placeholder>
            print(f'INTERNALERROR: {e}')
            results.exceptions += 1
        category = None
    return results


def fetch_and_insert_blogs(category: data.category) -> tools.insert_results:
    #try:
    results = tools.insert_results()
    parsed_html = tools.parse_html(category.url)
    for item in parsed_html.find_all('div', attrs={"class":"author-info"}):
        blog=data.blog()
        for title_html in item.find_all('div', attrs={"class":"title"}):
            title_html_a = title_html.find('a')
            blog.name = title_html_a.get_text()
            blog.url = title_html_a['href']
        for by_line_html in item.find_all('div', attrs={"class":"by-line"}):
            blog.author = by_line_html.find('a').get_text()
        blog.category_id = category.id
        try:
            blog.save()
            results.inserted += 1
        except peewee.IntegrityError as e:    # Related to unique constraint preventing insertion. Desired result | Skipped
            # <logging placeholder>
            results.not_inserted += 1
        except peewee.InternalError as e:
            # <logging placeholder>
            print(f'INTERNALERROR: {e}')
            results.exceptions += 1
    return results
    # except psycopg2.errors.UniqueViolation as e:
    #     print(f'UNIQUEVIOLATION: {e}')
    # except peewee.IntegrityError as e:
    #     print(f'INTEGRITYERROR: {e}')


def number_of_blog_pages(blog) -> int:
    base_page_url = blog.url + '/page/'
    try:
        results = (data.blog_count_pages.select().where(data.blog_count_pages.blog_id==blog.id).namedtuples())
        for result in results:
            valid_page = result.number
        print(f'Previous page count: {valid_page}')
        #page = data.blog_count_pages(number=valid_page, blog_id=blog.id)
    except Exception as e:   # no record for this blog exists yet
        if str(e).startswith('<Model: blog_count_pages> instance matching query does not exist') or \
           str(e).startswith("local variable 'valid_page' referenced before assignment"):
            valid_page = 1
            print(f'\nFirst page number count, starting with {valid_page}')
            page = data.blog_count_pages(number=valid_page, blog_id=blog.id)
        else:
            print(f'EXCPETION: {e}')
            exit()
    #original_number = valid_page
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
        if 'page' in locals():
            page.number = valid_page # = data.blog_count_pages(valid_page, 149)
            page.save()
        else:
            nrows = (data.blog_count_pages
                    .update(number=valid_page)
                    .where(data.blog_count_pages.blog_id == blog.id)
                    .execute())
            if nrows < 1:
                print(f'Page count failed to update: blog id {blog.id}')
        sys.stdout.write('\r' 'PAGES: ' + str(valid_page))
    return valid_page


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
    response = requests.get(post.url)
    #try:
    if response.status_code != 404:
        parsed_html = BS(response.content, 'html.parser')
        post.title = parsed_html.find("h1", {"class" : "entry-title"}).text
        for g_basic in parsed_html.find_all("div", {"class": "main-post"}):
            # try:
            post.author = g_basic.find("span", {"itemprop": "author"}).text
            # except AttributeError as e:
            #     if str(e) == "'NoneType' object has no attribute 'text'":
            #         post.author = 'MISSING'
            post.date = g_basic.find("span", {"itemprop": "datePublished dateModified"}).text
        post.content = parsed_html.find("div", {"class": "story-block"}).text
        post.content_html = ''
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
    # except AttributeError as e:
    #     print(f'\nATTRIBUTEERROR: {e}\n{post.url}')
    #     url_error = data.url_error_list(url=post.url, url_type='post', parent_id=post.blog_id, exception=f'AttributeError: {e}')
    #     nrow = url_error.save()
    #     if nrow > 0:
    #         print('Status: Logged')
    #     return None


def find_page_resume_scrape(blog_id):
    posts_in_blog = data.post.select().where(data.post.blog_id==blog_id)
    number_of_posts = len(posts_in_blog)
    number_of_pages = math.floor(number_of_posts / 10)
    return number_of_pages
