#!/usr/bin/env bash

# export OLLAMA_HOST="0.0.0.0:11434"
export OLLAMA_HOST=0.0.0.0
# export OLLAMA_ORIGINS="http://0.0.0.0:11434"
ollama serve &
ollama list
ollama pull llama3
ollama run llama3