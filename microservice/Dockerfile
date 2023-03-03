FROM public.ecr.aws/docker/library/python:3.10
ENV DockerHOME=/app/microservice
RUN apt-get update && apt-get install -y dos2unix
RUN mkdir -p $DockerHOME

WORKDIR $DockerHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy


COPY . $DockerHOME
COPY /microservice_entrypoint.sh /microservice_entrypoint.sh
RUN pipenv

ADD microservice_entrypoint.sh /microservice_entrypoint.sh
RUN chmod a+x /microservice_entrypoint.sh
RUN dos2unix /microservice_entrypoint.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*
