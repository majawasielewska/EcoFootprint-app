# carbon_footprint_website/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('calculate', views.calculate_footprint, name='calculate_footprint'),
    path('result/', views.result, name='result'),
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
]
