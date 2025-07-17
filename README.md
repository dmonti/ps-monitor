# PS Monitor

A lightweight system monitoring web application that provides real-time information about system resources through a clean web interface. Built using only Python standard libraries for the backend.

## Features

- **System Information**: View OS details and platform information
- **Disk Usage**: Monitor disk space usage across all mounted filesystems
- **Memory Usage**: Track physical and swap memory utilization
- **SQLite Database**: Persistent storage of disk usage metrics for historical analysis
- **Background Monitoring**: Collects disk usage data every 10 minutes
- **Cross-Platform**: Works on Linux, macOS, and Windows
- **No External Dependencies**: Pure Python implementation using standard libraries
- **Clean English UI**: All user interface text presented in English

## Requirements

- Python 3.6 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Project Structure

```
ps-monitor/
├── src/                       # Source code
│   ├── api/                   # API endpoint handlers
│   │   ├── __init__.py
│   │   ├── disk_usage.py      # Disk usage endpoint
│   │   ├── memory_usage.py    # Memory usage endpoint
│   │   └── system_info.py     # System info endpoint
│   ├── data/                  # Data storage components
│   │   └── db/                # Database related modules
│   │       ├── __init__.py
│   │       ├── database.py    # Database connection handler
│   │       ├── disk_usage_monitor.py # Background disk usage monitor
│   │       └── disk_usage_repository.py # Disk usage data storage
│   ├── static/                # Static web assets
│   │   ├── index.html         # Main HTML interface
│   │   └── index.js           # JavaScript for dynamic content
│   ├── web/                   # Web server implementation
│   │   ├── __init__.py
│   │   ├── http_server.py     # HTTP server implementation
│   │   └── request_handler.py # Requests handler
│   └── main.py                # Application entry point
└── README.md                  # Project documentation
```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/dmonti/ps-monitor.git
   cd ps-monitor
   ```

2. No additional installation steps needed! The application uses only Python standard libraries.

## Running the Application

1. Start the server:
   ```bash
   python3 src/main.py
   ```

   Optionally, you can specify a custom port using the environment variable:
   ```bash
   PS_MONITOR_PORT=9000 python3 src/main.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```
   (Or use the custom port if specified)

3. The application will display system information, disk usage, and memory usage statistics in your browser.

4. The application runs in the background with two threads:
   - A web server thread for handling HTTP requests
   - A disk usage monitoring thread that collects and stores disk usage data every 10 minutes

## API Endpoints

The application provides the following RESTful API endpoints:

- **`/api/system/info`** - Returns information about the operating system and platform
- **`/api/disk/usage`** - Returns disk usage statistics for all mounted filesystems
- **`/api/memory/usage`** - Returns physical and swap memory usage statistics

## URL Path Structure

- **`/api/...`** - API endpoints for retrieving system data
- **`/static/...`** - Static resources (HTML, JavaScript, CSS)
- **`/`** - Root path, serves the main application interface

## Customization

You can customize the following aspects of the application:

- **Server Port**: Set the `PS_MONITOR_PORT` environment variable (default is 8000)
- **Monitoring Interval**: The disk usage monitoring thread collects data every 10 minutes
- **Data Retention**: Disk usage records older than 30 days are automatically cleaned up

## Database

The application uses SQLite for persistent storage of disk usage data:

- Database file is stored in `src/data/db/ps_monitor.db`
- The database is created with secure permissions (700) when the application starts
- Schema includes tables for storing disk usage metrics with timestamps
- Data is automatically collected in the background

## Logging

The application uses Python's logging module with the following features:

- Log level set to INFO
- Log format includes timestamps, log level, thread name, and logger name
- Different components log to their own loggers (main, HttpServer, Database, DiskUsageMonitor)

## Troubleshooting

- If the server fails to start with an "Address already in use" error, another process might be using the default port. You can change the port by setting the `PS_MONITOR_PORT` environment variable.
- On some systems, you may need elevated permissions to access certain system metrics.
- If the database fails to initialize, check the logs for error messages and ensure the application has write permissions to the `src/data/db` directory.
- For any monitoring thread issues, check the logs for messages from the 'DiskUsageMonitor' logger.

## License

This project is available under the MIT License. See the LICENSE file for more information.