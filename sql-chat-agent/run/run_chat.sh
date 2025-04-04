#!/bin/bash

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set"
    echo "Please set it using: export OPENAI_API_KEY='your-api-key-here'"
    exit 1
fi

# Print first 8 characters of API key for verification
echo "Using API key: ${OPENAI_API_KEY:0:8}..."

# Run the chat agent
python3 ../src/gpt_request.py 