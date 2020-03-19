from pathlib import Path
import shutil
import sqlite3
import os
from .. import db_interface_sqlite as data

# PyPI
import pytest


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
        result = db.execute('SELECT name FROM sqlite_master WHERE type=\'table\'')# AND name=\'websites\'')   
    assert result[0][0] == 'websites'
    assert result[2][0] == 'categories'
    assert result[3][0] == 'blogs'
    assert result[4][0] == 'posts'


def test_insert_website(test_database=None):
    if test_database == None:
        test_database = sqlite3.connect("file::memory:?cache=shared")
    with data.database(test_database) as db:
        w = data.website(name='Patheos Blogs', url='https://www.patheos.com/blogs')
        db.insert_website(w)
        result = db.execute('SELECT url FROM websites WHERE name = \'Patheos Blogs\'')
    assert result[0] == 'https://www.patheos.com/blogs'


def test_teardown_install_files():
    try:
        if os.path.exists(Path.cwd() / 'tests' / 'test_files'):
            shutil.rmtree(Path.cwd() / 'tests' / 'test_files')
        assert os.path.exists(Path.cwd() / 'test' / 'test_files') == False
    except PermissionError:
        assert False