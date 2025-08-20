"""
Base class for all news API clients
Provides common functionality and interface standardization
"""
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime


class BaseNewsClient(ABC):
    """Abstract base class for news API clients"""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.base_article_structure = {
            'title': '',
            'description': '',
            'url': '',
            'urlToImage': None,
            'source': {'id': '', 'name': ''},
            'author': None,
            'publishedAt': '',
            'content': None
        }
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Check if API credentials are properly configured"""
        pass
    
    @abstractmethod
    async def fetch_news(self, query: str = "", language: str = "en", page_size: int = 20) -> Dict[str, Any]:
        """Fetch news articles from the API source"""
        pass
    
    @abstractmethod
    async def test_connection(self) -> Dict[str, Any]:
        """Test API connection and return status"""
        pass
    
    def normalize_article(self, raw_article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert raw API response to standardized article format
        Override this method in each client for their specific format
        """
        return raw_article
    
    def remove_duplicates(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate articles within same source based on exact title match"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            title = article.get('title', '').strip().lower()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_articles.append(article)
        
        return unique_articles
    
    def get_env_var(self, var_name: str) -> Optional[str]:
        """Get environment variable with None fallback"""
        return os.getenv(var_name)
    
    def format_error_response(self, error_message: str) -> Dict[str, Any]:
        """Standardized error response format"""
        return {
            'status': 'error',
            'source': self.source_name,
            'error': error_message,
            'articles': []
        }