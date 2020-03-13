# Plain classes for the Patheo Webscraper (now using Flask and sqlalchemy instead)

class category_alternate:
    """Intended use is with an insert function into the patheos_beliefs table."""
    def __init__(self, beliefs_name, beliefs_tradition_beliefs_url):
        self.beliefs_number = beliefs_number
        self.beliefs_name = beliefs_name
        self.beliefs_tradition = beliefs_tradition
        self.beliefs_url = beliefs_url
        self.last_date = last_date
        self.last_user = last_user
        self.create_date = create_date
        self.create_user = create_user
    
    
class blogs_alternate:
    """Intended use is with an insert function into the patheos_blogs table."""
    def __init__(self, blogs_author, beliefs_number, blogs_name, blogs_url):
        self.blogs_number = blogs_number
        self.blogs_auther = blogs_auther
        self.beliefs_number = beliefs_number
        self.blogs_name = blogs_name
        self.blogs_url = blogs_url
        self.last_date = last_date
        self.last_user = last_user
        self.create_date = create_date
        self.create_user = create_user


class posts_alternate:
        """Intended use is with an insert function into the patheos_posts table."""
    def __init__(self, posts_title, blogs_number, posts_author, posts_date, posts_tags,
                 posts_content, posts_url):
        self.posts_number = posts_number
        self.posts_title = posts_title
        self.blogs_number = blogs_number
        self.posts_author = posts_author
        self.posts_date = posts_date
        self.posts_tags = posts_tags
        self.posts_content = posts_content
        self.posts_url = posts_url
        self.last_date = last_date
        self.last_user = last_user
        self.create_date = create_date
        self.create_user = create_user
