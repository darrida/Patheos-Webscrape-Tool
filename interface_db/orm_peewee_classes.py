#PyPI
import peewee as pw
import datetime


#db = pw.SqliteDatabase('my_database.db')
class config_postgres:
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user     = user
        self.password = password
        self.host     = host
        self.port     = port
     

def connect():
    return pw.PostgresqlDatabase(
        database='postgres',
        user='postgres',
        password='postgrest',
        host='192.168.86.108',
        port='32834',
    )

db = connect()

class BaseModel(pw.Model):
    class Meta:
        database = db


# ORM CLASSES
class website(BaseModel):
    name        = pw.TextField()
    url         = pw.TextField(unique=True)
    last_date   = pw.DateTimeField(default=datetime.datetime.utcnow())
    last_user   = pw.TextField(default='user')
    create_date = pw.DateTimeField(default=datetime.datetime.utcnow())
    create_user = pw.TextField(default='user')
    

class category(BaseModel):
    """Intended use is with an insert function into the patheos_beliefs table."""
    name        = pw.TextField()
    context     = pw.TextField()
    url         = pw.TextField(unique=True)
    website_id  = pw.ForeignKeyField(website, backref='categories')
    last_date   = pw.DateTimeField(default=datetime.datetime.utcnow())
    last_user   = pw.TextField()
    create_date = pw.DateTimeField(default=datetime.datetime.utcnow())
    create_user = pw.TextField()
 
    
class blog(BaseModel):
    """Intended use is with an insert function into the patheos_blogs table."""
    author      = pw.TextField()
    name        = pw.TextField()
    url         = pw.TextField(unique=True)
    category_id = pw.ForeignKeyField(category, backref='blogs')
    last_date   = pw.DateTimeField(default=datetime.datetime.utcnow())
    last_user   = pw.TextField()
    create_date = pw.DateTimeField(default=datetime.datetime.utcnow())
    create_user = pw.TextField()
    
    
class post(BaseModel):
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
    last_user    = pw.TextField()
    create_date  = pw.DateTimeField(default=datetime.datetime.utcnow())
    create_user  = pw.TextField()


class blog_count_pages(BaseModel):
    number      = pw.IntegerField()
    blog_id     = pw.ForeignKeyField(blog, backref='blog_count_page')
    last_date   = pw.DateTimeField(default=datetime.datetime.utcnow())
    last_user   = pw.TextField()
    create_date = pw.DateTimeField(default=datetime.datetime.utcnow())
    create_user = pw.TextField()


class url_error_list(BaseModel):
    url         = pw.TextField()
    url_type    = pw.TextField()
    parent_id   = pw.IntegerField()
    resolved    = pw.BooleanField(default=False)
    last_date   = pw.DateTimeField(default=datetime.datetime.utcnow())
    last_user   = pw.TextField()
    create_date = pw.DateTimeField(default=datetime.datetime.utcnow())
    create_user = pw.TextField()


if __name__ == '__main__':
    db.connect()
    db.drop_tables([website, category, blog, post, blog_count_pages, url_error_list])
    db.create_tables([website, category, blog, post, blog_count_pages, url_error_list])
    website = website(name='Patheos Blogs', url='https://www.patheos.com/blogs')
    website.save()
    for i in blog.select():
        print(i.name, i.url)
    print(website.select().count())
    db.close()
    print(db.is_closed())
