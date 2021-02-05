from django.urls import path

from main import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='home_page'),
    path('generate', views.GeneratePage.as_view(), name='home_page'),
    path('download_file', views.download_file, name='home_page'),
    path('schema', views.ActionWithSchema.as_view(), name='new_schema'),
    path('add_column', views.AddColumn.as_view(), name='new_schema'),
]
