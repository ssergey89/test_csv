from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View


# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    # really low level
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is None:
                return render( request, 'login.html')
            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render( request, 'login.html')
            login(request, user)

            return redirect(reverse('home_page'))
        else:
            return render(request, 'login.html')


class LogoutSystem(LogoutView):

    next_page = 'login'
    template_name = 'login.html'
