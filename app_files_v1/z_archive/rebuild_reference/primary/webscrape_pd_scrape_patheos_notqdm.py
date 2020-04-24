from bs4 import BeautifulSoup as BS
import pandas as pd
from tqdm import tqdm
from urllib.request import urlopen, URLError
import requests

def full_scrape(input_list, unicode_escape_yes_no):
    invalid_urls = []

    patheos_posts = input_list #list_posts_only
    df_results = pd.DataFrame(columns=('posts_title','posts_date','posts_author','posts_content','posts_url','blogs_name','blogs_url','beliefs_name','beliefs_url'))

    def validate_web_url(url_test):
        try:
            #print(url_test)
            urlopen(url_test)
            return True
        except URLError:
            return False

    total = 0
    for url in input_list:   
        #print(url)
        url_str = url #[0]
        #print(url)
        #print(url_str)
        if validate_web_url(url_str) == True:
            #print("- VALID")
            response = requests.get(url_str)
            soup = BS(response.content, 'html.parser')
            #indiv_post = []
            g_name = url_str.split("/", 5)[4:5]
            for entry in g_name:
                g_blog_name = entry
                g_blog_url = "https://www.patheos.com/blogs/" + entry
            #url_bname = url_blog.split("/",5)[4:5]
            g_title = soup.find("h1", {"class" : "entry-title"})
            for g_basic in soup.find_all("div", {"class": "main-post"}):
                g_author = g_basic.find("span", {"itemprop": "author"})
                g_date = g_basic.find("span", {"itemprop": "datePublished dateModified"})
            g_content = soup.find("div", {"class": "story-block"})
            for g_category_info in soup.find_all("div", {"class": "btn btn-xs btn-prime-3 channel-breadcrumb"}):
                #print(g_category_info)
                g_category = g_category_info.find("a") # , {"class": "over-dark"})
                g_category_url = "https:" + g_category["href"]
                g_category_name = g_category.text
            if g_title and g_author and g_date and g_content and g_category_name and g_category_url is not None:
                df_temp = pd.DataFrame([
                                    [g_title.text,     # post title
                                     g_date.text,      # post date
                                     g_author.text,    # post author
                                     g_content.text,   # post content
                                     url_str,              # post url
                                     g_blog_name,      # blog name
                                     g_blog_url,       # blog url
                                     g_category_name,  # category name
                                     g_category_url]], # category url
                                   columns=('posts_title','posts_date','posts_author','posts_content','posts_url','blogs_name','blogs_url','beliefs_name','beliefs_url')
                                )
                df_results = df_results.append(df_temp, ignore_index=True)
                #print("- APPENDED")
            else: 
                #"- NOT APPENDED"
                invalid_urls.append(url)
    if unicode_escape_yes_no == "yes":
        df_results = df_results.applymap(lambda x: x.encode('unicode_escape').
                 decode('utf-8') if isinstance(x, str) else x)

    return df_results


# Notes about the unicode_escape:
# - It will turn single quotes and double quotes into character codes in the excel text
# - Characters found so far:
#   - \u2019: single quotation mark
#   - \u201c and u\201d: left and right double quotation marks