"""
Configuración de URLs para la aplicación app_1.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('', views.page_login, name='page_login'),
    path('login/', views.page_login, name='login'),
    path('register/', views.page_register, name='page_register'),
    path('logout/', views.user_logout, name='logout'),

    # Verificación de email
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),

    # Restablecimiento de contraseña
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset-confirm/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),

    # Dashboard (protegido)
    path('dashboard/', views.dashboard, name='dashboard'),

    # Gestión de sesiones
    path('terminate-session/<str:session_key>/', views.terminate_session, name='terminate_session'),
]