"""
AFP (Agence France-Presse) client implementation
Professional news service with OAuth2 authentication
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
        self.refresh_token = None
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
        """Get authorization headers for OAuth2 using clientId:clientSecret"""
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
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
                        self.refresh_token = token_data.get('refresh_token')
                        expires_in = token_data.get('expires_in', 18000)
                        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                        return True
                    else:
                        return False
                        
        except Exception:
            return False
    
    async def _refresh_token_if_needed(self) -> bool:
        """Use refresh token to get new access token if needed"""
        if not self.refresh_token:
            return await self._authenticate()
            
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/oauth/token"
                headers = await self._get_auth_headers()
                
                data = {
                    'grant_type': 'refresh_token',
                    'refresh_token': self.refresh_token
                }
                
                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 200:
                        token_data = await response.json()
                        self.access_token = token_data.get('access_token')
                        self.refresh_token = token_data.get('refresh_token')
                        expires_in = token_data.get('expires_in', 18000)
                        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                        return True
                    else:
                        return await self._authenticate()
                        
        except Exception:
            return await self._authenticate()
    
    async def _ensure_authenticated(self) -> bool:
        """Ensure we have a valid access token"""
        if (self.access_token and 
            self.token_expires_at and 
            datetime.now() < self.token_expires_at - timedelta(minutes=5)):
            return True
        
        return await self._refresh_token_if_needed()
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test AFP API connection"""
        if not self.is_configured():
            return {
                'source': self.source_name,
                'status': 'error',
                'message': 'AFP credentials not configured'
            }
        
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
                'message': 'Authentication failed'
            }
    
    async def fetch_news(self, query: str = "", language: str = "en", page_size: int = 20) -> Dict[str, Any]:
        """Fetch positive news from AFP using inspiring genre filter"""
        if not self.is_configured():
            return self.format_error_response("AFP credentials not configured")
        
        if not await self._ensure_authenticated():
            return self.format_error_response("AFP authentication failed")
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/v1/api/search?wt=g2"
                headers = {
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
                
                search_body = {
                    "dateRange": {
                        "from": "now-30d",
                        "to": "now"
                    },
                    "sortOrder": "desc",
                    "sortField": "published",
                    "maxRows": str(min(page_size, 100)),
                    "lang": language,
                    "query": {
                        "and": [
                            {
                                "name": "class",
                                "and": ["text"]
                            },
                        ]
                    }
                }
                
                if query:
                    search_body["query"]["and"].append({
                        "name": "fulltext", 
                        "and": [query]
                    })
                
                async with session.post(url, headers=headers, json=search_body) as response:
                    if response.status == 200:
                        try:
                            data = await response.json()
                            response_data = data.get('response', {})
                            total_hits = response_data.get('numFound', 0)
                            raw_articles = response_data.get('docs', [])
                            
                            normalized_articles = [
                                self.normalize_article(article) 
                                for article in raw_articles
                            ]
                            
                            unique_articles = self.remove_duplicates(normalized_articles)
                            
                            return {
                                'status': 'success',
                                'source': self.source_name,
                                'totalResults': total_hits,
                                'articles': unique_articles
                            }
                            
                        except Exception as json_error:
                            return self.format_error_response(f"Response parsing failed: {json_error}")
                            
                    else:
                        return self.format_error_response(f"Search error: HTTP {response.status}")
        
        except Exception as e:
            return self.format_error_response(f"Request failed: {str(e)}")
    
    def normalize_article(self, raw_article: Dict[str, Any]) -> Dict[str, Any]:
        """Convert AFP article to standard format"""
        normalized = self.base_article_structure.copy()
        
        # Handle creator field safely
        creator = raw_article.get('creator', 'AFP')
        if isinstance(creator, list):
            author = ', '.join(str(c) for c in creator) if creator else 'AFP'
        else:
            author = str(creator) if creator else 'AFP'
        
        # Handle news field - it's an array of paragraphs
        news_paragraphs = raw_article.get('news', [])
        if isinstance(news_paragraphs, list):
            content = '\n\n'.join(news_paragraphs)[:500] + '...' if news_paragraphs else ''
        else:
            content = str(news_paragraphs)[:500] + '...' if news_paragraphs else ''
        
        normalized.update({
            'title': raw_article.get('headline', raw_article.get('title', '')),
            'description': raw_article.get('abstract', ''),
            'url': raw_article.get('href', ''),
            'urlToImage': None,
            'source': {
                'id': 'afp',
                'name': 'Agence France-Presse'
            },
            'author': author,
            'publishedAt': raw_article.get('published', ''),
            'content': content,
            'api_source': 'afp'
        })
        
        return normalized