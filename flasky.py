# import flask
from flask import Flask
import pyscrape_copy as pyscrape
from interface_db import orm_peewee_classes as data

# initilize flask
app = Flask(__name__)


# setup the route
@app.route('/')
def index():
    number_websites = len(data.website.select())
    number_categories = len(data.category.select())
    number_blogs = len(data.blog.select())
    number_posts = len(data.post.select())
    number_counted_pages = len(data.blog_count_pages.select())
    number_error_posts = len(data.url_error_list.select())
    #number_posts = data.post.select(fn.MAX(data.post.id))
    return f"""<b>STATS</b>
    <ul style="list-style-type:circle">
        <li>Websites: {number_websites}</li>
        <li>Categories: {number_categories}</li>
        <li>Blogs: {number_blogs}</li>
        <li>Posts: {number_posts}</li>
        <li>Page Counts: {number_counted_pages}</li>
        <li>Errors: {number_error_posts}</li>
    </ul>
    """

# run the server
if __name__ == '__main__':
    app.run(debug=False)