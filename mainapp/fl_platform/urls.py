from django.contrib import admin
from django.urls import path, include
from social_django.urls import urlpatterns as social_django_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('mainapp.urls')),
    path('', include('social_django.urls', namespace='social'))
]
