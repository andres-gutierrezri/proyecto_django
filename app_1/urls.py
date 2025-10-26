from django.urls import path
from . import views

urlpatterns = [
    # Ruta original con plantilla básica
    path('', views.page_login, name='page_login'),
    path('register/', views.page_register, name='page_register'),
]