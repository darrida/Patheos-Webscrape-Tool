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
    df_scraped_urls = 
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
