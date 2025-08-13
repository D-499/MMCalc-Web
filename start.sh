#!/bin/bash
# Start script for Render deployment
export PORT=${PORT:-5000}
gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 main:app