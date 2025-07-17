#!/usr/bin/env python3
"""
PS Monitor - A simple system monitoring web application

Provides API endpoints for system information and disk usage,
and serves a web interface to display this information.
"""
import socketserver
import os
import platform

from utils.server_config import PORT
from handlers.request_handler import RequestHandler


def main():
    """Main entry point for the application"""
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print(f"Starting ps-monitor using Python v{platform.python_version()} with PID {os.getpid()}")
        print(f"Server running at http://localhost:{PORT}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()


if __name__ == "__main__":
    main()
