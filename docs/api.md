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
  "version": "0.11.0",
  "features": [
    "Multi-source news aggregation",
    "SQLite database storage with M49 integration",
    "Google Sheets A/B testing data",
    "Multi-prompt analysis framework",
    "Direct M49 code storage and hierarchical filtering"
  ]
}
```

---

### **GET /api/categories**
Get all available categories with metadata for dynamic frontend filtering.

**Query Parameters**: None

**Example Request**:
```bash
curl "http://localhost:8000/api/categories"
```

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
      "description": "breakthroughs, inventions, space, AI, research, discoveries",
      "color": "#E6FBFF",
      "accent": "#00A7C4"
    },
    {
      "id": 5,
      "name": "health",
      "filter_name": "Health",
      "emoji": "🩺",
      "description": "medical progress, wellbeing, mental health, public health improvements",
      "color": "#E9FBFB",
      "accent": "#0EA5A4"
    },
    {
      "id": 6,
      "name": "environment",
      "filter_name": "Environment",
      "emoji": "🌱",
      "description": "climate action, conservation, renewable energy, biodiversity recovery",
      "color": "#EAFBF1",
      "accent": "#22C55E"
    },
    {
      "id": 7,
      "name": "social progress",
      "filter_name": "Social Progress",
      "emoji": "✊",
      "description": "equality, inclusion, policy changes, social justice improvements",
      "color": "#FFEDEF",
      "accent": "#E84E5A"
    },
    {
      "id": 8,
      "name": "education",
      "filter_name": "Education",
      "emoji": "🎓",
      "description": "access to learning, teaching methods, scholarships, edtech",
      "color": "#F3F0FF",
      "accent": "#7C3AED"
    },
    {
      "id": 9,
      "name": "human kindness",
      "filter_name": "Human Kindness",
      "emoji": "💖",
      "description": "acts of generosity, rescues, donations, everyday hero stories",
      "color": "#EEF2FF",
      "accent": "#6366F1"
    },
    {
      "id": 10,
      "name": "diplomacy",
      "filter_name": "Diplomacy",
      "emoji": "🕊️",
      "description": "peace agreements, negotiations, conflict resolution, cooperation between nations",
      "color": "#EEFDF4",
      "accent": "#12B981"
    },
    {
      "id": 11,
      "name": "culture",
      "filter_name": "Culture",
      "emoji": "🎭",
      "description": "arts, heritage, creativity, festivals, inspiring cultural projects",
      "color": "#EAF6FF",
      "accent": "#3BA3FF"
    }
  ],
  "total": 8
}
```

**Category Field Descriptions**:
- `name`: Internal category name used by Gemini AI (e.g., "science tech")
- `filter_name`: Clean display name for frontend UI (e.g., "Science & Tech")
- `emoji`: Visual identifier for category
- `description`: Scope and examples of category content
- `color`: Background color for category chips/badges
- `accent`: Border and text color for selected states

---

### **GET /api/news**
Fetch positive news from all available sources with multi-prompt Gemini analysis, M49 geographic processing, and dual storage (SQLite database + Google Sheets).

**Query Parameters**:
- `q` (optional): Search keywords (default: positive keywords per source)
- `language` (optional): Language code (default: "en")  
- `pageSize` (optional): Number of articles to return (1-100, default: 20)

**Example Request**:
```bash
curl "http://localhost:8000/api/news?q=medical%20breakthrough&pageSize=5"
```

