#!/bin/bash

SKIP_QUESTIONS="$1" # executes everything without prompting the user

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

# Allow the user to turn off Ollama's service (not the container version)
if systemctl is-active --quiet ollama; then

    if [[ "$SKIP_QUESTIONS" =~ ^[yY]$ ]]; then
        read -p "Ollama service is running. Do you want to stop it? (y/n): " answer
    fi

    if [[ "$SKIP_QUESTIONS" =~ [yY]$ || "$answer" =~ ^[yY]$ ]]; then
        echo "[INFO] Stopping Ollama..."
        sudo systemctl stop ollama
        echo "[INFO] Ollama service has been stopped."
    fi
else
    echo "[INFO] Ollama service is not running."
fi

# Make sure the needed names are available
detect_and_stop_same_container_name "ollama-container"
detect_and_stop_same_container_name "lexigraph-api-ollama"
detect_and_stop_same_container_name "lexigraph-website"