from __future__ import unicode_literals

from django.template.loader import render_to_string

from services.hooks import ServicesHook
from alliance_auth import hooks

from .urls import urlpatterns


class MediawikiService(ServicesHook):
    def __init__(self):
        ServicesHook.__init__(self)
		self.name = 'mediawiki'
        self.urlpatterns = urlpatterns
        self.service_url = settings.MEDIAWIKI_URL

		def title(self):
		return 'Mediawiki Wiki'
    """
    Overload base methods here to implement functionality
    """

    def render_services_ctrl(self, request):
        """
        Example for rendering the service control panel row
        You can override the default template and create a
        custom one if you wish.
        :param request:
        :return:
        """
        urls = self.Urls()
        urls.auth_activate = 'auth_mediawiki_activate'
        urls.auth_deactivate = 'auth_mediawiki_deactivate'
        urls.auth_reset_password = 'auth_mediawiki_reset_password'
        urls.auth_set_password = 'auth_mediawiki_set_password'
        return render_to_string(self.service_ctrl_template, {
            'service_name': self.title,
            'urls': urls,
            'service_url': self.service_url,
            'username': request.user.mediawiki.username
        }, request=request)


@hooks.register('services_hook')
def register_service():
    return ExampleService()