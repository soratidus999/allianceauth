#Using Python (from Ubuntu) as core
FROM python:3

RUN apt-get update
RUN apt-get -y install unzip curl libssl-dev libbz2-dev libffi-dev

#no-cache-dir is top keep docker image small?
RUN pip install --no-cache-dir allianceauth gunicorn

RUN adduser --disabled-login allianceserver

COPY startup.sh /root/startup.sh
RUN chmod +x /root/startup.sh

VOLUME /home/allianceauth/myauth
VOLUME /var/www/static/

ENTRYPOINT ["/bin/sh", "/root/startup.sh"]
