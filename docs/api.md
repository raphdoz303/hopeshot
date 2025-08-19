# 🚀 HopeShot API Documentation

---

## 🌐 **Base URL**
- **Development**: `http://localhost:8000`
- **Production**: *TBD*

---

## 📋 **Available Endpoints**

### 🏠 **GET /** 
**Description**: Root endpoint providing basic API information

**Response**:
```json
{
  "message": "Hello from HopeShot backend! 🌟",
  "status": "running",
  "version": "0.1.0"
}
```

**Status Codes**:
- ✅ `200 OK`: Successful response

---

### 🧪 **GET /api/test**
**Description**: Connection test endpoint with sample data

**Response**:
```json
{
  "message": "Backend connection successful!",
  "data": {
    "timestamp": "2024-01-01",
    "backend_status": "healthy"
  }
}
```

**Status Codes**:
- ✅ `200 OK`: Successful response

---

### 📰 **GET /api/news**
**Description**: Fetch positive news articles from NewsAPI with automatic duplicate removal

**Query Parameters**:
- `q` (optional): Search keywords (default: "positive breakthrough innovation")
- `language` (optional): Language code (default: "en")  
- `pageSize` (optional): Number of articles to request (1-100, default: 20)

**Example Requests**:
```
GET /api/news
GET /api/news?q=medical breakthrough&pageSize=10
GET /api/news?q=space discovery&language=en&pageSize=5
```

**Response**:
```json
{
  "status": "success",
  "totalResults": 150,
  "requestedCount": 10,
  "uniqueArticles": 8,
  "duplicatesRemoved": 2,
  "articles": [
    {
      "title": "Medical Breakthrough: New Treatment Shows Promise",
      "description": "Scientists discover innovative approach to treating...",
      "url": "https://example.com/article",
      "urlToImage": "https://example.com/image.jpg",
      "source": {
        "id": "reuters",
        "name": "Reuters"
      },
      "author": "Jane Smith",
      "publishedAt": "2024-08-18T10:30:00Z",
      "content": "Full article content preview..."
    }
  ]
}
```

**Response Fields Explained**:
- `totalResults`: Total articles available from NewsAPI for this search
- `requestedCount`: Number of articles requested via pageSize parameter
- `uniqueArticles`: Number of unique articles returned (after duplicate removal)
- `duplicatesRemoved`: Number of duplicate articles filtered out
- `articles`: Array of unique news articles

**Duplicate Removal Logic**:
- Articles with identical titles (case-insensitive) are automatically filtered
- Only the first occurrence of each unique title is kept
- Helps ensure diverse content in search results

**Status Codes**:
- ✅ `200 OK`: Articles retrieved successfully
- ❌ `400 Bad Request`: Invalid parameters
- ❌ `500 Internal Server Error`: NewsAPI error or server issue

---

### 📊 **GET /api/news/sources** *(Planned)*
**Description**: Get available news sources for positive content filtering

**Response** *(Future)*:
```json
{
  "status": "success", 
  "sources": [
    {
      "id": "bbc-news",
      "name": "BBC News",
      "description": "Latest national and international news from the BBC",
      "category": "general"
    }
  ]
}
```

---

## 🚨 **Error Handling**

### Standard Error Response
```json
{
  "error": "Error description"
}
```

### Common Error Examples
```json
{
  "error": "NEWS_API_KEY not configured"
}
```

```json
{
  "error": "Failed to fetch news: HTTP error! status: 429"
}
```

### Status Codes
- ✅ `200 OK`: Request successful
- ❌ `400 Bad Request`: Invalid request parameters
- ❌ `404 Not Found`: Endpoint not found
- ❌ `429 Too Many Requests`: NewsAPI rate limit exceeded
- ❌ `500 Internal Server Error`: Server or NewsAPI error

---

## 🔧 **CORS Configuration**
- **Allowed Origins**: `http://localhost:3000` (Next.js frontend)
- **Allowed Methods**: All (`*`)
- **Allowed Headers**: All (`*`)
- **Credentials**: Enabled

---

## 🧪 **Testing**

### Manual Testing Interface
- **URL**: `http://localhost:3000/test`
- **Features**: Interactive buttons to test all endpoints
- **Response Display**: Formatted JSON with error handling

### Direct API Calls
```bash
# Test root endpoint
curl http://localhost:8000/

# Test connection
curl http://localhost:8000/api/test

# Test news API (default positive search)
curl http://localhost:8000/api/news

# Test news API with custom parameters
curl "http://localhost:8000/api/news?q=renewable%20energy&pageSize=5"
```

### Testing Tips
- Use small `pageSize` values (5-10) for faster testing
- Check the `duplicatesRemoved` field to see filtering in action
- Try different search terms: "medical breakthrough", "clean energy", "scientific discovery"

---

## 🚀 **Future Endpoints** *(Roadmap)*
- `POST /api/analyze` - Analyze article sentiment with AI
- `GET /api/health` - Detailed system health check
- `GET /api/news/categories` - Get news by positive categories
- `POST /api/feedback` - Submit article quality feedback

---

## 🔑 **Environment Configuration**
- **Required**: `NEWS_API_KEY` - Your NewsAPI.org API key
- **Optional**: `NEWS_API_BASE_URL` - NewsAPI base URL (defaults to official API)

---

*📅 Last Updated: August 18, 2025*  
*🔢 API Version: 0.1.0*  
*🏗️ Built with FastAPI + NewsAPI integration*