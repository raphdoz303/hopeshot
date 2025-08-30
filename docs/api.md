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
  "version": "0.9.0",
  "features": [
    "Multi-source news aggregation",
    "SQLite database storage with auto-creation",
    "Google Sheets A/B testing data",
    "Multi-prompt analysis framework",
    "Geographic hierarchy management"
  ]
}
```

---

### **GET /api/news**
Fetch positive news from all available sources with multi-prompt Gemini analysis and dual storage (SQLite database + Google Sheets).

**Query Parameters**:
- `q` (optional): Search keywords (default: positive keywords per source)
- `language` (optional): Language code (default: "en")  
- `pageSize` (optional): Number of articles to return (1-100, default: 20)

**Example Request**:
```bash
curl "http://localhost:8000/api/news?q=medical%20breakthrough&pageSize=5"
```

**Enhanced Response with Dual Storage**:
```json
{
  "status": "success",
  "query": "medical breakthrough",
  "totalSources": 1,
  "sourcesUsed": ["afp"],
  "sourcesFailed": [],
  "totalArticles": 5,
  "crossSourceDuplicatesRemoved": 0,
  "gemini_analyzed": true,
  "prompt_versions": ["v1_comprehensive", "v2_precision", "v3_empathy_depth"],
  "database_inserted": 5,
  "sheets_logged": true,
  "total_logged": 15,
  "gemini_stats": {
    "total_tokens_used": 3429,
    "total_batches_processed": 1,
    "prompt_versions_count": 3,
    "total_analyses": 15
  },
  "articles": [
    {
      "title": "Medical Breakthrough: New Treatment Shows Promise",
      "description": "Scientists discover innovative approach...",
      "url": "https://afp-apicore-prod.afp.com/objects/api/get?id=...",
      "urlToImage": null,
      "source": {
        "id": "afp",
        "name": "Agence France-Presse"
      },
      "author": "Jane Smith",
      "publishedAt": "2025-08-29T10:30:00Z",
      "content": "Full article content preview...",
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
        "categories": ["medical", "technology"],
        "source_credibility": "high",
        "fact_checkable_claims": "yes",
        "evidence_quality": "strong",
        "controversy_level": "low",
        "solution_focused": "yes",
        "age_appropriate": "all",
        "truth_seeking": "no",
        "geographical_impact_level": "Global",
        "geographical_impact_location_names": ["World"],
        "geographical_impact_location_ids": [],
        "overall_hopefulness": 0.75,
        "reasoning": "Medical breakthrough shows promise"
      }
    }
  ]
}
```

**New Response Fields (v0.9.0)**:
- `database_inserted`: Number of articles successfully stored in SQLite database
- `geographical_impact_location_names`: Array of location names for display
- `geographical_impact_location_ids`: Array of location database IDs for relationships

**Dual Storage Strategy**:
- **SQLite Database**: First prompt results only (clean application data, no duplicates)
- **Google Sheets**: All prompt results (A/B testing research data with comparative analysis)

**Auto-Creation Features**:
- Categories automatically created as Gemini discovers them
- Geographic locations auto-created with hierarchical relationships
- Junction tables link articles to multiple categories and locations

---

### **GET /api/sources**
Get information about all news sources with enhanced database statistics.

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
  },
  "database_stats": {
    "articles": 19,
    "categories": 8,
    "locations": 12,
    "category_relationships": 25,
    "location_relationships": 15,
    "articles_last_24h": 19,
    "top_categories": [
      {"name": "social", "count": 8},
      {"name": "human rights", "count": 6}
    ],
    "top_locations": [
      {"name": "USA", "level": "country", "count": 6},
      {"name": "Europe", "level": "region", "count": 3}
    ]
  }
}
```

---

### **GET /api/sources/test**
Test connection to all configured sources including database and Gemini services.

**Response**:
```json
{
  "status": "success",
  "sources_tested": 1,
  "results": {
    "afp": {
      "source": "afp",
      "status": "success", 
      "message": "Connected and authenticated successfully"
    }
  },
  "database": {
    "status": "success",
    "message": "Database connected with multi-location support",
    "stats": {
      "articles": 19,
      "categories": 8,
      "locations": 12
    },
    "junction_table_exists": true
  },
  "gemini": {
    "status": "success",
    "message": "Gemini connected successfully with multi-location support",
    "response": "Connected",
    "database_path": "C:\\Users\\User\\hopeshot\\backend\\hopeshot_news.db",
    "database_exists": true
  },
  "system_status": "All services operational"
}
```

