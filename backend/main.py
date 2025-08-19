# Main FastAPI application for HopeShot backend

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from dotenv import load_dotenv

# Import our unified news service
from services.news_service import NewsService

# Load environment variables from .env file
load_dotenv()

# Create the FastAPI application instance
app = FastAPI(
    title="HopeShot API",
    description="Unified positive news API aggregating multiple sources",
    version="0.2.0"  # Updated version since we added multi-source support
)

# Add CORS middleware so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the news service (will auto-detect available sources)
try:
    news_service = NewsService()
    print(f"✅ News service initialized with sources: {news_service.get_available_sources()}")
except ValueError as e:
    print(f"❌ Failed to initialize news service: {e}")
    news_service = None

@app.get("/")
async def root():
    """Root endpoint with API information"""
    available_sources = news_service.get_available_sources() if news_service else []
    
    return {
        "message": "Hello from HopeShot backend! 🌟",
        "status": "running",
        "version": "0.2.0",
        "available_sources": available_sources,
        "endpoints": [
            "/api/news - Fetch positive news from multiple sources",
            "/api/test - Connection test",
            "/api/sources - List available news sources"
        ]
    }

@app.get("/api/test")
async def test_connection():
    """Test endpoint for verifying backend connectivity"""
    return {
        "message": "Backend connection successful!",
        "data": {
            "timestamp": "2024-08-18",
            "backend_status": "healthy"
        }
    }

@app.get("/api/news")
async def get_news(
    q: str = "positive breakthrough innovation",  # Search query for positive news
    language: str = "en",                        # Language code
    articles_per_source: int = 10,               # Articles to fetch from each source
    sources: Optional[str] = None                # Comma-separated list of sources (optional)
):
    """
    Fetch positive news articles from multiple sources
    
    Args:
        q: Search keywords (focuses on positive topics by default)
        language: Language code (en, fr, es, etc.)  
        articles_per_source: Number of articles to fetch from each source
        sources: Comma-separated sources to use (e.g., "newsapi,newsdata")
    
    Returns:
        Unified response with articles from all requested sources
    """
    
    # Check if news service is available
    if not news_service:
        raise HTTPException(
            status_code=503, 
            detail="News service unavailable. Check API key configuration."
        )
    
    try:
        # Parse sources parameter if provided
        source_list = None
        if sources:
            source_list = [s.strip() for s in sources.split(",")]
        
        # Fetch news using the unified service
        result = await news_service.fetch_news(
            query=q,
            language=language,
            articles_per_source=articles_per_source,
            sources=source_list
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch news: {str(e)}"
        )

@app.get("/api/sources")
async def get_sources():
    """Get list of available news sources"""
    
    if not news_service:
        raise HTTPException(
            status_code=503,
            detail="News service unavailable"
        )
    
    available_sources = news_service.get_available_sources()
    
    return {
        "status": "success",
        "available_sources": available_sources,
        "total_sources": len(available_sources)
    }

@app.get("/api/sources/test")  
async def test_sources():
    """Test connectivity to all configured news sources"""
    
    if not news_service:
        raise HTTPException(
            status_code=503,
            detail="News service unavailable"
        )
    
    try:
        test_results = await news_service.test_all_sources()
        
        return {
            "status": "success", 
            "source_tests": test_results
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Source testing failed: {str(e)}"
        )