"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from guestapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index),

    url(r'^movie/$', views.movie),
    url(r'^refresh_movie/$', views.refresh_movie),

    url(r'^music/$', views.music),

    url(r'^picture/$', views.picture),
    url(r'^refresh_picture/$', views.refresh_picture),

    url(r'^novel/$', views.novel),
    url(r'^refresh_novel/$', views.refresh_novel),
    url(r'^search_page/$', views.search_page),
    url(r'^search_novel/$', views.search_novel),

]
