# Standard
import os
import urllib.parse as parse
import datetime

#PyPI
import peewee as pw


#db = pw.SqliteDatabase('my_database.db')
class config_postgres:
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user     = user
        self.password = password
        self.host     = host
        self.port     = port
     

def connect():
    # if 'HEROKU' in os.environ:
    parse.uses_netloc.append('postgres')
    url = parse.urlparse(os.environ['DATABASE_URL'])
    return pw.PostgresqlDatabase(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
        autorollback=True
    )
    # else:
    #     return pw.PostgresqlDatabase(
    #         database='postgres',
    #         user='postgres',
    #         password='postgrest',
    #         host='192.168.86.108',
    #         port='32834',
    #         autorollback=True
    #     )

psql_db = connect()

# class PostgresqlModel(pw.Model):
#     class Meta:
#         database = db


class PostgresqlModel(pw.Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db


# ORM CLASSES
class website(PostgresqlModel):
    name        = pw.TextField()
    url         = pw.TextField(unique=True)
    last_date   = pw.DateTimeField(default=datetime.datetime.utcnow())
    last_user   = pw.TextField(default='user')
    create_date = pw.DateTimeField(default=datetime.datetime.utcnow())
    create_user = pw.TextField(default='user')
    

class category(PostgresqlModel):
    """Intended use is with an insert function into the patheos_beliefs table."""
    name        = pw.TextField()
    context     = pw.TextField()
    url         = pw.TextField(unique=True)
    website_id  = pw.ForeignKeyField(website, backref='categories')
    last_date   = pw.DateTimeField(default=datetime.datetime.utcnow())
    last_user   = pw.TextField(default='user')
    create_date = pw.DateTimeField(default=datetime.datetime.utcnow())
    create_user = pw.TextField(default='user')
 
    
class blog(PostgresqlModel):
    """Intended use is with an insert function into the patheos_blogs table."""
    author      = pw.TextField()
    name        = pw.TextField()
    url         = pw.TextField(unique=True)
    category_id = pw.ForeignKeyField(category, backref='blogs')
    last_date   = pw.DateTimeField(default=datetime.datetime.utcnow())
    last_user   = pw.TextField(default='user')
    create_date = pw.DateTimeField(default=datetime.datetime.utcnow())
    create_user = pw.TextField(default='user')
    
    
class post(PostgresqlModel):
    """Intended use is with an insert function into the patheos_posts table."""
    title        = pw.TextField()
    author       = pw.TextField()
    date         = pw.TextField()
    tags         = pw.TextField()
    content      = pw.TextField()
    content_html = pw.TextField()
    url          = pw.TextField(unique=True)
    blog_id      = pw.ForeignKeyField(blog, backref='posts')
    last_date    = pw.DateTimeField(default=datetime.datetime.utcnow())
    last_user    = pw.TextField(default='user')
    create_date  = pw.DateTimeField(default=datetime.datetime.utcnow())
    create_user  = pw.TextField(default='user')


class blog_count_pages(PostgresqlModel):
    number      = pw.IntegerField()
    blog_id     = pw.ForeignKeyField(blog, backref='blog_count_page')
    last_date   = pw.DateTimeField(default=datetime.datetime.utcnow())
    last_user   = pw.TextField(default='user')
    create_date = pw.DateTimeField(default=datetime.datetime.utcnow())
    create_user = pw.TextField(default='user')


class url_error_list(PostgresqlModel):
    url         = pw.TextField()
    url_type    = pw.TextField()
    parent_id   = pw.IntegerField()
    exception   = pw.TextField()
    resolved    = pw.BooleanField(default=False)
    last_date   = pw.DateTimeField(default=datetime.datetime.utcnow())
    last_user   = pw.TextField(default='user')
    create_date = pw.DateTimeField(default=datetime.datetime.utcnow())
    create_user = pw.TextField(default='user')


def database_create_tables(drop=False):
    #if drop:
    drop = False
    psql_db.drop_tables([website, category, blog, post, blog_count_pages, url_error_list])
    psql_db.create_tables([website, category, blog, post, blog_count_pages, url_error_list])

if __name__ == '__main__':
    #db.connect()
    psql_db.drop_tables([website, category, blog, post, blog_count_pages, url_error_list])
    psql_db.create_tables([website, category, blog, post, blog_count_pages, url_error_list])
    website = website(name='Patheos Blogs', url='https://www.patheos.com/blogs')
    website.save()
    for i in blog.select():
        print(i.name, i.url)
    print(website.select().count())
    psql_db.close()
    print(psql_db.is_closed())
