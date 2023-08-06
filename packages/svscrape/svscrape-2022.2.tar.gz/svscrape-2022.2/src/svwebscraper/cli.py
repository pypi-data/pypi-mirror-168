import click

from urllib.parse import urljoin
from src.svwebscraper.exporter import SchoolCSVExporter
from src.svwebscraper.webscraper import SchoolDataWebScrapper

DEFAULT_BASE_URL = 'http://www.schulverzeichnis.eu/typ/'
SCHOOL_TYPES = ['neue-mittelschule', 'ahs-mit-nms', 'hauptschule', 'sonderschule']
DEFAULT_SCHOOL_TYPE = SCHOOL_TYPES[0]
DEFAULT_QUERY = '?bundesland=wien'


@click.command()
@click.option('--csv', nargs=1, type=click.File())
@click.option('--baseurl', nargs=1, default=DEFAULT_BASE_URL)
@click.option('--type', nargs=1, default=DEFAULT_SCHOOL_TYPE, type=click.Choice(SCHOOL_TYPES))
@click.option('--query', nargs=1, default=DEFAULT_QUERY)
def scrape_schools(csv, baseurl, type, query):
    url = urljoin(baseurl, type)
    web_scrapper = SchoolDataWebScrapper(f'{url}/{query}')
    schools = web_scrapper.retrieve_school_list()

    if csv:
        exporter = SchoolCSVExporter(schools)
        exporter.export_to_file(csv)
