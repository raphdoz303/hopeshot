"""
HopeShot FastAPI Backend
Multi-source positive news aggregation with dual storage (Database + Sheets)
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import Optional
from services.sentiment.sentiment_service import SentimentService
from services.sheets_service import SheetsService
from services.gemini_service import GeminiService
from services.database_service import DatabaseService
from services.news_service import NewsService

# Load variables
load_dotenv()

# Initialize services globally
sentiment_service = SentimentService()
news_service = NewsService()
sheets_service = SheetsService()
database_service = DatabaseService()

# Initialize FastAPI app
app = FastAPI(
    title="HopeShot API",
    description="Multi-source positive news aggregation with dual storage",
    version="0.11.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/categories")
async def get_categories():
    """Get all available categories for filtering"""
    try:
        from services.database_service import DatabaseService
        
        db = DatabaseService()
        
        # Get categories with proper structure for frontend
        categories = db.get_all_categories()
        
        return {
            "status": "success",
            "categories": categories,
            "total": len(categories)
        }
        
    except Exception as e:
        print(f"Categories API error: {e}")
        return {
            "status": "error",
            "message": "Failed to fetch categories",
            "categories": [],
            "total": 0
        }

@app.get("/")
async def root():
    """Root endpoint - API status and information"""
    return {
        "message": "Hello from HopeShot backend! 🌟",
        "status": "running",
        "version": "0.11.0",
        "features": [
            "Multi-source news aggregation",
            "SQLite database storage with M49 integration",
            "Google Sheets A/B testing data",
            "Multi-prompt analysis framework",
            "Direct M49 code storage and hierarchical filtering"
        ]
    }

@app.get("/api/news")
async def get_news(
    q: Optional[str] = None,
    language: str = "en", 
    pageSize: int = 20
):
    try:
        # Get articles from news service
        result = await news_service.fetch_unified_news(
            query=q or "",
            language=language,
            page_size=min(pageSize, 100)
        )
        
        if result["status"] != "success":
            return result
            
        # Multi-prompt Gemini analysis with M49 integration
        if result.get("articles"):
            gemini_service = GeminiService()
            
            # Filter out articles that already exist in database (deduplication)
            new_articles = []
            duplicate_count = 0
            
            for article in result["articles"]:
                if not database_service.check_url_exists(article.get('url', '')):
                    new_articles.append(article)
                else:
                    duplicate_count += 1
            
            if new_articles:
                print(f"📋 Processing {len(new_articles)} new articles ({duplicate_count} duplicates skipped)")
                
                # Analyze with all active prompts (includes M49 processing)
                gemini_result = await gemini_service.analyze_articles_batch(new_articles)
                
                if gemini_result["status"] == "success":
                    # Prepare articles for sheets logging (multiple rows per article - one per prompt)
                    articles_for_sheets = []
                    
                    # Create sheets entries for each prompt version
                    for prompt_version, prompt_data in gemini_result["results_by_prompt"].items():
                        analyses = prompt_data["results"]
                        
                        for i, article in enumerate(new_articles):
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
                    
                    # DATABASE: First prompt only for clean application data
                    first_prompt = list(gemini_result["results_by_prompt"].keys())[0]
                    first_prompt_data = gemini_result["results_by_prompt"][first_prompt]
                    first_analyses = first_prompt_data["results"]
                    
                    database_inserted = 0
                    for i, article in enumerate(new_articles):
                        if i < len(first_analyses):
                            article_id = database_service.insert_article(
                                article, 
                                first_analyses[i],
                                prompt_version=first_prompt,
                                prompt_name=first_prompt_data["config"].get("name", first_prompt)
                            )
                            if article_id:
                                database_inserted += 1
                    
                    # Add multi-prompt metadata to API response
                    result["gemini_analyzed"] = True
                    result["prompt_versions"] = gemini_result["prompt_versions"]
                    result["database_inserted"] = database_inserted
                    result["gemini_stats"] = {
                        "total_tokens_used": gemini_result.get("total_tokens_used", 0),
                        "total_batches_processed": gemini_result.get("total_batches_processed", 0),
                        "prompt_versions_count": len(gemini_result.get("prompt_versions", [])),
                        "total_analyses": len(articles_for_sheets)
                    }
                    
                    # For API response: show first prompt's analysis with populated location names AND EMOJIS
                    for i, article in enumerate(result["articles"]):
                        if i < len(first_analyses):
                            analysis = first_analyses[i]
                            
                            # Populate location names and emojis if M49 codes exist but names are empty
                            m49_codes = analysis.get('geographical_impact_m49_codes', [])
                            location_names = analysis.get('geographical_impact_location_names', [])
                            
                            print(f"🔍 DEBUG: Processing article {i}: M49 codes: {m49_codes}")
                            
                            if m49_codes and not location_names:
                                print(f"🔍 DEBUG: Looking up M49 codes: {m49_codes}")
                                location_names, location_emojis = database_service.get_location_names_and_emojis_by_m49(m49_codes)
                                print(f"🔍 DEBUG: Found location_names: {location_names}")
                                print(f"🔍 DEBUG: Found location_emojis: {location_emojis}")
                                analysis['geographical_impact_location_names'] = location_names
                                analysis['geographical_impact_location_emojis'] = location_emojis
                            elif m49_codes:
                                # Even if we have location names, get the emojis
                                print(f"🔍 DEBUG: Already have names, getting emojis for: {m49_codes}")
                                _, location_emojis = database_service.get_location_names_and_emojis_by_m49(m49_codes)
                                analysis['geographical_impact_location_emojis'] = location_emojis
                                print(f"🔍 DEBUG: Added emojis: {location_emojis}")
                            
                            article["gemini_analysis"] = analysis
                    
                    # Log to Google Sheets (multiple rows per article)
                    try:
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
            
            else:
                print("📋 All articles already exist in database - skipping analysis")
                result["gemini_analyzed"] = False
                result["database_inserted"] = 0
                result["duplicate_count"] = duplicate_count
            
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


@app.get("/api/articles")
async def get_articles(
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    impact_level: Optional[str] = Query(None)
):
    """
    Get articles from database (accumulated articles, not fresh API calls)
    
    Query Parameters:
    - limit: Number of articles to return (1-100, default 20)
    - category: Filter by category name (e.g., "health", "science tech")
    - impact_level: Filter by impact level ("Global", "Regional", "National", "Local")
    """
    try:
        # Prepare filters
        category_filter = [category] if category else None
        impact_filter = [impact_level] if impact_level else None
        
        # Get articles from database with M49 location integration
        articles = database_service.get_articles_with_locations(
            limit=limit,
            category_filter=category_filter,
            impact_level_filter=impact_filter
        )
        
        # Get database stats for metadata
        db_stats = database_service.get_database_stats()
        
        return {
            "status": "success",
            "source": "database",
            "totalArticles": len(articles),
            "articles": articles,
            "database_stats": {
                "total_in_db": db_stats.get('articles', 0),
                "categories_count": db_stats.get('categories', 0),
                "locations_count": db_stats.get('locations', 0),
                "recent_24h": db_stats.get('articles_last_24h', 0)
            },
            "filters_applied": {
                "category": category,
                "impact_level": impact_level,
                "limit": limit
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch articles from database: {str(e)}",
            "articles": []
        }

@app.get("/api/test")
async def test_endpoint():
    return {
        "message": "Backend connection successful!",
        "data": {
            "timestamp": "2025-09-02",
            "backend_status": "healthy",
            "available_sources": news_service.get_available_sources(),
            "database_stats": database_service.get_database_stats()
        }
    }

@app.get("/api/sources")
async def get_sources():
    try:
        return await news_service.get_source_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get source info: {str(e)}")

@app.get("/api/sources/test")
async def test_sources():
    try:
        return await news_service.test_all_sources()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to test sources: {str(e)}")

@app.get("/health")
async def health_check():
    try:
        available_sources = news_service.get_available_sources()
        source_info = await news_service.get_source_info()
        db_stats = database_service.get_database_stats()
        
        return {
            "status": "healthy",
            "version": "0.11.0",
            "sources": {
                "total_configured": len(available_sources),
                "available_sources": available_sources,
                "source_details": source_info.get('sources', {})
            },
            "database": {"status": "connected", "stats": db_stats},
            "system": {
                "environment": os.getenv("ENVIRONMENT", "development"),
                "python_version": "3.11+",
                "fastapi_status": "running"
            }
        }
    except Exception as e:
        return {"status": "degraded", "error": str(e), "available_sources": []}

@app.get("/api/news/afp")
async def get_afp_news(q: Optional[str] = Query(None), language: str = Query("en"), pageSize: int = Query(10, ge=1, le=50)):
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
        raise HTTPException(status_code=500, detail=f"AFP request failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)