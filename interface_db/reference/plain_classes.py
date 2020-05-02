

class website:
    """Intended use is with an insert function into the website table."""
    def __init__(self, id, name, url, last_date, last_user, create_date, create_user):
        self.id          = id
        self.name        = name
        self.url         = url
        self.last_date   = last_date
        self.last_user   = last_user
        self.create_date = create_date
        self.create_user = create_user


class category:
    """Intended use is with an insert function into the patheos_beliefs table."""
    def __init__(self, id, name, tradition, url, website_id, last_date, create_date, create_user):
        self.id          = id
        self.name        = name
        self.tradition   = tradition
        self.url         = url
        self.last_date   = last_date
        self.last_user   = last_user
        self.create_date = create_date
        self.create_user = create_user
    
    
class blog:
    """Intended use is with an insert function into the patheos_blogs table."""
    def __init__(self, id, author, name, url, category_id, last_date, create_date, create_user):
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
    """Intended use is with an insert function into the patheos_posts table."""
    def __init__(self, id, title, author, date, tags, content, url, blog_id, last_date, last_user, create_date, create_user):
        self.id          = id
        self.title       = title
        self.author      = author
        self.date        = date
        self.tags        = tags
        self.content     = content
        self.url         = url
        self.last_date   = last_date
        self.last_user   = last_user
        self.create_date = create_date
        self.create_user = create_user
