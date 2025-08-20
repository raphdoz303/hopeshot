# Quick test script for sentiment analysis
# This will help us verify the Transformers models load and work correctly

import sys
import os

# Add the backend directory to Python path so we can import our services
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.sentiment.sentiment_service import SentimentService

def test_sentiment_service():
    """Test the sentiment service with sample news articles."""
    print("🧪 Testing Sentiment Analysis Service")
    print("=" * 50)
    
    # Initialize the service (this will download models on first run)
    print("📥 Initializing sentiment service...")
    sentiment_service = SentimentService()
    
    # Check available analyzers
    available = sentiment_service.get_available_analyzers()
    print(f"✅ Available analyzers: {available}")
    
    # Test with sample positive news
    sample_articles = [
        {
            "title": "Scientists develop breakthrough cancer treatment",
            "description": "Researchers have discovered a revolutionary new therapy that shows incredible promise for treating cancer patients worldwide.",
            "source": {"name": "Science News"}
        },
        {
            "title": "Local community comes together to help flood victims", 
            "description": "Neighbors organize massive relief effort, providing food, shelter and hope to those affected by recent flooding.",
            "source": {"name": "Local News"}
        }
    ]
    
    print("\\n🔍 Testing sentiment analysis on sample articles...")
    
    for i, article in enumerate(sample_articles, 1):
        print(f"\\n--- Article {i} ---")
        print(f"Title: {article['title']}")
        
        # Analyze sentiment
        enhanced_article = sentiment_service.analyze_article_sentiment(article)
        sentiment = enhanced_article.get('sentiment_analysis', {})
        
        print(f"Uplift Score: {sentiment.get('uplift_score', 'N/A')}")
        print(f"Confidence: {sentiment.get('confidence', 'N/A')}")
        print(f"Positive: {sentiment.get('sentiment', {}).get('positive', 'N/A')}")
        
        # Show top emotions
        emotions = sentiment.get('uplift_emotions', {})
        if emotions:
            top_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"Top emotions: {top_emotions}")
        
        # NEW: Show raw emotions
        raw_emotions = sentiment.get('raw_emotions', {})
        if raw_emotions:
            print(f"Raw emotions: {raw_emotions}")
        else:
            print("❌ Raw emotions not found in response")
            
        # Debug: Show full sentiment structure
        print(f"Available keys in sentiment: {list(sentiment.keys())}")

if __name__ == "__main__":
    test_sentiment_service()