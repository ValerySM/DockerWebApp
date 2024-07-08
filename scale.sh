#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <up|down>"
    exit 1
fi

# Image name
image_name="dockerwebapp-app" # Specify your application image name here

# Get the current number of containers based on the image name
current_scale=$(docker ps --filter "ancestor=${image_name}" --format '{{.ID}}' | wc -l)
echo "Current number of containers for the image ${image_name}: $current_scale"

# Determine the new scale
if [ "$1" = "up" ]; then
    new_scale=$((current_scale + 5))
elif [ "$1" = "down" ]; then
    new_scale=$((current_scale - 5))
    # Ensure the scale does not go below 1 (minimum count)
    if [ $new_scale -lt 1 ]; then
        new_scale=1
    fi
else
    echo "Invalid argument. Use 'up' or 'down'."
    exit 1
fi

echo "Scaling to $new_scale containers for the image ${image_name}..."

# Scale the app service
docker-compose up -d --scale app=$new_scale

echo "Containers for the image ${image_name} scaled from $current_scale to $new_scale."