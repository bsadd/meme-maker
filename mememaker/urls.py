"""mememaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from mememaker import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include('memesbd.urls'), name='home'),
    path(r'accounts/', include('accounts.urls'), name="accounts"),
    path('accounts/', include('allauth.urls')),

    path('api/', include(('coreapp.urls', 'coreapp'), namespace='api')),
    path(r'rest-auth/', include(('rest_auth.urls', 'rest_auth'), namespace='rest-auth')),  # rest_login
    path(r'rest-auth/registration/', include(('rest_auth.registration.urls', 'rest_auth'),
                                             namespace='rest-auth-registration')),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
