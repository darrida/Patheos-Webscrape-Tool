# Standard
from datetime import datetime
from datetime import date

class url_error:
    """Intended use is with an insert function into the url_error_list table."""
    today = date.today()
    last_date = datetime.now()
    def __init__(self, url, url_type, parent_id, resolved=False,
                 id=None, 
                 last_date=last_date, last_user='default', 
                 create_date=today, create_user='default'):
        self.id          = id if id != None else None
        self.url         = url
        self.url_type    = url_type
        self.parent_id   = parent_id
        self.resolved    = resolved
        self.last_date   = last_date
        self.last_user   = last_user
        self.create_date = create_date
        self.create_user = create_user


class website:
    """Intended use is with an insert function into the websites table."""
    today = date.today()
    last_date = datetime.now()
    def __init__(self, name, url, 
                 id=None, 
                 last_date=last_date, last_user='default', 
                 create_date=today, create_user='default'):
        self.id          = id if id != None else None
        self.name        = name
        self.url         = url
        self.last_date   = last_date
        self.last_user   = last_user
        self.create_date = create_date
        self.create_user = create_user


class category:
    """Intended use is with an insert function into the categories table."""
    today = date.today()
    last_date = datetime.now()
    def __init__(self, name=None, url=None, website_id=None,
                 id=None, context=None,
                 last_date=last_date, last_user='default',
                 create_date=today, create_user='default'):
        self.id          = id if id != None else None
        self.name        = name
        self.context     = context
        self.url         = url
        self.website_id  = website_id
        self.last_date   = last_date
        self.last_user   = last_user
        self.create_date = create_date
        self.create_user = create_user
    
    
class blog:
    """Intended use is with an insert function into the blogs table."""
    today = date.today()
    last_date = datetime.now()
    def __init__(self, author=None, name=None, url=None, 
                 id=None, category_id=None, 
                 last_date=last_date, last_user='default', 
                 create_date=today, create_user='default'):
        self.id          = id
        self.author      = author
        self.name        = name
        self.url         = url
        self.category_id = category_id
        self.last_date   = last_date
        self.last_user   = last_user
        self.create_date = create_date
        self.create_user = create_user


class post:
    """Intended use is with an insert function into the pposts table."""
    today = date.today()
    last_date = datetime.now()
    def __init__(self, url, blog_id, title=None, author=None, date=None, tags=None, content=None, content_html=None,
                 id=None, 
                 last_date=last_date, last_user='default',
                 create_date=today, create_user='default'):
        self.id          = id
        self.title       = title
        self.author      = author
        self.date        = date
        self.tags        = tags
        self.content     = content
        self.content_html= content_html
        self.url         = url
        self.blog_id     = blog_id
        self.last_date   = last_date
        self.last_user   = last_user
        self.create_date = create_date
        self.create_user = create_user
