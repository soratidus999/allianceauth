import random
import string
import requests
import logging
from django.conf import settings


logger = logging.getLogger(__name__)

# Activate, Create service account

	@staticmethod
	def __sanitize_username(username):
		sanitized = username #check mediawiki requirements, here as placeholder
		return sanatized.lower() #but i mean who doesnt like lowering their cases
	
	def add_user(username,password,email="",realname="", logout=True):
	logger.debug("Adding mediawiki user with username #s, email %s, groups %s" % (
		username, email, groups))
		username_clean = MediawikiManager.__sanitize_username(username)
		request_create_token_data = {'action': 'query', 'format': 'json', 'meta': 'tokens', 'type': 'createaccount'}
		request_create_token = requests.post(settings.MEDIAWIKI_URL + 'api.php', data=request_create_token_data)
		create_token = request_create_token.json()['query']['tokens']['createaccounttoken']
		request_adduser_data = {'action': 'createaccount','format': 'json', 'username': __sanitize_username(username),'password': password,'retype': password,'email': email,'realname': realname,'createreturnurl': settings.MEDIAWIKI_URL,'createtoken': create_token}
		response = requests.post(settings.MEDIAWIKI_URL + 'api.php', data=request_adduser_data,cookies=request_create_token.cookies)
		if response['createaccout']['status'] = 'FAIL'
			return 'FAIL'
		else
			return 'PASS'

	

# Deactivate, delete service account i think this is block on mediawiki?

def disable_user

def delete_user

# Reset Password

# Set Password