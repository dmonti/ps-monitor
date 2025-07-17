"""
Disk usage monitoring module for PS Monitor application.
Handles periodic collection and storage of disk usage data.
"""
import threading
import time
import logging

from api.disk_usage import get_disk_usage
from datetime import datetime
from data.db.disk_usage_repository import DiskUsageRepository

logger = logging.getLogger('DiskUsageMonitor')

class DiskUsageMonitor:
    """Monitor class for collecting and storing disk usage data"""
    
    def __init__(self, interval_seconds=600):
        """Initialize the disk usage monitor
        
        Args:
            interval_seconds (int, optional): Interval between collections in seconds
        """
        self.interval_seconds = interval_seconds
        self.running = False
        self.monitor_thread = None
    
    def start(self):
        """Start the disk usage monitoring thread"""
        if self.monitor_thread and self.monitor_thread.is_alive():
            logger.warning("Disk usage monitoring thread is already running")
            return

        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor, daemon=True)
        self.monitor_thread.start()
        logger.info("Disk usage monitoring started")
    
    def stop(self):
        """Stop the disk usage monitoring thread"""
        self.running = False
        logger.info("Disk usage monitoring stopped")
    
    def _monitor(self):
        """Background thread to periodically collect and store disk usage data"""
        logger.info("Starting disk usage monitoring")
        
        while self.running:
            try:
                # Get current disk usage data
                disk_data = get_disk_usage()
                
                # Save to database
                records_inserted = DiskUsageRepository.save_disk_usage(disk_data)
                logger.info(f"Saved {records_inserted} disk usage records")
                
                # Clean up old records once a day (run at midnight)
                now = datetime.now()
                if now.hour == 0 and now.minute < 5:  # Between 12:00 AM and 12:05 AM
                    deleted = DiskUsageRepository.delete_old_records(30)  # Keep 30 days of data
                    if deleted > 0:
                        logger.info(f"Cleaned up {deleted} old disk usage records")
            except Exception as e:
                logger.error(f"Error in disk usage monitoring: {e}")
            
            # Sleep for the configured interval
            for _ in range(self.interval_seconds):
                if not self.running:
                    break
                time.sleep(1)

# Global instance that can be imported and used by other modules
disk_monitor = DiskUsageMonitor()

# Convenience functions for easier access from other modules
def start_monitoring():
    """Start the global disk usage monitor"""
    disk_monitor.start()

def stop_monitoring():
    """Stop the global disk usage monitor"""
    disk_monitor.stop()
