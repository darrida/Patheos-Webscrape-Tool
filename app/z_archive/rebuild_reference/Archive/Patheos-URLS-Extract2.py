
# coding: utf-8

# In[425]:


import requests


# In[426]:


url = 'http://www.patheos.com/blogs'


# In[427]:


response = requests.get(url)


# In[428]:


response.status_code


# In[429]:


response.headers


# In[430]:


response.content


# In[431]:


from bs4 import BeautifulSoup as BS


# In[432]:


soup = BS(response.content, 'html.parser')


# In[433]:


soup.prettify


# In[439]:


for blog in soup.find_all('div', attrs={"class":"col-sm-6"})[0:20]:
    blogname = blog.find('div', attrs={'class':'title'})
    blogurl = blog.find('a')
    
    print(blogurl.get('href'))



# In[435]:


blog_dict = {}


# In[442]:


for blog in soup.find_all('a'):
    blog_dict[blog.text] = blog['href']


# In[444]:


blog_dict

