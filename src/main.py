import http.server
import socketserver
import os
import platform
import json

PORT = 8000
DIRECTORY = os.path.join(os.path.dirname(__file__), "static")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/api/info':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
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
            self.wfile.write(json.dumps(info).encode('utf-8'))
        else:
            super().do_GET()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Starting ps-monitor using Python {platform.python_version()} with PID {os.getpid()}")
        httpd.serve_forever()
