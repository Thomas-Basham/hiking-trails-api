# pull official base image
#FROM python:3.9-alpine
FROM python:3.10

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

#RUN pip install --upgrade pip
# install psycopg2
RUN && add --virtual build-essential gcc python3-dev musl-dev \
    && add postgresql-dev \
    && pip install psycopg2
 # install dependencies
COPY ./requirements.txt .
RUN pip install psycopg2
RUN pip install --upgrade cython
RUN pip install pandas
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
#RUN python3 manage.py collectstatic --noinput

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# run gunicorn
CMD gunicorn hiking_trails_api_project.wsgi:application --bind 0.0.0.0:8000
