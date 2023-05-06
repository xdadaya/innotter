#FROM public.ecr.aws/docker/library/python:3.10
FROM python:3.10
ENV DockerHOME=/app
RUN apt-get update && apt-get install -y dos2unix
RUN mkdir -p $DockerHOME

WORKDIR $DockerHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock ./
COPY innotter/producer.py ./producer.py
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy


COPY . $DockerHOME
# run this command to install all dependencies
RUN pipenv


ADD run_server.sh /run_server.sh
ADD celery_entrypoint.sh /celery_entrypoint.sh
ADD producer_entrypoint.sh /producer_entrypoint.sh
RUN chmod a+x /run_server.sh /celery_entrypoint.sh /producer_entrypoint.sh
RUN dos2unix /run_server.sh /celery_entrypoint.sh /producer_entrypoint.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/run_server.sh"]
CMD ["run"]

