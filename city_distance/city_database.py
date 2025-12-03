"""Database manager for city coordinates."""
import sqlite3
from pathlib import Path
from typing import Optional, Tuple


class CityDatabase:
    """Manages city coordinates in SQLite database."""
    
    def __init__(self, db_path: str = "cities.db"):
        """Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(__file__).parent / db_path
        self._create_table()
    
    def _create_table(self) -> None:
        """Create cities table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def get_city_coordinates(self, city_name: str) -> Optional[Tuple[float, float]]:
        """Get coordinates for a city.
        
        Args:
            city_name: Name of the city
            
        Returns:
            Tuple of (latitude, longitude) or None if city not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT latitude, longitude FROM cities WHERE LOWER(name) = LOWER(?)",
                (city_name,)
            )
            result = cursor.fetchone()
            return result if result else None
    
    def add_city(self, city_name: str, latitude: float, longitude: float) -> bool:
        """Add a new city to the database.
        
        Args:
            city_name: Name of the city
            latitude: Latitude in degrees (-90 to 90)
            longitude: Longitude in degrees (-180 to 180)
            
        Returns:
            True if city was added, False if it already exists
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO cities (name, latitude, longitude) VALUES (?, ?, ?)",
                    (city_name, latitude, longitude)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def list_all_cities(self) -> list:
        """Get list of all cities in database.
        
        Returns:
            List of tuples (name, latitude, longitude)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, latitude, longitude FROM cities ORDER BY name")
            return cursor.fetchall()
