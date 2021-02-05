from django.contrib.auth import views as auth_views
from django.urls import path

from user import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutSystem.as_view(), name='logout'),
]
