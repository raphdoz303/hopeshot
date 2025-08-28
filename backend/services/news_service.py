"""
Unified news service orchestrator
Configurable multi-source management via sources.yaml
"""
import asyncio
import yaml
import os
from typing import Dict, List, Any, Optional
from .newsapi_client import NewsAPIClient
from .newsdata_client import NewsDataClient
from .afp_client import AFPClient


class NewsService:
    """Orchestrates multiple news sources with YAML configuration"""
    
    def __init__(self):
        # Load source configuration
        self.config = self._load_source_config()
        
        # Initialize configured clients
        self.clients = {}
        self._initialize_clients()
        
        # Build priority order from active sources
        self.priority_order = self._get_priority_order()
    
    def _load_source_config(self) -> Dict[str, Any]:
        """Load source configuration from YAML file"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'sources.yaml')
        
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # Fallback to defaults if no config file
            print("⚠️ sources.yaml not found, using defaults")
            return {
                'afp': {'active': True, 'priority': 1},
                'newsapi': {'active': True, 'priority': 2},
                'newsdata': {'active': True, 'priority': 3},
                'settings': {'total_daily_limit': 30}
            }
    
    def _initialize_clients(self):
        """Initialize only active news clients"""
        client_classes = {
            'afp': AFPClient,
            'newsapi': NewsAPIClient,
            'newsdata': NewsDataClient
            # Future: 'reuters': ReutersClient
        }
        
        for source_key, source_config in self.config.items():
            if source_key == 'settings':
                continue
                
            if source_config.get('active', False) and source_key in client_classes:
                client = client_classes[source_key]()
                if client.is_configured():
                    self.clients[source_key] = client
                    print(f"✅ {source_key.upper()} client initialized")
                else:
                    print(f"⚠️ {source_key.upper()} not configured (missing credentials)")
    
    def _get_priority_order(self) -> List[str]:
        """Build priority order from active sources"""
        active_sources = [
            (key, config.get('priority', 999))
            for key, config in self.config.items()
            if key != 'settings' and config.get('active', False) and key in self.clients
        ]
        
        active_sources.sort(key=lambda x: x[1])
        return [source[0] for source in active_sources]
    
    def get_available_sources(self) -> List[str]:
        """Get list of configured and available news sources"""
        return list(self.clients.keys())
    
    async def test_all_sources(self) -> Dict[str, Any]:
        """Test connection to all configured news sources"""
        results = {}
        
        tasks = []
        for source, client in self.clients.items():
            tasks.append(self._test_source(source, client))
        
        if tasks:
            test_results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in test_results:
                if isinstance(result, dict):
                    results[result['source']] = result
        
        return {
            'status': 'success',
            'sources_tested': len(results),
            'config_file': 'sources.yaml',
            'active_sources': self.priority_order,
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
        """Fetch news from active sources based on configuration"""
        available_sources = self.get_available_sources()
        
        if not available_sources:
            return {
                'status': 'error',
                'error': 'No news sources configured or active',
                'sources_used': [],
                'articles': []
            }
        
        # Apply global limits from settings
        settings = self.config.get('settings', {})
        max_articles = min(page_size, settings.get('total_daily_limit', 30))
        
        # Calculate articles per source based on their daily limits
        source_limits = {}
        for source in available_sources:
            source_config = self.config.get(source, {})
            source_limit = source_config.get('daily_limit', 10)
            source_limits[source] = min(source_limit, max_articles // len(available_sources))
        
        # Fetch from all sources concurrently
        tasks = []
        for source in available_sources:
            client = self.clients[source]
            limit = source_limits[source]
            tasks.append(self._fetch_from_source(source, client, query, language, limit))
        
        source_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        all_articles = []
        sources_used = []
        sources_failed = []
        
        for result in source_results:
            if isinstance(result, dict) and result.get('status') == 'success':
                articles = result.get('articles', [])
                
                # Apply quality filtering if configured
                min_quality = settings.get('min_quality_score', 0)
                source_quality = self.config.get(result.get('source'), {}).get('quality_score', 10)
                
                if source_quality >= min_quality and articles:
                    all_articles.extend(articles)
                    sources_used.append(result.get('source'))
            elif isinstance(result, dict):
                sources_failed.append({
                    'source': result.get('source', 'unknown'),
                    'error': result.get('error', 'Unknown error')
                })
        
        # Sort by priority
        all_articles.sort(key=lambda x: self.priority_order.index(x.get('api_source', 'newsdata')))
        
        # Remove cross-source duplicates
        unique_articles = self._remove_cross_source_duplicates(all_articles)
        final_articles = unique_articles[:max_articles]
        
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
        """Fetch articles from individual source"""
        try:
            result = await client.fetch_news(query, language, page_size)
            result['source'] = source
            return result
        except Exception as e:
            return {
                'status': 'error',
                'source': source,
                'error': f'Fetch failed: {str(e)}',
                'articles': []
            }
    
    def _remove_cross_source_duplicates(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate articles across sources using similarity check"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            title = article.get('title', '').strip().lower()
            title_words = set(title.split())
            is_duplicate = False
            
            for seen_title in seen_titles:
                seen_words = set(seen_title.split())
                
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
        """Get information about all configured sources"""
        source_info = {}
        
        for source_key, source_config in self.config.items():
            if source_key == 'settings':
                continue
                
            source_info[source_key] = {
                'name': source_config.get('name', source_key.upper()),
                'active': source_config.get('active', False),
                'configured': source_key in self.clients,
                'priority': source_config.get('priority', 999),
                'quality_score': source_config.get('quality_score', 5),
                'daily_limit': source_config.get('daily_limit', 10)
            }
        
        return {
            'status': 'success',
            'sources': source_info,
            'priority_order': self.priority_order,
            'settings': self.config.get('settings', {})
        }