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
Fetch positive news from all available sources with AI sentiment analysis and automatic Google Sheets logging.

**Query Parameters**:
- `q` (optional): Search keywords (default: positive keywords per source)
- `language` (optional): Language code (default: "en")  
- `pageSize` (optional): Number of articles to return (1-100, default: 20)

**Example Request**:
```bash
curl "http://localhost:8000/api/news?q=medical%20breakthrough&pageSize=10"
```

**Enhanced Response**:
```json
{
  "status": "success",
  "query": "medical breakthrough",
  "totalSources": 3,
  "sourcesUsed": ["newsapi", "newsdata"],
  "sourcesFailed": [
    {"source": "afp", "error": "Content subscription required"}
  ],
  "totalArticles": 8,
  "crossSourceDuplicatesRemoved": 2,
  "sentiment_analyzed": true,
  "analyzed_sources": ["newsapi", "newsdata"],
  "sheets_logged": true,
  "total_logged": 8,
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
      "publishedAt": "2024-08-21T10:30:00Z",
      "content": "Full article content preview...",
      "api_source": "newsapi",
      "uplift_score": 0.652,
      "sentiment_analysis": {
        "sentiment": {
          "positive": 0.945,
          "negative": 0.055,
          "neutral": 0.0
        },
        "confidence": 0.847,
        "raw_emotions": {
          "anger": 0.012,
          "disgust": 0.008,
          "fear": 0.043,
          "joy": 0.234,
          "neutral": 0.589,
          "sadness": 0.015,
          "surprise": 0.099
        },
        "uplift_emotions": {
          "joy": 0.234,
          "hope": 0.423,
          "gratitude": 0.376,
          "awe": 0.099,
          "relief": 0.471,
          "compassion": 0.398
        },
        "uplift_score": 0.652,
        "analyzer": "transformers"
      }
    }
  ]
}
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

### **GET /api/sources**
Get information about all news sources and their configuration.

**Response**:
```json
{
  "status": "success",
  "sources": {
    "afp": {
      "name": "AFP",
      "configured": true,
      "priority": 1
    },
    "newsapi": {
      "name": "NEWSAPI", 
      "configured": true,
      "priority": 2
    },
    "newsdata": {
      "name": "NEWSDATA",
      "configured": true, 
      "priority": 3
    }
  },
  "priority_order": ["afp", "newsapi", "newsdata"]
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