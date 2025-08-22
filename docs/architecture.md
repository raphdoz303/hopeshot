# HopeShot Architecture

## Project Overview
HopeShot is a learning-first project with simple, modular components designed for easy understanding and extension. The system aggregates positive news from multiple sources using AI-powered sentiment analysis via Google Gemini API and logs complete data to Google Sheets for research and algorithm improvement.

## Technology Stack
- **Frontend**: Next.js (React framework) with TypeScript and Tailwind CSS
- **Backend**: FastAPI (Python web framework) with Uvicorn ASGI server
- **Authentication**: OAuth2 password grant (AFP), API key authentication (NewsAPI, NewsData), Service account (Google Sheets)
- **HTTP Client**: aiohttp for concurrent async requests
- **AI/ML**: Google Gemini 2.5 Flash-Lite for comprehensive sentiment and emotional analysis
- **Data Storage**: Google Sheets for real-time data collection and analysis with 37-column rich schema
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
│   ├── test_sentiment.py          # Legacy sentiment analysis testing tool
│   ├── test_gemini.py             # Gemini API connection testing
│   ├── test_analysis.py           # Gemini analysis functionality testing
│   ├── test_full_pipeline.py      # End-to-end pipeline testing
│   ├── test_sheets_gemini.py      # Google Sheets integration testing
│   └── services/                  # Multi-source architecture
│       ├── sentiment/             # Legacy sentiment analysis service folder
│       │   ├── __init__.py        # Package initialization
│       │   ├── base_analyzer.py   # Abstract base for analyzers
│       │   ├── sentiment_service.py # Orchestrator managing multiple analyzers
│       │   └── transformers_analyzer.py # Legacy sentiment analyzer (backup)
│       ├── __init__.py            # Package initialization
│       ├── base_client.py         # Abstract base class
│       ├── newsapi_client.py      # NewsAPI.org client
│       ├── newsdata_client.py     # NewsData.io client  
│       ├── afp_client.py          # AFP client with OAuth2
│       ├── news_service.py        # Multi-source orchestrator
│       ├── gemini_service.py      # Google Gemini API integration
│       └── sheets_service.py      # Google Sheets integration with 37-column schema
└── scripts/                       # Utility scripts (empty)
```

## Service Architecture

### Enhanced Data Pipeline Flow
```
News APIs → News Service → Gemini Analysis → Google Sheets Storage
     ↓            ↓              ↓                    ↓
NewsAPI      Aggregation    Comprehensive      Real-time Rich Data
NewsData   → Deduplication → Emotional &       →   Collection for
AFP          Priority Sort   Contextual           Analysis & Training
                            Analysis
