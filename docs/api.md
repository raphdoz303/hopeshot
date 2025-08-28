# HopeShot API Documentation

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: *TBD*

---

## Core Endpoints

### **GET /**
Root endpoint providing basic API information.

**Response**:
```json
{
  "message": "Hello from HopeShot backend! 🌟",
  "status": "running",
  "version": "0.5.0",
  "features": [
    "Multi-source news aggregation",
    "AFP professional news integration", 
    "AI-powered sentiment analysis",
    "Real-time Google Sheets data logging",
    "Cross-source duplicate removal"
  ]
}
```

---

### **GET /api/news**
Fetch positive news from all available sources with multi-prompt Gemini analysis and automatic comparative Google Sheets logging.

**Query Parameters**:
- `q` (optional): Search keywords (default: positive keywords per source)
- `language` (optional): Language code (default: "en")  
- `pageSize` (optional): Number of articles to return (1-100, default: 20)

**Example Request**:
```bash
curl "http://localhost:8000/api/news?q=medical%20breakthrough&pageSize=5"
```

**A/B Testing Response Fields**:
- `prompt_versions`: Array of active prompt versions used for analysis
- `gemini_stats.prompt_versions_count`: Number of prompts that analyzed each article
- `gemini_stats.total_analyses`: Total analysis operations (articles × prompt versions)
- `sheets_logged`: Boolean indicating successful logging of comparative analysis data
- `total_logged`: Number of rows logged to Google Sheets (articles × prompt versions)

**Google Sheets Data Collection**:
- Each article generates multiple rows in Google Sheets (one per prompt version)
- Prompt version tracking in reserved columns for A/B testing comparison
- Side-by-side analysis results for identical articles enable systematic prompt optimization

**Response Structure**:
```json
{
  "status": "success",
  "query": "medical breakthrough",
  "totalSources": 3,
  "sourcesUsed": ["newsapi", "newsdata", "afp"],
  "sourcesFailed": [],
  "totalArticles": 5,
  "crossSourceDuplicatesRemoved": 1,
  "gemini_stats": {
    "total_tokens_used": 2450,
    "total_batches_processed": 2,
    "prompt_versions_count": 2,
    "total_analyses": 10
  },
  "articles": [
    {
      "title": "Medical Breakthrough: New Treatment Shows Promise",
      "description": "Scientists discover innovative approach...",
      "url": "https://example.com/article",
      "urlToImage": "https://example.com/image.jpg",
      "source": {
        "id": "reuters",
        "name": "Reuters"
      },
      "author": "Jane Smith",
      "publishedAt": "2025-08-25T10:30:00Z",
      "content": "Full article content preview...",
      "api_source": "newsapi",
      "gemini_analysis": {
        "sentiment": "positive",
        "confidence_score": 0.85,
        "emotions": {
          "hope": 0.8,
          "awe": 0.6,
          "gratitude": 0.4,
          "compassion": 0.7,
          "relief": 0.3,
          "joy": 0.5
        },
        "categories": ["medical", "technology"],
        "source_credibility": "high",
        "fact_checkable_claims": "yes",
        "evidence_quality": "strong",
        "controversy_level": "low",
        "solution_focused": "yes",
        "age_appropriate": "all",
        "truth_seeking": "no",
        "geographic_scope": ["World", "North America"],
        "country_focus": "United States",
        "local_focus": "California",
        "geographic_relevance": "primary",
        "overall_hopefulness": 0.75,
        "reasoning": "Medical breakthrough shows promise"
      }
    }
  ]
}_analyzed": true,
  "prompt_versions": ["v1_comprehensive", "v2_emotion_focused"],
  "analyzed_sources": ["newsapi", "newsdata", "afp"],
  "sheets_logged": true,
  "total_logged": 10,
  "gemini
```

**New Response Fields**:
- `sentiment_analyzed`: Boolean indicating if sentiment analysis was performed
- `analyzed_sources`: Array of sources that received sentiment analysis
- `sheets_logged`: Boolean indicating if articles were successfully logged to Google Sheets
- `total_logged`: Number of articles logged to sheets
- `uplift_score`: Overall positivity score (0.0 to 1.0) for each article
- `sentiment_analysis`: Complete sentiment breakdown with emotions and confidence

**Priority System**:
1. **AFP** (highest quality) - Professional journalism with "inspiring" genre filter
2. **NewsAPI** (mainstream) - Major news sources with positive keyword filtering  
3. **NewsData** (alternative) - International sources with category filtering

**Sentiment Analysis Coverage**:
- ✅ **NewsAPI articles** - Full sentiment analysis with uplift scoring
- ✅ **NewsData articles** - Full sentiment analysis with uplift scoring  
- ❌ **AFP articles** - Excluded (uses built-in positive filtering)


