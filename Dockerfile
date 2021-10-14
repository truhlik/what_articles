FROM python:3.9-slim-buster
EXPOSE 8000

# set the working directory
WORKDIR /app
# copy the repository files to it
COPY . /app

RUN pip install -r requirements-prod.txt
RUN chmod 755 start.sh
CMD ["/app/start.sh"]
