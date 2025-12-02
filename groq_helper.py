"""
Groq API Helper Module

This module provides a simple interface for interacting with the Groq API
for chat completions and other AI tasks.

Usage:
    from groq_helper import GroqClient
    from config_env import load_environment, get_api_key
    
    # Load environment and get API key
    load_environment()
    api_key = get_api_key('GROQ_API_KEY')
    
    # Initialize client
    client = GroqClient(api_key)
    
    # Send a chat message
    response = client.chat("Hello, how are you?")
    print(response)
"""

import os
import json
import requests
from typing import List, Dict, Optional


class GroqClient:
    """
    A client for interacting with the Groq API.
    """
    
    BASE_URL = "https://api.groq.com/openai/v1"
    DEFAULT_MODEL = "mixtral-8x7b-32768"  # Fast and capable model
    
    # Available models
    MODELS = {
        "mixtral": "mixtral-8x7b-32768",  # Fast, good for most tasks
        "llama3-70b": "llama3-70b-8192",  # Most capable
        "llama3-8b": "llama3-8b-8192",    # Fastest, good for simple tasks
        "gemma-7b": "gemma-7b-it",        # Google's open model
    }
    
    def __init__(self, api_key: str, model: str = None):
        """
        Initialize the Groq client.
        
        Args:
            api_key: Your Groq API key
            model: Model to use (default: mixtral-8x7b-32768)
        """
        self.api_key = api_key
        self.model = model or self.DEFAULT_MODEL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(
        self, 
        message: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Send a chat message to Groq API.
        
        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set behavior
            temperature: Controls randomness (0.0 to 2.0)
            max_tokens: Maximum tokens in response
            conversation_history: Previous messages for context
            
        Returns:
            The assistant's response text
            
        Example:
            >>> client = GroqClient(api_key)
            >>> response = client.chat("What is the capital of France?")
            >>> print(response)
        """
        # Build messages array
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })
        
        # Make API request
        response = self._make_request(
            endpoint="/chat/completions",
            data={
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        )
        
        # Extract and return response text
        return response["choices"][0]["message"]["content"]
    
    def chat_stream(
        self, 
        message: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ):
        """
        Send a chat message with streaming response.
        
        Args:
            message: The user message to send
            system_prompt: Optional system prompt
            temperature: Controls randomness
            max_tokens: Maximum tokens in response
            
        Yields:
            Chunks of the response as they arrive
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": message
        })
        
        url = f"{self.BASE_URL}/chat/completions"
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }
        
        response = requests.post(
            url, 
            headers=self.headers, 
            json=data, 
            stream=True
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    line = line[6:]  # Remove 'data: ' prefix
                    if line == '[DONE]':
                        break
                    try:
                        chunk = json.loads(line)
                        if 'choices' in chunk and len(chunk['choices']) > 0:
                            delta = chunk['choices'][0].get('delta', {})
                            content = delta.get('content', '')
                            if content:
                                yield content
                    except json.JSONDecodeError:
                        continue
    
    def _make_request(self, endpoint: str, data: dict) -> dict:
        """
        Make a request to the Groq API.
        
        Args:
            endpoint: API endpoint (e.g., '/chat/completions')
            data: Request payload
            
        Returns:
            Response JSON as dictionary
            
        Raises:
            requests.exceptions.HTTPError: If request fails
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        response = requests.post(
            url,
            headers=self.headers,
            json=data
        )
        
        # Raise exception for bad status codes
        response.raise_for_status()
        
        return response.json()
    
    def set_model(self, model: str):
        """
        Change the model used for requests.
        
        Args:
            model: Model name (use MODELS dict for available options)
            
        Example:
            >>> client.set_model(GroqClient.MODELS["llama3-70b"])
        """
        self.model = model


# Example usage and testing
if __name__ == "__main__":
    from config_env import load_environment, get_api_key
    
    print("=" * 60)
    print("Groq API Client Test")
    print("=" * 60)
    
    # Load environment and get API key
    load_environment()
    
    try:
        api_key = get_api_key('GROQ_API_KEY')
        print("✓ API key loaded successfully\n")
        
        # Initialize client
        client = GroqClient(api_key)
        print(f"✓ Client initialized with model: {client.model}\n")
        
        # Test simple chat
        print("Testing simple chat:")
        print("-" * 60)
        response = client.chat(
            message="What is 2+2? Reply in one short sentence.",
            temperature=0.1
        )
        print(f"Response: {response}\n")
        
        # Test with system prompt
        print("Testing with system prompt:")
        print("-" * 60)
        response = client.chat(
            message="Analyze this building defect: major crack",
            system_prompt="You are a structural engineer assistant. Provide concise analysis.",
            temperature=0.3
        )
        print(f"Response: {response}\n")
        
        # Test streaming
        print("Testing streaming response:")
        print("-" * 60)
        print("Response: ", end="", flush=True)
        for chunk in client.chat_stream(
            message="Count from 1 to 5 slowly.",
            temperature=0.1
        ):
            print(chunk, end="", flush=True)
        print("\n")
        
        print("=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
        
    except ValueError as e:
        print(f"✗ Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file in the project root")
        print("2. Added GROQ_API_KEY=your_key_here to the .env file")
        print("3. Get your free API key from: https://console.groq.com/")
    except requests.exceptions.HTTPError as e:
        print(f"✗ API Error: {e}")
        print("Please check your API key is valid")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
