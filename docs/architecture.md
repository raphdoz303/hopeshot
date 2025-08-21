# HopeShot Architecture

## Project Overview
HopeShot is a learning-first project with simple, modular components designed for easy understanding and extension. The system aggregates positive news from multiple sources using AI-powered sentiment analysis and logs complete data to Google Sheets for research and algorithm improvement.

## Technology Stack
- **Frontend**: Next.js (React framework) with TypeScript and Tailwind CSS
- **Backend**: FastAPI (Python web framework) with Uvicorn ASGI server
- **Authentication**: OAuth2 password grant (AFP), API key authentication (NewsAPI, NewsData), Service account (Google Sheets)
- **HTTP Client**: aiohttp for concurrent async requests
- **AI/ML**: Transformers (Hugging Face) for sentiment analysis with dual-model approach
- **Data Storage**: Google Sheets for real-time data collection and analysis
- **Version Control**: Git + GitHub

## Project Structure
```
hopeshot/
├── README.md                      # Project overview
├── CHANGELOG.md                   # Version history  
├── .env.example                   # Environment variables template
├── .gitignore                     # Define files to ignore for Git
├── docs/                          # Documentation
│   ├── api.md                     # API endpoint documentation
│   ├── architecture.md            # This file
│   └── setup.md                   # Installation and setup guide
├── frontend/                      # Next.js application
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx           # Homepage component
│   │   │   └── test/page.tsx      # API testing interface
│   │   └── components/
│   │       └── StatusBanner.tsx   # Reusable status display component
│   ├── package.json               # Node.js dependencies
│   └── tailwind.config.js         # Styling configuration
├── backend/
│   ├── main.py                    # FastAPI application with unified endpoints
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # API keys and configuration
│   ├── gsheetapi_credentials.json # Google Sheets service account (gitignored)
│   ├── test_sentiment.py          # Sentiment analysis testing tool
│   ├── debug_emotions.py          # Raw emotion model debugging tool
│   └── services/                  # Multi-source architecture
│       ├── sentiment/             # Sentiment analysis service folder
│       │   ├── __init__.py        # Package initialization
│       │   ├── base_analyzer.py   # Abstract base for analyzers
│       │   ├── sentiment_service.py # Orchestrator managing multiple analyzers
│       │   └── transformers_analyzer.py # Primary sentiment analyzer
│       ├── __init__.py            # Package initialization
│       ├── base_client.py         # Abstract base class
│       ├── newsapi_client.py      # NewsAPI.org client
│       ├── newsdata_client.py     # NewsData.io client  
│       ├── afp_client.py          # AFP client with OAuth2
│       ├── news_service.py        # Multi-source orchestrator
│       └── sheets_service.py      # Google Sheets integration
└── scripts/                       # Utility scripts (empty)
```

## Service Architecture

### Data Pipeline Flow
```
News APIs → News Service → Sentiment Analysis → Google Sheets Storage
     ↓            ↓              ↓                    ↓
NewsAPI      Aggregation    Transformers        Real-time Data
NewsData   → Deduplication → Models        →   Collection for
AFP          Priority Sort   Uplift Calc        Analysis
```

### News Service Layer
- **NewsService**: Multi-source orchestrator with priority system and concurrent fetching
- **BaseNewsClient**: Abstract base providing shared functionality for all clients
- **Client Implementations**: 
  - **NewsAPIClient**: Mainstream news sources with positive keyword filtering
  - **NewsDataClient**: Alternative/international sources with category filtering
  - **AFPClient**: Professional journalism with OAuth2 authentication and "inspiring" genre filter

### Sentiment Analysis Layer
- **SentimentService**: Multi-analyzer orchestrator ready for VADER, OpenAI integration
- **TransformersAnalyzer**: Primary analyzer using dual-model approach (sentiment + emotions)
- **Weighted Scoring System**: Custom uplift calculation prioritizing hope and awe over joy

### Data Storage Layer
- **SheetsService**: Google Sheets integration with service account authentication
- **Data Flattening**: Converts nested article+sentiment objects into 25-column spreadsheet rows
- **Batch Operations**: Efficient logging of multiple articles with error handling

## Design Patterns

### Architectural Patterns
- **Template Method**: BaseNewsClient defines common interface, clients implement specifics
- **Strategy Pattern**: Interchangeable news sources and sentiment analyzers with unified interfaces
- **Observer Pattern**: Sheets logging triggered by API calls without tight coupling
- **Service-Oriented Architecture**: Separate concerns (news, sentiment, sheets) with clean interfaces

