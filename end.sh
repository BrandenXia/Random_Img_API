#!/bin/bash
# Stop the server
kill $(ps aux | grep 'uvicorn main:app' | awk '{print $2}')