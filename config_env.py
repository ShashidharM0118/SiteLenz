"""
Environment Variables Configuration for Python Applications

This module demonstrates how to properly load and use environment variables
in Python applications within this project.

Usage:
    from config_env import get_api_key
    
    api_key = get_api_key('GEMINI_API_KEY')
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
def load_environment():
    """
    Load environment variables from .env file in project root.
    Call this once at the start of your application.
    """
    # Get the project root directory
    env_path = Path(__file__).parent / '.env'
    
    # Load the .env file
    load_dotenv(dotenv_path=env_path)
    
    print(f"✓ Environment variables loaded from: {env_path}")


def get_api_key(key_name: str, required: bool = True) -> str:
    """
    Get an API key from environment variables.
    
    Args:
        key_name: Name of the environment variable
        required: If True, raises error when key is not found
        
    Returns:
        The API key value
        
    Raises:
        ValueError: If required=True and key is not found
        
    Example:
        >>> api_key = get_api_key('GEMINI_API_KEY')
        >>> print(f"Key found: {bool(api_key)}")
    """
    value = os.getenv(key_name)
    
    if required and not value:
        raise ValueError(
            f"Environment variable '{key_name}' not found!\n"
            f"Please ensure you have:\n"
            f"1. Created a .env file in the project root\n"
            f"2. Added {key_name}=your_key_here to the .env file\n"
            f"3. Called load_environment() before getting keys"
        )
    
    return value or ""


def get_config(key_name: str, default=None):
    """
    Get a configuration value from environment variables.
    Returns default if not found.
    
    Args:
        key_name: Name of the environment variable
        default: Default value if not found
        
    Returns:
        The configuration value or default
        
    Example:
        >>> debug = get_config('DEBUG', 'False')
        >>> log_level = get_config('LOG_LEVEL', 'INFO')
    """
    return os.getenv(key_name, default)


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Environment Variables Test")
    print("=" * 60)
    
    # Load environment
    load_environment()
    
    # Test API keys
    print("\nTesting API Keys:")
    print("-" * 60)
    
    try:
        gemini_key = get_api_key('GEMINI_API_KEY', required=False)
        if gemini_key:
            # Only show first and last 4 characters for security
            masked_key = f"{gemini_key[:8]}...{gemini_key[-4:]}"
            print(f"✓ GEMINI_API_KEY: {masked_key}")
        else:
            print("✗ GEMINI_API_KEY: Not found")
    except ValueError as e:
        print(f"✗ Error: {e}")
    
    try:
        chat_key = get_api_key('GEMINI_CHAT_API_KEY', required=False)
        if chat_key:
            masked_key = f"{chat_key[:8]}...{chat_key[-4:]}"
            print(f"✓ GEMINI_CHAT_API_KEY: {masked_key}")
        else:
            print("✗ GEMINI_CHAT_API_KEY: Not found")
    except ValueError as e:
        print(f"✗ Error: {e}")
    
    # Test configuration
    print("\nTesting Configuration:")
    print("-" * 60)
    debug = get_config('DEBUG', 'False')
    log_level = get_config('LOG_LEVEL', 'INFO')
    
    print(f"DEBUG: {debug}")
    print(f"LOG_LEVEL: {log_level}")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
