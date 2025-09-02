# HopeShot API Documentation

> **Purpose**: Endpoint specifications, request/response formats, and API integration examples

## Base URL
- **Development**: `http://localhost:8000`

---

## Core Endpoints

### **GET /**
API information and status.

**Response**:
```json
{
  "message": "Hello from HopeShot backend! 🌟",
  "status": "running",
  "version": "0.12.0",
  "features": ["Multi-source news aggregation", "M49 integration", "A/B testing"]
}
```

### **GET /health**
System health check with database statistics.

**Response**:
```json
{
  "status": "healthy",
  "database": {
    "articles": 25,
    "categories": 8,
    "locations": 278,
    "location_relationships": 42
  },
  "sources": {
    "available_sources": ["afp"],
    "total_configured": 1
  },
  "ab_testing": {
    "active_prompts": 1,
    "prompt_versions": ["v1_comprehensive"]
  }
}
```

### **GET /api/categories**
Get category metadata for frontend filtering.

**Response**:
```json
{
  "status": "success",
  "categories": [
    {
      "id": 4,
      "name": "science tech",
      "filter_name": "Science & Tech",
      "emoji": "🔬",
      "description": "breakthroughs, inventions, space, AI, research",
      "color": "#E6FBFF",
      "accent": "#00A7C4"
    }
  ],
  "total": 8
}
```

### **GET /api/news**
Main news endpoint with Gemini analysis and M49 geographic processing.

**Query Parameters**:
- `q` (optional): Search keywords
- `language` (optional): Language code (default: "en")
- `pageSize` (optional): Articles to return (1-100, default: 20)

**Example Request**:
```bash
curl "http://localhost:8000/api/news?pageSize=3"
```

**Response Structure**:
```json
{
  "status": "success",
  "totalArticles": 3,
  "sourcesUsed": ["afp"],
  "gemini_analyzed": true,
  "database_inserted": 3,
  "sheets_logged": true,
  "articles": [
    {
      "title": "Medical Breakthrough Shows Promise",
      "description": "Scientists discover innovative approach...",
      "url": "https://example.com/article",
      "source": {"id": "afp", "name": "Agence France-Presse"},
      "author": "Jane Smith",
      "publishedAt": "2025-09-02T10:30:00Z",
      "api_source": "afp",
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
        "categories": ["health", "science tech"],
        "source_credibility": "high",
        "geographical_impact_level": "Global",
        "geographical_impact_m49_codes": [840, 124],
        "geographical_impact_location_names": ["United States", "Canada"],
        "geographical_impact_location_emojis": ["🇺🇸", "🇨🇦"],
        "overall_hopefulness": 0.75
      }
    }
  ]
}
```

### **GET /api/sources**
Source configuration and database statistics.

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
      "daily_limit": 20
    }
  },
  "database_stats": {
    "articles": 25,
    "categories": 8,
    "locations": 278,
    "m49_integration": {
      "schema_updated": true,
      "direct_storage": true
    }
  }
}
```

### **GET /api/sources/test**
Test all configured news sources and database connectivity.

**Response**:
```json
{
  "status": "success",
  "results": {
    "afp": {
      "status": "success",
      "message": "Connected and authenticated successfully"
    }
  },
  "database": {
    "status": "success",
    "stats": {"articles": 25, "categories": 8, "locations": 278}
  },
  "system_status": "All services operational"
}
```

---

## Authentication
- **NewsAPI/NewsData**: API key authentication
- **AFP**: OAuth2 password grant (auto-managed)
- **Google Sheets**: Service account JSON credentials
- **Gemini**: API key with rate limiting

## Error Handling
- **Missing M49 codes**: Returns empty location_names array
- **Service failures**: Graceful degradation, other sources continue
- **Rate limits**: 2-minute batch spacing for Gemini API safety

---
*API version: 0.12.0*