# Standard
import sqlite3
import os
from pathlib import Path
from datetime import datetime
from datetime import date

# PyPI

# LOCAL

# Variables to make pylint happy
test_database=None


class website:
    """Intended use is with an insert function into the websites table."""
    today = date.today()
    def __init__(self, name, url, 
                 id=None, 
                 last_date=today, last_user='default', 
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
    def __init__(self, name=None, url=None, website_id=None,
                 id=None, context=None,
                 last_date=today, last_user='default',
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
    def __init__(self, author=None, name=None, url=None, 
                 id=None, category_id=None, 
                 last_date=today, last_user='default', 
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
    def __init__(self, url, blog_id, title=None, author=None, date=None, tags=None, content=None, content_html=None,
                 id=None, 
                 last_date=today, last_user='default',
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


class database(object):
    """Handles all database connectsion, inputs, and outputs
    
    Class constructor initiates sqlite3 database connection. If used in WITH statement
    the connection will cleanly close after the statement is finished. If there are
    uncommitted transactions they will be rolled back prior to connection closure.
    
    """
    def __init__(self, test_database=None):
        if test_database:
            self.__db_connection = test_database
            self.cur = self.__db_connection.cursor()
        else:
            __DB_LOCATION = (
                Path.home() 
                / "py_apps" 
                / "_appdata" 
                / "webscraper"
                / "webscraper.db"
            )
            if os.path.exists(__DB_LOCATION):
                self.__db_connection = sqlite3.connect(str(__DB_LOCATION))
                self.cur = self.__db_connection.cursor()
            else:
                Path(
                    Path.home() / "py_apps" / "_appdata" / "webscraper"
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
    

    def query_websites(self, name=None, url=None, website_id=None):
        if name:
            result = self.cur.execute(f"""SELECT * FROM websites WHERE name = '{name}'""").fetchone()
        elif url:
            result = self.cur.execute(f"""SELECT * FROM websites WHERE url = '{url}'""").fetchone()
        elif website_id:
            result = self.cur.execute(f"""SELECT * FROM websites WHERE id = '{website_id}'""").fetchone()
        else:
            return 'query_websites() requires name or url'
        if result:
            return website(id          = result[0], # id
                           name        = result[1], # name
                           url         = result[2], # url
                           last_date   = result[3], # last_date
                           last_user   = result[4], # last_user
                           create_date = result[5], # create_date
                           create_user = result[6]) # create_user
        else:
            return None


    def query_categories(self, name=None, category_id=None):
        if name:
            result = self.cur.execute(f"""SELECT * FROM categories WHERE name = '{name}'""").fetchone()
        if category_id:
            result = self.cur.execute(f"""SELECT * FROM categories WHERE id = '{category_id}'""").fetchone()
        if result:
            return category(id          = result[0], # id
                            name        = result[1], # name
                            context     = result[2], # context
                            url         = result[3], # url
                            website_id  = result[4], # website_id
                            last_date   = result[5], # last_date
                            last_user   = result[6], # last_user
                            create_date = result[7], # create_date
                            create_user = result[8]) # create_user)
            #return result
        else:
            return None

    
    def query_blogs(self, name):
        result = self.cur.execute(f"""SELECT * FROM blogs WHERE name = '{name}'""").fetchone()
        if result:
            return blog(id          = result[0], # id
                        author      = result[1], # name
                        name        = result[2], # context
                        url         = result[3], # url
                        category_id = result[4], # website_id
                        last_date   = result[5], # last_date
                        last_user   = result[6], # last_user
                        create_date = result[7], # create_date
                        create_user = result[8]) # create_user)
        else:
            return None

    
    def execute(self, new_data: str) -> tuple:
        """Executes an valid SQL statement passed through as a string.

        Arugments:
            new_data (string): Valid SQL statement

        """
        return self.cur.execute(new_data).fetchall()
    

    def insert_update_site_pages(self, page_number: int, site_id: int):
        """Inserts a website record. Designed for use with the website class.

        Arguments:
            website (website class): class or dictionary containing the following values:
                -

        """
        # existing_url = self.insert_update_website(url=website.url)
        # new = True if existing_url == None else False
        today = date.today()
        try:
            result = self.cur.execute(f"SELECT number FROM site_pages WHERE site_id = {site_id}").fetchall()
            #print(result)
            if result[0]:
                self.cur.execute(
                    f"""UPDATE site_pages
                        SET number = '{page_number}',
                            last_date = '{today}',
                            last_user = 'user'
                        WHERE site_id = '{site_id}'
                    """
                )
            #print('updated or same')
        except IndexError:
            next_id = self.cur.execute("""SELECT MAX(id) FROM site_pages""").fetchone()[0]
            next_id = next_id + 1 if next_id else 1
            self.cur.execute(
                f"""INSERT INTO site_pages
                                VALUES (
                                        NULL,
                                        "{page_number}",
                                        "{site_id}",
                                        "{today}",
                                        "user",
                                        "{today}",
                                        "user"
                            )"""
            ).fetchall()
            #print('new')
        # else:
        #     self.cur.execute(
        #         f"""UPDATE websites
        #             SET number = '{page_number}',
        #                 last_date = '{today}',
        #                 last_user = 'user'
        #             WHERE website_id = '{website_id}'
        #         """
        #     ).fetchall()
        #     return self.query_websites(url=website.url)
        # else:
        #     return f'Not inserted. If exists, then {existing_url.url} is already present, named {existing_url.name}.'


    def insert_website(self, website: object) -> object:
        """Inserts a website record. Designed for use with the website class.

        Arguments:
            website (website class): class or dictionary containing the following values:
                -

        """
        existing_url = self.query_websites(url=website.url)
        new = True if existing_url == None else False
        if new == True:
            next_id = self.cur.execute("""SELECT MAX(id) FROM websites""").fetchone()[0]
            if next_id:
                next_id = next_id + 1 if next_id else 1
            today = date.today()
            self.cur.execute(
                f"""INSERT INTO websites
                                VALUES (
                                        NULL,
                                        "{website.name}",
                                        "{website.url}",
                                        "{today}",
                                        "user",
                                        "{today}",
                                        "user"
                            )"""
            ).fetchall()
            return self.query_websites(url=website.url)
        else:
            return f'Not inserted. If exists, then {existing_url.url} is already present, named {existing_url.name}.'

    
    def insert_category(self, category):
        """Inserts a category record. Designed for use with the category class.

        Arguments:
            category (category class): class or dictionary containing the following values:
                -

        """
        category.id = self.cur.execute("""SELECT MAX(id) FROM categories""").fetchone()[0]
        category.id = category.id + 1 if category.id else 1
        return self.cur.execute(
            f"""INSERT INTO categories
                             VALUES (
                                        "{category.id}",
                                        "{category.name}",
                                        "{category.context}",
                                        "{category.url}",
                                        "{category.website_id}",
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
        blog.id = self.cur.execute("""SELECT MAX(id) FROM blogs""").fetchone()[0]
        blog.id = blog.id + 1 if blog.id else 1
        blog.name = blog.name.replace('"', '')
        return self.cur.execute(
            f"""INSERT INTO blogs
                             VALUES (
                                        "{blog.id}",
                                        "{blog.author}",
                                        "{blog.name}",
                                        "{blog.url}",
                                        "{blog.category_id}",
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
        post.id = self.cur.execute("""SELECT MAX(id) FROM posts""").fetchone()[0]
        post.id = post.id + 1 if post.id else 1
        self.cur.execute(
            f"""INSERT INTO posts
                                VALUES (
                                        "{post.id}",
                                        "{post.title}",
                                        "{post.author}",
                                        "{post.date}",
                                        "{post.tags}",
                                        "{post.content}",
                                        "{post.content_html}",
                                        "{post.url}",
                                        "{post.blog_id}",
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
                            site_pages (
                                id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                                number       INTEGER NOT NULL,
                                site_id      INTEGER NOT NULL UNIQUE,
                                last_date    TIMESTAMP,
                                last_user    VARCHAR(100),
                                create_date  TIMESTAMP,
                                create_user  VARCHAR(100)
                        )"""
        )
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS 
                            websites (
                                id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                                name         VARCHAR(100) NOT NULL, 
                                url          VARCHAR(2000) NOT NULL,
                                last_date    TIMESTAMP,
                                last_user    VARCHAR(100),
                                create_date  TIMESTAMP,
                                create_user  VARCHAR(100)
                        )"""
        )
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS 
                            categories (
                                id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                                name         VARCHAR(100) NOT NULL, 
                                context      VARCHAR(100), 
                                url          VARCHAR(2000) NOT NULL,
                                website_id   INTEGER NOT NULL,
                                last_date    TIMESTAMP,
                                last_user    VARCHAR(100),
                                create_date  TIMESTAMP,
                                create_user  VARCHAR(100)
                        )"""
        )
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS
                            blogs (
                                id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                                auther       VARCHAR(255),
                                name         VARCHAR(255), 
                                url          TEXT NOT NULL,
                                category_id  INTEGER NOT NULL, 
                                last_date    TIMESTAMP,
                                last_user    VARCHAR(100),
                                create_date  TIMESTAMP,
                                create_user  VARCHAR(100)
                    )"""
        )
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS
                            posts (
                                id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                                title        VARCHAR(255) NOT NULL,
                                author       VARCHAR(255),
                                date         TIMESTAMP, 
                                tags         VARCHAR(255), 
                                content      TEXT, 
                                content_html TEXT,
                                url          TEXT NOT NULL,
                                blog_id      INTEGER NOT NULL,
                                last_date    TIMESTAMP,
                                last_user    VARCHAR(100),
                                create_date  TIMESTAMP,
                                create_user  VARCHAR(100)
                    )"""
        )


    def check_url_new(self, table: str, url: str) -> bool:
        """Check a URL against a database table to see if it already exists.
        
        Arguments:
            url (str): webpage page address to check against database table
            table (str): database table to check against

        Return
            bool: True if url exists in given table; False if it doesn't exist.
        
        """
        existing_url = self.cur.execute(f'SELECT url FROM {table} WHERE url = \'{url}\'')
        if len(existing_url) == 0:
            return True
        else: 
            return False

    def commit(self):
        """Use after any other database class function to commit changes.
        This function is separated from initial transactions to enable the __exit__ function to rollback changes in the case that errors are encountered.
        """
        self.__db_connection.commit()
