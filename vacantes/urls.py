from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('publicar/', views.publicar_vacantes, name='publicar_vacantes'),
]
