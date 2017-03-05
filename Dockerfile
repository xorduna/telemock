

FROM ubuntu
MAINTAINER Xavier Orduña <xorduna@gmail.com>

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install python3 python3-pip git npm
ADD . /telemock
WORKDIR /telemock
RUN pip3 install -r requirements.txt
WORKDIR ./telemock
ENV C_FORCE_ROOT true
