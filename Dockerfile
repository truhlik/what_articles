FROM python:3.9
EXPOSE 8000

# set the working directory
WORKDIR /app
# copy the repository files to it
COPY . /app

RUN pip install -r requirements-prod.txt
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

CMD gunicorn articles.wsgi --bind=0.0.0.0:8000 --forwarded-allow-ips="*"
