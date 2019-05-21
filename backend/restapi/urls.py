"""restapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
#from appfront.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
 #   path('user/', include('users.urls')),
    path(r'user/', include('users.urls')),
    path(r'invoice/', include('invoices.urls')),
    path(r'contact/', include('contacts.urls')),
    #path('', index,name='index'),
]

if settings.DEBUG:
    urlpatterns = [
        path('admin/', admin.site.urls),
        #   path('user/', include('users.urls')),
        path('api/user/', include('users.urls')),
        path('api/invoice/', include('invoices.urls')),
        path('api/contact/', include('contacts.urls')),
        #path('', index,name='index'),
    ]