FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/backend

COPY .env .env
COPY calendar_app calendar_app
COPY manage.py manage.py 
COPY custom_auth custom_auth
COPY the_site the_site
COPY demos_news_app demos_news_app
COPY mail_app mail_app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

