#!/bin/bash
# Stop the server
kill "$(pgrep -o -f -l 'python run.py' | awk '{print $1}')"