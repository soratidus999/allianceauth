from __future__ import unicode_literals
from django.conf.urls import url, include

from . import views

module_urls = [
    # Wiki Service Control
    url(r'^activate/$', views.activate_mediawiki, name='auth_activate_mediawiki'),
    url(r'^deactivate/$', views.deactivate_mediawiki, name='auth_deactivate_mediawiki'),
    url(r'^reset_password/$', views.reset_mediawiki_password, name='auth_reset_mediawiki_password'),
    url(r'^set_password/$', views.set_mediawiki_password, name='auth_set_mediawiki_password'),
]

urlpatterns = [
    url(r'^mediawiki/', include(module_urls)),
]
