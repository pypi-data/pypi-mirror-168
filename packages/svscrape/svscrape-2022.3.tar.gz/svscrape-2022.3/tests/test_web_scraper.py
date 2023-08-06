from unittest import TestCase
from unittest.mock import patch

from svwebscraper.webscraper import SchoolDataWebScrapper, RequestFailedException, School, ParsedPage
from tests.util.testdata_loader import load_file_to_string

SCHOOL_LIST_HTML_PAGE_WITH_SUCCESSOR = load_file_to_string('testdata/sv_list_with_succeeding_pages.html')
SCHOOL_LIST_HTML_PAGE_WITH_NO_SUCCESSOR = load_file_to_string('testdata/sv_list_with_no_successor.html')
SCHOOL_DETAIL_HTML_PAGE = load_file_to_string('./testdata/sv_detail_view.html')


class HttpResponseMock:
    def __init__(self, text, status_code, apparent_encoding):
        self.text = text
        self.status_code = status_code
        self.apparent_encoding = apparent_encoding


class SchoolPageTest(TestCase):
    @patch('requests.get', side_effect=lambda _: HttpResponseMock(SCHOOL_DETAIL_HTML_PAGE, 200, 'UTF-8'))
    def test_successful_parsing(self, get):
        school = School('')

        self.assertEqual(school.get_name(), 'Neue Mittelschule Wien')
        self.assertEqual(school.get_address(), 'Neubaugasse 42')
        self.assertEqual(school.get_postal_code(), '1070')
        self.assertEqual(school.get_city(), 'Wien')
        self.assertEqual(school.get_phone_number(), '01/526 15 94')


class ParsedPageTest(TestCase):
    def test_parse_page_with_successor(self):
        parsed_page = ParsedPage(SCHOOL_LIST_HTML_PAGE_WITH_SUCCESSOR)

        self.assertTrue(parsed_page.has_next())
        self.assertEqual(parsed_page.get_next_query_params(), '?bundesland=wien&start=20')
        self.assertEqual(len(parsed_page.get_schools()), 20)

    def test_parse_page_without_successor(self):
        parsed_page = ParsedPage(SCHOOL_LIST_HTML_PAGE_WITH_NO_SUCCESSOR)

        self.assertFalse(parsed_page.has_next())
        self.assertIsNone(parsed_page.get_next_query_params())
        self.assertEqual(len(parsed_page.get_schools()), 8)


class SchoolDataWebScrapperTest(TestCase):
    @patch('requests.get', side_effect=[HttpResponseMock(SCHOOL_LIST_HTML_PAGE_WITH_SUCCESSOR, 200, 'UTF-8'),
                                        HttpResponseMock(SCHOOL_LIST_HTML_PAGE_WITH_NO_SUCCESSOR, 200, 'UTF-8')])
    @patch('svwebscraper.webscraper.School')
    def test_retrieve_schools(self, school_mock, get_mock):
        webscraper = SchoolDataWebScrapper("https://schulverzeichnis.eu")
        schools = webscraper.retrieve_school_list()

        self.assertEqual(len(schools), 28)

    @patch('requests.get', side_effect=[HttpResponseMock(SCHOOL_LIST_HTML_PAGE_WITH_SUCCESSOR, 200, 'UTF-8')])
    def test_successful_fetch_html_source(self, get):
        webscraper = SchoolDataWebScrapper("https://schulverzeichnis.eu")
        retrieved_html = webscraper._fetch_html_source("?bundesland=wien")

        self.assertEqual(retrieved_html, SCHOOL_LIST_HTML_PAGE_WITH_SUCCESSOR)

    @patch('requests.get', side_effect=[HttpResponseMock(None, 404, 'UTF-8')])
    def test_fetch_html_source_with_unsuccessful_statuscode(self, get):
        webscraper = SchoolDataWebScrapper("https://schulverzeichnis.eu")

        with self.assertRaises(RequestFailedException):
            webscraper._fetch_html_source("?bundesland=wien")
