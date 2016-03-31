"""sgpa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sgpa/', include('sgpa2016.urls',namespace="sgpa2016")),
    
    url(r'^$', 'sgpa2016.views.inicio'),
    url(r'^ingresar/$','sgpa2016.views.ingresar'),
    url(r'^index/$','sgpa2016.views.index'),
    url(r'^cerrar/$', 'sgpa2016.views.cerrar'),
    url(r'^creditos/$', 'sgpa2016.views.creditos'),
]
