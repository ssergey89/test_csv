import datetime
import json
import csv
import random
import string

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView
from django.views.generic.edit import DeletionMixin

from main.forms import SchemaForm, ColumnSchemaForm, ManageSchemaForm
from main.models import Schema, TypeField, ColumnSchema, Separator, Character, ManageSchema
from main.task import generate_csv
from utils.create_file import CsvFile


@method_decorator(login_required(login_url='/auth/login'), name='dispatch')
class IndexPage(View):
    def get(self, request):
        list_object = Schema.objects.all()
        return render(request, 'index.html', {'queryset': list_object})


@method_decorator(login_required(login_url='/auth/login'), name='dispatch')
class GeneratePage(CreateView):

    def get(self, request, *args, **kwargs):
        id_schema = request.GET.get('id', '')
        if id_schema != '':
            list_object = ManageSchema.objects.filter(schema_id=id_schema)
            print(list_object)
            return render(request, 'generate_dataset.html', {'queryset': list_object})
        else:
            return redirect('/')

    def post(self, request, *args, **kwargs):
        form = ManageSchemaForm({"schema_id": request.POST['id'], 'status': False, 'rows': int(request.POST['count_rows'])})
        if form.is_valid():
            schema = form.save()
            schema.save()
            generate_csv.apply_async((schema.id,), {}, queue='csv_queue')
        return JsonResponse({"status": 200})


@method_decorator(login_required(login_url='/auth/login'), name='dispatch')
class ActionWithSchema(CreateView, DeletionMixin):
    model = Schema

    def get(self, request, *args, **kwargs):
        id_schema = request.GET.get('id', '')
        list_separator = Separator.objects.all()
        list_character = Character.objects.all()
        list_column = ColumnSchema.objects.filter(schema_id_id=id_schema) if id_schema != '' else []
        schema_object = Schema.objects.get(id=id_schema) if id_schema != '' else {'name': '',
                                                                                  'type': '',
                                                                                  'character': ''}
        list_types = TypeField.objects.all()
        return render(request, 'schema.html', {"list_type": list_types,
                                               "list_column": list_column,
                                               "list_separator": list_separator,
                                               "list_character": list_character,
                                               "schema": schema_object})

    def post(self, request, *args, **kwargs):
        form = SchemaForm(request.POST)
        if form.is_valid():
            schema = form.save()
            schema.save()
            return JsonResponse({"status": 200, "id": schema.id})
        else:
            return JsonResponse({"status": 500})

    def put(self, *args, **kwargs):
        request = args[0]
        data = {x[0]: x[1] for x in [x.split("=") for x in request.body.decode("utf-8").split("&")]}
        save_data = data.copy()
        save_data.pop('id', None)
        save_data.pop('csrfmiddlewaretoken', None)
        instance = get_object_or_404(Schema, id=data['id'])
        form = SchemaForm(save_data or None, instance=instance)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": 200})
        else:
            return JsonResponse({"status": 500})

    def delete(self, request, *args, **kwargs):
        id = request.body.decode("utf-8").split('=')[1]
        ColumnSchema.objects.filter(schema_id_id=id).delete()
        Schema.objects.filter(id=id).delete()
        return JsonResponse({"status": 200})


@method_decorator(login_required(login_url='/auth/login'), name='dispatch')
class AddColumn(CreateView):
    model = ColumnSchema

    def post(self, request, *args, **kwargs):
        data_list = json.loads(request.POST['data'])
        x = ColumnSchema.objects.filter(schema_id_id=data_list[0]['schema_id'])
        x.delete()
        for column in data_list:
            form = ColumnSchemaForm(column)
            if form.is_valid():
                schema = form.save()
                schema.save()
        return JsonResponse({"status": 200})


def download_file(request):
    id = request.GET['id']
    object_schema = ManageSchema.objects.get(id=id)
    with open(object_schema.path_file, 'r') as file_Csv:
        response = HttpResponse(file_Csv.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + object_schema.path_file.split('/')[-1]
        return response
