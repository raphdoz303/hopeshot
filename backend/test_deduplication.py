"""
Test script for DeduplicationService
Run this to verify the service works correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.deduplication_service import DeduplicationService

def test_deduplication_service():
    """Test the deduplication service with sample articles."""
    
    # Initialize service
    dedup = DeduplicationService()
    print("🔍 Testing DeduplicationService...")
    
    # Test article samples
    test_article_new = {
        "url": "https://example.com/test-article-unique-12345",
        "title": "Breakthrough Discovery in Renewable Energy Technology",
        "description": "Scientists make amazing discovery"
    }
    
    test_article_similar_title = {
        "url": "https://different-source.com/energy-story",
        "title": "Breakthrough Discovery in Renewable Energy Tech",  # Very similar
        "description": "Same story from different source"
    }
    
    # Test 1: New article (should not be duplicate)
    is_dup, reason = dedup.is_duplicate(test_article_new)
    print(f"✅ New article duplicate check: {is_dup} ({reason})")
    
    # Test 2: Get current stats
    stats = dedup.get_duplicate_stats()
    print(f"📊 Database stats: {stats}")
    
    print("🎉 DeduplicationService test completed!")

if __name__ == "__main__":
    test_deduplication_service()