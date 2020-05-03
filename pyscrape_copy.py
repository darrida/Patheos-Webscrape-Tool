# STANDARD
from pprint import pprint

# PyPI
import click
import requests
import peewee

# LOCAL
#from interface_db import db_interface_postgres as data
from interface_website import website_tools as tools
from interface_website import website_patheos_psql as patheos
from interface_db import orm_peewee_classes as pw


@click.group()
def cli():
    """PYSCRAPE CLI TOOL

    This tool scrapes data from configured websites and inserts data into a database.
    """


@cli.command('start', help='Begins or resumes scraping of configured websites.')
@click.option('-u', '--update', 'update', is_flag=True)
@click.option('-s', '--stop', 'stop', is_flag=True, help='Process stops after category and blog update.')
@click.option('-p', '--print_progress', 'print_progress', is_flag=True, help='Print numbers that show basic progress.')
def pyscrape_start(update, stop, print_progress):
    """Main function that initializes the webscrapers and begins
    """
    #try:
    websites = pw.website.select()
    #for website in websites:
        #print(website.id)
    for website in websites:
        #print(website)
        if website.name == 'Patheos Blogs':
            print(website.name)
            if update:
                patheos.fetch_and_insert_categories(website)
                #with data.database() as db:
                categories = pw.category.select()
                for category in categories:
                    #print(category.url)
                    results = patheos.fetch_and_insert_blogs(category)
                    #print(category.name)
                    print(f'Inserted: {results.inserted} '
                        + f'| Not Inserted: {results.not_inserted} '
                        + f' | Errors: {results.exceptions}')
            if stop:
                exit()
            else:
                patheos.scrape_patheos(website, print_progress)
        else:
            pass
#except Exception:


@cli.command('init', help='Initializes table creation in database.')
@click.option('-d', '--drop', 'drop', is_flag=True, help='Drop (ERASES) all tables before creation statements')
def initialize(drop):
    delete_tables = True if drop else False
    pw.database_create_tables(delete_tables)


@cli.command('websites', help='List and manage top level websites.')
@click.argument('name', required=False)
@click.argument('url', required=False)
def websites(name, url):
    try:
        if (name and url == None) or (url and name == None):
            click.echo('Both NAME and URL are needed to add a site.\n')
            exit()
        if name and url:
            website = pw.website(name=name, url=url)
            website.save()
        websites = pw.website.select() #.order_by(website.last_date)
        for website in websites:
            click.echo('WEBSITE NAME:' + website.name)
            click.echo('WEBSITE URL:'+ website.url + '\n')
    except peewee.IntegrityError as e:
        click.echo(f'INTEGRITY ERROR: {e}')


# @cli.command('hold')
# def placeholder1():
#     with data.database() as db:
#         db.create_tables()
#         db.insert_update_site_pages(0, 149)
#         result = db.execute(f"SELECT number FROM site_pages WHERE site_id = 47")
#         #print(result[0][0])
#         for i in result:
#             results = patheos.fetch_and_insert_blogs(i[0])
#             print(f'Inserted: {results.inserted} | Not Inserted: {results.not_inserted} | Errors: {results.exceptions}')


# def placeholder2():
#     patheos.insert_website('Patheos Blogs', 'https://patheos.com/blogs')
#     #results = patheos.fetch_and_insert_categories('Patheos Blogs', 1)
#     #with data.database() as db:
#         result = db.execute("SELECT name FROM categories")
#         for i in result:
#             results = patheos.fetch_and_insert_blogs(i[0])
#             print(f'Inserted: {results.inserted} | Not Inserted: {results.not_inserted} | Errors: {results.exceptions}')

if __name__ == '__main__':
    cli()