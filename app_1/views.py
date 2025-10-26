from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.conf import settings

def app_1(request):
    """Vista original de app_1 con plantilla básica"""
    template = loader.get_template('home.html')
    return HttpResponse(template.render())
