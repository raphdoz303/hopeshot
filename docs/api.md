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
  "version": "0.3.0",
  "features": [
    "Multi-source news aggregation",
    "AFP professional news integration", 
    "Positive news filtering",
    "Cross-source duplicate removal"
  ]
}
```

---

### **GET /api/news**
Fetch positive news from all available sources with intelligent aggregation.

**Query Parameters**:
- `q` (optional): Search keywords (default: positive keywords per source)
- `language` (optional): Language code (default: "en")  
- `pageSize` (optional): Number of articles to return (1-100, default: 20)

**Example Request**:
```bash
curl "http://localhost:8000/api/news?q=medical%20breakthrough&pageSize=10"
```

**Response**:
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
      "publishedAt": "2024-08-19T10:30:00Z",
      "content": "Full article content preview...",
      "api_source": "newsapi"
    }
  ]
}
```

**Priority System**:
1. **AFP** (highest quality) - Professional journalism with "inspiring" genre filter
2. **NewsAPI** (mainstream) - Major news sources with positive keyword filtering  
3. **NewsData** (alternative) - International sources with category filtering

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
Comprehensive system health check.

**Response**:
```json
{
  "status": "healthy",
  "version": "0.3.0", 
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
    "fastapi_status": "running"
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
    "timestamp": "2024-08-19",
    "backend_status": "healthy",
    "available_sources": ["newsapi", "newsdata"]
  }
}
```

---

### **GET /api/news/afp**
Get news specifically from AFP source (testing endpoint).

**Query Parameters**: Same as main `/api/news` endpoint

**Response**: Standard article format with only AFP results

---

## Enhanced Endpoints

### **GET /api/news** (Updated)
Fetch positive news with integrated sentiment analysis.

**New Response Fields**:
```json
{
  "sentiment_analyzed": true,
  "analyzed_sources": ["newsapi", "newsdata"],
  "articles": [
    {
      "title": "...",
      "api_source": "newsapi",
      "uplift_score": 0.652,
      "sentiment_analysis": {
        "sentiment": {"positive": 0.945, "negative": 0.055, "neutral": 0.0},
        "confidence": 0.847,
        "raw_emotions": {
          "anger": 0.012, "disgust": 0.008, "fear": 0.043,
          "joy": 0.234, "neutral": 0.589, "sadness": 0.015, "surprise": 0.099
        },
        "uplift_emotions": {
          "joy": 0.234, "hope": 0.423, "gratitude": 0.376,
          "awe": 0.099, "relief": 0.471, "compassion": 0.398
        },
        "uplift_score": 0.652,
        "analyzer": "transformers"
      }
    }
  ]
}

---

## Error Handling

### Standard Error Response
```json
{
  "detail": "Error description"
}
```

### Common Errors
- `NEWS_API_KEY not configured`
- `Failed to fetch news: HTTP error! status: 429`
- `AFP authentication failed - check credentials`

### Status Codes
- `200 OK` - Request successful
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Endpoint not found
- `429 Too Many Requests` - API rate limit exceeded
- `500 Internal Server Error` - Server or API error
- `503 Service Unavailable` - Source not configured

---

## CORS Configuration
- **Allowed Origins**: `http://localhost:3000` (Next.js frontend)
- **Methods**: All
- **Headers**: All
- **Credentials**: Enabled

---

## Testing

### Manual Testing Interface
Visit `http://localhost:3000/test` for interactive API testing with buttons and formatted JSON responses.

### Direct API Calls
```bash
# Test system health
curl http://localhost:8000/health

# Test source availability
curl http://localhost:8000/api/sources

# Test source connections
curl http://localhost:8000/api/sources/test

# Test unified news aggregation
curl "http://localhost:8000/api/news?pageSize=5"

# Test with custom search
curl "http://localhost:8000/api/news?q=renewable%20energy&pageSize=10"
```

### Testing Tips
- Use small `pageSize` values (5-10) for faster testing
- Check `crossSourceDuplicatesRemoved` field to verify deduplication
- Monitor `sourcesUsed` and `sourcesFailed` arrays for source health
- Try positive search terms: "medical breakthrough", "clean energy", "scientific discovery"

---

## Environment Configuration

Required environment variables in `.env` file:

```bash
# NewsAPI.org (1000 requests/day free)
NEWS_API_KEY=your_newsapi_key_here

# NewsData.io (200 requests/day free)  
NEWSDATA_API_KEY=your_newsdata_key_here

# AFP (Professional news service)
AFP_CLIENT_ID=your_afp_client_id
AFP_CLIENT_SECRET=your_afp_client_secret
AFP_USERNAME=your_afp_email@example.com
AFP_PASSWORD=your_afp_password

# Optional
ENVIRONMENT=development
```

---

## Future Endpoints (Roadmap)
- `POST /api/analyze` - Analyze article sentiment with AI
- `GET /api/news/categories` - Get news by positive categories
- `POST /api/feedback` - Submit article quality feedback

---

*Last Updated: August 19, 2025*  
*API Version: 0.3.0*  
*Built with FastAPI + Multi-source integration*