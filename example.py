#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example script demonstrating how to use the SQL Chat Agent.
"""

import os
import sys
import json
import sqlite3
from pathlib import Path

# Add the parent directory to the path so we can import the sql-chat-agent module
sys.path.append(str(Path(__file__).parent))

# Import the SQL Chat Agent
try:
    from sql_chat_agent.src.agent import SQLChatAgent
except ImportError:
    print("Error: Could not import SQLChatAgent. Make sure you have installed the required dependencies.")
    print("Try running: pip install -r requirements.txt")
    sys.exit(1)

def main():
    """
    Main function demonstrating how to use the SQL Chat Agent.
    """
    # Check if OpenAI API key is set
    if "OPENAI_API_KEY" not in os.environ:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set it with: export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Initialize the SQL Chat Agent
    agent = SQLChatAgent(
        model="gpt-3.5-turbo",  # You can change this to gpt-4 if you have access
        temperature=0.0,
        max_tokens=1000,
        db_path="./data/dev_databases/sample/sample.sqlite",
        sql_dialect="SQLite"
    )
    
    # Example questions
    questions = [
        "What is the average age of users over 18?",
        "How many orders does each user have?",
        "What is the total spending for each user?"
    ]
    
    # Process each question
    for question in questions:
        print(f"\nQuestion: {question}")
        
        # Generate SQL query
        sql_query = agent.generate_sql(question)
        print(f"Generated SQL: {sql_query}")
        
        # Execute SQL query
        try:
            result = agent.execute_sql(sql_query)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error executing SQL: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    main() 