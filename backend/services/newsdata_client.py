# NewsData.io client service for fetching articles from NewsData.io API

import os
import httpx
from typing import List, Dict, Any, Optional

class NewsDataClient:
    """Client for fetching news from NewsData.io"""
    
    def __init__(self):
        # Get configuration from environment variables
        self.api_key = os.getenv("NEWSDATA_API_KEY")
        self.base_url = os.getenv("NEWSDATA_BASE_URL", "https://newsdata.io/api/1/news")
        
        if not self.api_key:
            raise ValueError("NEWSDATA_API_KEY environment variable not set")
    
    async def fetch_articles(
        self,
        query: str = "positive breakthrough innovation",
        language: str = "en",
        page_size: int = 10  # NewsData.io has lower limits on free tier
    ) -> Dict[str, Any]:
        """
        Fetch articles from NewsData.io
        
        Args:
            query: Search keywords for articles
            language: Language code (en, fr, es, etc.)
            page_size: Number of articles to fetch (max 10 for free tier)
            
        Returns:
            Dict with articles and metadata
        """
        
        # Build request parameters (NewsData.io uses different parameter names)
        params = {
            "apikey": self.api_key,  # Different from NewsAPI
            "q": query,
            "language": language,
            "size": min(page_size, 10),  # Enforce free tier limit
            "category": "top,science,technology",  # Focus on positive categories
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Check if NewsData.io returned an error
                if data.get("status") == "error":
                    raise Exception(f"NewsData.io API error: {data.get('message', 'Unknown error')}")
                
                # Remove duplicates within NewsData.io results
                articles = self._remove_duplicates(data.get("results", []))
                
                return {
                    "source": "newsdata",
                    "total_results": data.get("totalResults", len(articles)),  # NewsData.io doesn't always provide this
                    "articles": articles,
                    "requested_count": page_size,
                    "unique_count": len(articles)
                }
                
        except httpx.HTTPError as e:
            raise Exception(f"NewsData.io request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"NewsData.io unexpected error: {str(e)}")
    
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
        """Convert NewsData.io article to standard format"""
        return {
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "url": article.get("link", ""),  # Different field name
            "image_url": article.get("image_url", ""),
            "source_name": article.get("source_id", "Unknown"),  # Different structure
            "author": article.get("creator", [""])[0] if article.get("creator") else "",  # Creator is an array
            "published_at": article.get("pubDate", ""),  # Different field name
            "content_preview": (article.get("content", "") or article.get("description", ""))[:200] + "..." if article.get("content") or article.get("description") else "",
            "source_api": "newsdata"
        }