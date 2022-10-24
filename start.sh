#!/bin/bash
# Get the current time
now=$(date +"%Y-%m-%d %H:%M")
# Start the server
nohup python run.py > ./logs/"$now".log 2>&1 &