import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task

from allianceauth.notifications import notify
from allianceauth.services.hooks import NameFormatter
from .manager import MediawikiManager
from .models import MediawikiUser

logger = logging.getLogger(__name__)


class MediawikiTasks:
    def __init__(self):
        pass

    @staticmethod
    def get_username(user):
        from .auth_hooks import MediawikiService
        return NameFormatter(MediawikiService(), user).format_name()

    @staticmethod
    def has_account(user):
        try:
            return user.mediawiki.username != ''
        except ObjectDoesNotExist:
            return False