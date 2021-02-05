from django.contrib import admin

# Register your models here.
from main.models import Schema, ColumnSchema, TypeField

admin.site.register(Schema)
admin.site.register(ColumnSchema)
admin.site.register(TypeField)