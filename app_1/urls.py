from django.urls import path
from . import views

urlpatterns = [
    path('app_1/', views.app_1, name='app_1'),
]