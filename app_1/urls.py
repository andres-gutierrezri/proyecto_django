from django.urls import path
from . import views

urlpatterns = [
    # Ruta original con plantilla básica
    path('', views.app_1, name='app_1'),
]