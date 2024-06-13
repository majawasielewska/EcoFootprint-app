from django.contrib import admin
from django.urls import path, include
from carbon_footprint_website import views as footprint_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', footprint_views.home, name='home'),  # Ensure the home view is included
    path('ecofootprint/', include('carbon_footprint_website.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', footprint_views.signup, name='signup'),
  #  path('', include('carbon_footprint_website.urls')),
]
