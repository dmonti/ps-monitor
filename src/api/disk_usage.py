"""
Disk usage API endpoint
Provides disk usage information for all mounted filesystems
"""
import platform
import json
import shutil
import subprocess
import re


def handle_disk_usage_request(handler):
    """Handle /api/disk-usage endpoint request
    
    Args:
        handler: The request handler instance
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'application/json')
    handler.end_headers()
    
    # Get disk usage information using standard library
    disks = get_disk_usage()
    
    response = {
        'disks': disks,
        'count': len(disks)
    }
    handler.wfile.write(json.dumps(response).encode('utf-8'))


def get_disk_usage():
    """Get disk usage information for all mounted filesystems
    
    Returns:
        list: A list of disk usage information dictionaries
    """
    disks = []
    
    # First try to get root disk usage with shutil (standard library)
    try:
        usage = shutil.disk_usage('/')
        disks.append({
            'device': 'root',
            'mountpoint': '/',
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent_used': round((usage.used / usage.total) * 100, 2),
            'percent_free': round((usage.free / usage.total) * 100, 2)
        })
    except Exception:
        # Root disk usage failed, continue with other methods
        pass
    
    # If we're on Linux/Unix, use df command
    if platform.system() != 'Windows':
        try:
            # Run df command to get all filesystem info
            process = subprocess.Popen(['df', '-P'], stdout=subprocess.PIPE)
            output, _ = process.communicate()
            output = output.decode('utf-8')
            
            # Parse the output
            lines = output.strip().split('\n')
            for line in lines[1:]:  # Skip header
                parts = re.split(r'\s+', line)
                if len(parts) >= 6:
                    device = parts[0]
                    total = int(parts[1]) * 1024  # Convert from KB to bytes
                    used = int(parts[2]) * 1024   # Convert from KB to bytes
                    free = int(parts[3]) * 1024   # Convert from KB to bytes
                    percent_used = int(parts[4].rstrip('%'))
                    mountpoint = parts[5]
                    
                    # Skip if we already have info for this mountpoint
                    if any(d['mountpoint'] == mountpoint for d in disks):
                        continue
                        
                    disks.append({
                        'device': device,
                        'mountpoint': mountpoint,
                        'total': total,
                        'used': used,
                        'free': free,
                        'percent_used': percent_used,
                        'percent_free': 100 - percent_used
                    })
        except Exception:
            # df command failed, continue with other methods
            pass
    
    # If we're on Windows, get disk information differently
    elif platform.system() == 'Windows':
        try:
            # Get drive letters
            import ctypes
            drives_bitmask = ctypes.windll.kernel32.GetLogicalDrives()
            for letter in range(ord('A'), ord('Z') + 1):
                if drives_bitmask & (1 << (letter - ord('A'))):
                    drive = chr(letter) + ':\\'
                    try:
                        usage = shutil.disk_usage(drive)
                        disks.append({
                            'device': drive,
                            'mountpoint': drive,
                            'total': usage.total,
                            'used': usage.used,
                            'free': usage.free,
                            'percent_used': round((usage.used / usage.total) * 100, 2),
                            'percent_free': round((usage.free / usage.total) * 100, 2)
                        })
                    except Exception:
                        # Skip drives that cannot be accessed
                        pass
        except Exception:
            # Windows-specific method failed
            pass
            
    return disks
