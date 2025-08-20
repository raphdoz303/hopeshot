# HopeShot Architecture

## Project Overview
HopeShot is a learning-first project with simple, modular components designed for easy understanding and extension. The system aggregates positive news from multiple sources using AI-powered sentiment analysis.

## Technology Stack
- **Frontend**: Next.js (React framework) with TypeScript and Tailwind CSS
- **Backend**: FastAPI (Python web framework) with Uvicorn ASGI server
- **Authentication**: OAuth2 password grant (AFP), API key authentication (NewsAPI, NewsData)
- **HTTP Client**: aiohttp for concurrent async requests
- **AI/ML**: OpenAI API for sentiment analysis (planned)
- **Data Storage**: Google Sheets for prototyping (planned)
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
│   └── services/                  # Multi-source news architecture
│       ├── sentiment/                        # Sentiment analysis service folder
│       │   ├── __init__.py                   # Package initialization
│       │   ├── base_analyzer.py
│       │   ├── sentiment_service.py           
│   │   │   └── transformers_analyzer.py 
│       ├── __init__.py           # Package initialization
│       ├── base_client.py        # Abstract base class
│       ├── newsapi_client.py     # NewsAPI.org client
│       ├── newsdata_client.py    # NewsData.io client  
│       ├── afp_client.py         # AFP client with OAuth2
│       └── news_service.py       # Multi-source orchestrator
└── scripts/                       # Utility scripts (empty)
```

## Service Architecture

### News Service Layer
- **NewsService**: Multi-source orchestrator with priority system and concurrent fetching
- **BaseNewsClient**: Abstract base providing shared functionality for all clients
- **Client Implementations**: 
  - **NewsAPIClient**: Mainstream news sources with positive keyword filtering
  - **NewsDataClient**: Alternative/international sources with category filtering
  - **AFPClient**: Professional journalism with OAuth2 authentication and "inspiring" genre filter

### Design Patterns
- **Template Method**: BaseNewsClient defines common interface, clients implement specifics
- **Strategy Pattern**: Interchangeable news sources with unified interface
- **Circuit Breaker**: Failed sources don't impact others (graceful degradation)
- **Priority Queue**: Articles sorted by source quality (AFP → NewsAPI → NewsData)

### Data Flow
1. Frontend calls `/api/news`
2. NewsService identifies available sources
3. All sources called concurrently via aiohttp
4. Each client converts response to standard article format
5. Cross-source duplicate removal (70% word overlap)
6. Articles sorted by source priority
7. Unified results returned with source tracking metadata

## API Architecture

### Core Endpoints
- **GET /api/news** - Unified aggregation from all available sources
- **GET /api/sources** - Source configuration and priority information
- **GET /api/sources/test** - Health check for all news source connections
- **GET /api/news/afp** - Direct AFP testing endpoint
- **GET /health** - Comprehensive system health dashboard

### Response Enhancement
- **API Source Tracking**: All articles include `api_source` field for quality analysis
- **Error Reporting**: `sourcesUsed` and `sourcesFailed` arrays in responses
- **Cross-Source Deduplication**: Smart duplicate removal across different APIs
- **Priority Ordering**: Articles automatically sorted by source quality

### Authentication Systems
- **NewsAPI**: Simple API key authentication
- **NewsData**: API key with query parameters
- **AFP**: OAuth2 password grant with automatic token management (5-hour expiry)

## Frontend Architecture

### Component Design
- **StatusBanner**: Reusable status display with configurable props
  - Props: `status`, `message`, `emoji`
  - Variants: development, success, warning, error
  - Styling: Tailwind CSS with dynamic classes

### Testing Interface
- **Location**: `http://localhost:3000/test`
- **Purpose**: Visual testing of backend API endpoints
- **Features**: Interactive buttons, real-time response display, error handling

## Sentiment Analysis Architecture

### Service Layer Design
- **SentimentService**: Multi-analyzer orchestrator ready for VADER, OpenAI integration
- **TransformersAnalyzer**: Primary analyzer using dual-model approach (sentiment + emotions)
- **Weighted Scoring System**: Custom uplift calculation prioritizing hope and awe over joy

### Data Flow Enhancement
News Service → Articles → Sentiment Service → Enhanced Articles with Uplift Scores

### Integration Points
- **Main API**: `/api/news` endpoint includes sentiment analysis for NewsAPI + NewsData
- **Source Filtering**: AFP articles excluded (use native positive filtering)
- **Frontend**: Test page displays sentiment data in enhanced JSON format

## Development Approach
1. **Documentation First** - Always document before coding
2. **Small Steps** - One feature at a time with testing
3. **Modular Design** - Each component has single responsibility
4. **Learning Focus** - Code optimized for understanding

## Current Status
- ✅ Multi-source news aggregation (NewsAPI + NewsData active)
- ✅ AFP integration with OAuth2 (awaiting content subscription activation)
- ✅ Cross-source duplicate detection
- ✅ API source tracking for quality analysis
- ⏳ Sentiment analysis integration (planned)
- ⏳ Google Sheets data storage (planned)

---
*Last updated: August 19, 2025*