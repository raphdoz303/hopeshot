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
            
            # DEBUG: Check what categories look like
            print(f"DEBUG Categories: {gemini_analysis.get('categories')} (type: {type(gemini_analysis.get('categories'))})")
            
            # Handle categories (many-to-many relationship) - SINGLE CLEAN VERSION
            categories = gemini_analysis.get('categories', [])
            print(f"DEBUG: Raw categories = {categories}")

            # Handle both list and string formats
            if isinstance(categories, str):
                try:
                    categories = json.loads(categories)
                    print(f"DEBUG: Parsed string to list = {categories}")
                except json.JSONDecodeError:
                    categories = [categories] if categories else []
                    print(f"DEBUG: JSON parse failed, using as single item = {categories}")
            elif not isinstance(categories, list):
                categories = []
                print(f"DEBUG: Not a list or string, setting to empty list")

            print(f"DEBUG: Final categories list = {categories}")

            # Create categories and link to article
            for category_name in categories:
                print(f"DEBUG: Processing category: '{category_name}'")
                if category_name and category_name.strip():
                    category_id = self.get_or_create_category(category_name.strip(), conn=conn)
                    print(f"DEBUG: Created/found category ID: {category_id}")
                    if category_id:
                        cursor.execute(
                            "INSERT OR IGNORE INTO article_categories (article_id, category_id) VALUES (?, ?)",
                            (article_id, category_id)
                        )
                        print(f"DEBUG: Linked article {article_id} to category {category_id}")
                else:
                    print(f"DEBUG: Skipping empty/invalid category: '{category_name}'")
            
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

    def get_articles_with_locations(self, limit: int = 50, location_filter: str = None) -> List[Dict[str, Any]]:
        """
        Get recent articles with their categories and locations using proper joins
        Supports filtering by specific location name
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Base query with location joins
            base_query = """
                SELECT DISTINCT a.*
                FROM articles a
                LEFT JOIN article_locations al ON a.id = al.article_id
                LEFT JOIN locations l ON al.location_id = l.id
            """
            
            # Add location filter if specified
            where_clause = ""
            params = []
            
            if location_filter:
                where_clause = "WHERE l.name LIKE ? OR a.geographical_impact_level = ?"
                params = [f"%{location_filter}%", location_filter]
            
            # Complete query
            query = f"""
                {base_query}
                {where_clause}
                ORDER BY a.timestamp DESC
                LIMIT ?
            """
            params.append(limit)
            
            cursor.execute(query, params)
            columns = [description[0] for description in cursor.description]
            articles = []
            
            for row in cursor.fetchall():
                article = dict(zip(columns, row))
                
                # Get categories for this article
                cursor.execute("""
                    SELECT c.name, c.description, c.color, c.emoji
                    FROM categories c
                    JOIN article_categories ac ON c.id = ac.category_id
                    WHERE ac.article_id = ?
                """, (article['id'],))
                
                categories = cursor.fetchall()
                article['categories'] = [
                    {'name': cat[0], 'description': cat[1], 'color': cat[2], 'emoji': cat[3]}
                    for cat in categories
                ]
                
                # Get locations for this article (multi-location support)
                cursor.execute("""
                    SELECT l.id, l.name, l.level, l.parent_id,
                           parent.name as parent_name, parent.level as parent_level
                    FROM locations l
                    JOIN article_locations al ON l.id = al.location_id
                    LEFT JOIN locations parent ON l.parent_id = parent.id
                    WHERE al.article_id = ?
                    ORDER BY l.level, l.name
                """, (article['id'],))
                
                locations = cursor.fetchall()
                article['locations'] = [
                    {
                        'id': loc[0],
                        'name': loc[1], 
                        'level': loc[2],
                        'parent_id': loc[3],
                        'parent_name': loc[4],
                        'parent_level': loc[5]
                    }
                    for loc in locations
                ]
                
                articles.append(article)
            
            conn.close()
            return articles
            
        except Exception as e:
            print(f"Error retrieving articles with locations: {e}")
            return []

    def get_articles_by_location(self, location_name: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get articles that mention a specific location (including parent relationships)
        Example: get_articles_by_location("France") returns articles about France
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Find articles that mention this location or its children
            query = """
                SELECT DISTINCT a.*
                FROM articles a
                JOIN article_locations al ON a.id = al.article_id
                JOIN locations l ON al.location_id = l.id
                LEFT JOIN locations parent ON l.parent_id = parent.id
                WHERE l.name = ? OR parent.name = ?
                ORDER BY a.timestamp DESC
                LIMIT ?
            """
            
            cursor.execute(query, (location_name, location_name, limit))
            columns = [description[0] for description in cursor.description]
            articles = []
            
            for row in cursor.fetchall():
                article = dict(zip(columns, row))
                
                # Add location and category data
                article = self._add_article_relationships(cursor, article)
                articles.append(article)
            
            conn.close()
            return articles
            
        except Exception as e:
            print(f"Error retrieving articles by location: {e}")
            return []

    def _add_article_relationships(self, cursor, article: Dict) -> Dict:
        """Helper method to add categories and locations to an article"""
        article_id = article['id']
        
        # Get categories
        cursor.execute("""
            SELECT c.name, c.description, c.color, c.emoji
            FROM categories c
            JOIN article_categories ac ON c.id = ac.category_id
            WHERE ac.article_id = ?
        """, (article_id,))
        
        categories = cursor.fetchall()
        article['categories'] = [
            {'name': cat[0], 'description': cat[1], 'color': cat[2], 'emoji': cat[3]}
            for cat in categories
        ]
        
        # Get locations with hierarchy
        cursor.execute("""
            SELECT l.id, l.name, l.level, l.parent_id,
                   parent.name as parent_name, parent.level as parent_level
            FROM locations l
            JOIN article_locations al ON l.id = al.location_id
            LEFT JOIN locations parent ON l.parent_id = parent.id
            WHERE al.article_id = ?
            ORDER BY l.level, l.name
        """, (article_id,))
        
        locations = cursor.fetchall()
        article['locations'] = [
            {
                'id': loc[0],
                'name': loc[1], 
                'level': loc[2],
                'parent_id': loc[3],
                'parent_name': loc[4],
                'parent_level': loc[5]
            }
            for loc in locations
        ]
        
        return article

    def get_recent_articles(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent articles with categories and locations"""
        return self.get_articles_with_locations(limit)

    def get_location_hierarchy(self, location_id: int) -> Dict[str, Any]:
        """Get full hierarchy for a location (child -> parent -> grandparent)"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get location with its full hierarchy
            cursor.execute("""
                WITH RECURSIVE location_hierarchy AS (
                    SELECT id, name, level, parent_id, 0 as depth
                    FROM locations 
                    WHERE id = ?
                    
                    UNION ALL
                    
                    SELECT l.id, l.name, l.level, l.parent_id, lh.depth + 1
                    FROM locations l
                    JOIN location_hierarchy lh ON l.id = lh.parent_id
                )
                SELECT * FROM location_hierarchy ORDER BY depth
            """, (location_id,))
            
            hierarchy = cursor.fetchall()
            conn.close()
            
            return {
                'location_chain': [
                    {'id': row[0], 'name': row[1], 'level': row[2], 'depth': row[4]}
                    for row in hierarchy
                ]
            }
            
        except Exception as e:
            print(f"Error getting location hierarchy: {e}")
            return {'location_chain': []}

    def get_articles_by_category(self, category_name: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get articles by category with full location data"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT DISTINCT a.*
                FROM articles a
                JOIN article_categories ac ON a.id = ac.article_id
                JOIN categories c ON ac.category_id = c.id
                WHERE c.name = ?
                ORDER BY a.timestamp DESC
                LIMIT ?
            """
            
            cursor.execute(query, (category_name, limit))
            columns = [description[0] for description in cursor.description]
            articles = []
            
            for row in cursor.fetchall():
                article = dict(zip(columns, row))
                article = self._add_article_relationships(cursor, article)
                articles.append(article)
            
            conn.close()
            return articles
            
        except Exception as e:
            print(f"Error retrieving articles by category: {e}")
            return []

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

    def search_articles(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search articles by title, description, or location/category names
        Full-text search across multiple fields
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT DISTINCT a.*
                FROM articles a
                LEFT JOIN article_categories ac ON a.id = ac.article_id
                LEFT JOIN categories c ON ac.category_id = c.id
                LEFT JOIN article_locations al ON a.id = al.article_id
                LEFT JOIN locations l ON al.location_id = l.id
                WHERE 
                    a.title LIKE ? OR 
                    a.description LIKE ? OR 
                    c.name LIKE ? OR 
                    l.name LIKE ?
                ORDER BY a.timestamp DESC
                LIMIT ?
            """
            
            search_param = f"%{search_term}%"
            cursor.execute(query, (search_param, search_param, search_param, search_param, limit))
            
            columns = [description[0] for description in cursor.description]
            articles = []
            
            for row in cursor.fetchall():
                article = dict(zip(columns, row))
                article = self._add_article_relationships(cursor, article)
                articles.append(article)
            
            conn.close()
            return articles
            
        except Exception as e:
            print(f"Error searching articles: {e}")
            return []

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