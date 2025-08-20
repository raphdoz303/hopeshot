"""
NewsAPI.org client implementation
Handles NewsAPI.org integration with positive news filtering
"""
import aiohttp
from typing import Dict, List, Any
from .base_client import BaseNewsClient


class NewsAPIClient(BaseNewsClient):
    """Client for NewsAPI.org service"""
    
    def __init__(self):
        super().__init__("newsapi")
        self.api_key = self.get_env_var("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
    
    def is_configured(self) -> bool:
        """Check if NewsAPI key is configured"""
        return self.api_key is not None and len(self.api_key) > 0
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test NewsAPI connection"""
        if not self.is_configured():
            return {
                'source': self.source_name,
                'status': 'error',
                'message': 'NEWS_API_KEY not configured'
            }
        
        try:
            # Test with minimal request
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/everything"
                params = {
                    'q': 'test',
                    'pageSize': 1,
                    'apiKey': self.api_key
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return {
                            'source': self.source_name,
                            'status': 'success',
                            'message': 'Connected successfully'
                        }
                    else:
                        return {
                            'source': self.source_name,
                            'status': 'error',
                            'message': f'HTTP {response.status}'
                        }
        
        except Exception as e:
            return {
                'source': self.source_name,
                'status': 'error',
                'message': f'Connection failed: {str(e)}'
            }
    
    async def fetch_news(self, query: str = "", language: str = "en", page_size: int = 20) -> Dict[str, Any]:
        """Fetch positive news from NewsAPI"""
        if not self.is_configured():
            return self.format_error_response("NEWS_API_KEY not configured")
        
        # Default to positive keywords if no query provided
        if not query:
            query = "positive breakthrough innovation hope success"
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/everything"
                params = {
                    'q': query,
                    'language': language,
                    'sortBy': 'relevancy',
                    'pageSize': min(page_size, 100),  # NewsAPI max is 100
                    'apiKey': self.api_key
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Normalize articles
                        normalized_articles = [
                            self.normalize_article(article) 
                            for article in data.get('articles', [])
                        ]
                        
                        # Remove duplicates
                        unique_articles = self.remove_duplicates(normalized_articles)
                        
                        return {
                            'status': 'success',
                            'source': self.source_name,
                            'totalResults': data.get('totalResults', 0),
                            'articles': unique_articles
                        }
                    else:
                        error_data = await response.json()
                        return self.format_error_response(
                            f"NewsAPI error: {error_data.get('message', 'Unknown error')}"
                        )
        
        except Exception as e:
            return self.format_error_response(f"Request failed: {str(e)}")
    
    def normalize_article(self, raw_article: Dict[str, Any]) -> Dict[str, Any]:
        """Convert NewsAPI article to standard format"""
        # NewsAPI already uses our standard format, just ensure all fields exist
        normalized = self.base_article_structure.copy()
        normalized.update({
            'title': raw_article.get('title', ''),
            'description': raw_article.get('description', ''),
            'url': raw_article.get('url', ''),
            'urlToImage': raw_article.get('urlToImage'),
            'source': raw_article.get('source', {'id': '', 'name': ''}),
            'author': raw_article.get('author'),
            'publishedAt': raw_article.get('publishedAt', ''),
            'content': raw_article.get('content'),
            'api_source': 'newsapi'  # Track which API provided this article
        })
        return normalized