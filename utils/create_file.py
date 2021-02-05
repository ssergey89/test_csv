import csv
import random
import string
import datetime

from main.models import ColumnSchema


class CsvFile:

    def __init__(self, process):
        self.proc = process
        self.schema = process.schema_id
        self.rows = process.rows
        self.separator = process.schema_id.separator_id.value
        self.character = process.schema_id.character_id.value

    def generate_text(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def generate_range_text(self, range):
        ket = random.randrange(0, range)
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=ket))

    def generate_number(self, start, end):
        return random.randrange(start, end)

    def create(self):
        name = datetime.datetime.now().timestamp()
        list_column = ColumnSchema.objects.filter(schema_id=self.schema)
        with open(f'media/csv_file|{name}.csv', 'w', newline='') as csv_file:
            f_csv = csv.writer(csv_file, delimiter=self.separator, doublequote='``', quoting=csv.QUOTE_MINIMAL)
            f_csv.writerow([col.name_column for col in list_column])
            for i in range(int(self.rows)):
                new_row = []
                for column in list_column:
                    if column.type_field_id.id == 7:
                        new_row.append(self.generate_range_text(column.to_value))
                    elif column.type_field_id.id == 8:
                        new_row.append(self.generate_number(column.from_value, column.to_value))
                    else:
                        new_row.append(self.generate_text())
                f_csv.writerow(new_row)
        self.proc.status = True
        self.proc.path_file = f'media/csv_file|{name}.csv'
        self.proc.save()
        return f'media/csv_file|{name}.csv'
