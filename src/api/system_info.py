"""
System information API endpoint
Provides basic OS and platform information
"""
import os
import platform
import json


def handle_system_info_request(handler):
    """Handle /api/info endpoint request
    
    Args:
        handler: The request handler instance
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'application/json')
    handler.end_headers()
    
    info = {
        'os': {
            'name': os.name
        },
        'platform': {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python': f'v{platform.python_version()}'
        },
    }
    
    handler.wfile.write(json.dumps(info).encode('utf-8'))
