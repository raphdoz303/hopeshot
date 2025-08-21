"""
HopeShot FastAPI Backend
Multi-source positive news aggregation with AFP, NewsAPI, and NewsData integration
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import Optional
from services.sentiment.sentiment_service import SentimentService
from services.sheets_service import SheetsService

# Initialize sheets service globally
sheets_service = SheetsService()

# Import our new service architecture
from services.news_service import NewsService

# Load variables
load_dotenv()
sentiment_service = SentimentService()
news_service = NewsService()

# Initialize FastAPI app
app = FastAPI(
    title="HopeShot API",
    description="Multi-source positive news aggregation service",
    version="0.3.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint - API status and information"""
    return {
        "message": "Hello from HopeShot backend! 🌟",
        "status": "running",
        "version": "0.3.0",
        "features": [
            "Multi-source news aggregation",
            "AFP professional news integration", 
            "Positive news filtering",
            "Cross-source duplicate removal"
        ]
    }


@app.get("/api/test")
async def test_endpoint():
    """Connection test endpoint for frontend verification"""
    return {
        "message": "Backend connection successful!",
        "data": {
            "timestamp": "2024-08-19",
            "backend_status": "healthy",
            "available_sources": news_service.get_available_sources()
        }
    }


@app.get("/api/news")
async def get_news(
    q: str = None,
    language: str = "en",
    pageSize: int = 20
):
    """Get unified news from all available sources with sentiment analysis and Google Sheets logging"""
    
    try:
        # Get news from all sources
        result = await news_service.fetch_unified_news(
            query=q,
            language=language,
            page_size=pageSize
        )
        
        # Analyze sentiment for applicable articles
        analyzed_articles = []
        sentiment_analyzed = False
        analyzed_sources = []
        
        for article in result["articles"]:
            api_source = article.get("api_source", "")
            
            # Only analyze NewsAPI and NewsData articles
            if api_source in ["newsapi", "newsdata"]:
                try:
                    sentiment_result = sentiment_service.analyze_article_sentiment(article)
                    article.update(sentiment_result)
                    sentiment_analyzed = True
                    if api_source not in analyzed_sources:
                        analyzed_sources.append(api_source)
                except Exception as e:
                    print(f"Sentiment analysis failed for {api_source} article: {e}")
            
            analyzed_articles.append(article)
        
        # Log articles to Google Sheets
        try:
            sheets_service.log_articles(analyzed_articles)
            sheets_logged = True
        except Exception as e:
            print(f"Failed to log to Google Sheets: {e}")
            sheets_logged = False
        
        # Build response with enhanced metadata
        response = {
            **result,  # Include all original fields
            "articles": analyzed_articles,
            "sentiment_analyzed": sentiment_analyzed,
            "analyzed_sources": analyzed_sources,
            "sheets_logged": sheets_logged,
            "total_logged": len(analyzed_articles)
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")


@app.get("/api/sources")
async def get_sources():
    """
    Get information about all news sources
    Shows which sources are configured and their priority order
    """
    try:
        return await news_service.get_source_info()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get source info: {str(e)}"
        )


@app.get("/api/sources/test")
async def test_sources():
    """
    Test connection to all configured news sources
    Useful for debugging API key issues and source availability
    """
    try:
        return await news_service.test_all_sources()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to test sources: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """
    Comprehensive health check endpoint
    Shows overall system status and source availability
    """
    try:
        available_sources = news_service.get_available_sources()
        source_info = await news_service.get_source_info()
        
        return {
            "status": "healthy",
            "version": "0.3.0",
            "sources": {
                "total_configured": len(available_sources),
                "available_sources": available_sources,
                "source_details": source_info.get('sources', {})
            },
            "system": {
                "environment": os.getenv("ENVIRONMENT", "development"),
                "python_version": "3.11+",
                "fastapi_status": "running"
            }
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "available_sources": []
        }


# Optional: Add a simple endpoint to get just AFP news (for testing)
@app.get("/api/news/afp")
async def get_afp_news(
    q: Optional[str] = Query(None, description="Search query"),
    language: str = Query("en", description="Language code"),
    pageSize: int = Query(10, ge=1, le=50, description="Number of articles")
):
    """Get news specifically from AFP source (for testing purposes)"""
    try:
        afp_client = news_service.clients['afp']
        
        if not afp_client.is_configured():
            raise HTTPException(status_code=503, detail="AFP client not configured")
        
        result = await afp_client.fetch_news(q or "", language, pageSize)
        
        if result.get('status') == 'error':
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AFP request failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)