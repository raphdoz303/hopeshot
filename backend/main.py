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
from services.gemini_service import GeminiService


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
    q: Optional[str] = None,
    language: str = "en", 
    pageSize: int = 20
):
    try:
        # Get articles from existing news service
        news_service = NewsService()
        result = await news_service.fetch_unified_news(
            query=q or "",
            language=language,
            page_size=min(pageSize, 100)
        )
        
        if result["status"] != "success":
            return result
            
        # Multi-prompt Gemini analysis
        if result.get("articles"):
            gemini_service = GeminiService()
            
            # Analyze with all active prompts
            gemini_result = await gemini_service.analyze_articles_batch(result["articles"])
        
            
            if gemini_result["status"] == "success":
            
                # Prepare articles for sheets logging (multiple rows per article - one per prompt)
                articles_for_sheets = []
                
                # Create sheets entries for each prompt version
                for prompt_version, prompt_data in gemini_result["results_by_prompt"].items():
                    analyses = prompt_data["results"]
                    
                    for i, article in enumerate(result["articles"]):
                        if i < len(analyses):
                            # Create separate sheet entry for this prompt version
                            articles_for_sheets.append({
                                "article": article.copy(),  # Don't modify original
                                "gemini_analysis": {
                                    **analyses[i],  # Include all analysis fields
                                    "prompt_version": prompt_version,  # Add version tracking
                                    "prompt_name": prompt_data["config"].get("name", prompt_version)
                                }
                            })
                
                # Add multi-prompt metadata to API response
                result["gemini_analyzed"] = True
                result["prompt_versions"] = gemini_result["prompt_versions"]
                result["gemini_stats"] = {
                    "total_tokens_used": gemini_result.get("total_tokens_used", 0),
                    "total_batches_processed": gemini_result.get("total_batches_processed", 0),
                    "prompt_versions_count": len(gemini_result.get("prompt_versions", [])),
                    "total_analyses": len(articles_for_sheets)
                }
                
                # For API response: show first prompt's analysis (backward compatibility)
                first_prompt = list(gemini_result["results_by_prompt"].keys())[0]
                first_analyses = gemini_result["results_by_prompt"][first_prompt]["results"]
                
                for i, article in enumerate(result["articles"]):
                    if i < len(first_analyses):
                        article["gemini_analysis"] = first_analyses[i]
                
                # Log to Google Sheets (multiple rows per article)
                try:
                    sheets_service = SheetsService()
                    sheets_result = await sheets_service.log_articles_with_gemini_analysis(articles_for_sheets)
                    result["sheets_logged"] = sheets_result.get("status") == "success"
                    result["total_logged"] = sheets_result.get("logged_count", 0)
                    
                except Exception as sheets_error:
                    print(f"⚠️ Sheets logging failed: {sheets_error}")
                    result["sheets_logged"] = False
                    result["sheets_error"] = str(sheets_error)
                    
            else:
                result["gemini_analyzed"] = False
                result["gemini_error"] = gemini_result.get("message", "Analysis failed")
            
            result["analyzed_sources"] = list(set([article.get("api_source") for article in result["articles"]]))
        else:
            result["gemini_analyzed"] = False
            result["analyzed_sources"] = []
            
        return result
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"News aggregation failed: {str(e)}"
        }


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