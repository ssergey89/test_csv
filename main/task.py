import time

from main.models import ManageSchema
from testCSV.celery import app
from utils.create_file import CsvFile


@app.task(queue='csv_queue')
def generate_csv(val):
    schema = ManageSchema.objects.get(id=val)
    CsvFile(schema).create()
