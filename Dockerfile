FROM ubuntu:quantal
MAINTAINER Laurens Van Houtven, _@lvh.io

RUN apt-get update # 4 Mar 2014 17:07
RUN apt-get install -y python-setuptools python-pip git build-essential python-dev libffi-dev
RUN pip install tox

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:chris-lea/node.js
RUN apt-get update
RUN apt-get install -y nodejs ruby-compass

RUN apt-get install -y authbind
WORKDIR /etc/authbind
RUN touch 80 443
RUN chmod 777 80 443

RUN git clone https://github.com/crypto101/website.git /var/website # 10 Mar 2014 13:35

WORKDIR /var/website/static
RUN npm install -g grunt-cli 2>&1
RUN npm install 2>&1 # 4 Mar 2014 17:07
RUN grunt build

WORKDIR /var/website
RUN tox -e py27

RUN apt-get remove -y python-setuptools python-pip git build-essential python-dev libffi-dev
RUN apt-get remove -y nodejs ruby-compass
RUN apt-get -y autoremove

RUN chown -R nobody /var/website

ENV CERTIFICATE_PATH /var/website/local/cert-chain.pem
ENV STATIC_PATH /var/website/static/dist
EXPOSE 80 443
VOLUME ["/var/website/local"]
USER nobody
ENTRYPOINT /var/website/run
