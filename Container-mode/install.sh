#!/bin/bash

#TODO run with "bash install.sh -y"

SKIP_QUESTIONS="$1"

# Function to detect and stop a Docker container with the same name
function detect_and_stop_same_container_name() {
    local TARGET_CONTAINER="$1"
    if sudo docker ps -a --format "{{.Names}}" | grep -q "^$TARGET_CONTAINER$"; then
        echo "There's already a container with the name: $TARGET_CONTAINER"

        if [[ "$SKIP_QUESTIONS" =~ ^[yY]$ ]]; then
            read -p "Remove it and build a new one? (y/n): " answer
        fi

        if [[ "$SKIP_QUESTIONS" =~ [yY]$ || "$answer" =~ ^[yY]$ ]]; then
            echo "Removing the container '"$TARGET_CONTAINER"'"
            sudo docker stop "$TARGET_CONTAINER"
            sudo docker rm "$TARGET_CONTAINER"
        else
            echo "Exiting without removing the existing container."
            exit 1
        fi
    fi
}

# Make sure the needed names are available
detect_and_stop_same_container_name "ollama-container"
detect_and_stop_same_container_name "lexigraph-api-ollama"
detect_and_stop_same_container_name "lexigraph-website"