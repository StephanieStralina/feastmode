from django.contrib.auth.views import LoginView
from django.shortcuts import render

# Create your views here.

class Home(LoginView):
    template_name = 'home.html'