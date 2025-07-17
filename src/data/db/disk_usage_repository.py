"""
Repository for disk usage data.
Handles database operations for disk usage information.
"""
from data.db.database import Database


class DiskUsageRepository:
    """Repository for disk usage data"""
    
    @classmethod
    def save_disk_usage(cls, disk_data):
        """Save disk usage data to the database
        
        Args:
            disk_data (list): List of disk usage information dictionaries
        
        Returns:
            int: Number of records inserted
        """
        conn = Database.get_connection()
        try:
            cursor = conn.cursor()
            records_inserted = 0
            
            for disk in disk_data:
                cursor.execute('''
                INSERT INTO disk_usage 
                (device, mountpoint, total, used, free, percent_used, percent_free)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    disk['device'],
                    disk['mountpoint'],
                    disk['total'],
                    disk['used'],
                    disk['free'],
                    disk['percent_used'],
                    disk['percent_free']
                ))
                records_inserted += 1
            
            conn.commit()
            return records_inserted
        finally:
            conn.close()
    
    @classmethod
    def get_latest_disk_usage(cls):
        """Get the latest disk usage data for each mountpoint
        
        Returns:
            list: Latest disk usage data for each mountpoint
        """
        conn = Database.get_connection()
        try:
            cursor = conn.cursor()
            
            # Using a subquery to get the latest timestamp for each mountpoint
            cursor.execute('''
            SELECT d.*
            FROM disk_usage d
            INNER JOIN (
                SELECT mountpoint, MAX(timestamp) as latest_timestamp
                FROM disk_usage
                GROUP BY mountpoint
            ) latest ON d.mountpoint = latest.mountpoint AND d.timestamp = latest.latest_timestamp
            ORDER BY d.percent_used DESC
            ''')
            
            return cursor.fetchall()
        finally:
            conn.close()
    
    @classmethod
    def get_disk_usage_history(cls, mountpoint, limit=100):
        """Get historical disk usage data for a specific mountpoint
        
        Args:
            mountpoint (str): The mountpoint to get history for
            limit (int, optional): Maximum number of records to return
        
        Returns:
            list: Historical disk usage data
        """
        conn = Database.get_connection()
        try:
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT *
            FROM disk_usage
            WHERE mountpoint = ?
            ORDER BY timestamp DESC
            LIMIT ?
            ''', (mountpoint, limit))
            
            return cursor.fetchall()
        finally:
            conn.close()
            
    @classmethod
    def delete_old_records(cls, days_to_keep=30):
        """Delete disk usage records older than the specified number of days
        
        Args:
            days_to_keep (int, optional): Number of days of data to keep
            
        Returns:
            int: Number of records deleted
        """
        conn = Database.get_connection()
        try:
            cursor = conn.cursor()
            
            cursor.execute('''
            DELETE FROM disk_usage
            WHERE timestamp < datetime('now', ? || ' days')
            ''', (f'-{days_to_keep}',))
            
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count
        finally:
            conn.close()
