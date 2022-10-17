#!/bin/bash
# Start the server
nohup uvicorn main:app --reload > log.txt &