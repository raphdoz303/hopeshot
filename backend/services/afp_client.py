"""
AFP (Agence France-Presse) client implementation
Handles AFP API integration with OAuth2 authentication and built-in positive filtering
"""
import aiohttp
import base64
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from .base_client import BaseNewsClient


class AFPClient(BaseNewsClient):
    """Client for AFP API service with OAuth2 authentication"""
    
    def __init__(self):
        super().__init__("afp")
        self.client_id = self.get_env_var("AFP_CLIENT_ID")
        self.client_secret = self.get_env_var("AFP_CLIENT_SECRET")
        self.username = self.get_env_var("AFP_USERNAME")
        self.password = self.get_env_var("AFP_PASSWORD")
        self.base_url = "https://afp-apicore-prod.afp.com"
        self.access_token = None
        self.token_expires_at = None
    
    def is_configured(self) -> bool:
        """Check if all AFP credentials are configured"""
        return all([
            self.client_id,
            self.client_secret,
            self.username,
            self.password
        ])
    
    async def _get_auth_headers(self) -> Dict[str, str]:
        """Get authorization headers for OAuth2"""
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    
    async def _authenticate(self) -> bool:
        """Authenticate with AFP API using OAuth2 password grant"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/oauth/token"
                headers = await self._get_auth_headers()
                data = {
                    'grant_type': 'password',
                    'username': self.username,
                    'password': self.password
                }
                
                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 200:
                        token_data = await response.json()
                        self.access_token = token_data.get('access_token')
                        expires_in = token_data.get('expires_in', 18000)  # Default 5 hours
                        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                        return True
                    else:
                        return False
        except Exception:
            return False
    
    async def _ensure_authenticated(self) -> bool:
        """Ensure we have a valid access token"""
        # Check if token exists and is not expired
        if (self.access_token and 
            self.token_expires_at and 
            datetime.now() < self.token_expires_at - timedelta(minutes=5)):  # 5 min buffer
            return True
        
        # Re-authenticate
        return await self._authenticate()
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test AFP API connection"""
        if not self.is_configured():
            return {
                'source': self.source_name,
                'status': 'error',
                'message': 'AFP credentials not configured (need CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD)'
            }
        
        # Test authentication
        if await self._authenticate():
            return {
                'source': self.source_name,
                'status': 'success',
                'message': 'Connected and authenticated successfully'
            }
        else:
            return {
                'source': self.source_name,
                'status': 'error',
                'message': 'Authentication failed - check credentials'
            }
    
    async def fetch_news(self, query: str = "", language: str = "en", page_size: int = 20) -> Dict[str, Any]:
        """Fetch positive news from AFP using built-in genre filtering"""
        if not self.is_configured():
            return self.format_error_response("AFP credentials not configured")
        
        if not await self._ensure_authenticated():
            return self.format_error_response("AFP authentication failed")
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/v1/api/search"
                headers = {
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                }
                
                # AFP search query with built-in positive filtering
                search_body = {
                    "dateRange": {"from": "now-7d", "to": "now"},
                    "sortOrder": "desc",
                    "sortField": "published",
                    "lang": language,
                    "maxRows": str(min(page_size, 100)),
                    "query": {
                        "and": [
                            {"name": "class", "and": ["text"]},
                            {"name": "genre", "and": ["inspiring"]}  # AFP's built-in positive filter!
                        ]
                    }
                }
                
                # Add custom query terms if provided
                if query:
                    search_body["query"]["and"].append({
                        "name": "fulltext", 
                        "and": [query]
                    })
                
                async with session.post(url, headers=headers, json=search_body) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # DEBUG: Let's see what AFP actually returns
                        print(f"🔍 AFP Response Status: {response.status}")
                        print(f"🔍 AFP Raw Data Keys: {list(data.keys())}")
                        print(f"🔍 AFP Total Results: {data}")
                        
                        # Normalize articles
                        raw_articles = data.get('documents', [])
                        normalized_articles = [
                            self.normalize_article(article) 
                            for article in raw_articles
                        ]
                        
                        # Remove duplicates
                        unique_articles = self.remove_duplicates(normalized_articles)
                        
                        return {
                            'status': 'success',
                            'source': self.source_name,
                            'totalResults': data.get('totalHits', len(unique_articles)),
                            'articles': unique_articles
                        }
                    else:
                        error_text = await response.text()
                        return self.format_error_response(
                            f"AFP search error: HTTP {response.status} - {error_text}"
                        )
        
        except Exception as e:
            return self.format_error_response(f"AFP request failed: {str(e)}")
    
    def normalize_article(self, raw_article: Dict[str, Any]) -> Dict[str, Any]:
        """Convert AFP article to standard format"""
        normalized = self.base_article_structure.copy()
        
        # AFP has complex nested structure
        header = raw_article.get('header', {})
        
        normalized.update({
            'title': header.get('headline', ''),
            'description': header.get('abstract', ''),
            'url': raw_article.get('href', ''),
            'urlToImage': None,  # AFP typically doesn't include images in search results
            'source': {
                'id': 'afp',
                'name': 'Agence France-Presse'
            },
            'author': ', '.join(header.get('byline', [])) if header.get('byline') else 'AFP',
            'publishedAt': header.get('published', ''),
            'content': raw_article.get('contentSet', {}).get('inlineData', '')[:200] + '...' if raw_article.get('contentSet') else None,
            'api_source': 'afp'  # Track which API provided this article
        })
        return normalized