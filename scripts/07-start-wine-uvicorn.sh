#!/bin/bash

source /scripts/02-common.sh

log_message "RUNNING" "07-start-wine-uvicorn.sh"

log_message "INFO" "Starting Uvicorn server in Wine environment..."

# Run the Uvicorn app using Wine's Python
wine python -m uvicorn /app/main:app --host 0.0.0.0 --port 5000 &

UVICORN_PID=$!

# Give the server some time to start
sleep 5

# Check if the Uvicorn server is running
if ps -p $UVICORN_PID > /dev/null; then
    log_message "INFO" "Uvicorn server in Wine started successfully with PID $UVICORN_PID."
else
    log_message "ERROR" "Failed to start Uvicorn server in Wine."
    exit 1
fi