---

### **GET /health**
Comprehensive system health check including database statistics and A/B testing framework status.

**Response**:
```json
{
  "status": "healthy",
  "version": "0.9.0",
  "sources": {
    "total_configured": 1,
    "available_sources": ["afp"],
    "source_details": {
      "afp": {"name": "AFP", "configured": true, "priority": 1}
    }
  },
  "database": {
    "status": "connected",
    "stats": {
      "articles": 19,
      "categories": 8,
      "locations": 12,
      "category_relationships": 25,
      "location_relationships": 15,
      "articles_last_24h": 19,
      "top_categories": [
        {"name": "social", "count": 8},
        {"name": "human rights", "count": 6}
      ],
      "top_locations": [
        {"name": "USA", "level": "country", "count": 6},
        {"name": "Europe", "level": "region", "count": 3}
      ],
      "database_path": "C:\\Users\\User\\hopeshot\\backend\\hopeshot_news.db"
    }
  },
  "ab_testing": {
    "active_prompts": 3,
    "prompt_versions": ["v1_comprehensive", "v2_precision", "v3_empathy_depth"]
  },
  "system": {
    "environment": "development",
    "python_version": "3.11+",
    "fastapi_status": "running",
    "storage": "dual (database + sheets)"
  }
}
```

---

### **GET /api/test**
Connection test endpoint for frontend verification with database statistics.

**Response**:
```json
{
  "message": "Backend connection successful!",
  "data": {
    "timestamp": "2025-08-29",
    "backend_status": "healthy",
    "available_sources": ["afp"],
    "database_stats": {
      "articles": 19,
      "categories": 8,
      "locations": 12,
      "category_relationships": 25,
      "location_relationships": 15
    }
  }
}
```

---

## Database Integration Features

### Auto-Creation Capabilities
- **Categories**: Automatically created as Gemini discovers them in article analysis
- **Geographic Locations**: Auto-created with hierarchical relationships (country → region → continent)
- **Junction Relationships**: Many-to-many links established automatically

### Multi-Location Support
Articles can be linked to multiple locations for complex stories:
```json
"geographical_impact_location_names": ["USA", "Japan"],
"geographical_impact_location_ids": [3, 8]
```

### Geographic Hierarchy Queries
The junction table architecture enables sophisticated geographic filtering:
- Articles about specific countries: Direct location match
- Articles about regions: Includes all child countries
- Articles about continents: Includes all child regions and countries

### Deduplication Strategy
- **Hard Check**: URL uniqueness enforced by database constraints
- **Soft Check**: Title similarity detection (70% threshold) 
- **Database-First**: Existing URLs checked before Gemini analysis to save API costs

---

## Authentication Systems
- **NewsAPI**: Simple API key authentication
- **NewsData**: API key with query parameters
- **AFP**: OAuth2 password grant with automatic token management (5-hour expiry)
- **Google Sheets**: Service account with JSON credentials file
- **Gemini**: API key authentication with comprehensive rate limiting for multi-prompt processing
- **SQLite**: Local file-based database with connection pooling

---

## Error Handling

### Database Connection Management
The system uses connection reuse patterns to prevent database locking during bulk operations:
```json
{
  "database_inserted": 5,
  "sheets_logged": true,
  "sheets_error": null
}
```

### Graceful Degradation
Services fail independently without affecting the overall system:
- Database failures don't prevent sheets logging
- Sheets failures don't prevent database storage
- Individual source failures don't affect other sources

---

## Performance Considerations

### Rate Limiting with Multi-Prompt A/B Testing
- **Gemini API**: 14 requests/minute, 900 requests/day with 2-minute batch spacing
- **Multi-Prompt Overhead**: 3x analysis time for comparative data collection
- **Database Operations**: Local SQLite with optimized junction table queries
- **Connection Pooling**: Reused connections prevent lock contention

### Scaling Implications
- **Current Capacity**: ~24,000 articles/day with 3 active prompts
- **Database Performance**: SQLite suitable for single-user applications
- **Production Scaling**: Consider PostgreSQL for multi-user deployment

---

*Last updated: August 29, 2025*
*API version: 0.9.0*