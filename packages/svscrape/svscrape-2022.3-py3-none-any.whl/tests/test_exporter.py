from unittest import TestCase, mock
from unittest.mock import patch, mock_open

from svwebscraper.exporter import SchoolCSVExporter


class School:
    def __init__(self, name, address, postal_code, city, phone_number):
        self.name = name
        self.address = address
        self.postal_code = postal_code
        self.city = city
        self.phone_number = phone_number

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_postal_code(self):
        return self.postal_code

    def get_city(self):
        return self.city

    def get_phone_number(self):
        return self.phone_number


class ExporterTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schools = [
            School('Freie Waldorfschule Wien-West', 'Seuttergasse 29', '1120', 'Wien', '01/1234567'),
            School('Mittelschule des Schulvereins der Dominikanerinnen', 'Schlossberggasse 17', '1130', 'Wien',
                   '01/1234567'),
            School('Neue Mittelschule Wien', 'Neubaugasse 42', '1070', 'Wien', '01/1234567')
        ]

    def test_export_to_file(self):
        with patch('builtins.open', mock_open()) as file_handle:
            exporter = SchoolCSVExporter(ExporterTest.schools)
            exporter.export_to_file('testfile.csv')

            self.assertEqual(file_handle.return_value.write.call_count, 4)

            file_handle.return_value.write.assert_has_calls([
                mock.call('NAME;ADRESSE;PLZ;ORT;TEL_NR\n'),
                mock.call('Freie Waldorfschule Wien-West;Seuttergasse 29;1120;Wien;01/1234567\n'),
                mock.call(
                    'Mittelschule des Schulvereins der Dominikanerinnen;Schlossberggasse 17;1130;Wien;01/1234567\n'),
                mock.call('Neue Mittelschule Wien;Neubaugasse 42;1070;Wien;01/1234567\n')
            ])

    def test_export_to_file_with_custom_delimiters(self):
        with patch('builtins.open', mock_open()) as file_handle:
            exporter = SchoolCSVExporter(ExporterTest.schools, delimiter=',')
            exporter.export_to_file('testfile.csv')

            self.assertEqual(file_handle.return_value.write.call_count, 4)

            file_handle.return_value.write.assert_has_calls([
                mock.call('NAME,ADRESSE,PLZ,ORT,TEL_NR\n'),
                mock.call('Freie Waldorfschule Wien-West,Seuttergasse 29,1120,Wien,01/1234567\n'),
                mock.call(
                    'Mittelschule des Schulvereins der Dominikanerinnen,Schlossberggasse 17,1130,Wien,01/1234567\n'),
                mock.call('Neue Mittelschule Wien,Neubaugasse 42,1070,Wien,01/1234567\n')
            ])

    def test_export_to_file_with_custom_newline(self):
        with patch('builtins.open', mock_open()) as file_handle:
            exporter = SchoolCSVExporter(ExporterTest.schools, newline='\r\n')
            exporter.export_to_file('testfile.csv')

            self.assertEqual(file_handle.return_value.write.call_count, 4)

            file_handle.return_value.write.assert_has_calls([
                mock.call('NAME;ADRESSE;PLZ;ORT;TEL_NR\r\n'),
                mock.call('Freie Waldorfschule Wien-West;Seuttergasse 29;1120;Wien;01/1234567\r\n'),
                mock.call(
                    'Mittelschule des Schulvereins der Dominikanerinnen;Schlossberggasse 17;1130;Wien;01/1234567\r\n'),
                mock.call('Neue Mittelschule Wien;Neubaugasse 42;1070;Wien;01/1234567\r\n')
            ])