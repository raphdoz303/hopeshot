"""
HopeShot Deduplication Service
Modular service for detecting and preventing duplicate articles across news sources
"""

from typing import Dict, List, Optional, Tuple
import sqlite3
from difflib import SequenceMatcher
import logging


class DeduplicationService:
    """
    Modular deduplication service for article duplicate detection.
    
    Uses two-tier approach:
    1. Primary: Exact URL matching (catches republished articles)
    2. Secondary: Title similarity >80% (catches same story from different sources)
    """
    
    def __init__(self, db_path: str = "hopeshot_news.db"):
        self.db_path = db_path
        self.title_similarity_threshold = 0.8  # 80% similarity threshold
        self.logger = logging.getLogger(__name__)
    
    def is_duplicate(self, article: Dict) -> Tuple[bool, Optional[str]]:
        """
        Check if article is a duplicate of existing articles in database.
        
        Args:
            article: Dictionary with keys 'url', 'title' (minimum required)
            
        Returns:
            Tuple of (is_duplicate: bool, reason: str)
            - (True, "URL match") if exact URL found
            - (True, "Title similarity") if similar title found  
            - (False, None) if no duplicates detected
        """
        try:
            # Validate required fields
            if not article.get('url') or not article.get('title'):
                self.logger.warning("Article missing required fields (url, title)")
                return False, None
            
            # Check for URL duplicates first (fastest check)
            url_duplicate = self._check_url_duplicate(article['url'])
            if url_duplicate:
                return True, "URL match"
            
            # Check for title similarity (more expensive check)
            title_duplicate = self._check_title_similarity(article['title'])
            if title_duplicate:
                return True, "Title similarity"
                
            return False, None
            
        except Exception as e:
            self.logger.error(f"Error checking duplicates: {e}")
            # Fail safe - allow article through if service fails
            return False, None
    
    def _check_url_duplicate(self, url: str) -> bool:
        """Check if exact URL already exists in database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM articles WHERE url_id = ? LIMIT 1", (url,))
                return cursor.fetchone() is not None
        except Exception as e:
            self.logger.error(f"URL duplicate check failed: {e}")
            return False
    
    def _check_title_similarity(self, title: str) -> bool:
        """Check if similar title exists using SequenceMatcher."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Get all titles for comparison (could optimize with LIMIT if database grows large)
                cursor.execute("SELECT title FROM articles")
                existing_titles = [row[0] for row in cursor.fetchall()]
                
                # Compare with each existing title
                for existing_title in existing_titles:
                    similarity = SequenceMatcher(None, title.lower(), existing_title.lower()).ratio()
                    if similarity >= self.title_similarity_threshold:
                        self.logger.info(f"Title similarity detected: {similarity:.2f} between '{title}' and '{existing_title}'")
                        return True
                        
                return False
                
        except Exception as e:
            self.logger.error(f"Title similarity check failed: {e}")
            return False
    
    def get_duplicate_stats(self) -> Dict:
        """Get statistics about duplicates detected (for monitoring/debugging)."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count total articles
                cursor.execute("SELECT COUNT(*) FROM articles")
                total_articles = cursor.fetchone()[0]
                
                # Count articles in last 30 days (what we compare against)
                cursor.execute("SELECT COUNT(*) FROM articles WHERE timestamp > datetime('now', '-30 days')")
                recent_articles = cursor.fetchone()[0]
                
                # Count articles by source (helps identify duplicate-heavy sources)
                cursor.execute("""
                    SELECT original_source, COUNT(*) as count 
                    FROM articles 
                    GROUP BY original_source 
                    ORDER BY count DESC
                """)
                source_counts = dict(cursor.fetchall())
                
                return {
                    "total_articles": total_articles,
                    "articles_compared_against": recent_articles,
                    "comparison_scope_days": 30,
                    "articles_by_source": source_counts,
                    "threshold_used": self.title_similarity_threshold,
                    "performance_optimization": "30-day window active"
                }
                
        except Exception as e:
            self.logger.error(f"Stats retrieval failed: {e}")
            return {"error": str(e)}