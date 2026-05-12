#!/bin/bash

# Start the API server in the background
uvicorn app.api:app --host 0.0.0.0 --port 8000 &

# Start the frontend server in the foreground
cd frontend && python -m http.server 8080
