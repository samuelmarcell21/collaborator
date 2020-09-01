from django.conf.urls import url

from . import views

urlpatterns =[
	url(r'^$',views.index),
	url(r'^(?P<nidn>[0-9]{10})/$', views.show_detailauthor),
	# url(r'^SVG/$',views.SVG),
	# url(r'^filter/$',views.filter),
	# url('ajax/',views.ajaxhome),
	# url('ajax/proses',views.ajaxproses),

	# url(r'^coba/$',views.coba),
]