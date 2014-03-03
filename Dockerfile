FROM ubuntu
MAINTAINER Laurens Van Houtven, _@lvh.io

RUN apt-get update

RUN apt-get install -y python-setuptools python-pip git build-essential python-dev libffi-dev
RUN pip install tox
RUN git clone https://github.com/crypto101/website.git /var/website # 2014-03-03 17:22
WORKDIR /var/website
RUN tox -e py27

WORKDIR /var/website/static
RUN apt-get install -y npm
RUN npm install
RUN grunt build

RUN apt-get remove python-setuptools python-pip git build-essential python-dev libffi-dev
RUN apt-get remove npm

RUN mkdir /var/website/external
VOLUME ["/var/website/external"]
