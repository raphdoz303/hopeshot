# Sentiment Service - Orchestrates multiple sentiment analyzers
# This service manages and combines results from different sentiment analysis approaches

import logging
from typing import Dict, Any, List, Optional
from .transformers_analyzer import TransformersAnalyzer

class SentimentService:
    """
    Main sentiment analysis service that orchestrates multiple analyzers.
    Currently uses Transformers as primary, with space for VADER and OpenAI later.
    """
    
    def __init__(self):
        self.analyzers = {}
        self._initialize_analyzers()
    
    def _initialize_analyzers(self):
        """Initialize all available sentiment analyzers."""
        try:
            # Initialize Transformers analyzer (primary)
            self.analyzers['transformers'] = TransformersAnalyzer()
            logging.info("🎯 SentimentService initialized with Transformers analyzer")
            
            # Future: Add VADER here
            # self.analyzers['vader'] = VaderAnalyzer()
            
            # Future: Add OpenAI here  
            # self.analyzers['openai'] = OpenAIAnalyzer()
            
        except Exception as e:
            logging.error(f"❌ Failed to initialize sentiment analyzers: {e}")
    
    def analyze_article_sentiment(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze sentiment for a news article.
        
        Args:
            article (Dict): Article with title, description, content fields
            
        Returns:
            Dict: Article enhanced with sentiment analysis
        """
        # Combine title and description for analysis
        text_to_analyze = self._prepare_text(article)
        
        if not text_to_analyze:
            return self._add_empty_sentiment(article)
        
        # Get sentiment analysis from primary analyzer
        sentiment_result = self._get_primary_sentiment(text_to_analyze)
        
        # Add sentiment data to article
        enhanced_article = article.copy()
        enhanced_article['sentiment_analysis'] = sentiment_result
        enhanced_article['uplift_score'] = sentiment_result.get('uplift_score', 0.0)
        
        return enhanced_article
    
    def _prepare_text(self, article: Dict[str, Any]) -> str:
        """Prepare text from article for sentiment analysis."""
        title = article.get('title', '') or ''
        description = article.get('description', '') or ''
        
        # Combine title and description with proper spacing
        text_parts = []
        if title.strip():
            text_parts.append(title.strip())
        if description.strip():
            text_parts.append(description.strip())
        
        return ' '.join(text_parts)
    
    def _get_primary_sentiment(self, text: str) -> Dict[str, Any]:
        """Get sentiment analysis from primary analyzer (Transformers)."""
        primary_analyzer = self.analyzers.get('transformers')
        
        if primary_analyzer and primary_analyzer.is_available():
            return primary_analyzer.analyze_sentiment(text)
        else:
            logging.warning("⚠️ Primary sentiment analyzer not available")
            return self._create_fallback_sentiment()
    
    def _add_empty_sentiment(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Add empty sentiment data when no text available."""
        enhanced_article = article.copy()
        enhanced_article['sentiment_analysis'] = self._create_fallback_sentiment()
        enhanced_article['uplift_score'] = 0.0
        return enhanced_article
    
    def _create_fallback_sentiment(self) -> Dict[str, Any]:
        """Create neutral sentiment response when analysis fails."""
        return {
            "sentiment": {"positive": 0.0, "negative": 0.0, "neutral": 1.0},
            "confidence": 0.0,
            "uplift_emotions": {
                "joy": 0.0, "hope": 0.0, "gratitude": 0.0,
                "awe": 0.0, "relief": 0.0, "compassion": 0.0
            },
            "uplift_score": 0.0,
            "analyzer": "fallback",
            "note": "No sentiment analysis available"
        }
    
    def get_available_analyzers(self) -> List[str]:
        """Get list of available analyzers."""
        available = []
        for name, analyzer in self.analyzers.items():
            if analyzer.is_available():
                available.append(name)
        return available
    
    def test_analyzers(self) -> Dict[str, Any]:
        """Test all analyzers with sample text."""
        test_text = "Scientists make breakthrough discovery that could help millions of people worldwide."
        
        results = {}
        for name, analyzer in self.analyzers.items():
            if analyzer.is_available():
                try:
                    result = analyzer.analyze_sentiment(test_text)
                    results[name] = {
                        "status": "success",
                        "uplift_score": result.get('uplift_score', 0.0),
                        "confidence": result.get('confidence', 0.0)
                    }
                except Exception as e:
                    results[name] = {
                        "status": "error", 
                        "error": str(e)
                    }
            else:
                results[name] = {"status": "unavailable"}
        
        return {
            "test_text": test_text,
            "analyzer_results": results,
            "available_analyzers": self.get_available_analyzers()
        }