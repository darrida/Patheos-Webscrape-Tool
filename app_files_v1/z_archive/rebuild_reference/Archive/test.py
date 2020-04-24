import requests

pn = 0
page_number = 1
increment = 500
return_str = page_number
continue_on = True
if page_number < 1:
    pn = increment
else:
    pn = page_number + increment
# print("page number: " + str(pn))
while continue_on:
    blog_page_url = 'https://www.patheos.com/blogs/comingoutchristian' + "/page/" + str(pn)
# print(blog_page_url)
    # print("\n" + blog_page_url)
    try:
        url_test = requests.head('https://www.patheos.com/blogs/comingoutchristian', timeout=5)  # , allow_redirects=True)
        if url_test.status_code != 404:
            return_str = pn
            pn = pn + increment
        else:
            print(url_test.status_code)
            continue_on = False
    except:
        return_str = -1