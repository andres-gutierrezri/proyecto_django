from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.conf import settings

def page_login(request):
    """Vista original de app_1 con plantilla básica"""
    template = loader.get_template('app_1/page_login.html')
    return HttpResponse(template.render())

def page_register(request):
    """Vista original de page_register con plantilla básica"""
    template = loader.get_template('app_1/page_register.html')
    return HttpResponse(template.render())

