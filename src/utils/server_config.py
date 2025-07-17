"""
Server configuration utilities
"""
import os

# Server configuration
PORT = 8000
DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
