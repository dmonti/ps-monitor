"""
Server module for the PS Monitor application.

This module provides server functionality to run the web application,
handling the server lifecycle and request processing.
"""
import socketserver
import os
import platform

from web.request_handler import RequestHandler

# Server configuration
PORT = 8000


class HttpServer:
    """
    Server class for the PS Monitor application.
    
    Handles server lifecycle including setup, startup, and shutdown.
    """
    
    def __init__(self, host="", port=PORT):
        """
        Initialize the server with host and port.
        
        Args:
            host (str): Host address to bind to. Empty string means all interfaces.
            port (int, optional): Port to listen on. Defaults to the configured PORT.
        """
        self.host = host
        self.port = port
        self.httpd = None
    
    def create_server(self):
        """
        Create the TCPServer instance.
        
        Returns:
            socketserver.TCPServer: The configured server instance.
        """
        return socketserver.TCPServer((self.host, self.port), RequestHandler)
    
    def run(self, startup_callback=None):
        """Run the server and handle the server lifecycle.
        
        Args:
            startup_callback (callable, optional): Callback function to be called after server startup.
                The callback will receive the startup time in milliseconds as an argument.
        """
        self.httpd = self.create_server()
        
        print(f"Starting ps-monitor using Python v{platform.python_version()} with PID {os.getpid()}")
        print(f"Server running at http://localhost:{self.port}")
        
        # Call the startup callback with the startup time if provided
        if startup_callback:
            startup_callback()
        
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self.shutdown()
    
    def shutdown(self):
        """Shutdown the server gracefully."""
        if self.httpd:
            self.httpd.server_close()
            print("Server stopped.")

