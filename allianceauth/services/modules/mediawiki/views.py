from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect

from allianceauth.services.forms import ServicePasswordForm
from .manager import MediawikiManager
from .tasks import MediawikiTasks
from .models import MediawikiUser

import logging

logger = logging.getLogger(__name__)

ACCESS_PERM = 'mediawiki.access_mediawiki'


@login_required
@permission_required(ACCESS_PERM)

def activate_mediawiki(request):
    logger.debug("activate_mediawiki called by user %s" % request.user)
    character = request.user.profile.main_character
    logger.debug("Adding mediawiki user for user %s with main character %s" % (request.user, character))
    result = MediaiwkiManager.add_user(MediawikiTaks.get_username(request.user),password,request.user.email,MediawikiTaks.get_username(request.user), logout=True):
    
@login_required
@permission_required(ACCESS_PERM)
def deactivate_mediawiki(request):
    logged.debug("")

@login_required
@permission_required(ACCESS_PERM)
def reset_mediawiki_password(request):
    logger.debug("")


@login_required
@permission_required(ACCESS_PERM)
def set_mediawiki_password(request):
    logger.debug("")