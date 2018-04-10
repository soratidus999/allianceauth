import random
import string
import requests
import logging
from django.conf import settings


logger = logging.getLogger(__name__)

# Activate, Create service account

class MediawikiManager:
        def __init__(self):
                pass
        
        def sanitize_username(username):
                #The list of illegal characters is as follows: #<>[]|{}, non-printable characters 0 through 31, and 'delete' character 127.
                sanitized = username #check mediawiki requirements, here as placeholder
                return sanatized.lower() #because why not, mediawiki does capitalize 1st fyi
	
        def generate_random_pass():
                return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
	
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
                username_clean = sanitize_username(username)
                ## Create Token
                request_create_token_data = {'action': 'query', 'format': 'json', 'meta': 'tokens', 'type': 'createaccount'}
                login_cookie = mediawiki_login()
                request_create_token = requests.post(settings.MEDIAWIKI_URL + 'api.php', data=request_create_token_data, cookies=login_cookie)
                create_token = request_create_token.json()['query']['tokens']['createaccounttoken']
                ## Build Change Cookie
                create_cookie = login_cookie.copy()
                create_cookie.update(request_create_token.cookies)
                ## Apply User Change
                request_adduser_data = {'action': 'createaccount','format': 'json', 'username': username_clean,'password': password,'retype': password,'email': email,'realname': realname,'createreturnurl': settings.MEDIAWIKI_URL,'createtoken': create_token}
                response = requests.post(settings.MEDIAWIKI_URL, data=request_adduser_data,cookies=create_cookie)
                if response['createaccout']['status'] == 'FAIL':
                        return 'FAIL'
                else:
                        return 'PASS'

# Deactivate, delete service account i think this is block on mediawiki?

        def disable_user(username,password):
                ## CSRF Token
                request_csrf_token_data = {'action': 'query', 'format': 'json', 'meta': 'tokens', 'type': 'csrftoken'}
                login_cookie = mediawiki_login()
                request_csrf_token = requests.post(settings.MEDIAWIKI_URL + 'api.php', data=request_csrf_token_data, cookies=login_cookie)
                csrf_token = request_csrf_token.json()['query']['tokens']['csrftoken']
                ## Build CSRF Cookie
                csrf_cookie = login_cookie.copy()
                csrf_cookie.update(request_csrf_token.cookies)
                ## Apply user block change
                request_blockuser_data = {'action': 'block', 'format': 'json', 'user': username, 'expiry': 'never', 'reason': 'AA Disable Account', 'token': csrf_token}
                response = requests.post(settings.MEDIAWIKI_URL, data=request_blockuser_data,cookies=csrf_cookie)

