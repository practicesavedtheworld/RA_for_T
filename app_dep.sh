#!/bin/bash

# After tests have been done it change in .env "MODE" param for connection to the
# correct database and start work normally

python3 mode_changer.py

alembic upgrade head

gunicorn main:app --workers=4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000