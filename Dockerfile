FROM python:3.11

WORKDIR ./

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get -y install postgresql-client

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./ ./

CMD ["python manage.py runserver 8080"]