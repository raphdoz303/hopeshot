"""
NewsData.io client implementation
Handles NewsData.io integration with positive news filtering
"""
import aiohttp
from typing import Dict, List, Any
from .base_client import BaseNewsClient


class NewsDataClient(BaseNewsClient):
    """Client for NewsData.io service"""
    
    def __init__(self):
        super().__init__("newsdata")
        self.api_key = self.get_env_var("NEWSDATA_API_KEY")
        self.base_url = "https://newsdata.io/api/1"
    
    def is_configured(self) -> bool:
        """Check if NewsData API key is configured"""
        return self.api_key is not None and len(self.api_key) > 0
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test NewsData.io connection"""
        if not self.is_configured():
            return {
                'source': self.source_name,
                'status': 'error',
                'message': 'NEWSDATA_API_KEY not configured'
            }
        
        try:
            # Test with minimal request
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/news"
                params = {
                    'apikey': self.api_key,
                    'q': 'test',
                    'size': 1
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
    
    async def fetch_news(self, query: str = "", language: str = "en", page_size: int = 10) -> Dict[str, Any]:
        """Fetch positive news from NewsData.io"""
        if not self.is_configured():
            return self.format_error_response("NEWSDATA_API_KEY not configured")
        
        # Default to positive keywords if no query provided
        if not query:
            query = "breakthrough innovation success positive"
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/news"
                params = {
                    'apikey': self.api_key,
                    'q': query,
                    'language': language,
                    'size': min(page_size, 10),  # NewsData free tier max is 10
                    'category': 'technology,science,health'  # Focus on positive categories
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Normalize articles
                        normalized_articles = [
                            self.normalize_article(article) 
                            for article in data.get('results', [])
                        ]
                        
                        # Remove duplicates
                        unique_articles = self.remove_duplicates(normalized_articles)
                        
                        return {
                            'status': 'success',
                            'source': self.source_name,
                            'totalResults': data.get('totalResults', len(unique_articles)),
                            'articles': unique_articles
                        }
                    else:
                        error_text = await response.text()
                        return self.format_error_response(
                            f"NewsData error: HTTP {response.status} - {error_text}"
                        )
        
        except Exception as e:
            return self.format_error_response(f"Request failed: {str(e)}")
    
    def normalize_article(self, raw_article: Dict[str, Any]) -> Dict[str, Any]:
        """Convert NewsData.io article to standard format"""
        normalized = self.base_article_structure.copy()
        normalized.update({
            'title': raw_article.get('title', ''),
            'description': raw_article.get('description', ''),
            'url': raw_article.get('link', ''),  # NewsData uses 'link' not 'url'
            'urlToImage': raw_article.get('image_url'),
            'source': {
                'id': raw_article.get('source_id', ''),
                'name': raw_article.get('source_name', '')
            },
            'author': ', '.join(raw_article.get('creator', [])) if raw_article.get('creator') else None,
            'publishedAt': raw_article.get('pubDate', ''),
            'content': raw_article.get('content'),
            'api_source': 'newsdata'  # Track which API provided this article
        })
        return normalized