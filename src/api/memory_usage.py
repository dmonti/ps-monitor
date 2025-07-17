"""
Memory usage API endpoint
Provides system memory information using standard libraries
"""
import json
import platform
import subprocess
import re


def handle_memory_usage_request(handler):
    """Handle /api/memory-usage endpoint request
    
    Args:
        handler: The request handler instance
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'application/json')
    handler.end_headers()
    
    memory_info = get_memory_info()
    
    handler.wfile.write(json.dumps(memory_info).encode('utf-8'))


def get_memory_info():
    """Get system memory usage information
    
    Returns:
        dict: Memory usage information
    """
    result = {
        'total': 0,
        'used': 0,
        'free': 0,
        'percent_used': 0,
        'swap_total': 0,
        'swap_used': 0,
        'swap_free': 0,
        'swap_percent_used': 0,
        'units': 'bytes'
    }
    
    system = platform.system()
    
    if system == 'Linux':
        # Read memory info from /proc/meminfo
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
                
            # Parse memory information
            mem_total = int(re.search(r'MemTotal:\s+(\d+)', meminfo).group(1)) * 1024  # KB to bytes
            mem_free = int(re.search(r'MemFree:\s+(\d+)', meminfo).group(1)) * 1024
            mem_available = int(re.search(r'MemAvailable:\s+(\d+)', meminfo).group(1)) * 1024
            
            # Swap information
            swap_total = int(re.search(r'SwapTotal:\s+(\d+)', meminfo).group(1)) * 1024
            swap_free = int(re.search(r'SwapFree:\s+(\d+)', meminfo).group(1)) * 1024
            
            # Calculate used memory
            mem_used = mem_total - mem_available
            swap_used = swap_total - swap_free
            
            # Calculate usage percentages
            mem_percent = round((mem_used / mem_total) * 100, 2) if mem_total > 0 else 0
            swap_percent = round((swap_used / swap_total) * 100, 2) if swap_total > 0 else 0
            
            # Update result
            result.update({
                'total': mem_total,
                'used': mem_used,
                'free': mem_available,
                'percent_used': mem_percent,
                'swap_total': swap_total,
                'swap_used': swap_used,
                'swap_free': swap_free,
                'swap_percent_used': swap_percent
            })
        except Exception as e:
            result['error'] = str(e)
            
    elif system == 'Darwin':  # macOS
        try:
            # Use vm_stat command
            vm_stat = subprocess.run(['vm_stat'], stdout=subprocess.PIPE, text=True).stdout
            
            # Parse output
            page_size = int(subprocess.run(['sysctl', '-n', 'hw.pagesize'], 
                                         stdout=subprocess.PIPE, text=True).stdout.strip())
            
            mem_free = int(re.search(r'Pages free:\s+(\d+)', vm_stat).group(1)) * page_size
            mem_active = int(re.search(r'Pages active:\s+(\d+)', vm_stat).group(1)) * page_size
            mem_inactive = int(re.search(r'Pages inactive:\s+(\d+)', vm_stat).group(1)) * page_size
            mem_wired = int(re.search(r'Pages wired down:\s+(\d+)', vm_stat).group(1)) * page_size
            
            # Get total memory using sysctl
            mem_total = int(subprocess.run(['sysctl', '-n', 'hw.memsize'], 
                                         stdout=subprocess.PIPE, text=True).stdout.strip())
            
            mem_used = mem_active + mem_wired
            mem_percent = round((mem_used / mem_total) * 100, 2)
            
            # Get swap info
            swap_info = subprocess.run(['sysctl', '-n', 'vm.swapusage'], 
                                     stdout=subprocess.PIPE, text=True).stdout.strip()
            
            swap_total_match = re.search(r'total = (\d+(?:\.\d+)?)([MGT])', swap_info)
            swap_used_match = re.search(r'used = (\d+(?:\.\d+)?)([MGT])', swap_info)
            swap_free_match = re.search(r'free = (\d+(?:\.\d+)?)([MGT])', swap_info)
            
            # Convert to bytes
            multipliers = {'M': 1024 * 1024, 'G': 1024 * 1024 * 1024, 'T': 1024 * 1024 * 1024 * 1024}
            
            swap_total = float(swap_total_match.group(1)) * multipliers.get(swap_total_match.group(2), 1)
            swap_used = float(swap_used_match.group(1)) * multipliers.get(swap_used_match.group(2), 1)
            swap_free = float(swap_free_match.group(1)) * multipliers.get(swap_free_match.group(2), 1)
            swap_percent = round((swap_used / swap_total) * 100, 2) if swap_total > 0 else 0
            
            # Update result
            result.update({
                'total': mem_total,
                'used': mem_used,
                'free': mem_free,
                'percent_used': mem_percent,
                'swap_total': swap_total,
                'swap_used': swap_used,
                'swap_free': swap_free,
                'swap_percent_used': swap_percent
            })
        except Exception as e:
            result['error'] = str(e)
            
    elif system == 'Windows':
        try:
            # Use wmic command for memory info
            memory_output = subprocess.run(
                ['wmic', 'OS', 'get', 'FreePhysicalMemory,TotalVisibleMemorySize'],
                stdout=subprocess.PIPE, text=True
            ).stdout
            
            total_memory = int(re.search(r'(\d+)\s*$', memory_output.splitlines()[1]).group(1)) * 1024  # KB to bytes
            free_memory = int(re.search(r'(\d+)', memory_output.splitlines()[2]).group(1)) * 1024
            used_memory = total_memory - free_memory
            percent_used = round((used_memory / total_memory) * 100, 2) if total_memory > 0 else 0
            
            # Get swap (pagefile) info
            pagefile_output = subprocess.run(
                ['wmic', 'pagefile', 'get', 'AllocatedBaseSize,CurrentUsage'],
                stdout=subprocess.PIPE, text=True
            ).stdout
            
            lines = pagefile_output.splitlines()
            if len(lines) >= 3:
                swap_total = int(re.search(r'(\d+)', lines[1]).group(1)) * 1024 * 1024  # MB to bytes
                swap_used = int(re.search(r'(\d+)', lines[2]).group(1)) * 1024 * 1024
                swap_free = swap_total - swap_used
                swap_percent = round((swap_used / swap_total) * 100, 2) if swap_total > 0 else 0
                
                result.update({
                    'total': total_memory,
                    'used': used_memory,
                    'free': free_memory,
                    'percent_used': percent_used,
                    'swap_total': swap_total,
                    'swap_used': swap_used,
                    'swap_free': swap_free,
                    'swap_percent_used': swap_percent
                })
            else:
                result.update({
                    'total': total_memory,
                    'used': used_memory,
                    'free': free_memory,
                    'percent_used': percent_used
                })
        except Exception as e:
            result['error'] = str(e)
    else:
        result['error'] = f"Unsupported operating system: {system}"
        
    return result
