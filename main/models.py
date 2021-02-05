import pytz
from django.db import models
import datetime


# Create your models here.

class Schema(models.Model):
    name = models.CharField(max_length=50)
    modified = models.DateField(default=datetime.date.today)
    separator_id = models.ForeignKey('Separator', on_delete=models.CASCADE)
    character_id = models.ForeignKey('Character', on_delete=models.CASCADE)

    def __str__(self):
        return f'Schema (name={self.name})'


class TypeField(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'TypeField (name={self.name})'


class Separator(models.Model):
    title = models.CharField(max_length=50)
    value = models.CharField(max_length=5)

    def __str__(self):
        return f'Separator (name={self.title})'


class Character(models.Model):
    title = models.CharField(max_length=50)
    value = models.CharField(max_length=5)

    def __str__(self):
        return f'Character (name={self.title})'


class ColumnSchema(models.Model):
    name_column = models.CharField(max_length=250)
    schema_id = models.ForeignKey('Schema', on_delete=models.CASCADE)
    type_field_id = models.ForeignKey('TypeField', on_delete=models.CASCADE)
    from_value = models.IntegerField(null=True)
    to_value = models.IntegerField(null=True)

    def __str__(self):
        return f'ColumnSchema (name={self.schema_id.name}, column={self.type_field_id.name})'


class ManageSchema(models.Model):

    schema_id = models.ForeignKey('Schema', on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField()
    path_file = models.CharField(max_length=250, null=True)
    rows = models.IntegerField()

    def __str__(self):
        return f'ManageSchema (name={self.schema_id.name}, date={self.date})'
