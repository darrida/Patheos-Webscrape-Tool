from pathlib import Path
import shutil
import sqlite3
#from .. import db_interface_sqlite as data

# PyPI
import pytest


def test_test():
    assert True


# def test_create_test_db():
#     connection = sqlite3.connect(Path.cwd() / 'test_files' / 'test.db')
#     cur = connection.cursor()
#     assert cur


# def test_insert_website(test_database=None):
#     if test_database == None:
#         test_database = sqlite3.connect("file::memory:?cache=shared")
#     with data.database(test_database) as db:
#         w = data.website(name='Patheos Blogs', url='https://www.patheos.com/blogs')
#         db.insert_website(w)
#         result = db.execute('SELECT url FROM websites WHERE name = \'Patheos Blogs\'')
#     assert result[0] == 'https://www.patheos.com/blogs'