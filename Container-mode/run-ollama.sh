#!/usr/bin/env bash

export OLLAMA_HOST="0.0.0.0:11434"
export OLLAMA_ORIGINS="http://0.0.0.0:11434"
ollama serve &
ollama list
ollama pull llama3
ollama run llama3

echo "To the infinity, and beyond!"
while true; do
    sleep 3600
done