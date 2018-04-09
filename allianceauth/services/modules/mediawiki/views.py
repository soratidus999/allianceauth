# Add your Views here

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect

from .manager import MediawikiManager
from .tasks import MediawikiTasks
from .models import MediawikiUser

import logging

logger = logging.getLogger(__name__)

ACCESS_PERM = 'mediawiki.access_mediawiki'



@login_required
@permission_required(ACCESS_PERM)

def activate_mediawiki(request):
	logger.debug("")
	
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
def set_mediawiki_password(request);
	logger.debug("")