import sqlite3
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime

class DatabaseService:
    def __init__(self):
        """Initialize database service with direct M49 code integration"""
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

    def get_location_names_and_emojis_by_m49(self, m49_codes: List[int]) -> tuple[List[str], List[str]]:
        """Get location names and emojis by M49 codes for API response display"""
        if not m49_codes:
            return [], []
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
        
            # Build query with placeholders - fetch both name and emoji
            placeholders = ','.join('?' for _ in m49_codes)
            query = f"SELECT name, emoji FROM locations WHERE m49_code IN ({placeholders}) ORDER BY hierarchy_level"
        
            cursor.execute(query, m49_codes)
            results = cursor.fetchall()
            conn.close()
        
            # Separate names and emojis
            names = [row[0] for row in results]
            emojis = [row[1] if row[1] else '🌍' for row in results]  # Default emoji if missing
        
            return names, emojis
        
        except Exception as e:
            print(f"Error looking up location names and emojis: {e}")
            return [], []

    def insert_article(self, article: Dict[str, Any], gemini_analysis: Dict[str, Any], 
                      prompt_version: str = None, prompt_name: str = None) -> Optional[int]:
        """
        Insert article with Gemini analysis using direct M49 code storage
        No more location_id conversion - stores M49 codes directly in junction table
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
            
            # Extract other analysis fields (no geographic columns in articles table anymore)
            analysis_data = {
                'source_credibility': gemini_analysis.get('source_credibility', ''),
                'fact_checkable_claims': gemini_analysis.get('fact_checkable_claims', ''),
                'evidence_quality': gemini_analysis.get('evidence_quality', ''),
                'controversy_level': gemini_analysis.get('controversy_level', ''),
                'solution_focused': gemini_analysis.get('solution_focused', ''),
                'age_appropriate': gemini_analysis.get('age_appropriate', ''),
                'truth_seeking': gemini_analysis.get('truth_seeking', ''),
                'geographical_impact_level': gemini_analysis.get('geographical_impact_level', ''),  # Keep this for filtering
                'reasoning': gemini_analysis.get('reasoning', ''),
                'analyzer_type': 'gemini',
                'overall_hopefulness': gemini_analysis.get('overall_hopefulness', 0.0),
                'prompt_id': prompt_version,
                'prompt_name': prompt_name
            }
            
            # Combine all data
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
            
            # Handle M49 codes - NEW DIRECT STORAGE APPROACH
            m49_codes = gemini_analysis.get('geographical_impact_m49_codes', [])
            
            if m49_codes:
                for m49_code in m49_codes:
                    if m49_code:
                        # Store M49 code directly - no location_id conversion needed
                        cursor.execute(
                            "INSERT OR IGNORE INTO article_locations (article_id, m49_code) VALUES (?, ?)",
                            (article_id, m49_code)
                        )
            else:
                # Fallback: if no M49 codes provided, default to World (001)
                cursor.execute(
                    "INSERT OR IGNORE INTO article_locations (article_id, m49_code) VALUES (?, ?)",
                    (article_id, 1)  # World
                )
            
            conn.commit()
            conn.close()
            
            print(f"Inserted article: {article_data['title'][:50]}... (ID: {article_id})")
            print(f"  M49 codes stored: {m49_codes}")
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

    def get_articles_with_locations(self, limit: int = 20, category_filter: List[str] = None, 
                                   impact_level_filter: List[str] = None) -> List[Dict[str, Any]]:
        """
        Get articles with their location information via M49 JOIN
        Supports filtering by categories and impact levels
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Build query with optional filters
            base_query = """
                SELECT DISTINCT
                    a.id,
                    a.title,
                    a.description,
                    a.url_id as url,
                    a.author,
                    a.published_at as publishedAt,
                    a.source_name,
                    a.geographical_impact_level,
                    a.overall_hopefulness,
                    GROUP_CONCAT(DISTINCT c.name) as categories,
                    GROUP_CONCAT(DISTINCT l.name) as location_names,
                    GROUP_CONCAT(DISTINCT al.m49_code) as m49_codes
                FROM articles a
                LEFT JOIN article_categories ac ON a.id = ac.article_id
                LEFT JOIN categories c ON ac.category_id = c.id
                LEFT JOIN article_locations al ON a.id = al.article_id
                LEFT JOIN locations l ON al.m49_code = l.m49_code
            """
            
            where_conditions = []
            params = []
            
            # Category filtering
            if category_filter:
                placeholders = ','.join('?' for _ in category_filter)
                where_conditions.append(f"c.name IN ({placeholders})")
                params.extend(category_filter)
            
            # Impact level filtering
            if impact_level_filter:
                placeholders = ','.join('?' for _ in impact_level_filter)
                where_conditions.append(f"a.geographical_impact_level IN ({placeholders})")
                params.extend(impact_level_filter)
            
            # Add WHERE clause if we have conditions
            if where_conditions:
                base_query += " WHERE " + " AND ".join(where_conditions)
            
            # Group and order
            base_query += """
                GROUP BY a.id
                ORDER BY a.published_at DESC
                LIMIT ?
            """
            params.append(limit)
            
            cursor.execute(base_query, params)
            rows = cursor.fetchall()
            
            articles = []
            for row in rows:
                # Parse categories and locations
                categories = row[9].split(',') if row[9] else []
                m49_codes = [int(code) for code in row[11].split(',') if code] if row[11] else [1]

                # Use the new function to get both names and emojis
                location_names, location_emojis = self.get_location_names_and_emojis_by_m49(m49_codes)

                # Fallback to defaults if empty
                if not location_names:
                    location_names = ['World']
                    location_emojis = ['🌍']
                
                article = {
                    'title': row[1],
                    'description': row[2],
                    'url': row[3],
                    'author': row[4],
                    'publishedAt': row[5],
                    'source': {'name': row[6]},
                    'gemini_analysis': {
                        'categories': categories,
                        'geographical_impact_level': row[7],
                        'geographical_impact_location_names': location_names,
                        'geographical_impact_location_emojis': location_emojis,  # ADD THIS LINE
                        'geographical_impact_m49_codes': m49_codes,
                        'overall_hopefulness': row[8]
                    }
                }
                articles.append(article)
            
            conn.close()
            return articles
            
        except Exception as e:
            print(f"Error fetching articles with locations: {e}")
            return []

    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics with M49 integration info"""
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
            
            # Get top locations by M49 code
            cursor.execute("""
                SELECT l.name, l.hierarchy_level, l.m49_code, COUNT(*) as count
                FROM locations l
                JOIN article_locations al ON l.m49_code = al.m49_code
                GROUP BY l.m49_code, l.name, l.hierarchy_level
                ORDER BY count DESC
                LIMIT 5
            """)
            top_locations = cursor.fetchall()
            
            # Test M49 schema
            cursor.execute("PRAGMA table_info(article_locations)")
            al_schema = cursor.fetchall()
            has_m49_column = any(col[1] == 'm49_code' for col in al_schema)
            
            conn.close()
            
            return {
                'articles': article_count,
                'categories': category_count,
                'locations': location_count,
                'category_relationships': category_relationships,
                'location_relationships': location_relationships,
                'articles_last_24h': recent_articles,
                'top_categories': [{'name': cat[0], 'count': cat[1]} for cat in top_categories],
                'top_locations': [{'name': loc[0], 'level': loc[1], 'm49_code': loc[2], 'count': loc[3]} for loc in top_locations],
                'database_path': str(self.db_path),
                'm49_integration': {
                    'schema_updated': has_m49_column,
                    'junction_table': 'article_locations (article_id, m49_code)',
                    'direct_storage': True
                }
            }
            
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return {}

    def test_connection(self) -> Dict[str, Any]:
        """Test database connection and M49 integration"""
        try:
            stats = self.get_database_stats()
            
            # Test M49 join query
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Test that we can join on M49 codes
            cursor.execute("""
                SELECT COUNT(*) 
                FROM article_locations al
                JOIN locations l ON al.m49_code = l.m49_code
            """)
            join_test = cursor.fetchone()[0]
            
            # Test article_locations schema
            cursor.execute("PRAGMA table_info(article_locations)")
            schema = cursor.fetchall()
            columns = [col[1] for col in schema]
            
            conn.close()
            
            return {
                'status': 'success',
                'message': 'Database connected with direct M49 integration',
                'stats': stats,
                'article_locations_schema': columns,
                'm49_join_test_count': join_test,
                'schema_version': 'm49_direct_v1'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Database connection failed: {str(e)}'
            }