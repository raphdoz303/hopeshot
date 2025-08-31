import sqlite3
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime

class DatabaseService:
    def __init__(self):
        """Initialize database service with multi-location junction table support"""
        self.db_path = Path(__file__).parent.parent / 'hopeshot_news.db'
        
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")
        
        print(f"Database service initialized: {self.db_path}")

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with foreign keys enabled"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def get_all_categories(self):
        """Get all categories with their metadata for frontend filtering"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, filter_name, emoji, description, color, accent
                FROM categories 
                ORDER BY filter_name
            """)
            
            rows = cursor.fetchall()
            categories = []
            
            for row in rows:
                categories.append({
                    "id": row[0],
                    "name": row[1],           # For API/Gemini (e.g., "science tech")
                    "filter_name": row[2],   # For UI display (e.g., "Science & Tech") 
                    "emoji": row[3],
                    "description": row[4],
                    "color": row[5],
                    "accent": row[6]
                })
            
            conn.close()
            return categories
            
        except Exception as e:
            print(f"Error fetching categories: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_or_create_category(self, name: str, description: str = None, color: str = None, emoji: str = None,
                            conn: Optional[sqlite3.Connection] = None) -> Optional[int]:
        """
        Get category ID, create if it doesn't exist.
        Uses existing connection if provided (prevents multiple open connections).
        """
        try:
            # If no connection is passed, open a new one (standalone usage)
            own_connection = False
            if conn is None:
                conn = self._get_connection()
                own_connection = True

            cursor = conn.cursor()

            # Check if category exists
            cursor.execute("SELECT id FROM categories WHERE name = ?", (name,))
            result = cursor.fetchone()
            if result:
                return result[0]

            # Create new category
            cursor.execute(
                "INSERT INTO categories (name, description, color, emoji) VALUES (?, ?, ?, ?)",
                (name, description, color, emoji)
            )
            category_id = cursor.lastrowid

            # Only commit if we own this connection
            if own_connection:
                conn.commit()

            print(f"Created new category: {name} (ID: {category_id})")
            return category_id

        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower():
                print(f"Database locked while creating category '{name}'. Consider WAL mode or retries.")
            else:
                print(f"Error with category creation: {e}")
            return None

        except Exception as e:
            print(f"Unexpected error with category creation: {e}")
            return None

        finally:
            # Close only if we opened the connection
            if own_connection:
                conn.close()

    def get_or_create_location(self, name: str, level: str, parent_name: str = None) -> Optional[int]:
        """
        Get location ID, create if doesn't exist with hierarchy
        This mirrors the GeminiService location logic
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if location exists
            cursor.execute("SELECT id FROM locations WHERE name = ? AND level = ?", (name, level))
            result = cursor.fetchone()
            
            if result:
                location_id = result[0]
                conn.close()
                return location_id
            
            # Find or create parent if needed
            parent_id = None
            if parent_name and parent_name != name:
                parent_level = self._get_parent_level(level)
                if parent_level:
                    parent_id = self.get_or_create_location(parent_name, parent_level)
            
            # Create new location
            cursor.execute(
                "INSERT INTO locations (name, level, parent_id) VALUES (?, ?, ?)",
                (name, level, parent_id)
            )
            location_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"Created new location: {name} ({level}) with ID {location_id}")
            return location_id
            
        except Exception as e:
            print(f"Error with location creation: {e}")
            return None

    def _get_parent_level(self, current_level: str) -> Optional[str]:
        """Get parent level in geographic hierarchy"""
        hierarchy = {
            'country': 'region',
            'region': 'continent'
        }
        return hierarchy.get(current_level)

    def insert_article(self, article: Dict[str, Any], gemini_analysis: Dict[str, Any], 
                      prompt_version: str = None, prompt_name: str = None) -> Optional[int]:
        """
        Insert article with Gemini analysis into database
        Auto-creates categories and handles multi-location arrays
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Extract basic article data
            article_data = {
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'url_id': article.get('url', ''),
                'author': article.get('author', ''),
                'published_at': article.get('publishedAt', ''),
                'language': article.get('language', 'en'),
                'news_type': article.get('news_type', 'article'),
                'source_type': article.get('source_type', 'api'),
                'source_name': article.get('source', {}).get('name', ''),
                'source_id': article.get('source', {}).get('id', ''),
                'original_source': article.get('api_source', '')
            }
            
            # Extract sentiment analysis from Gemini
            emotions = gemini_analysis.get('emotions', {})
            sentiment_data = {
                'uplift_score': gemini_analysis.get('overall_hopefulness', 0.0),
                'sentiment_positive': 1 if gemini_analysis.get('sentiment') == 'positive' else 0,
                'sentiment_negative': 1 if gemini_analysis.get('sentiment') == 'negative' else 0,
                'sentiment_neutral': 1 if gemini_analysis.get('sentiment') == 'neutral' else 0,
                'sentiment_confidence': gemini_analysis.get('confidence_score', 0.0),
                'emotion_hope': emotions.get('hope', 0.0),
                'emotion_awe': emotions.get('awe', 0.0),
                'emotion_gratitude': emotions.get('gratitude', 0.0),
                'emotion_compassion': emotions.get('compassion', 0.0),
                'emotion_relief': emotions.get('relief', 0.0),
                'emotion_joy': emotions.get('joy', 0.0)
            }
            
            # Extract other analysis fields (note: no geographical_impact_location here)
            analysis_data = {
                'source_credibility': gemini_analysis.get('source_credibility', ''),
                'fact_checkable_claims': gemini_analysis.get('fact_checkable_claims', ''),
                'evidence_quality': gemini_analysis.get('evidence_quality', ''),
                'controversy_level': gemini_analysis.get('controversy_level', ''),
                'solution_focused': gemini_analysis.get('solution_focused', ''),
                'age_appropriate': gemini_analysis.get('age_appropriate', ''),
                'truth_seeking': gemini_analysis.get('truth_seeking', ''),
                'geographical_impact_level': gemini_analysis.get('geographical_impact_level', ''),
                'reasoning': gemini_analysis.get('reasoning', ''),
                'analyzer_type': 'gemini',
                'prompt_id': prompt_version,
                'prompt_name': prompt_name
            }
            
            # Combine all data (excluding geographical_impact_location)
            all_data = {**article_data, **sentiment_data, **analysis_data}
            
            # Build INSERT query for main articles table
            columns = list(all_data.keys())
            placeholders = ['?' for _ in columns]
            values = list(all_data.values())
            
            insert_query = f"""
                INSERT INTO articles ({', '.join(columns)}) 
                VALUES ({', '.join(placeholders)})
            """
            
            cursor.execute(insert_query, values)
            article_id = cursor.lastrowid
            
            # Handle categories (many-to-many relationship)
            categories = gemini_analysis.get('categories', [])
            
            # Handle both list and string formats
            if isinstance(categories, str):
                try:
                    categories = json.loads(categories)
                except json.JSONDecodeError:
                    categories = [categories] if categories else []
            elif not isinstance(categories, list):
                categories = []

            # Create categories and link to article
            for category_name in categories:
                if category_name and category_name.strip():
                    category_id = self.get_or_create_category(category_name.strip(), conn=conn)
                    if category_id:
                        cursor.execute(
                            "INSERT OR IGNORE INTO article_categories (article_id, category_id) VALUES (?, ?)",
                            (article_id, category_id)
                        )
            
            # Handle locations (many-to-many relationship via junction table)
            location_ids = gemini_analysis.get('geographical_impact_location_ids', [])
            if location_ids:
                for location_id in location_ids:
                    if location_id:
                        cursor.execute(
                            "INSERT OR IGNORE INTO article_locations (article_id, location_id) VALUES (?, ?)",
                            (article_id, location_id)
                        )
            
            conn.commit()
            conn.close()
            
            print(f"Inserted article: {article_data['title'][:50]}... (ID: {article_id})")
            return article_id
            
        except Exception as e:
            print(f"Error inserting article: {e}")
            import traceback
            traceback.print_exc()
            return None

    def check_url_exists(self, url: str) -> bool:
        """Check if URL already exists in database (for deduplication)"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM articles WHERE url_id = ?", (url,))
            count = cursor.fetchone()[0]
            conn.close()
            
            return count > 0
            
        except Exception as e:
            print(f"Error checking URL existence: {e}")
            return False

    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics including junction tables"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Count main tables
            cursor.execute("SELECT COUNT(*) FROM articles")
            article_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM categories")
            category_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM locations")
            location_count = cursor.fetchone()[0]
            
            # Count junction table relationships
            cursor.execute("SELECT COUNT(*) FROM article_categories")
            category_relationships = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM article_locations")
            location_relationships = cursor.fetchone()[0]
            
            # Get recent activity
            cursor.execute("SELECT COUNT(*) FROM articles WHERE timestamp > datetime('now', '-24 hours')")
            recent_articles = cursor.fetchone()[0]
            
            # Get top categories
            cursor.execute("""
                SELECT c.name, COUNT(*) as count
                FROM categories c
                JOIN article_categories ac ON c.id = ac.category_id
                GROUP BY c.name
                ORDER BY count DESC
                LIMIT 5
            """)
            top_categories = cursor.fetchall()
            
            # Get top locations
            cursor.execute("""
                SELECT l.name, l.level, COUNT(*) as count
                FROM locations l
                JOIN article_locations al ON l.id = al.location_id
                GROUP BY l.name, l.level
                ORDER BY count DESC
                LIMIT 5
            """)
            top_locations = cursor.fetchall()
            
            conn.close()
            
            return {
                'articles': article_count,
                'categories': category_count,
                'locations': location_count,
                'category_relationships': category_relationships,
                'location_relationships': location_relationships,
                'articles_last_24h': recent_articles,
                'top_categories': [{'name': cat[0], 'count': cat[1]} for cat in top_categories],
                'top_locations': [{'name': loc[0], 'level': loc[1], 'count': loc[2]} for loc in top_locations],
                'database_path': str(self.db_path)
            }
            
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return {}

    def test_connection(self) -> Dict[str, Any]:
        """Test database connection and junction table setup"""
        try:
            stats = self.get_database_stats()
            
            # Test junction table exists
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='article_locations'")
            junction_exists = bool(cursor.fetchone())
            conn.close()
            
            return {
                'status': 'success',
                'message': 'Database connected with multi-location support',
                'stats': stats,
                'junction_table_exists': junction_exists
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Database connection failed: {str(e)}'
            }