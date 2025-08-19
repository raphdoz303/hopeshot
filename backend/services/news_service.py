# Unified news service that aggregates articles from multiple sources

import asyncio
from typing import List, Dict, Any, Optional
from .newsapi_client import NewsAPIClient
from .newsdata_client import NewsDataClient

class NewsService:
    """
    Unified service for fetching news from multiple sources
    Handles aggregation, deduplication, and source management
    """
    
    def __init__(self):
        # Initialize all news clients
        self.clients = {}
        
        # Try to initialize each client (some might fail if API keys missing)
        try:
            self.clients["newsapi"] = NewsAPIClient()
        except ValueError as e:
            print(f"NewsAPI client not available: {e}")
        
        try:
            self.clients["newsdata"] = NewsDataClient()
        except ValueError as e:
            print(f"NewsData client not available: {e}")
        
        if not self.clients:
            raise ValueError("No news API clients available. Check your API keys.")
    
    async def fetch_news(
        self,
        query: str = "positive breakthrough innovation",
        language: str = "en",
        articles_per_source: int = 10,
        sources: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Fetch news articles from multiple sources
        
        Args:
            query: Search keywords
            language: Language code 
            articles_per_source: How many articles to get from each source
            sources: List of sources to use (default: all available)
            
        Returns:
            Dict with aggregated articles and metadata
        """
        
        # Determine which sources to use
        if sources is None:
            sources = list(self.clients.keys())
        
        # Filter to only available sources
        available_sources = [s for s in sources if s in self.clients]
        
        if not available_sources:
            raise Exception(f"No available sources from requested: {sources}")
        
        # Fetch from all sources concurrently (faster!)
        tasks = []
        for source_name in available_sources:
            client = self.clients[source_name]
            # Adjust page size based on source limitations
            page_size = self._get_optimal_page_size(source_name, articles_per_source)
            task = self._fetch_from_source(client, query, language, page_size)
            tasks.append(task)
        
        # Wait for all requests to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and handle any errors
        all_articles = []
        source_stats = {}
        errors = []
        
        for i, result in enumerate(results):
            source_name = available_sources[i]
            
            if isinstance(result, Exception):
                # Log error but continue with other sources
                errors.append(f"{source_name}: {str(result)}")
                source_stats[source_name] = {"articles": 0, "error": str(result)}
            else:
                # Add articles from successful source
                articles = result["articles"]
                all_articles.extend(articles)
                source_stats[source_name] = {
                    "articles": len(articles),
                    "total_available": result["total_results"],
                    "requested": result["requested_count"]
                }
        
        # Sort by publication date (newest first)
        all_articles.sort(key=lambda x: x.get("published_at", ""), reverse=True)
        
        return {
            "status": "success",
            "query": query,
            "language": language,
            "total_articles": len(all_articles),
            "sources_used": list(source_stats.keys()),
            "source_stats": source_stats,
            "errors": errors if errors else None,
            "articles": all_articles
        }
    
    async def _fetch_from_source(
        self, 
        client, 
        query: str, 
        language: str, 
        page_size: int
    ) -> Dict[str, Any]:
        """
        Wrapper to fetch from a single source with error handling
        """
        return await client.fetch_articles(query, language, page_size)
    
    def _get_optimal_page_size(self, source_name: str, requested: int) -> int:
        """
        Get the optimal page size for each source based on their limits
        """
        limits = {
            "newsapi": 100,    # NewsAPI allows up to 100
            "newsdata": 10,    # NewsData.io free tier limit
        }
        
        max_allowed = limits.get(source_name, requested)
        return min(requested, max_allowed)
    
    def get_available_sources(self) -> List[str]:
        """Get list of currently available news sources"""
        return list(self.clients.keys())
    
    async def test_all_sources(self) -> Dict[str, Any]:
        """
        Test connectivity to all configured sources
        Useful for debugging and health checks
        """
        results = {}
        
        for source_name, client in self.clients.items():
            try:
                # Try to fetch just 1 article for testing
                result = await client.fetch_articles(
                    query="test", 
                    language="en", 
                    page_size=1
                )
                results[source_name] = {
                    "status": "success",
                    "articles_found": len(result["articles"])
                }
            except Exception as e:
                results[source_name] = {
                    "status": "error", 
                    "error": str(e)
                }
        
        return results