```

### News Service Layer
- **NewsService**: Multi-source orchestrator with priority system and concurrent fetching
- **BaseNewsClient**: Abstract base providing shared functionality for all clients
- **Client Implementations**: 
  - **NewsAPIClient**: Mainstream news sources with positive keyword filtering
  - **NewsDataClient**: Alternative/international sources with category filtering
  - **AFPClient**: Professional journalism with OAuth2 authentication and "inspiring" genre filter

### Gemini Analysis Layer
- **GeminiService**: Complete AI analysis service using Google Gemini 2.5 Flash-Lite
- **Comprehensive Analysis**: Emotions, sentiment, categories, fact-checking readiness, geographic scope
- **Intelligent Batch Processing**: Up to 100 articles per request with 2-minute pacing for optimal efficiency
- **Conservative Rate Limiting**: Exact token tracking with hard stops to prevent quota violations

### Data Storage Layer
- **SheetsService**: Google Sheets integration with service account authentication and 37-column unified schema
- **Enhanced Data Flattening**: Rich article metadata + comprehensive Gemini analysis
- **Unified Pipeline**: Single sheet for all news types with complete emotional and contextual analysis

## Design Patterns

### Architectural Patterns
- **Template Method**: BaseNewsClient defines common interface, clients implement specifics
- **Service-Oriented Architecture**: Clean separation between news, analysis, and storage services
- **Circuit Breaker**: Failed services don't impact others (graceful degradation)
- **Pipeline Pattern**: Sequential processing through aggregation → analysis → storage
- **Batch Processing**: Optimized large-batch processing for API efficiency

### Data Flow Patterns
- **Single Source of Truth**: Unified Google Sheets schema for all analysis data
- **Priority Queue**: Articles sorted by source quality (AFP → NewsAPI → NewsData)
- **Smart Rate Limiting**: Conservative buffering with exact usage tracking
- **Comprehensive Metadata Collection**: Future-proofed data capture for model training

## API Architecture

### Core Endpoints
- **GET /api/news** - Unified aggregation with Gemini analysis and automatic sheets logging
- **GET /api/sources** - Source configuration and priority information
- **GET /api/sources/test** - Health check for all news source connections
- **GET /api/news/afp** - Direct AFP testing endpoint
- **GET /health** - Comprehensive system health dashboard

### Enhanced Response Structure
```json
{
  "status": "success",
  "gemini_analyzed": true,
  "analyzed_sources": ["newsapi", "newsdata", "afp"],
  "sheets_logged": true,
  "total_logged": 5,
  "articles": [
    {
      "title": "...",
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

### Authentication Systems
- **NewsAPI**: Simple API key authentication
- **NewsData**: API key with query parameters
- **AFP**: OAuth2 password grant with automatic token management (5-hour expiry)
- **Google Sheets**: Service account with JSON credentials file
- **Gemini**: API key authentication with comprehensive rate limiting

## Data Architecture

### Enhanced Google Sheets Schema (37 Columns)
```
Basic Article Data (9 columns):
- timestamp, title, description, url, author, published_at
- api_source, source_id, source_name

Sentiment Analysis (5 columns):
- uplift_score, sentiment_positive, sentiment_negative, sentiment_neutral, sentiment_confidence

Target Emotions (6 columns):
- emotion_hope, emotion_awe, emotion_gratitude, emotion_compassion, emotion_relief, emotion_joy

Fact-checking Readiness (3 columns):
- source_credibility, fact_checkable_claims, evidence_quality

Content Analysis (4 columns):
- controversy_level, solution_focused, age_appropriate, truth_seeking

Geographic Analysis (4 columns):
- geographic_scope, country_focus, local_focus, geographic_relevance

Enhanced Metadata (3 columns):
- categories, reasoning, analyzer_type

Future Expansion (3 columns):
- reserved1, reserved2, reserved3
```

### Unified Data Flow
```
News Service → All Articles → Gemini Analysis → Rich Metadata → Single Google Sheets Pipeline
```

### Scale and Capacity
- **Gemini Capacity**: 72,000 articles/day (100 articles × 720 requests/day)
- **Actual Need**: ~5,000 articles/day from all sources
- **Headroom**: 13x capacity for growth and experimentation
- **Cost Safety**: Conservative rate limiting prevents quota violations

## Frontend Architecture

### Component Design
- **StatusBanner**: Reusable status display with configurable props
  - Props: `status`, `message`, `emoji`
  - Variants: development, success, warning, error
  - Styling: Tailwind CSS with dynamic classes

### Testing Interface
- **Location**: `http://localhost:3000/test`
- **Purpose**: Visual testing of backend API endpoints with real-time data
- **Features**: 6 source-specific buttons, enhanced JSON display, comprehensive analysis visualization

## Development Approach
1. **Documentation First** - Always document before coding
2. **Small Steps** - One feature at a time with testing
3. **Modular Design** - Each component has single responsibility
4. **Learning Focus** - Code optimized for understanding
5. **Data-Driven** - Collect comprehensive data for algorithm improvement

## Current Status
- ✅ Complete Google Gemini 2.5 Flash-Lite integration with rich analysis
- ✅ Unified 37-column Google Sheets pipeline for comprehensive data collection
- ✅ Multi-source news aggregation (NewsAPI + NewsData active, AFP authenticated)
- ✅ Intelligent batch processing with 100 articles per request
- ✅ Conservative rate limiting with exact token tracking and hard stops
- ✅ Massive scale capacity (72k articles/day vs 5k needed)
- 🔄 Prompt optimization for consistent analysis quality (in progress)
- 📋 Integration with main news pipeline (planned)

## Technical Debt
- **Prompt engineering**: Current Gemini prompts need refinement for consistent results
- **Legacy sentiment code**: Transformers-based analysis kept as backup but not actively used
- **Error monitoring**: No comprehensive logging dashboard for analysis quality tracking
- **Caching strategy**: No duplicate article detection to avoid re-analyzing identical content

## Scaling Considerations
- **API Integration**: Ready to handle full news volume with massive capacity headroom
- **Data Storage**: Google Sheets suitable for prototype; database migration needed for production scale
- **Analysis Quality**: Systematic prompt optimization needed for consistent emotional scoring
- **User Interface**: Rich analysis data ready for dashboard and filtering features

---
*Last updated: August 22, 2025*
*Architecture version: 0.6.0*