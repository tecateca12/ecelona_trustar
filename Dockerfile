#Pull minimalistic bitnami image
FROM bitnami/minideb:latest
MAINTAINER ecelona

# Install OS dependencies
RUN apt-get update && install_packages \
	python \
	python-dev \
  python3-dev \
	python-virtualenv \
	python-pip \
	virtualenv \
	git \
	libnss3 \
	xvfb \
  ffmpeg \
	gcc \
  wget \
  bzip2 \
  chromium \
  chromium-driver \
  curl \
  unzip \
  ca-certificates

RUN virtualenv --python=python3 .env

run /.env/bin/python -m pip install python-Levenshtein

RUN /.env/bin/python -m pip install lxml


# Set up argument variables
ARG env="prod"
ARG tp="Tests"
ARG s="Dockerfile"
ARG filt="None"
ENV environment=$env
ENV testpath=$tp
ENV secrets=$s
ENV filter=$filt

# Copy repository into docker image and set up python dependencies
RUN mkdir container
COPY . ./container/

# Run the tests with the specified environment

WORKDIR /container

#RUN rm -f /reports/*
RUN cp -f /usr/bin/chromedriver libs/chromedriver
RUN /.env/bin/python -m pip install -r requirements.txt
CMD ./../.env/bin/python runner.py -e $environment -f $filter $testpath