**Enhanced Response with M49 Integration**:
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
  "prompt_versions": ["v1_comprehensive"],
  "database_inserted": 5,
  "sheets_logged": true,
  "total_logged": 5,
  "gemini_stats": {
    "total_tokens_used": 1581,
    "total_batches_processed": 1,
    "prompt_versions_count": 1,
    "total_analyses": 5
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
      "publishedAt": "2025-09-01T10:30:00Z",
      "content": "Full article content preview...",
      "api_source": "afp",
      "gemini_analysis": {
        "article_index": 0,
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
        "fact_checkable_claims": "yes",
        "evidence_quality": "strong",
        "controversy_level": "low",
        "solution_focused": "yes",
        "age_appropriate": "all",
        "truth_seeking": "yes",
        "geographical_impact_level": "Global",
        "geographical_impact_m49_codes": [840, 124],
        "geographical_impact_location_names": ["United States", "Canada"],
        "overall_hopefulness": 0.75,
        "reasoning": "Medical breakthrough shows promise"
      }
    }
  ]
}
```

**New Response Fields (v0.11.0)**:
- `geographical_impact_m49_codes`: Array of UN M49 standard codes for precise location identification
- `geographical_impact_location_names`: Array of location names derived from M49 database lookup
- `database_inserted`: Number of articles successfully stored in SQLite database with M49 integration

**M49 Integration Features**:
- **Direct Storage**: M49 codes stored in junction table without ID conversion
- **Hierarchical Support**: Codes support recursive filtering (Asia includes all Asian countries)
- **Name Resolution**: Location names populated via database JOIN on M49 codes
- **Multi-Location**: Articles can reference multiple geographic locations

---

### **GET /api/sources**
Get information about all news sources with enhanced M49 database statistics.

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
    }
  },
  "priority_order": ["afp"],
  "database_stats": {
    "articles": 25,
    "categories": 8,
    "locations": 278,
    "category_relationships": 35,
    "location_relationships": 42,
    "articles_last_24h": 25,
    "top_categories": [
      {"name": "culture", "count": 12},
      {"name": "social progress", "count": 8}
    ],
    "top_locations": [
      {"name": "United States", "level": 5, "m49_code": 840, "count": 8},
      {"name": "Asia", "level": 2, "m49_code": 142, "count": 6}
    ],
    "m49_integration": {
      "schema_updated": true,
      "junction_table": "article_locations (article_id, m49_code)",
      "direct_storage": true
    }
  }
}
```

---

### **GET /api/sources/test**
Test connection to all configured sources including M49 database integration.

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
    "message": "Database connected with direct M49 integration",
    "stats": {
      "articles": 25,
      "categories": 8,
      "locations": 278
    },
    "article_locations_schema": ["article_id", "m49_code"],
    "m49_join_test_count": 42,
    "schema_version": "m49_direct_v1"
  },
  "gemini": {
    "status": "success",
    "message": "Gemini connected successfully with direct M49 integration",
    "response": "Connected",
    "database_path": "C:\\Users\\User\\hopeshot\\backend\\hopeshot_news.db",
    "database_exists": true
  },
  "system_status": "All services operational with M49 integration"
}
```

---

### **GET /health**
Comprehensive system health check including M49 integration status and database statistics.

**Response**:
```json
{
  "status": "healthy",
  "version": "0.11.0",
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
      "articles": 25,
      "categories": 8,
      "locations": 278,
      "category_relationships": 35,
      "location_relationships": 42,
      "articles_last_24h": 25,
      "top_categories": [
        {"name": "culture", "count": 12},
        {"name": "social progress", "count": 8}
      ],
      "top_locations": [
        {"name": "United States", "level": 5, "m49_code": 840, "count": 8},
        {"name": "Asia", "level": 2, "m49_code": 142, "count": 6}
      ],
      "database_path": "C:\\Users\\User\\hopeshot\\backend\\hopeshot_news.db",
      "m49_integration": {
        "schema_updated": true,
        "junction_table": "article_locations (article_id, m49_code)",
        "direct_storage": true
      }
    }
  },
  "ab_testing": {
    "active_prompts": 1,
    "prompt_versions": ["v1_comprehensive"]
  },
  "system": {
    "environment": "development",
    "python_version": "3.11+",
    "fastapi_status": "running",
    "storage": "dual (database + sheets)",
    "geographic_system": "UN M49 direct integration"
  }
}
```

---

### **GET /api/test**
Connection test endpoint for frontend verification with M49 database statistics.

**Response**:
```json
{
  "message": "Backend connection successful!",
  "data": {
    "timestamp": "2025-09-01",
    "backend_status": "healthy",
    "available_sources": ["afp"],
    "database_stats": {
      "articles": 25,
      "categories": 8,
      "locations": 278,
      "category_relationships": 35,
      "location_relationships": 42,
      "m49_integration": {
        "schema_updated": true,
        "direct_storage": true
      }
    }
  }
}
```

---

## M49 Geographic Integration Features

### Direct M49 Code Storage
The system stores UN M49 standard geographic codes directly in junction tables without conversion overhead:

```sql
-- Junction table structure
article_locations:
- article_id (INTEGER) - Foreign key to articles table
- m49_code (INTEGER) - UN M49 standard code (840=USA, 392=Japan, 001=World)

-- Example data
article_id | m49_code
-----------|----------
1          | 840      -- Article about USA
1          | 392      -- Same article also affects Japan
2          | 001      -- Article with global impact
```

### Location Name Resolution
Location names are populated via database JOIN queries rather than stored redundantly:

```sql
-- API query to populate location names
SELECT DISTINCT
    a.title,
    a.geographical_impact_level,
    GROUP_CONCAT(l.name) as location_names,
    GROUP_CONCAT(al.m49_code) as m49_codes
