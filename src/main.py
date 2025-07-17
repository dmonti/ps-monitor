#!/usr/bin/env python3
"""
PS Monitor - A simple system monitoring web application

Provides API endpoints for system information and disk usage,
and serves a web interface to display this information.
"""
import threading
import time
import signal
import sys

from web.http_server import HttpServer

startup_at = time.time()
server_thread = None
http_server = HttpServer()

def signal_handler(sig, frame):
    print("\nReceived shutdown signal, stopping server...")
    http_server.shutdown()
    sys.exit(0)

def on_server_startup():
    global startup_at
    startup_time_ms = int((time.time() - startup_at) * 1000)
    print(f"ps-monitor started in {startup_time_ms}ms. Press Ctrl+C to stop.")

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    global server_thread
    server_thread = threading.Thread(target=http_server.run, args=(on_server_startup,), daemon=True)
    server_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
