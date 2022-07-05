FROM python:3.9 AS requirements

ARG ENVIRONMENT

COPY ./requirements /requirements
WORKDIR /requirements
RUN pip3 install -r /requirements/requirements.txt

FROM requirements as final

COPY ./app /app/app
COPY ./setup.py /app 
COPY ./.env /app

WORKDIR /app

RUN pip3 install .