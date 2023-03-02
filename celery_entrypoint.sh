#!/bin/sh

celery -A innotter worker -l info

exec "$@"