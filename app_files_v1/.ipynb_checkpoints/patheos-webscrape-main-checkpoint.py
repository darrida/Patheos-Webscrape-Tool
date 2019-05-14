# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:hydrogen
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.2'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from bs4 import BeautifulSoup as BS
import pandas as pd
import csv
import requests
import time
import re
import numpy as np
import openpyxl
from urllib.request import urlopen, URLError
from tqdm import tqdm
import colorama
import parse_tns as tns
from sqlalchemy import types, create_engine
from pandas.io.sql import SQLTable
import cx_Oracle
import sys
import webscrape_sql_insert_patheos as pinsert
import webscrape_pd_scrape_patheos as pscrape
import webscrape_compare_current_patheos as pcompare
import webscrape_process_results_main as pprocess

# %%
url = 'http://www.patheos.com/blogs'
response = requests.get(url)

# %%
soup = BS(response.content, 'html.parser')
#soup.prettify

# %%
blog_dict = {}
url_list1 = []

while True:

    for blog in soup.find_all('div', attrs={"class":"col-sm-6"})[0:20]:
        blogurl = blog.find('a')
        blog_dict[blog.text] = blogurl['href']
    i = 0    
    for urls in tqdm(blog_dict.values(), desc='Fetch Blogs from Categories'):
#        print(urls)
        if urls and (i < 2):
            sub_blog = requests.get(urls)
            soup1 = BS(sub_blog.content, 'html.parser')
            soup1.prettify
            for a in soup1.find_all('a', href=True):
                url_list1.append(a['href'])
            #print("FINISHED " + urls)
            i = i + 1
        else:
            continue
    else:
        break

# %%
print("'Strip items that start with /, #, www.'")
unique_blogs = list(set(url_list1))
prefixes = ('/','#','www.')
i = 0
for word in unique_blogs:
    if word.startswith(prefixes):
        unique_blogs.remove(word)
#unique_blogs

# %%
len(unique_blogs)

# %%
print("Remove non-Blog Title URLS.")
prefixes2 = ('http://www.patheos.com/blogs/')
for word2 in unique_blogs:
    if not word2.startswith(prefixes2):
        unique_blogs.remove(word2)
#unique_blogs
print("Done.")

# %%
len(unique_blogs)

# %%
# This uses .split() to designate the "/" as the marker between sections, 
# which grabs the text after section 4, but does not include section 5.
print("Fetch just blogs names.")
final_bname = []
url_prefix = 'http://www.patheos.com/blogs/'
for url_blog in unique_blogs:
    url_bname = url_blog.split("/",5)[4:5]
    for words in url_bname:
        final_bname.append(words)     
#final_bname
print("Done.")

# %%
print("Append blog name to 'http://www.patheos.com/blogs/'")
final_url = [url_prefix + x for x in final_bname]
#final_url
print("Done.")

# %%
len(final_url)

# %%
print("Strip out duplicates.")
final_url_dedupe = list(set(final_url))
len(final_url_dedupe)


# %%
final_url_dedupe

# %%
subblog_list = []

while True:
    i = 0    
    for blog_urls in tqdm(final_url_dedupe, desc='Fetch Post URLs from Blogs (pass 1)'):
#        print(blog_urls)
        if blog_urls: # and (i < 10):
        #if blog_urls:
            subsub_blog = requests.get(blog_urls)
            soup2 = BS(subsub_blog.content, 'html.parser')
            #print(soup2.prettify)
            for a in soup2.find_all('a', href=True):
                subblog_list.append(a['href'])
            #print("FINISHED " + blog_urls)  
            i = i + 1
        else:
            continue
    else:
        break

# %%
print("Remove duplicate blog post urls.")
unique_subblog_list = list(set(subblog_list))
#unique_subblog_list

# %%
len(unique_subblog_list)
#unique_subblog_list

# %%
year = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
final_real_post = []

url_real_prefix = 'https://www.patheos.com/blogs/'

for post_url in tqdm(unique_subblog_list):
    #print(post_url)
    for blog_name in final_bname:
        test_url = url_real_prefix + blog_name
        #i = 2010
        #while (i < 2020):
        for y in year:
            if post_url.startswith(test_url + "/" + str(y)):
                final_real_post.append(post_url)
            #i = i + 1
#final_real_post

# %%
len(final_real_post)

# %%
individual_posts = list(set(final_real_post))
len(individual_posts)

comments1 = "#disqus_thread"

list_without_disqus = []

for word3 in individual_posts:
    if not word3.endswith(comments1):
        #individual_posts.remove(word3)
        list_without_disqus.append(word3)

# %%
#len(individual_posts)
len(list_without_disqus)

# %%
list_posts_only = []

for word4 in list_without_disqus:
    count_list = word4.rsplit("/")
    count = len(count_list)
    if (count > 8):
        list_posts_only.append(word4)

# %%
len(list_posts_only)

# %%
df_scraped_urls = pd.DataFrame(list_posts_only)
#df_new_urls.to_csv('patheos_posts.csv')

# %%
df_scraped_urls


# %%
def main():
    tnsnames_path = ""
    server = "PATHEOSDBAPEX"
    #df_scraped_urls = pd.DataFrame
    environment = tns.parse_tnsnames(tnsnames_path, server)
    print(environment)
    database_user = "no_input" #input("Xnumber or Banner Username: ")
    database_user = database_user.upper()
    #banner_database = environment_select(input("Banner database: "))
    #environment_user = ("Data base user: ")
    environment_user = 'system'
    environment_password = 'oracle' #getpass.getpass(environment_user + " Password: ")
    temp_list = pprocess.process_results(pcompare.access_compare_query(environment_user, environment_password, database_user, environment, df_scraped_urls))
    temp_df = pscrape.full_scrape(temp_list, "yes")
    pprocess.process_results(pinsert.access_insert_execute(environment_user, environment_password, database_user, environment, temp_df))
    
    return temp_df

main()
#df_test = main()

#df_test

# %%
df_results.to_excel('patheos_posts_content.xlsx')
df_results.to_csv('patheos_posts_content.csv')

# %%
for i in invalid urls:
    print(i)
