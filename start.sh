#!/bin/bash
# Create log directory if not already existed
[ -d ./logs ] || mkdir ./logs
# Get current date and time
now=$(date +"%Y-%m-%d %H:%M")
# Start the server
nohup uvicorn main:app --port 8045 --reload > ./logs/"$now".log 2>&1 &