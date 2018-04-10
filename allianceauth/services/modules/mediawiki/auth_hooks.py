import logging

from django.conf import settings
from django.template.loader import render_to_string

from allianceauth import hooks
from allianceauth.services.hooks import ServicesHook

from .tasks import MediawikiTasks
from .models import MediawikiUser
from .urls import urlpatterns

logger = logging.getLogger(__name__)

class MediawikiService(ServicesHook):
    def __init__(self):
        ServicesHook.__init__(self)
        self.name = 'mediawiki'
        self.urlpatterns = urlpatterns
        self.service_url = settings.MEDIAWIKI_URL
        self.access_perm = 'mediawiki.access_mediawiki'
        self.service_ctrl_template = 'services/mediawiki/mediawiki_service_ctrl.html'
    """
    Overload base methods here to implement functionality
    """

    def render_services_ctrl(self, request):
        urls = self.Urls()
        urls.auth_activate = mediawiki:activate
        urls.auth_deactivate = mediawiki:deactivate
        urls.auth_reset_password = mediawiki:reset_password
        urls.auth_set_password = mediawiki:set_password
        return render_to_string(self.service_ctrl_template, {
            'service_name': self.title,
            'urls': urls,
            'service_url': self.service_url,
            'username': request.user.mediawiki.username
        }, request=request)


@hooks.register('services_hook')
def register_mediawiki_service():
    return MediawikiService()