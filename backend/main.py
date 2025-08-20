"""
HopeShot FastAPI Backend
Multi-source positive news aggregation with AFP, NewsAPI, and NewsData integration
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import Optional

# Import our new service architecture
from services.news_service import NewsService

# Load environment variables
load_dotenv()

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

# Initialize news service (orchestrator)
news_service = NewsService()


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
    q: Optional[str] = Query(None, description="Search query for news articles"),
    language: str = Query("en", description="Language code (en, fr, es, etc.)"),
    pageSize: int = Query(20, ge=1, le=100, description="Number of articles to return (1-100)")
):
    """
    Fetch positive news from all available sources
    Combines AFP, NewsAPI, and NewsData with intelligent deduplication
    """
    try:
        # Use the orchestrator to fetch from all sources
        result = await news_service.fetch_unified_news(
            query=q or "",
            language=language,
            page_size=pageSize
        )
        
        if result.get('status') == 'error':
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch news: {str(e)}"
        )


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