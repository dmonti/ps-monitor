"""
Request handler for the PS Monitor web server.

This module defines the HTTP request handler for the PS Monitor application,
which processes API requests and serves static files.
"""
import http.server

from api.system_info import handle_system_info_request
from api.disk_usage import handle_disk_usage_request
from api.memory_usage import handle_memory_usage_request
from utils.server_config import DIRECTORY


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Handler for HTTP requests to the PS Monitor web server.
    
    Handles API endpoint requests and serves static files from the configured directory.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the handler with the static directory.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        """
        Handle GET requests.
        
        Routes requests to appropriate handlers based on path:
        - API endpoints (/api/...)
        - Static resources (/static/...)
        - Root path (/)
        - Other paths
        """
        if self._is_api_request():
            self._handle_api_request()
        elif self._is_static_resource():
            self._handle_static_resource()
        elif self._is_root_path():
            self._handle_root_path()
        else:
            self._handle_default_request()
    
    def _is_api_request(self):
        """Check if the request is for an API endpoint."""
        return self.path.startswith('/api/')
    
    def _is_static_resource(self):
        """Check if the request is for a static resource."""
        return self.path.startswith('/static/')
    
    def _is_root_path(self):
        """Check if the request is for the root path."""
        return self.path == '/'
    
    def _handle_api_request(self):
        """Handle API endpoint requests."""
        if self.path == '/api/system/info':
            handle_system_info_request(self)
        elif self.path == '/api/disk/usage':
            handle_disk_usage_request(self)
        elif self.path == '/api/memory/usage':
            handle_memory_usage_request(self)
        else:
            self.send_error(404, "API endpoint not found")
    
    def _handle_static_resource(self):
        """Handle static resource requests."""
        # Rewrite path to remove /static prefix
        self.path = self.path[7:]  # Remove '/static/' prefix
        super().do_GET()
    
    def _handle_root_path(self):
        """Handle root path requests."""
        self.path = '/index.html'
        super().do_GET()
    
    def _handle_default_request(self):
        """Handle all other requests."""
        super().do_GET()
