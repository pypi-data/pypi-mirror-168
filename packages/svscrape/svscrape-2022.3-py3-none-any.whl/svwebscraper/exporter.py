import os

HEADER = ['NAME', 'ADRESSE', 'PLZ', 'ORT', 'TEL_NR']
EXPORT_DIRECTORY = './export/'


class SchoolCSVExporter:
    def __init__(self, schools, delimiter=';', newline='\n'):
        self.schools = schools
        self.delimiter = delimiter
        self.newline = newline

        if not os.path.isdir(EXPORT_DIRECTORY):
            os.makedirs(EXPORT_DIRECTORY)

    def export_to_file(self, filename, append=False):
        print(f'Export {len(self.schools)} schools to csv file "{filename}"')

        if append:
            mode = 'w+'
        else:
            mode = 'w'

        with open(EXPORT_DIRECTORY + filename, mode) as file:
            self._append_header_to_file(file)
            for school in self.schools:
                self._append_school_to_file(file, school)

    def _append_header_to_file(self, file):
        file.write(self.delimiter.join(HEADER) + self.newline)

    def _append_school_to_file(self, file, school):
        school_fields = [
            school.get_name(),
            school.get_address(),
            school.get_postal_code(),
            school.get_city(),
            school.get_phone_number()
        ]
        file.write(self.delimiter.join(school_fields) + self.newline)
