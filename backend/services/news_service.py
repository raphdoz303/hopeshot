"""
Unified news service orchestrator
Combines multiple news sources with priority system and graceful degradation
"""
import asyncio
from typing import Dict, List, Any, Optional
from .newsapi_client import NewsAPIClient
from .newsdata_client import NewsDataClient
from .afp_client import AFPClient


class NewsService:
    """Orchestrates multiple news sources with priority system"""
    
    def __init__(self):
        # Initialize all clients
        self.clients = {
            'afp': AFPClient(),
            'newsapi': NewsAPIClient(),
            'newsdata': NewsDataClient()
        }
        
        # Priority order (highest to lowest quality)
        self.priority_order = ['afp', 'newsapi', 'newsdata']
    
    def get_available_sources(self) -> List[str]:
        """Get list of configured and available news sources"""
        return [
            source for source, client in self.clients.items() 
            if client.is_configured()
        ]
    
    async def test_all_sources(self) -> Dict[str, Any]:
        """Test connection to all configured news sources"""
        results = {}
        
        # Test all sources concurrently
        tasks = []
        for source, client in self.clients.items():
            if client.is_configured():
                tasks.append(self._test_source(source, client))
        
        if tasks:
            test_results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in test_results:
                if isinstance(result, dict):
                    results[result['source']] = result
        
        return {
            'status': 'success',
            'sources_tested': len(results),
            'results': results
        }
    
    async def _test_source(self, source: str, client) -> Dict[str, Any]:
        """Test individual source connection"""
        try:
            return await client.test_connection()
        except Exception as e:
            return {
                'source': source,
                'status': 'error',
                'message': f'Test failed: {str(e)}'
            }
    
    async def fetch_unified_news(self, query: str = "", language: str = "en", page_size: int = 20) -> Dict[str, Any]:
        """
        Fetch news from all available sources and combine results
        Uses priority system: AFP -> NewsAPI -> NewsData
        """
        available_sources = self.get_available_sources()
        
        if not available_sources:
            return {
                'status': 'error',
                'error': 'No news sources configured',
                'sources_used': [],
                'articles': []
            }
        
        # Calculate articles per source (distribute evenly)
        articles_per_source = max(1, page_size // len(available_sources))
        
        # Fetch from all sources concurrently
        tasks = []
        for source in available_sources:
            client = self.clients[source]
            tasks.append(self._fetch_from_source(source, client, query, language, articles_per_source))
        
        source_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        all_articles = []
        sources_used = []
        sources_failed = []
        
        for result in source_results:
            if isinstance(result, dict) and result.get('status') == 'success':
                articles = result.get('articles', [])
                if articles:
                    # Note: api_source is already added by normalize_article() in each client
                    all_articles.extend(articles)
                    sources_used.append(result.get('source'))
            elif isinstance(result, dict):
                sources_failed.append({
                    'source': result.get('source', 'unknown'),
                    'error': result.get('error', 'Unknown error')
                })
        
        # Sort articles by priority (AFP first, then NewsAPI, then NewsData)
        all_articles.sort(key=lambda x: self.priority_order.index(x.get('api_source', 'newsdata')))
        
        # Remove cross-source duplicates and limit to requested size
        unique_articles = self._remove_cross_source_duplicates(all_articles)
        final_articles = unique_articles[:page_size]
        
        # No need to clean up metadata - api_source stays in the response
        
        return {
            'status': 'success',
            'query': query,
            'totalSources': len(available_sources),
            'sourcesUsed': sources_used,
            'sourcesFailed': sources_failed,
            'totalArticles': len(final_articles),
            'crossSourceDuplicatesRemoved': len(all_articles) - len(unique_articles),
            'articles': final_articles
        }
    
    async def _fetch_from_source(self, source: str, client, query: str, language: str, page_size: int) -> Dict[str, Any]:
        """Fetch articles from individual source with error handling"""
        try:
            result = await client.fetch_news(query, language, page_size)
            result['source'] = source  # Ensure source is included
            return result
        except Exception as e:
            return {
                'status': 'error',
                'source': source,
                'error': f'Fetch failed: {str(e)}',
                'articles': []
            }
    
    def _remove_cross_source_duplicates(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicate articles across different sources based on title similarity
        TODO: Enhance this later to use more sophisticated text comparison (semantic similarity, etc.)
        """
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            title = article.get('title', '').strip().lower()
            
            # Simple word-based similarity check
            title_words = set(title.split())
            is_duplicate = False
            
            for seen_title in seen_titles:
                seen_words = set(seen_title.split())
                
                # If 70% of words overlap, consider it duplicate
                if title_words and seen_words:
                    overlap = len(title_words.intersection(seen_words))
                    similarity = overlap / max(len(title_words), len(seen_words))
                    if similarity > 0.7:
                        is_duplicate = True
                        break
            
            if not is_duplicate and title:
                seen_titles.add(title)
                unique_articles.append(article)
        
        return unique_articles
    
    async def get_source_info(self) -> Dict[str, Any]:
        """Get information about all news sources and their configuration status"""
        source_info = {}
        
        for source, client in self.clients.items():
            source_info[source] = {
                'name': source.upper(),
                'configured': client.is_configured(),
                'priority': self.priority_order.index(source) + 1
            }
        
        return {
            'status': 'success',
            'sources': source_info,
            'priority_order': self.priority_order
        }