FROM python:3.8

# Environment variables
#ENV REDIS_END='redis'
#ENV REDIS_PORT=6379
#ENV RQ_NAME='edeservice'
#ENV EDE_HOST='0.0.0.0'
#ENV EDE_PORT=5001

EXPOSE 5001

RUN mkdir /edeservice
WORKDIR /edeservice

RUN apt-get update

COPY requirements_service.txt /edeservice/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /edeservice

CMD ["python", "service/run.py"]