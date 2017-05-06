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
		## Login Token
		request_login_token_data = {'action': 'query', 'format': 'json', 'meta': 'tokens', 'type': 'login'}
		request_login_token = requests.post('http://127.0.0.1/mediawiki/api.php', data=request_login_token_data)
		login_token = request_login_token.json()['query']['tokens']['logintoken']
		## Login Process
		request_login_data = {'action': 'login', 'format': 'json', 'lgname': 'Admin@allianceauth', 'lgpassword': '3d4j5i3an2l4ci55s8qf6sca7jqbpg7m', 'lgtoken': login_token}
		request_login = requests.post('http://127.0.0.1/mediawiki/api.php', data=request_login_data, cookies=request_login_token.cookies)
		## Create Token
		request_create_token_data = {'action': 'query', 'format': 'json', 'meta': 'tokens', 'type': 'createaccount'}
		request_create_token = requests.post('http://127.0.0.1/mediawiki/api.php', data=request_create_token_data, cookies=request_login.cookies)
		create_token = request_create_token.json()['query']['tokens']['createaccounttoken']
		## Build Change Cookie
		create_cookie = request_login.cookies.copy()
		create_cookie.update(request_create_token.cookies)
		## Apply User Change
		request_adduser_data = {'action': 'createaccount','format': 'json', 'username': 'testuser2','password': 'password','retype': 'password','email': 'test@test.com','realname': 'realname','createreturnurl': 'http://example.com','createtoken': create_token}
		if response['createaccout']['status'] = 'FAIL'
			return 'FAIL'
		else
			return 'PASS'

	

# Deactivate, delete service account i think this is block on mediawiki?

def disable_user

def delete_user

# Reset Password

# Set Password