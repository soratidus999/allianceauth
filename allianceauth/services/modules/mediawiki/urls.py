from django.conf.urls import url, include

from . import views

app_name - 'mediawiki'

module_urls = [
    # mediawiki Service Control
    url(r'^activate/$', views.activate_mediawiki, name='activate'),
    url(r'^deactivate/$', views.deactivate_mediawiki, name='deactivate'),
    url(r'^reset_password/$', views.reset_mediawiki_password, name='reset_password'),
    url(r'^set_password/$', views.set_mediawiki_password, name='set_password'),
]

urlpatterns = [
    url(r'^mediawiki/', include((module_urls, app_name), namespace=app_name))
]
