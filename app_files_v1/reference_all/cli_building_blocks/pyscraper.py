# STANDARD
from pprint import pprint

# LOCAL
import db_interface_sqlite as db

# PyPI
import click


@click.group()
def cli():
    """CLI Maintenance for webscraping application"""

@cli.command('target', help='Configure target websites available for webscraping.')
@click.argument('website', required=False)
@click.option('-l', '--list', 'list', is_flag=True, help='Show all available websites for scraping.')
@click.option('-n', '--add_name', 'add_name', help='Add an entry\'s name')
@click.option('-u', '--add_url', 'add_url', help='Add an entry\'s url')
def websites_setup(website, list, add_name=None, add_url=None):
    if list and website:
        pass
    elif add_name and add_url:
        with db.database() as data:
            if data.query_websites(website):
                click.echo(f'{website} already exists.')
                record = db.website(name=add_name, url=add_url)
                print(record.name)
                click.echo(f'Name: {record.name}\n'
                           f'UNID: {record.id}\n'
                           f'URL:  {record.url}')
            else:
                record = db.website(name=add_name, url=add_url)
                result = data.insert_website(record)
                print(result)
                data.commit()
    else:
        with db.database() as data:
            if data.query_websites(website):
                record = data.query_websites(website)
                click.echo(f'Name: {record.name}\n'
                           f'UNID: {record.id}\n'
                           f'URL:  {record.url}')
            else:
                click.echo('TEST: nothing')
