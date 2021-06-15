from celery import shared_task
from csv_project.celery import app

import csv
import random
import string
from csv_project import settings
from .models import Schema, Column, Dataset

from faker import Faker
fake = Faker()
fake_ru = Faker('ru_RU')


@app.task
def write_csv(dataset_id):

    dataset = Dataset.objects.filter(id=dataset_id).first()
    if not dataset:
        return
    schema = Schema.objects.filter(id=dataset.schema_id).first()
    columns = Column.objects.filter(schema=schema.id).values()
    delimeter = schema.column_separator
    quotechar = schema.string_character
    row_number = dataset.row

    header = []
    all_rows = []

    for column in columns:
        header.append(column["name"])

    for row in range(row_number):
        raw_row = []
        for column in columns:
            column_type = column["column_type"]
            if column_type == Column.FULL_NAME:
                data = fake.name()
            elif column_type == Column.JOB:
                data = fake.job()
            elif column_type == Column.EMAIL:
                data = fake.email()
            elif column_type == Column.DOMAIN_NAME:
                data = fake.domain_name()
            elif column_type == Column.PHONE_NUMBER:
                data = fake.phone()
            elif column_type == Column.COMPANY_NAME:
                data = fake.company()
            elif column_type == Column.TEXT:
                data = fake.sentences(
                    nb=fake.random_int(
                        min=column["range_from"] or 1,
                        max=column["range_to"] or 10
                    )
                )
                data = " ".join(data)

            elif column_type == Column.INTEGER:
                data = fake.random_int(
                    min=column["range_from"] or 0,
                    max=column["range_to"] or 999
                )
            elif column_type == Column.ADDRESS:
                data = fake.address()
            elif column_type == Column.DATE:
                data = fake.date()
            else:
                data = None
            raw_row.append(data)

        all_rows.append(raw_row)

        with open(f'media/schema_{schema.id}dataset_{dataset_id}.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=delimeter,
                                quotechar=quotechar, quoting=csv.QUOTE_ALL)
            writer.writerow(header)
            writer.writerows(all_rows)

            dataset.status = dataset.Status.READY
            dataset.save()

        data = open(f'media/schema_{schema.id}dataset_{dataset_id}.csv', 'rb')
