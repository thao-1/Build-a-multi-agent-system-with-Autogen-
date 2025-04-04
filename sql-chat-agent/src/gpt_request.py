#!/usr/bin/env python3
import argparse
from openai import OpenAI
import json
import os
import sys
import httpx
import time

def main():
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set")
        sys.exit(1)
    
    print(f"Using API key: {api_key[:8]}...")  # Print first 8 chars for verification
    
    # Initialize the OpenAI client
    try:
        # Create a custom HTTP client without proxy settings
        http_client = httpx.Client(
            timeout=60.0,  # Increased timeout
            verify=True
        )
        
        # Initialize the client with the standard OpenAI client
        client = OpenAI(
            api_key=api_key,
            http_client=http_client
        )
        
        # Test the connection
        print("Testing API connection...")
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": "Test connection"}],
            max_tokens=5
        )
        print("API connection successful!")
        
    except Exception as e:
        print(f"\nError initializing API client: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Verify your API key is correct")
        print("2. Check if the API endpoint is accessible")
        print("3. Ensure you have proper network connectivity")
        print("4. Verify the API version is supported")
        sys.exit(1)

    # Simple chat loop
    print("\nChat Agent (type 'exit' to quit)")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
            
        # Add retry logic for API calls
        max_retries = 3
        retry_count = 0
        success = False
        
        while retry_count < max_retries and not success:
            try:
                # Create a chat completion
                response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant specializing in SQL query generation."},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                # Print the response
                print("\nAssistant:", response.choices[0].message.content)
                success = True
                
            except Exception as e:
                retry_count += 1
                print(f"\nError during API call (attempt {retry_count}/{max_retries}): {str(e)}")
                
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count  # Exponential backoff
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("\nTroubleshooting tips:")
                    print("1. Check your internet connection")
                    print("2. Verify the API endpoint is responding")
                    print("3. Ensure your API key has sufficient permissions")
                    print("4. Check if you've exceeded API rate limits")
                    print("5. Try increasing your API usage limit in your account settings")
    
    # Close the HTTP client when done
    http_client.close()

if __name__ == "__main__":
    main()
