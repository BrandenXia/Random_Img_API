#!/bin/bash
# Stop the server
kill "$(pgrep -f -l 'uvicorn main:app --port 8045 --reload' | awk '{print $1}')"