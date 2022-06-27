import click
from harvester.oai.harvester import fetch_list, fetch_list_async, fetch_url
from harvester.orcid.orcid import get_orcid_list_by_org, ORCID_API


@click.group()
def harvester():
    """This script showcases different terminal UI helpers in Click."""
    pass


@harvester.command()
@click.argument('url')
@click.argument('data_dir')
def fetchone(url, data_dir):
    print(url, data_dir)
    fetch_url(url, data_dir)


@harvester.command()
@click.argument('list_file')
@click.argument('data_dir')
def fetch(list_file, data_dir):
    fetch_list(list_file, data_dir)


@harvester.command()
@click.argument('list_file')
@click.argument('data_dir')
def fetchasync(list_file, data_dir):
    fetch_list_async(list_file, data_dir)


@harvester.command()
def orcid():
    get_orcid_list_by_org()