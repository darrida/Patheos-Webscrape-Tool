# #PyPI
# from sqlalchemy import connect, Column, Integer, String
# import sqlalchemy
# from sqlalchemy.ext.declarative import declarative_base

# db = sqlalchemy.connect()

# # ORM CLASSES

# class website(db.Model):
#     __tablename__ = 'websites'
#     id          = db.Column(db.Integer, primary_key=True)
#     name        = db.Column(db.String(255))
#     url         = db.Column(db.String(255))
#     last_date   = db.Column(db.DateTime, index=True, default=datetime.utcnow())
#     last_user   = db.Column(String(50))
#     create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
#     create_user = db.Column(db.String(50))
#     categories  = db.relationship('category', backref='categories', lazy='dynamic')
    

# class category(db.Model):
#     """Intended use is with an insert function into the patheos_beliefs table."""
#     __tablename__ = 'categories'
#     id          = db.Column(db.Integer, primary_key=True)
#     name        = db.Column(db.String(255))
#     tradition   = db.Column(db.String(255))
#     url         = db.Column(db.String(2000))
#     website_id  = db.Column(db.Integer, db.ForeignKey('websites.id'))
#     last_date   = db.Column(db.DateTime, index=True, default=datetime.utcnow())
#     last_user   = db.Column(String(50))
#     create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
#     create_user = db.Column(db.String(50))
#     blogs = db.relationship('blog', backref='blogs', lazy='dynamic')
 
    
# class blog(db.Model):
#     """Intended use is with an insert function into the patheos_blogs table."""
#     __tablename__ = 'blogs'
#     id          = db.Column(db.Integer, primary_key=True)
#     author      = db.Column(db.String(255))
#     name        = db.Column(db.String(255))
#     url         = db.Column(db.String(2000))
#     category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
#     last_date   = db.Column(db.DateTime, index=True, default=datetime.utcnow())
#     last_user   = db.Column(String(50))
#     create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
#     create_user = db.Column(db.String(50))
#     posts = db.relationship('post', backref='posts', lazy='dynamic')
    
    
# class posts(db.Model):
#     """Intended use is with an insert function into the patheos_posts table."""
#     __tablename__ = 'posts'
#     id          = db.Column(db.Integer, primary_key=True)
#     name        = db.Column(db.String(500))
#     author      = db.Column(db.String(255))
#     date        = db.Column(db.DateTime, index=True)
#     tags        = db.Column(db.String(500))
#     content     = db.Column(db.Test)
#     url         = db.Column(db.String(2000))
#     blog_id     = db.Column(db.Integer, db.ForeignKey('blogs.id'))
#     last_date   = db.Column(db.DateTime, index=True, default=datetime.utcnow())
#     last_user   = db.Column(String(50))
#     create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
#     create_user = db.Column(db.String(50))
