#!/bin/sh

python3 -m uvicorn microservice.main:app --reload --host 0.0.0.0 --port 5000

exec "$@"