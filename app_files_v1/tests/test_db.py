# STANDARD
from pathlib import Path
import shutil
import sqlite3
import os
from datetime import date

# PyPI
import pytest

# LOCAL
from .. import db_interface_sqlite as data


def test_test():
    assert True


def test_create_test_db():
    __DB_LOCATION = Path.cwd() / 'tests' / 'test_files' / 'test.db'
    if os.path.exists(__DB_LOCATION):
        connection = sqlite3.connect(str(__DB_LOCATION))
        cur = connection.cursor()
    else:
        Path(
            Path.cwd() / 'tests' / 'test_files'
        ).mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(str(__DB_LOCATION))
        cur = connection.cursor()
    assert cur


def test_create_tables():
    __DB_LOCATION = Path.cwd() / 'tests' / 'test_files' / 'test.db'
    connection = sqlite3.connect(str(__DB_LOCATION))
    with data.database(connection) as db:
        db.create_tables()
        websites   = db.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'websites\'')
        categories = db.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'categories\'')
        blogs      = db.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'blogs\'')
        posts      = db.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'posts\'')
    assert websites[0][0] == 'websites'
    assert categories[0][0] == 'categories'
    assert blogs[0][0] == 'blogs'
    assert posts[0][0] == 'posts'


def test_insert_website(connection=None):
    if connection == None:
        __DB_LOCATION = Path.cwd() / 'tests' / 'test_files' / 'test.db'
        connection = sqlite3.connect(str(__DB_LOCATION))
    with data.database(connection) as db:
        w = data.website(name='Patheos Blogs', url='https://www.patheos.com/blogs')
        db.insert_website(w)
        result = db.execute('SELECT url FROM websites WHERE name = \'Patheos Blogs\'')
    assert result[0][0] == 'https://www.patheos.com/blogs'


def test_insert_category(connection=None):
    if connection == None:
        __DB_LOCATION = Path.cwd() / 'tests' / 'test_files' / 'test.db'
        connection = sqlite3.connect(str(__DB_LOCATION))
    with data.database(connection) as db:
        c = data.category(name='Buddhist Blogs',
                          context='Context',
                          url='https://www.patheos.com/buddhist-blogs',
                          website_id=1)
        db.insert_category(c)
        result = db.execute('SELECT name FROM categories WHERE name = \'Buddhist Blogs\'')
    assert result[0][0] == 'Buddhist Blogs'


def test_insert_blog(connection=None):
    if connection == None:
        __DB_LOCATION = Path.cwd() / 'tests' / 'test_files' / 'test.db'
        connection = sqlite3.connect(str(__DB_LOCATION))
    with data.database(connection) as db:
        b = data.blog(author='darrida',
                      name='American Buddhist',
                      url='https://www.patheos.com/blogs/americanbuddhist/',
                      category_id=1)
        db.insert_blog(b)
        result = db.execute('SELECT url FROM blogs WHERE name = \'American Buddhist\'')
    assert result[0][0] == 'https://www.patheos.com/blogs/americanbuddhist/'


def test_insert_post(connection=None):
    if connection == None:
        __DB_LOCATION = Path.cwd() / 'tests' / 'test_files' / 'test.db'
        connection = sqlite3.connect(str(__DB_LOCATION))
    with data.database(connection) as db:
        p = data.post(title='Shambhala Buddhist Community Faces New Allegations in Chapman Student Investigation',
                      author='JUSTIN WHITAKER',
                      date='JANUARY 4, 2020',
                      tags='tag1, tag2',
                      content='In a video that should be seen by university students and professors...',
                      url='https://www.patheos.com/blogs/americanbuddhist/2020/01/shambhala-buddhist-community-faces-new-allegations-in-chapman-student-investigation.html',
                      blog_id=1)
        db.insert_post(p)
        result = db.execute('SELECT author FROM posts WHERE title = \'Shambhala Buddhist Community Faces New Allegations in Chapman Student Investigation\'')
    assert result[0][0] == 'JUSTIN WHITAKER'


def test_teardown_install_files():
    try:
        if os.path.exists(Path.cwd() / 'tests' / 'test_files'):
            shutil.rmtree(Path.cwd() / 'tests' / 'test_files')
        assert os.path.exists(Path.cwd() / 'test' / 'test_files') == False
    except PermissionError:
        assert False