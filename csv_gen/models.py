from django.db import models
#from users.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()


class Schema(models.Model):

    COMMA = ','
    SEMICOLON = ';'
    DOUBLEQUOTE = '"'
    SINGLEQUOTE = "'"

    COLUMN_CHOICES = [
        (COMMA, 'Comma (,)'),
        (SEMICOLON, 'Semicolon (;)')
    ]
    STRING_CHOICES = [
        (DOUBLEQUOTE, 'Double-quote (")'),
        (SINGLEQUOTE, "Single-quote (')")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    column_separator = models.CharField(
        choices=COLUMN_CHOICES, default=COMMA, max_length=10)
    string_character = models.CharField(
        choices=STRING_CHOICES, default=DOUBLEQUOTE, max_length=10)
    modified = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


class Column(models.Model):

    FULL_NAME = 'Full name'
    JOB = 'Job'
    EMAIL = 'Email'
    DOMAIN_NAME = 'Domain name'
    PHONE_NUMBER = 'Phone number'
    COMPANY_NAME = 'Company name'
    TEXT = 'Text'
    INTEGER = 'Integer'
    ADDRESS = 'Address'
    DATE = 'Date'

    COLUMN_CHOICES = [
        (FULL_NAME, 'Full name'),
        (JOB, 'Job'),
        (EMAIL, 'Email'),
        (DOMAIN_NAME, 'Domain name'),
        (PHONE_NUMBER, 'Phone number'),
        (COMPANY_NAME, 'Company name'),
        (TEXT, 'Text'),
        (INTEGER, 'Integer'),
        (ADDRESS, 'Address'),
        (DATE, 'Date')
    ]

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    range_from = models.IntegerField(null=True, blank=True)
    range_to = models.IntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(null=True)
    column_type = models.CharField(
        choices=COLUMN_CHOICES, default=TEXT, max_length=20)


class Dataset(models.Model):
    class Status(models.TextChoices):
        READY = 'Ready'
        PROCESSING = "Processing"

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    row = models.IntegerField(null=True)
    status = models.CharField(max_length=15, choices=Status.choices)
