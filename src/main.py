#!/usr/bin/env python3
"""
PS Monitor - A simple system monitoring web application

Provides API endpoints for system information and disk usage,
and serves a web interface to display this information.
"""
import http.server
import socketserver
import os
import platform

# Import modules from the project
from utils.server_config import PORT, DIRECTORY
from api.system_info import handle_system_info_request
from api.disk_usage import handle_disk_usage_request


class Handler(http.server.SimpleHTTPRequestHandler):
    """Request handler for the PS Monitor web server"""
    
    def __init__(self, *args, **kwargs):
        """Initialize the handler with the static directory"""
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/info':
            handle_system_info_request(self)
        elif self.path == '/api/disk-usage':
            handle_disk_usage_request(self)
        else:
            # Let SimpleHTTPRequestHandler handle static files
            super().do_GET()


def main():
    """Main entry point for the application"""
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Starting ps-monitor using Python {platform.python_version()} with PID {os.getpid()}")
        print(f"Server running at http://localhost:{PORT}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()


if __name__ == "__main__":
    main()
