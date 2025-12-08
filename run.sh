#!/usr/bin/env bash
set -e

IMAGE_NAME=nfl-api

# Build the Docker image from the Dockerfile in this folder
docker build -t "$IMAGE_NAME" .

# Run the container on port 8080, using env vars from .env.example
docker run --rm -p 8080:8080 --env-file .env.example "$IMAGE_NAME"
