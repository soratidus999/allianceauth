#!/bin/sh

cd /home/allianceserver/

allianceauth start myauth

cd /home/allianceserver/myauth/

#replace DB settings
sed -i "s@    'USER': '',@    'USER': 'username',@" /home/allianceserver/myauth/myauth/settings/local.py
sed -i "s@    'PASSWORD': '',@    'USER': 'password',@" /home/allianceserver/myauth/myauth/settings/local.py

#configure SSO and email, pass these through from arguments? or build doc?
# @ is used as sed delimiter, will break if @ is used in SSO token, check if possible
sed -i "s@ESI_SSO_CLIENT_ID = ''@ESI_SSO_CLIENT_ID = ''@" /home/allianceserver/myauth/myauth/settings/local.py
sed -i "s@ESI_SSO_CLIENT_SECRET = ''@ESI_SSO_CLIENT_SECRET = ''@" /home/allianceserver/myauth/myauth/settings/local.py
sed -i "s@ESI_SSO_CALLBACK_URL = ''@ESI_SSO_CALLBACK_URL = ''@" /home/allianceserver/myauth/myauth/settings/local.py

# email config
# email config
# email config
# email config

#migration requires valid SSO from here down.
python manage.py migrate

#collect static files and take ownership.
mkdir -p /var/www/myauth/static
python manage.py collectstatic
chown -R www-data:www-data /var/www/myauth/static

#grant allianceserver rights, processes should run from now via supervisor as allianceserver
chown -R allianceserver:allianceserver /home/allianceserver/myauth
