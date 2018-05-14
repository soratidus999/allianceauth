#Using Python (from Ubuntu) as core
FROM python:3

# Update is neccessary for apt-get to find redis-server
RUN apt-get update
RUN apt-get -y install unzip git redis-server curl libssl-dev libbz2-dev libffi-dev supervisor

RUN adduser --disabled-login allianceserver

#no-cache-dir is top keep docker image small?
RUN pip install --no-cache-dir allianceauth gunicorn

#allianceauth needs to run inside path, no ability to set path yet.
RUN cd /home/allianceserver && allianceauth start myauth

#deleting lines 25to30 to comment out mySQL, sqllite3 will kick in, dont try to comment it was annoying...
RUN sed -i -e '25,33d' /home/allianceserver/myauth/myauth/settings/local.py

#configure SSO and email, pass these through from arguments? or build doc?
# @ is used as sed delimiter, will break if @ is used in SSO token, check if possible
RUN sed -i "s@ESI_SSO_CLIENT_ID = ''@ESI_SSO_CLIENT_ID = ''@" /home/allianceserver/myauth/myauth/settings/local.py
RUN sed -i "s@ESI_SSO_CLIENT_SECRET = ''@ESI_SSO_CLIENT_SECRET = ''@" /home/allianceserver/myauth/myauth/settings/local.py
RUN sed -i "s@ESI_SSO_CALLBACK_URL = ''@ESI_SSO_CALLBACK_URL = ''@" /home/allianceserver/myauth/myauth/settings/local.py

# email config
# email config
# email config
# email config

#migration requires valid SSO from here down.
RUN python /home/allianceserver/myauth/manage.py migrate

#collect static files and take ownership.
RUN mkdir -p /var/www/myauth/static
RUN python /home/allianceserver/myauth/manage.py collectstatic
RUN chown -R www-data:www-data /var/www/myauth/static

#grant allianceserver rights, processes should run from now via supervisor as allianceserver
RUN chown -R allianceserver:allianceserver /home/allianceserver/myauth

#supervisor gunicorn config has to be changed slightly to bind to all network interfaces, because docker
RUN sed -i "s@command=/usr/local/bin/gunicorn myauth.wsgi --workers=3 --timeout 120@command=/usr/local/bin/gunicorn myauth.wsgi --workers=3 --timeout 120 -b 0.0.0.0:8000@" /home/allianceserver/myauth/supervisor.conf
RUN ln -s /home/allianceserver/myauth/supervisor.conf /etc/supervisor/conf.d/myauth.conf

EXPOSE 8000
CMD ["/usr/bin/supervisord", "-n"]