FROM articles a
LEFT JOIN article_locations al ON a.id = al.article_id
LEFT JOIN locations l ON al.m49_code = l.m49_code
GROUP BY a.id;
```

### Hierarchical Filtering Support
The M49 system enables sophisticated geographic filtering:

```sql
-- Find all articles about "Asia" (includes Vietnam, Japan, etc.)
WITH RECURSIVE asia_hierarchy AS (
  SELECT id, name, m49_code FROM locations WHERE m49_code = 142  -- Asia
  UNION ALL
  SELECT l.id, l.name, l.m49_code
  FROM locations l
  JOIN asia_hierarchy ah ON l.parent_id = ah.id
)
SELECT DISTINCT a.*
FROM articles a
JOIN article_locations al ON a.id = al.article_id
JOIN asia_hierarchy ah ON al.m49_code = ah.m49_code;
```

---

## Authentication Systems
- **NewsAPI**: Simple API key authentication
- **NewsData**: API key with query parameters
- **AFP**: OAuth2 password grant with automatic token management (5-hour expiry)
- **Google Sheets**: Service account with JSON credentials file
- **Gemini**: API key authentication with comprehensive rate limiting for multi-prompt processing
- **SQLite**: Local file-based database with M49 junction table integration

---

## Error Handling

### M49 Integration Error Patterns
The system handles various M49-related errors gracefully:

**Missing M49 Codes in Database:**
```json
{
  "geographical_impact_m49_codes": [158],
  "geographical_impact_location_names": []
}
```
- Occurs when Gemini returns valid M49 codes not present in locations table
- System stores M49 codes but location name lookup returns empty array

**Invalid M49 Codes from Gemini:**
```json
{
  "geographical_impact_m49_codes": [36],
  "geographical_impact_location_names": ["Australia"]
}
```
- Gemini returns wrong M49 code (36=Australia instead of 360=Indonesia)
- System processes whatever Gemini provides, resulting in incorrect location names

### Database Connection Management
The system uses direct M49 storage to eliminate connection overhead:
```json
{
  "database_inserted": 5,
  "sheets_logged": true,
  "m49_codes_stored": [840, 392, 156],
  "location_names_resolved": 3
}
```

### Graceful Degradation
Services fail independently without affecting the overall system:
- M49 lookup failures don't prevent article storage
- Location name resolution errors don't affect sentiment analysis
- Individual source failures don't impact other sources

---

## Performance Considerations

### M49 Integration Performance
- **Direct Storage**: No ID conversion overhead during article insertion
- **Indexed Joins**: M49 codes indexed for fast location name resolution
- **Batch Processing**: Multiple M49 codes processed efficiently in single queries
- **Hierarchical Queries**: Recursive CTEs enable complex geographic filtering

### Rate Limiting with Multi-Prompt A/B Testing
- **Gemini API**: 14 requests/minute, 900 requests/day with 2-minute batch spacing
- **Multi-Prompt Overhead**: 1x analysis time with combined prompt approach
- **Database Operations**: Local SQLite with optimized M49 junction table queries
- **M49 Lookup Performance**: Direct code matching eliminates conversion latency

### Scaling Implications
- **Current Capacity**: ~24,000 articles/day with M49 processing and dual storage
- **Database Performance**: SQLite suitable for single-user applications with M49 indexing
- **Production Scaling**: Consider PostgreSQL for multi-user deployment with M49 constraints

---

## Known Issues & Data Quality

### M49 Integration Issues
- **Gemini Code Accuracy**: AI returns incorrect M49 codes (Indonesia→36 instead of 360, Vietnam→100 instead of 704)
- **Database Coverage**: Not all M49 codes exist in locations table causing name lookup failures
- **Validation Gap**: No middleware to catch obviously wrong codes before database storage
- **Prompt Ambiguity**: Geographic instructions need specific M49 examples for better accuracy

### Location Name Resolution
- **Empty Name Arrays**: Valid M49 codes return empty names when codes missing from locations table
- **Wrong Code Propagation**: Incorrect M49 codes from Gemini result in wrong location names
- **Fallback Handling**: No default location names when M49 lookup fails

### Suggested Improvements
- **M49 Validation Layer**: Pre-insertion validation against known code ranges
- **Complete Location Import**: Full UN M49 reference data import from provided CSV
- **Gemini Prompt Enhancement**: Add correct M49 examples and validation instructions
- **Error Recovery System**: Fallback mechanisms when location resolution fails

---

*Last updated: September 1, 2025*
*API version: 0.11.0*