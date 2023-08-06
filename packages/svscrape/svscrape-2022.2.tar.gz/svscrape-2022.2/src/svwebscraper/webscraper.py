import logging
import requests
from bs4 import BeautifulSoup, Tag

from src.svwebscraper.exceptions import RequestFailedException


class SchoolDataWebScrapper:
    def __init__(self, url):
        splitted_url = url.split('?')

        self.base_url = url.split('?')[0]

        if len(splitted_url) > 1:
            self.initial_query_part = f"?{''.join(splitted_url[1:])}"
        else:
            self.initial_query_part = ''

    def retrieve_school_list(self):
        print("Start scrapping schools from base url...")

        parsed_web_page = self._parse_web_page(self.initial_query_part)
        schools = parsed_web_page.get_schools()

        print(f'{len(schools)} schools scrapped from "{self.base_url}"')

        while parsed_web_page.has_next():
            parsed_web_page = self._parse_web_page(parsed_web_page.get_next_query_params())
            schools += parsed_web_page.get_schools()

            print(f'{len(schools)} schools scrapped from "{self.base_url}"')

        return schools

    def _parse_web_page(self, query_params):
        html_source = self._fetch_html_source(query_params)
        return ParsedPage(html_source)

    def _fetch_html_source(self, query_params):
        response = requests.get(f"{self.base_url}{query_params}")

        if response.status_code != 200:
            raise RequestFailedException(response.status_code)

        response.encoding = response.apparent_encoding
        return response.text


class ParsedPage:
    def __init__(self, source):
        self.soup = BeautifulSoup(source, 'html.parser')

    def has_next(self):
        return self.get_next_query_params() is not None

    def get_schools(self):
        school_divs = self.soup.find_all('div', class_='school_name')
        schools = list()

        for school_tag in school_divs:
            name_tag = school_tag.find_all('a')[0]
            try:
                schools.append(School(name_tag['href']))
            except RequestFailedException:
                logging.error(f'Parsing school {name_tag["href"]} failed.')

        return schools

    def get_next_query_params(self):
        paging_div = self.soup.find_all('div', class_='paging')[0]

        for child in paging_div.contents:
            if type(child) is Tag and child.text.startswith('weiter'):
                return child['href']
        return None


class School:
    def __init__(self, school_meta_url):
        response = requests.get(school_meta_url)
        response.encoding = response.apparent_encoding

        if response.status_code != 200:
            logging.error(f'Response of request to {school_meta_url} resulted in status_code {response.status_code}.')
            raise RequestFailedException(response.status_code)

        soup = BeautifulSoup(response.text, 'html.parser')
        self.info_div = soup.find_all('p', class_='map_title')[0].parent

    def get_name(self):
        tag = self.info_div.findChild('p', class_='map_title')
        if tag:
            return tag.text
        return None

    def get_address(self):
        tag = self.info_div.findChild('span', itemprop="streetAddress")

        if tag:
            return tag.text
        return None

    def get_postal_code(self):
        tag = self.info_div.findChild('span', itemprop="postalCode")
        if tag:
            return tag.text
        return None

    def get_city(self):
        tag = self.info_div.findChild('span', itemprop="addressLocality")
        if tag:
            return tag.text
        return None

    def get_phone_number(self):
        tag = self.info_div.findChild('span', itemprop="telephone")
        if tag:
            return tag.text
        return None
