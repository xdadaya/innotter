#!/bin/sh
pipenv run celery -A innotter worker -l INFO