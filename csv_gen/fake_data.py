import csv
import random
import string
from csv_project import settings
from .models import Schema, Column, Dataset

from faker import Faker
fake = Faker()
fake_ru = Faker('ru_RU')


# def random_name(*args):
#     return fake_ru.name()

# def random_phone(*args):
#     return fake_ru.phone_number()

# def random_job(*args):
#     return fake_ru.job()

# def random_address(*args):
#     return fake_ru.address()

# def random_company(*args):
#     return fake_ru.company()

# def random_date(*args):
#     return fake.date()

# def random_mail(*args):
#     return fake_ru.email()

# def random_domain(*args):
#     return fake.domain_name()

# def random_text(*args):
#     return fake_ru.text()

# # faker way with age
# def random_num(*args):
#     return fake.random_number(digits=2)

#     # simple way with age
# def random_age(min, max):
#     return random.randint(min, max)

# def random_int(col_filter):
#     nmb_to = col_filter.get('to', 100)
#     nmb_from = col_filter.get('from', 0)
#     return random.randint(nmb_from, nmb_to)

# FAKE_DATA = {
#     'Full name': random_name(),
#     'Job': random_job(),
#     'Email': random_mail(),
#     'Domain name': random_domain(),
#     'Phone number': random_phone(),
#     'Company name': random_company(),
#     'Text': random_text(),
#     'Integer': random_age(10, 15),
#     'Address': random_address(),
#     'Date': random_date(),
# }

# for k, v in dict(FAKE_DATA).items():
#     print("{}: {}".format(k, v))


# rows = int(10)


def write_csv(dataset_id):
    
    dataset = Dataset.objects.filter(id=dataset_id)
    schema = Schema.objects.filter(id=dataset.schema_id)
    columns = Column.objects.filter(schema=schema.id).values()
    delimeter = schema.column_separator
    quotechar = schema.string_character
    row_number = dataset.rows

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

        with open('schema.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=delimeter, quotechar=quotechar, quoting=csv.QUOTE_ALL)
            writer.writerow(header)
            writer.writerows(all_rows)

            dataset.is_ready = True
            dataset.save()
        
        data = open(f'{settings.MEDIA_ROOT}schema.csv', 'rb')