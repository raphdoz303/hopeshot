import asyncio
from services.gemini_service import GeminiService
from services.sheets_service import SheetsService

async def test_full_pipeline():
    """Test the complete pipeline: Articles → Gemini Analysis → Google Sheets"""
    
    print("🚀 Testing Full Gemini Pipeline")
    print("=" * 50)
    
    # Initialize services
    gemini = GeminiService()
    sheets = SheetsService()
    
    # Test with diverse article types to see Gemini's analysis range
    test_articles = [
        {
            "title": "Scientists develop breakthrough cancer treatment with 90% success rate",
            "description": "Researchers at Stanford University have created a revolutionary immunotherapy that has shown remarkable success in clinical trials, offering new hope for patients with advanced cancer.",
            "url": "https://example.com/cancer-breakthrough",
            "author": "Dr. Sarah Johnson",
            "publishedAt": "2025-08-21T10:00:00Z",
            "api_source": "newsapi",
            "source": {"id": "reuters", "name": "Reuters"}
        },
        {
            "title": "Community raises $100,000 to rebuild local school after fire",
            "description": "In just two weeks, neighbors and local businesses came together to fund the reconstruction of Elementary School, demonstrating the power of community solidarity.",
            "url": "https://example.com/school-rebuild",
            "author": "Maria Rodriguez",
            "publishedAt": "2025-08-21T09:30:00Z",
            "api_source": "newsdata",
            "source": {"id": "local-news", "name": "Local News Network"}
        },
        {
            "title": "Stock market experiences significant volatility amid economic uncertainty",
            "description": "Major indices fell 3% today as investors react to mixed economic signals and geopolitical tensions in global markets.",
            "url": "https://example.com/market-drop",
            "author": "Financial Team",
            "publishedAt": "2025-08-21T09:00:00Z",
            "api_source": "newsapi", 
            "source": {"id": "financial-times", "name": "Financial Times"}
        },
        {
            "title": "New renewable energy project to power 50,000 homes",
            "description": "The largest solar farm in the region begins operation this month, providing clean energy and creating 200 local jobs in the green technology sector.",
            "url": "https://example.com/solar-farm",
            "author": "Environmental Reporter",
            "publishedAt": "2025-08-21T08:45:00Z",
            "api_source": "newsdata",
            "source": {"id": "green-news", "name": "Green Energy Today"}
        },
        {
            "title": "Political tensions rise over healthcare reform legislation",
            "description": "Congressional leaders remain divided on the proposed healthcare bill, with both parties claiming the moral high ground in heated debates.",
            "url": "https://example.com/healthcare-debate",
            "author": "Political Correspondent",
            "publishedAt": "2025-08-21T08:00:00Z",
            "api_source": "newsapi",
            "source": {"id": "political-news", "name": "Political Weekly"}
        }
    ]
    
    print(f"📰 Testing with {len(test_articles)} diverse articles")
    print("\nArticle types:")
    for i, article in enumerate(test_articles, 1):
        print(f"  {i}. {article['title'][:60]}...")
    
    # Step 1: Test Gemini Analysis
    print(f"\n🤖 Step 1: Running Gemini Analysis")
    gemini_result = await gemini.analyze_articles_batch(test_articles)
    
    if gemini_result['status'] != 'success':
        print(f"❌ Gemini analysis failed: {gemini_result}")
        return
    
    print(f"✅ Gemini analysis completed:")
    print(f"   - Processed: {gemini_result['processed_articles']} articles")
    print(f"   - Total tokens: {gemini_result['total_tokens_used']}")
    print(f"   - Avg tokens/article: {gemini_result['average_tokens_per_article']:.0f}")
    
    # Step 2: Show sample analysis results
    print(f"\n🔍 Step 2: Sample Analysis Results")
    for i, result in enumerate(gemini_result['results'][:3]):  # Show first 3
        article_title = test_articles[i]['title'][:50]
        print(f"\nArticle {i+1}: {article_title}...")
        print(f"   Sentiment: {result.get('sentiment', 'unknown')}")
        print(f"   Hopefulness: {result.get('overall_hopefulness', 0):.2f}")
        print(f"   Top emotions: ", end="")
        emotions = result.get('emotions', {})
        top_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]
        print(", ".join([f"{emotion}:{score:.2f}" for emotion, score in top_emotions]))
        print(f"   Categories: {', '.join(result.get('categories', []))}")
        print(f"   Reasoning: {result.get('reasoning', 'N/A')}")
    
    # Step 3: Prepare data for Google Sheets
    print(f"\n📊 Step 3: Preparing data for Google Sheets")
    articles_with_analysis = []
    for i, article in enumerate(test_articles):
        if i < len(gemini_result['results']):
            articles_with_analysis.append({
                'article': article,
                'gemini_analysis': gemini_result['results'][i]
            })
        else:
            articles_with_analysis.append({
                'article': article,
                'gemini_analysis': None
            })
    
    # Step 4: Log to Google Sheets
    print(f"📈 Step 4: Logging to Google Sheets")
    sheets_result = await sheets.log_articles_with_gemini_analysis(articles_with_analysis)
    
    if sheets_result['status'] == 'success':
        print(f"✅ Google Sheets logging completed:")
        print(f"   - Logged: {sheets_result['logged_count']} articles")
        print(f"   - Spreadsheet ID: {sheets_result['spreadsheet_id']}")
    else:
        print(f"❌ Google Sheets logging failed: {sheets_result}")
    
    # Step 5: Usage summary
    print(f"\n📈 Step 5: Usage Summary")
    usage_stats = gemini.get_usage_stats()
    print(f"   - Requests today: {usage_stats['requests_today']}")
    print(f"   - Requests remaining: {usage_stats['requests_remaining_today']}")
    print(f"   - Tokens this minute: {usage_stats['tokens_this_minute']}")
    print(f"   - Can make request now: {usage_stats['can_make_request_now']}")
    
    print(f"\n🎉 Full pipeline test completed!")
    print(f"Ready to process your entire news feed with Gemini analysis!")

if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
    