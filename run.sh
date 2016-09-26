#!/usr/bin/env sh
celery -A tasks worker --loglevel=info --concurrency=16