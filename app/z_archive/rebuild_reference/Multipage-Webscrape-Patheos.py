
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup as BS
import pandas as pd
import csv
import requests
from tqdm import tqdm
from pandas.io.sql import SQLTable
import webscrape_pd_scrape_patheos as pscrape
#import numpy as np
#import cx_Oracle
#import parse_tns as tns
#from sqlalchemy import types, create_engine
#import time
#import sys
#import re
#import openpyxl
#import colorama
#from urllib.request import urlopen, URLError


# In[ ]:


blog = "https://www.patheos.com/blogs/keithgiles/"
page_prefix = "page/"

p = 1
url_list = []
continue_on = True

while continue_on == True:
    blog_page_url = blog + page_prefix + str(p)
    url_test = requests.get(blog_page_url)
    if url_test.status_code != 404:
        url_list.append(blog_page_url)
        print(blog_page_url)
        p = p + 1
        continue_on = True
    else:
        continue_on = False


# In[ ]:


subblog_list = []

while True:
    i = 0    
    for blog_urls in tqdm(url_list, desc='Fetch Post URLs from Blogs (pass 1)'):
        if blog_urls: # and (i < 10):
            subsub_blog = requests.get(blog_urls)
            if subsub_blog != "<Response [404]>":
                soup2 = BS(subsub_blog.content, 'html.parser')
                for blog in soup2.find_all('h2', attrs={"class":"entry-title"}):
                    blog_url1 = blog.find('a')
                    blog_url2 = blog_url1['href']
                    subblog_list.append(blog_url2) 
                i = i + 1
        else:
            continue
    else:
        break

for i in subblog_list:
    print(i)

len(subblog_list)    


# In[ ]:


df = pscrape.full_scrape(subblog_list, "yes")


# In[ ]:


df


# In[ ]:


df.to_excel('patheos_posts_content.xlsx')
df.to_csv('patheos_posts_content.csv')

