# PS Monitor

A lightweight system monitoring web application that provides real-time information about system resources through a clean web interface. Built using only Python standard libraries for the backend.

## Features

- **System Information**: View OS details and platform information
- **Disk Usage**: Monitor disk space usage across all mounted filesystems
- **Memory Usage**: Track physical and swap memory utilization
- **Cross-Platform**: Works on Linux, macOS, and Windows
- **No External Dependencies**: Pure Python implementation using standard libraries

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
│   ├── handlers/              # HTTP request handlers
│   │   ├── __init__.py
│   │   └── request_handler.py # Main request handler
│   ├── static/                # Static web assets
│   │   ├── index.html         # Main HTML interface
│   │   └── index.js           # JavaScript for dynamic content
│   ├── utils/                 # Utility modules
│   │   ├── __init__.py
│   │   └── server_config.py   # Server configuration
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

2. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```

3. The application will display system information, disk usage, and memory usage statistics in your browser.

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

You can modify the server port by editing `src/utils/server_config.py`.

## Troubleshooting

- If the server fails to start with an "Address already in use" error, another process might be using port 8000. You can change the port in `src/utils/server_config.py`.
- On some systems, you may need elevated permissions to access certain system metrics.

## License

This project is available under the MIT License. See the LICENSE file for more information.