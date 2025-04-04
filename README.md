# SQL Chat Agent

A simple chat agent that uses OpenAI's API to generate SQL queries based on natural language questions.

## Features

- Interactive chat interface
- SQL query generation
- Retry logic for handling connection issues
- Configurable API settings

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key:
   ```
   export OPENAI_API_KEY="your-api-key-here"
   ```
4. Run the chat agent:
   ```
   cd run
   ./run_chat.sh
   ```

## Usage

- Type your questions about SQL queries
- The agent will generate SQL queries based on your questions
- Type 'exit' to quit the chat agent

## Requirements

- Python 3.6+
- OpenAI API key
- Required Python packages (see requirements.txt)
