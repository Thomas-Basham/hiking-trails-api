# pull official base image
FROM python:3.10.4-alpine3.16
# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
RUN apk --update add --no-cache g++

RUN apk update \
    && apk add --virtual build-essential gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2
 # install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --upgrade cython
#RUN pip3 install pandas numpy
RUN pip install -r requirements.txt --no-deps

# copy project
COPY . .

# collect static files
#RUN python3 manage.py collectstatic --noinput

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# run gunicorn
CMD gunicorn hiking_trails_api_project.wsgi:app --bind 0.0.0.0:8000
