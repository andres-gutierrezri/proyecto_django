from django.urls import path
from . import views

urlpatterns = [
    # Ruta original con plantilla básica
    path('app_1/', views.app_1, name='app_1'),
]