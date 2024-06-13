from django.urls import path
from .views import register, CustomLoginView, CustomLogoutView
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
]


