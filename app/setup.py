from setuptools import setup

setup(
    name='pyscrape',
    version='0.1',
    py_modules=['pyscrape'],
    install_requires=[
        'Click',
        'pyscrape',
        'requests',
        'bs4',
        
    ],
    entry_points='''
        [console_scripts]
        pyscrape=pyscrape:cli
    ''',
)