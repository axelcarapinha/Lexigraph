#!/usr/bin/env bash

export OLLAMA_HOST=0.0.0.0
ollama serve &
ollama list
ollama pull llama3
ollama run llama3