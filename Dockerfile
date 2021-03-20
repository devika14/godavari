FROM python:3.8
COPY . /workdir
WORKDIR /workdir
RUN pip3 install -r requirements.txt 
RUN rm -rf /.cachec
ENV PYTHONUNBUFFERED=0
ENTRYPOINT FLASK_APP=app/routes.py flask run --host=0.0.0.0 -p 8080