### Data Flow Patterns
- **Circuit Breaker**: Failed sources don't impact others (graceful degradation)
- **Priority Queue**: Articles sorted by source quality (AFP → NewsAPI → NewsData)
- **Pipeline Pattern**: Sequential processing through aggregation → analysis → storage
- **Batch Processing**: Multiple articles processed together for efficiency

## API Architecture

### Core Endpoints
- **GET /api/news** - Unified aggregation with sentiment analysis and automatic sheets logging
- **GET /api/sources** - Source configuration and priority information
- **GET /api/sources/test** - Health check for all news source connections
- **GET /api/news/afp** - Direct AFP testing endpoint
- **GET /health** - Comprehensive system health dashboard

### Enhanced Response Structure
```json
{
  "status": "success",
  "sentiment_analyzed": true,
  "analyzed_sources": ["newsapi", "newsdata"],
  "sheets_logged": true,
  "total_logged": 5,
  "articles": [
    {
      "title": "...",
      "api_source": "newsapi",
      "uplift_score": 0.652,
      "sentiment_analysis": {
        "sentiment": {"positive": 0.945, "negative": 0.055, "neutral": 0.0},
        "confidence": 0.847,
        "raw_emotions": {...},
        "uplift_emotions": {...},
        "uplift_score": 0.652,
        "analyzer": "transformers"
      }
    }
  ]
}
```

### Authentication Systems
- **NewsAPI**: Simple API key authentication
- **NewsData**: API key with query parameters
- **AFP**: OAuth2 password grant with automatic token management (5-hour expiry)
- **Google Sheets**: Service account with JSON credentials file

## Data Architecture

### Google Sheets Schema (25 Columns)
```
Basic Article Data (9 columns):
- timestamp, title, description, url, author, published_at
- api_source, source_id, source_name

Sentiment Scores (5 columns):
- uplift_score, sentiment_positive, sentiment_negative, sentiment_neutral, sentiment_confidence

Raw Emotions (6 columns):
- emotion_anger, emotion_disgust, emotion_fear, emotion_joy, emotion_sadness, emotion_surprise

Uplift Emotions (5 columns):
- uplift_hope, uplift_gratitude, uplift_awe, uplift_relief, uplift_compassion
```

### Data Flow Enhancement
News Service → Articles → Sentiment Service → Enhanced Articles with Uplift Scores → Google Sheets Logging

### Integration Points
- **Main API**: `/api/news` endpoint includes sentiment analysis for NewsAPI + NewsData
- **Source Filtering**: AFP articles excluded from sentiment analysis (use native positive filtering)
- **Real-time Logging**: All API calls automatically generate research data
- **Error Isolation**: Sheets logging failures don't impact API responses

## Frontend Architecture

### Component Design
- **StatusBanner**: Reusable status display with configurable props
  - Props: `status`, `message`, `emoji`
  - Variants: development, success, warning, error
  - Styling: Tailwind CSS with dynamic classes

### Testing Interface
- **Location**: `http://localhost:3000/test`
- **Purpose**: Visual testing of backend API endpoints with real-time data
- **Features**: 6 source-specific buttons, enhanced JSON display, sentiment analysis visualization

## Development Approach
1. **Documentation First** - Always document before coding
2. **Small Steps** - One feature at a time with testing
3. **Modular Design** - Each component has single responsibility
4. **Learning Focus** - Code optimized for understanding
5. **Data-Driven** - Collect real data to improve algorithms

## Current Status
- ✅ Multi-source news aggregation (NewsAPI + NewsData active)
- ✅ AFP integration with OAuth2 (awaiting content subscription activation)
- ✅ Complete sentiment analysis with Transformers models
- ✅ Google Sheets data pipeline for real-time collection
- ✅ Cross-source duplicate detection and priority ranking
- ✅ API source tracking for quality analysis
- 🔄 Sentiment algorithm calibration (using collected data)
- 📋 Enhanced data analysis dashboard (planned)

## Technical Debt
- **Neutral scoring calibration** - Transformers correctly return 0 for neutral articles, need algorithm tuning
- **No caching mechanism** - Repeated sentiment analysis on same articles wastes compute
- **Hard-coded sheet structure** - 25 columns fixed in code rather than configurable
- **Single service account** - No credential rotation or backup authentication
- **No data archival** - Google Sheets will grow indefinitely without cleanup strategy

---
*Last updated: August 21, 2025*
*Architecture version: 0.5.0*