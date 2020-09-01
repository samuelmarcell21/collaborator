from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('author/', include('author.urls')),
    path('affiliation/', include('affiliation.urls')),
    path('topic/', include('topic.urls')),
    path('search/', views.search),
    path('', views.index),
]
