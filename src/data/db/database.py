"""
Database module for PS Monitor application.
Provides database connectivity and configuration.
"""
import logging
import os
import sqlite3

logger = logging.getLogger('Database')

class Database:
    """Database connector class for PS Monitor application"""
    
    # SQLite database file path
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db', 'ps_monitor.db')
    
    @classmethod
    def ensure_db_directory(cls):
        """Ensure the database directory exists"""
        db_dir = os.path.dirname(cls.DB_PATH)
        os.makedirs(db_dir, exist_ok=True)
        
        # Set secure permissions for the directory
        os.chmod(db_dir, 0o700)  # Only owner can read, write, execute
    
    @classmethod
    def get_connection(cls):
        """Get a connection to the SQLite database
        
        Returns:
            sqlite3.Connection: The database connection
        """
        # Ensure the database directory exists with secure permissions
        cls.ensure_db_directory()
        
        # Connect to the database
        conn = sqlite3.connect(cls.DB_PATH)
        
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Row factory to get results as dictionaries
        conn.row_factory = cls.dict_factory
        
        return conn
    
    @staticmethod
    def dict_factory(cursor, row):
        """Convert row object to dictionary
        
        Args:
            cursor: The database cursor
            row: The row data
            
        Returns:
            dict: Row data as dictionary
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    @classmethod
    def initialize_schema(cls):
        """Initialize the database schema if not already created"""
        conn = cls.get_connection()
        try:
            cursor = conn.cursor()
            
            # Create tables if they don't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS disk_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device TEXT NOT NULL,
                mountpoint TEXT NOT NULL,
                total BIGINT NOT NULL,
                used BIGINT NOT NULL,
                free BIGINT NOT NULL,
                percent_used REAL NOT NULL,
                percent_free REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            conn.commit()
            logger.info("Database schema initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database schema: {e}")
        finally:
            conn.close()
