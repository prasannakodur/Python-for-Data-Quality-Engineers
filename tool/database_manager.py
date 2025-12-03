"""Database Manager for Feed Records

Manages database storage for different record types with duplicate checking.
Uses SQLite for local storage with separate tables for each record type.

Features:
1. Separate tables for News, PrivateAd, and Recipe records
2. Automatic duplicate detection and prevention
3. Timestamp tracking for all records
4. Simple query interface

Tables:
- news: id, text, city, published_at, created_at
- private_ads: id, text, expiration_date, published_at, created_at
- recipes: id, title, ingredients, ingredient_count, complexity, published_at, created_at
"""
from __future__ import annotations
import sqlite3
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Configuration for database connection."""
    db_path: Path
    
    def __post_init__(self):
        self.db_path = Path(self.db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)


class FeedDatabaseManager:
    """Manages database operations for feed records."""
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file (defaults to feed_records.db in current directory)
        """
        if db_path is None:
            db_path = Path(__file__).parent / "feed_records.db"
        
        self.config = DatabaseConfig(db_path=db_path)
        self.conn: Optional[sqlite3.Connection] = None
        self._initialize_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.config.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
        return self.conn
    
    def _initialize_database(self) -> None:
        """Create tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # News table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                city TEXT NOT NULL,
                published_at TEXT NOT NULL,
                content_hash TEXT UNIQUE NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Private Ads table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS private_ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                expiration_date TEXT NOT NULL,
                published_at TEXT NOT NULL,
                content_hash TEXT UNIQUE NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Recipes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                ingredient_count INTEGER NOT NULL,
                complexity TEXT NOT NULL,
                published_at TEXT NOT NULL,
                content_hash TEXT UNIQUE NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for faster duplicate checking
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_news_hash ON news(content_hash)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ads_hash ON private_ads(content_hash)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_recipes_hash ON recipes(content_hash)
        """)
        
        conn.commit()
        print(f"✅ Database initialized at {self.config.db_path}")
    
    def _generate_content_hash(self, record_type: str, **fields) -> str:
        """Generate unique hash for record content to detect duplicates.
        
        Args:
            record_type: Type of record (news, privatead, recipe)
            **fields: Record fields to include in hash
            
        Returns:
            SHA256 hash of record content
        """
        # Create a deterministic string from record data
        content_parts = [record_type]
        for key in sorted(fields.keys()):
            content_parts.append(f"{key}:{fields[key]}")
        
        content_str = "|".join(content_parts)
        return hashlib.sha256(content_str.encode('utf-8')).hexdigest()
    
    def save_news(self, text: str, city: str, published_at: Optional[str] = None) -> Tuple[bool, str]:
        """Save a news record to database.
        
        Args:
            text: News text content
            city: City name
            published_at: Publication timestamp (defaults to current time)
            
        Returns:
            (success, message) tuple
        """
        if published_at is None:
            published_at = datetime.now().isoformat()
        
        # Generate content hash for duplicate check
        content_hash = self._generate_content_hash(
            "news",
            text=text.strip().lower(),
            city=city.strip().lower()
        )
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO news (text, city, published_at, content_hash)
                VALUES (?, ?, ?, ?)
            """, (text, city, published_at, content_hash))
            conn.commit()
            return True, f"✅ News record saved (ID: {cursor.lastrowid})"
        
        except sqlite3.IntegrityError:
            return False, "⚠️  Duplicate news record - already exists in database"
        except Exception as e:
            return False, f"❌ Error saving news: {e}"
    
    def save_private_ad(self, text: str, expiration_date: str, published_at: Optional[str] = None) -> Tuple[bool, str]:
        """Save a private ad record to database.
        
        Args:
            text: Advertisement text
            expiration_date: Expiration date (YYYY-MM-DD)
            published_at: Publication timestamp (defaults to current time)
            
        Returns:
            (success, message) tuple
        """
        if published_at is None:
            published_at = datetime.now().isoformat()
        
        # Generate content hash for duplicate check
        content_hash = self._generate_content_hash(
            "privatead",
            text=text.strip().lower(),
            expiration_date=expiration_date
        )
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO private_ads (text, expiration_date, published_at, content_hash)
                VALUES (?, ?, ?, ?)
            """, (text, expiration_date, published_at, content_hash))
            conn.commit()
            return True, f"✅ Private ad saved (ID: {cursor.lastrowid})"
        
        except sqlite3.IntegrityError:
            return False, "⚠️  Duplicate private ad - already exists in database"
        except Exception as e:
            return False, f"❌ Error saving private ad: {e}"
    
    def save_recipe(self, title: str, ingredients: str, ingredient_count: int, 
                    complexity: str, published_at: Optional[str] = None) -> Tuple[bool, str]:
        """Save a recipe record to database.
        
        Args:
            title: Recipe title
            ingredients: Comma-separated ingredients
            ingredient_count: Number of ingredients
            complexity: Complexity level (SIMPLE, MODERATE, COMPLEX)
            published_at: Publication timestamp (defaults to current time)
            
        Returns:
            (success, message) tuple
        """
        if published_at is None:
            published_at = datetime.now().isoformat()
        
        # Normalize ingredients for consistent duplicate detection
        ing_list = [i.strip().lower() for i in ingredients.split(',')]
        normalized_ingredients = ','.join(sorted(ing_list))
        
        # Generate content hash for duplicate check
        content_hash = self._generate_content_hash(
            "recipe",
            title=title.strip().lower(),
            ingredients=normalized_ingredients
        )
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO recipes (title, ingredients, ingredient_count, complexity, published_at, content_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, ingredients, ingredient_count, complexity, published_at, content_hash))
            conn.commit()
            return True, f"✅ Recipe saved (ID: {cursor.lastrowid})"
        
        except sqlite3.IntegrityError:
            return False, "⚠️  Duplicate recipe - already exists in database"
        except Exception as e:
            return False, f"❌ Error saving recipe: {e}"
    
    def get_all_news(self) -> List[Dict[str, Any]]:
        """Retrieve all news records."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, text, city, published_at, created_at FROM news ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_private_ads(self) -> List[Dict[str, Any]]:
        """Retrieve all private ad records."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, text, expiration_date, published_at, created_at FROM private_ads ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_recipes(self) -> List[Dict[str, Any]]:
        """Retrieve all recipe records."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, ingredients, ingredient_count, complexity, published_at, created_at FROM recipes ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict[str, int]:
        """Get record count statistics.
        
        Returns:
            Dictionary with counts for each record type
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM news")
        news_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM private_ads")
        ads_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM recipes")
        recipes_count = cursor.fetchone()[0]
        
        return {
            "news": news_count,
            "private_ads": ads_count,
            "recipes": recipes_count,
            "total": news_count + ads_count + recipes_count
        }
    
    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def main():
    """Demo of database functionality."""
    import sys
    from pathlib import Path
    
    # Add parent to path for imports
    sys.path.insert(0, str(Path(__file__).parent))
    
    # Create database manager
    db = FeedDatabaseManager()
    
    # Demo: Save some records
    print("\n" + "="*50)
    print("Database Manager Demo")
    print("="*50)
    
    # Save news
    success, msg = db.save_news("Breaking: New technology discovered", "San Francisco")
    print(msg)
    
    # Try to save duplicate news
    success, msg = db.save_news("Breaking: New technology discovered", "San Francisco")
    print(msg)
    
    # Save private ad
    success, msg = db.save_private_ad("Selling laptop", "2025-12-31")
    print(msg)
    
    # Save recipe
    success, msg = db.save_recipe("Pasta Carbonara", "pasta, eggs, bacon, parmesan", 4, "SIMPLE")
    print(msg)
    
    # Show statistics
    print("\n" + "="*50)
    print("Database Statistics:")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    db.close()


if __name__ == "__main__":
    main()
