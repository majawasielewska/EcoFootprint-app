# carbon_footprint_website/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculate_footprint, name='calculate_footprint'),
    path('result/', views.result, name='result'),
]
