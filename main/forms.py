from django.forms import ModelForm, ModelMultipleChoiceField

from main.models import Schema, ColumnSchema, Separator, Character, ManageSchema


class SchemaForm(ModelForm):
    class Meta:
        model = Schema
        fields = ['name', 'separator_id', 'character_id']


class ColumnSchemaForm(ModelForm):
    class Meta:
        model = ColumnSchema
        fields = ['name_column', 'schema_id', 'type_field_id', 'from_value', 'to_value']


class ManageSchemaForm(ModelForm):
    class Meta:
        model = ManageSchema
        fields = ['schema_id', 'status', 'rows']
