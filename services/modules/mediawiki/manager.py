import random
import string
import requests
import logging
from django.conf import settings


logger = logging.getLogger(__name__)

# Activate, Create service account

	def sanitize_username(username):
		sanitized = username #check mediawiki requirements, here as placeholder
		return sanatized.lower() #but i mean who doesnt like lowering their cases
	
	def mediawiki_login():
		## Login Token
		request_login_token_data = {'action': 'query', 'format': 'json', 'meta': 'tokens', 'type': 'login'}
		request_login_token = requests.post(settings.MEDIAWIKI_URL, data=request_login_token_data)
		login_token = request_login_token.json()['query']['tokens']['logintoken']
		## Login Process
		request_login_data = {'action': 'login', 'format': 'json', 'lgname': settings.MEDIAWIKI_BOTUSERNAME, 'lgpassword': settings.MEDIAWIKI_BOTPASSWORD, 'lgtoken': login_token}
		request_login = requests.post(settings.MEDIAWIKI_URL + 'api.php', data=request_login_data, cookies=request_login_token.cookies)
		return request_login.cookies
	
	def add_user(username,password,email="",realname="", logout=True):
	logger.debug("Adding mediawiki user with username #s, email %s, groups %s" % (
		username, email, groups))
		username_clean = MediawikiManager.__sanitize_username(username)
		## Create Token
		request_create_token_data = {'action': 'query', 'format': 'json', 'meta': 'tokens', 'type': 'createaccount'}
		login_cookie = mediawiki_login()
		request_create_token = requests.post(settings.MEDIAWIKI_URL + 'api.php', data=request_create_token_data, cookies=login_cookie)
		create_token = request_create_token.json()['query']['tokens']['createaccounttoken']
		## Build Change Cookie
		create_cookie = login_cookie.copy()
		create_cookie.update(request_create_token.cookies)
		## Apply User Change
		request_adduser_data = {'action': 'createaccount','format': 'json', 'username': username,'password': password,'retype': password,'email': email,'realname': realname,'createreturnurl': settings.MEDIAWIKI_URL,'createtoken': create_token}
		if response['createaccout']['status'] = 'FAIL'
			return 'FAIL'
		else
			return 'PASS'

	

# Deactivate, delete service account i think this is block on mediawiki?

def disable_user

def delete_user

# Reset Password

# Set Password