**Enhanced Response with Gemini Analysis**:
```json
{
  "status": "success",
  "query": "medical breakthrough",
  "totalSources": 3,
  "sourcesUsed": ["newsapi", "newsdata", "afp"],
  "sourcesFailed": [],
  "totalArticles": 8,
  "crossSourceDuplicatesRemoved": 2,
  "gemini_analyzed": true,
  "analyzed_sources": ["newsapi", "newsdata", "afp"],
  "sheets_logged": true,
  "total_logged": 8,
  "gemini_stats": {
    "total_tokens_used": 1250,
    "average_tokens_per_article": 156,
    "batches_processed": 1
  },
  "articles": [
    {
      "title": "Medical Breakthrough: New Treatment Shows Promise",
      "description": "Scientists discover innovative approach...",
      "url": "https://example.com/article",
      "urlToImage": "https://example.com/image.jpg",
      "source": {
        "id": "reuters",
        "name": "Reuters"
      },
      "author": "Jane Smith",
      "publishedAt": "2024-08-22T10:30:00Z",
      "content": "Full article content preview...",
      "api_source": "newsapi",
      "gemini_analysis": {
        "sentiment": "positive",
        "confidence_score": 0.85,
        "emotions": {
          "hope": 0.8,
          "awe": 0.6,
          "gratitude": 0.4,
          "compassion": 0.7,
          "relief": 0.3,
          "joy": 0.5
        },
        "categories": ["medical", "technology"],
        "source_credibility": "high",
        "fact_checkable_claims": "yes",
        "evidence_quality": "strong",
        "controversy_level": "low",
        "solution_focused": "yes",
        "age_appropriate": "all",
        "truth_seeking": "no",
        "geographic_scope": ["World", "North America"],
        "country_focus": "United States",
        "local_focus": "California",
        "geographic_relevance": "primary",
        "overall_hopefulness": 0.75,
        "reasoning": "Medical breakthrough shows promise"
      }
    }
  ]
}
```

**New Response Fields**:
- `gemini_analyzed`: Boolean indicating if Gemini analysis was performed
- `analyzed_sources`: Array of sources that received Gemini analysis
- `sheets_logged`: Boolean indicating if articles were successfully logged to Google Sheets
- `total_logged`: Number of articles logged to sheets
- `gemini_stats`: Token usage and processing statistics
- `gemini_analysis`: Complete comprehensive analysis with emotions, categories, and metadata

**Gemini Analysis Fields**:
- **Sentiment**: `positive/negative/neutral` with confidence score
- **Target Emotions** (0.0-1.0): `hope`, `awe`, `gratitude`, `compassion`, `relief`, `joy`
- **Categories**: Dynamically discovered categories (e.g., medical, technology, environment)
- **Fact-checking Readiness**: `source_credibility`, `fact_checkable_claims`, `evidence_quality`
- **Content Analysis**: `controversy_level`, `solution_focused`, `age_appropriate`, `truth_seeking`
- **Geographic Analysis**: `geographic_scope`, `country_focus`, `local_focus`, `geographic_relevance`
- **Overall Assessment**: `overall_hopefulness` score and brief `reasoning`

---

### Source Configuration Response Updates

The `/api/news` endpoint now respects `sources.yaml` configuration:

**Configuration-Based Filtering**:
- Only active sources (marked `active: true`) are queried
- Daily limits per source are enforced
- Quality thresholds filter low-quality sources
- AFP's "inspiring" genre filter limits results to 4-10 articles/week

**Performance Improvements**:
- Multi-prompt analysis now completes in ~10 seconds (vs 2+ minutes)
- Single Gemini request analyzes all prompt versions simultaneously
- 2-minute rate limiting only applies between different article batches


---

### **GET /api/sources**
Get information about all news sources and their configuration.

**Response**:
```json
{
  "status": "success",
  "sources": {
    "afp": {
      "name": "Agence France-Presse",
      "active": true,
      "configured": true,
      "priority": 1,
      "quality_score": 10,
      "daily_limit": 20
    },
    "newsapi": {
      "name": "NewsAPI.org",
      "active": false,
      "configured": true,
      "priority": 2,
      "quality_score": 5,
      "daily_limit": 10
    },
    "newsdata": {
      "name": "NewsData.io",
      "active": false,
      "configured": true,
      "priority": 3,
      "quality_score": 3,
      "daily_limit": 5
    }
  },
  "priority_order": ["afp"],
  "settings": {
    "total_daily_limit": 30,
    "min_quality_score": 7,
    "refresh_interval": "6h",
    "pagination_size": 10
  }
}
```

---

### **GET /api/sources/test**
Test connection to all configured news sources.

**Response**:
```json
{
  "status": "success",
  "sources_tested": 3,
  "results": {
    "newsapi": {
      "source": "newsapi",
      "status": "success", 
      "message": "Connected successfully"
    },
    "newsdata": {
      "source": "newsdata",
      "status": "success",
      "message": "Connected successfully"  
    },
    "afp": {
      "source": "afp",
      "status": "success",
      "message": "Connected and authenticated successfully"
    }
  }
}
```

---

### **GET /health**
Comprehensive system health check including Google Sheets integration status.

**Response**:
```json
{
  "status": "healthy",
  "version": "0.5.0", 
  "sources": {
    "total_configured": 3,
    "available_sources": ["newsapi", "newsdata", "afp"],
    "source_details": {
      "afp": {"name": "AFP", "configured": true, "priority": 1},
      "newsapi": {"name": "NEWSAPI", "configured": true, "priority": 2}, 
      "newsdata": {"name": "NEWSDATA", "configured": true, "priority": 3}
    }
  },
  "system": {
    "environment": "development",
    "python_version": "3.11+",
    "fastapi_status": "running",
    "sentiment_analysis": "active",
    "google_sheets": "connected"
  }
}
```

---

### **GET /api/test**
Connection test endpoint for frontend verification.

**Response**:
```json
{
  "message": "Backend connection successful!",
  "data": {
    "timestamp": "2024-08-21",
    "