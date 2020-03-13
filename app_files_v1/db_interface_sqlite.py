# Standard
import sqlite3
import os
from pathlib import Path
from datetime import datetime

# PyPI

# LOCAL


class website:
    """Intended use is with an insert function into the website table."""
    def __init__(self, id, name, url, last_date, last_user, create_date, create_user)
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
    def __init__(self, id, title, author, date, tags, content, url, blog_id, last_date, last_user, c
                 reate_date, create_user):
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


class database(object):
    """Handles all database connectsion, inputs, and outputs
    
    Class constructor initiates sqlite3 database connection. If used in WITH statement
    the connection will cleanly close after the statement is finished. If there are
    uncommitted transactions they will be rolled back prior to connection closure.
    
    """
    def __init__(self):
        __DB_LOCATION = (
            Path.home() / "py_apps" / "_appdata" / "webscrape_patheos" / "patheos.db"
        )
        if os.path.exists(__DB_LOCATION):
            self.__db_connection = sqlite3.connect(str(__DB_LOCATION))
            self.cur = self.__db_connection.cursor()
        else:
            Path(
                Path.home() / "py_apps" / "_appdata" / "webscrape_patheos"
            ).mkdir(parents=True, exist_ok=True)
            self.__db_connection = sqlite3.connect(str(__DB_LOCATION))
            self.cur = self.__db_connection.cursor()
            
    
    def __del__(self):
        self.__db_connection.close()

    
    def __enter__(self):
        return self

    
    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.__db_connection.rollback()
        else:
            self.__db_connection.commit()
        self.__db_connection.close()
    
    
    def execute(self, new_data: str) -> tuple:
        """Executes an valid SQL statement passed through as a string.

        Arugments:
            new_data (string): Valid SQL statement

        """
        return self.cur.execute(new_data)

    
    def executemany(self, many_new_data: str) -> None:
        """Not currently in use.
        """
        self.cur.executemany("REPLACE INTO <table> VALUES(?, ?, ?, ?)", many_new_data)
    
    
    def insert_category(self, category):
        """Inserts a category record. Designed for use with the category class.

        Arguments:
            category (category class): class or dictionary containing the following values:
                -

        """
        category.id = self.cur.execute("""SELECT MAX(beliefs_number) FROM patheos_beliefs""").fetchone()[0]
        category.id = category.id + 1 if category.id else 1
        self.cur.execute(
            f"""INSERT INTO patheos_beliefs
                             VALUES (
                                        "{category.beliefs_number}",
                                        "{category.beliefs_name}",
                                        "{category.beliefs_url}",
                                        "{category.last_date}",
                                        "{category.last_user}",
                                        "{category.create_date}",
                                        "{category.create_user}"
                        )"""
        )
    
    
    def insert_blog(self, blog):
        """Inserts a category record. Designed for use with the category class.

        Arguments:
            category (category class): class or dictionary containing the following values:
                -

        """
        blog.id = self.cur.execute("""SELECT MAX(blogs_number) FROM patheos_blogs""").fetchone()[0]
        blog.id = blog.id + 1 if blog.id else 1
        self.cur.execute(
            f"""INSERT INTO patheos_blogs
                             VALUES (
                                        "{blog.blogs_number}",
                                        "{blog.blogs_name}",
                                        "{blog.blogs_url}",
                                        "{blog.last_date}",
                                        "{blog.last_user}",
                                        "{blog.create_date}",
                                        "{blog.create_user}"
                        )"""
        )
        
        
        def insert_post(self, post):
        """Inserts a category record. Designed for use with the category class.

        Arguments:
            category (category class): class or dictionary containing the following values:
                -

        """
        post.id = self.cur.execute("""SELECT MAX(posts_number) FROM patheos_posts""").fetchone()[0]
        post.id = post.id + 1 if post.id else 1
        self.cur.execute(
            f"""INSERT INTO patheos_posts
                             VALUES (
                                        "{post.posts_number}",
                                        "{post.posts_name}",
                                        "{post.posts_url}",
                                        "{post.last_date}",
                                        "{post.last_user}",
                                        "{post.create_date}",
                                        "{post.create_user}"
                        )"""
        )
        
    
    def create_tables(self):
        """This function confirms the existence of or creates the path, database, and tables.
        
        Can be used by calling the function directly, but is designed to by used by install.py, which is called by the install.bat file.
        
        """
        if (
            Path.home() / "py_apps" / "_appdata" / "webscrape_patheos" / "patheos.db"
        ):
            pass
        else:
            Path(Path.home() / "py_apps" / "_appdata" / "webscrape_patheos" / "patheos.db").mkdir(
                parents=True, exist_ok=True
            )

        """create a database table if it does not exist already"""
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS 
                            patheos_beliefs (
                                beliefs_number     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                                beliefs_name       VARCHAR(100) NOT NULL, 
                                beliefs_tradition  VARCHAR(100), 
                                beliefs_url        VARCHAR(2000) NOT NULL,
                                last_date          TIMESTAMP,
                                last_user          VARCHAR(100),
                                create_date        TIMESTAMP,
                                create_user        VARCHAR(100)
                        )"""
        )
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS
                            patheos_blogs (
                                blogs_number       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                                blogs_auther       VARCHAR(150),
                                beliefs_number     INTEGER NOT NULL, 
                                blogs_name         VARCHAR(255), 
                                blogs_url          VARCHAR(2000) NOT NULL,
                                last_date          TIMESTAMP,
                                last_user          VARCHAR(100),
                                create_date        TIMESTAMP,
                                create_user        VARCHAR(100),
                                FOREIGN KEY (beliefs_number) REFERENCES patheos_beliefs(beliefs_number)
                    )"""
        )
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS
                            patheos_posts (
                                posts_number       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                                posts_title V      ARCHAR(255) NOT NULL, 
                                blogs_number       INTEGER NOT NULL, 
                                posts_author       VARCHAR(255), 
                                posts_date         DATE, 
                                posts_tags         VARCHAR(255), 
                                posts_content      TEXT, 
                                posts_url          VARCHAR(2000) NOT NULL,
                                last_date          TIMESTAMP,
                                last_user          VARCHAR(100),
                                create_date        TIMESTAMP,
                                create_user        VARCHAR(100),
                                FOREIGN KEY (blogs_number) REFERENCES patheo_blogs(blogs_number)
                    )"""
        )