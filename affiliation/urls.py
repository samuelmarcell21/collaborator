from django.conf.urls import url

from . import views

urlpatterns =[
	url(r'^$',views.index),
	url(r'^(?P<id_univ>[0-9]+)/$', views.show_detailaffiliation),
]