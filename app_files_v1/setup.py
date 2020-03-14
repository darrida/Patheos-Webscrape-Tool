from setuptools import setup

setup(
    name='pyscraper',
    version='0.1',
    py_modules=['pyscraper'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pyscraper=pyscraper:cli
    ''',
)