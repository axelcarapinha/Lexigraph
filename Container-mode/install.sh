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

# Run Ollama's container
# sudo docker run -d -v ./ollama-data:/root/.ollama -p 0.0.0.0:11434:11434 --network=container-mode_lexigraph-network --name ollama-container ollama/ollama
# sudo docker run -d \
#   -v ./ollama-data:/root/.ollama \
#   -p 0.0.0.0:11434:11434 \
#   --network=container-mode_lexigraph-network \
#   --name ollama-container \
#   -e OLLAMA_HOST=0.0.0.0:11434 \
#   -e OLLAMA_ORIGINS=http://0.0.0.0:11434 \
#   ollama/ollama

# sudo docker exec -d ollama-container ollama run llama3



# # Pull the Ollama Docker image and run the container
# sudo docker pull ollama/ollama
# detect_and_stop_same_container_name "ollama"
# sudo docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
# sudo docker exec -it ollama ollama run llama3 # Pulls the model if needed

# # Build and run the Lexigraph API Docker container
# sudo docker build -t lexigraph-api-ollama .
# detect_and_stop_same_container_name "lexigraph-api-ollama"
# sudo docker run -d --name lexigraph-api-ollama -p 5050:5050 --network="host" lexigraph-api-ollama

#TODO consider a separate network