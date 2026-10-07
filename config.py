"""Configuration loader supporting environment variables, local_config.py, and defaults."""
import os

try:
    from local_config import GEMINI_API_KEY, GITHUB_TOKEN
except ImportError:
    GEMINI_API_KEY, GITHUB_TOKEN = '', ''

# Environment variables take precedence if present
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', GEMINI_API_KEY)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', GITHUB_TOKEN)
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-3.5-flash-lite')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'gemini-embedding-001')
