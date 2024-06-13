from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calculate/', views.calculate_footprint, name='calculate_footprint'),
    path('result/', views.result, name='result'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('account/', views.account, name='account')
]
