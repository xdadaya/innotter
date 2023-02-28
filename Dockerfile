# base image
FROM public.ecr.aws/docker/library/python:3.11
# setup environment variable
ENV DockerHOME=/app
#RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev
RUN apt-get update && apt-get install -y dos2unix
# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy


# copy whole project to your docker home directory.
COPY . $DockerHOME
# run this command to install all dependencies
RUN pipenv


ADD run_server.sh /run_server.sh
RUN chmod a+x /run_server.sh
RUN dos2unix /run_server.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/run_server.sh"]
CMD ["run"]

