#!/bin/bash
# Start the server
nohup uvicorn main:app --port 8045 --reload > log.txt &