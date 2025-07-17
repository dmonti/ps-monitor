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
import logging
import platform
import os

from data.db.database import Database
from data.db.disk_usage_monitor import start_monitoring
from web.http_server import HttpServer

startup_at = time.time()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-5s [%(threadName)19s] %(name)-16s: %(message)s')
logger = logging.getLogger('main')

http_server = HttpServer()
running = True

def signal_handler(signal, frame):
    logger.info(f"Received shutdown signal({signal}), stopping server...")
    global running
    running = False
    http_server.shutdown()
    sys.exit(0)

def main():
    logger.info(f"Starting ps-monitor using Python v{platform.python_version()} with PID {os.getpid()}")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    Database.initialize_schema()
    start_monitoring()

    server_thread = threading.Thread(target=http_server.run, daemon=True)
    http_start_time = time.time()
    server_thread.start()

    startup_time_ms = int((time.time() - startup_at) * 1000)
    http_start_time_ms = int((time.time() - http_start_time) * 1000)
    logger.info(f"Started ps-monitor in {http_start_time_ms}ms (process running for {startup_time_ms}ms)")

    try:
        global running
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        running = False
        http_server.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()
