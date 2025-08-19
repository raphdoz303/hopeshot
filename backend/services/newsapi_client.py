# NewsAPI client service for fetching articles from NewsAPI.org

import os
import httpx
from typing import List, Dict, Any, Optional

class NewsAPIClient:
    """Client for fetching news from NewsAPI.org"""
    
    def __init__(self):
        # Get configuration from environment variables
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"
        
        if not self.api_key:
            raise ValueError("NEWS_API_KEY environment variable not set")
    
    async def fetch_articles(
        self,
        query: str = "positive breakthrough innovation",
        language: str = "en", 
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        Fetch articles from NewsAPI
        
        Args:
            query: Search keywords for articles
            language: Language code (en, fr, es, etc.)
            page_size: Number of articles to fetch (1-100)
            
        Returns:
            Dict with articles and metadata
        """
        
        # Build request parameters
        params = {
            "q": query,
            "language": language,
            "pageSize": page_size,
            "sortBy": "publishedAt",
            "apiKey": self.api_key
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Remove duplicates within NewsAPI results
                articles = self._remove_duplicates(data.get("articles", []))
                
                return {
                    "source": "newsapi",
                    "total_results": data.get("totalResults", 0),
                    "articles": articles,
                    "requested_count": page_size,
                    "unique_count": len(articles)
                }
                
        except httpx.HTTPError as e:
            raise Exception(f"NewsAPI request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"NewsAPI unexpected error: {str(e)}")
    
    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title"""
        unique_articles = []
        seen_titles = set()
        
        for article in articles:
            title = article.get("title", "").strip().lower()
            if title and title not in seen_titles:
                seen_titles.add(title)
                # Normalize article format
                normalized_article = self._normalize_article(article)
                unique_articles.append(normalized_article)
        
        return unique_articles
    
    def _normalize_article(self, article: Dict) -> Dict:
        """Convert NewsAPI article to standard format"""
        return {
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "url": article.get("url", ""),
            "image_url": article.get("urlToImage", ""),
            "source_name": article.get("source", {}).get("name", "Unknown"),
            "author": article.get("author", ""),
            "published_at": article.get("publishedAt", ""),
            "content_preview": article.get("content", "")[:200] + "..." if article.get("content") else "",
            "source_api": "newsapi"
        }