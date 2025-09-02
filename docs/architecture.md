# HopeShot Architecture

> **Purpose**: Current system structure, component relationships, and key architectural decisions for session continuity

## Project Overview
HopeShot aggregates positive news using AI-powered sentiment analysis via Google Gemini with multi-prompt A/B testing, storing normalized data in SQLite and research data in Google Sheets. Learning-first project with modular, documented components.

## Technology Stack
- **Frontend**: Next.js + TypeScript + Tailwind CSS v4 (CSS variables)
- **Backend**: FastAPI + SQLite + Google Gemini 2.5 Flash-Lite
- **Data**: Dual storage (SQLite for app, Google Sheets for A/B testing)
- **Geographic**: UN M49 codes for location identification
- **APIs**: NewsAPI, NewsData, AFP with OAuth2

## Current System Architecture (v0.12.0)

### Core Data Flow
```
News APIs → Multi-Source Aggregation → Gemini Analysis → M49 Processing → Dual Storage
     ↓              ↓                       ↓                ↓              ↓
NewsAPI        Deduplication         All Active Prompts   Direct M49     SQLite + Sheets
NewsData   →   Priority Sort     →   Geographic Analysis → Junction    + Frontend API
AFP            Cross-Source          M49 Code Validation   Storage       Integration
```

### Database Schema (SQLite)
```sql
articles: 37 columns (basic + sentiment + emotions + analysis + geographic impact level only)
categories: id, name, filter_name, emoji, description, color, accent
locations: id, name, m49_code, hierarchy_level, parent_id, emoji, iso_codes
article_categories: article_id, category_id (many-to-many)
article_locations: article_id, m49_code (many-to-many, direct M49 storage)
```

### Project structure
```
hopeshot/
├── README.md                      # Project overview
├── CHANGELOG.md                   # Version history  
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── docs/                          # Documentation
│   ├── api.md                     # API endpoint documentation
│   ├── architecture.md            # This file
│   ├── setup.md                   # Installation and setup guide
│   └── parameters_reference.md    # TypeScript interfaces and parameter guide
├── frontend/                      # Next.js application
│   ├── services/                  # API service layer
│   │   └── api.ts                 # Centralized backend communication + TypeScript interfaces
│   ├── hooks/                     # Custom React hooks
│   │   └── useNews.ts             # Custom hook for data fetching + filtering state
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx           # Homepage with hero + top 3 articles
│   │   │   ├── explore/page.tsx   # News feed with real API integration
│   │   │   ├── test-cards/page.tsx # Component testing interface
│   │   │   └── globals.css        # Sky & Growth color palette via CSS variables
│   │   └── components/
│   │       └── VerticalNewsCard.tsx # Article cards with dynamic categories + M49 emojis
│   ├── package.json               # Node.js dependencies
│   └── tailwind.config.js         # Tailwind configuration (unused in v4)
├── backend/
│   ├── main.py                    # FastAPI application with M49-enhanced endpoints
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # API keys and configuration (gitignored)
│   ├── prompts.yaml               # A/B testing prompt configurations with M49 instructions
│   ├── sources.yaml               # News source configuration with ethical limits
│   ├── hopeshot_news.db          # SQLite database (gitignored)
│   ├── gsheetapi_credentials.json # Google Sheets service account (gitignored)
│   ├── database_setup.py          # SQLite schema creation script
│   ├── test_sentiment.py          # Legacy sentiment analysis testing tool
│   ├── test_gemini.py             # Gemini API connection testing
│   ├── test_analysis.py           # Gemini analysis functionality testing
│   ├── test_full_pipeline.py      # End-to-end pipeline testing
│   ├── test_sheets_gemini.py      # Google Sheets integration testing
│   └── services/                  # Service-oriented architecture
│       ├── sentiment/             # Legacy sentiment analysis (backup)
│       │   ├── __init__.py        # Package initialization
│       │   ├── base_analyzer.py   # Abstract base for analyzers
│       │   ├── sentiment_service.py # Orchestrator for analyzers
│       │   └── transformers_analyzer.py # Legacy sentiment (backup)
│       ├── __init__.py            # Package initialization
│       ├── base_client.py         # Abstract base class for news clients
│       ├── newsapi_client.py      # NewsAPI.org client
│       ├── newsdata_client.py     # NewsData.io client  
│       ├── afp_client.py          # AFP client with OAuth2
│       ├── news_service.py        # Multi-source orchestrator with YAML config
│       ├── gemini_service.py      # Multi-prompt analysis with direct M49 integration
│       ├── sheets_service.py      # Google Sheets for A/B testing research data
│       └── database_service.py    # SQLite with M49 junction tables + location emoji lookup
└── scripts/                       # Utility scripts (empty)
```

## Key Architectural Decisions

### M49 Geographic System
- **Direct Storage**: M49 codes stored in junction table without ID conversion
- **Database JOIN**: Location names + emojis populated via real-time queries
- **Hierarchical Support**: Enables filtering (Asia includes Vietnam, Japan, etc.)

### Dual Storage Strategy
- **SQLite**: Clean application data (first prompt only) for frontend
- **Google Sheets**: All prompt variations for A/B testing research

### Frontend Service Integration
- **ApiService Class**: Centralized HTTP client with TypeScript interfaces
- **useNews() Hook**: State management for articles, categories, filtering
- **Dynamic Components**: Category colors/emojis from database API, not hardcoded

### Category System (8 Standardized)
```
science tech (🔬), health (🩺), environment (🌱), social progress (✊)
education (🎓), human kindness (💖), diplomacy (🕊️), culture (🎭)
```

## Current Status & Technical Debt

### Working Features ✅
- Complete frontend-backend integration with real data
- M49 flag emoji display via database JOIN
- Geographic search filtering (client-side)
- Dynamic category system with database-driven colors
- Memory-optimized Next.js configuration

### Known Issues ⚠️
- **M49 Accuracy**: Gemini returns wrong codes (Indonesia→Australia, Vietnam→Bulgaria)
- **Client-Side Filtering**: Geographic search requires all articles loaded
- **Memory Management**: Development requires Next.js optimization
- **Backend Filtering**: Server-side category/impact filtering not implemented

### Architecture Ready For 🔄
- Background collection service for continuous news gathering
- Backend filtering implementation to replace client-side logic
- Geographic autocomplete with location suggestions
- Production database migration (SQLite → PostgreSQL)

---
*Architecture version: 0.12.0*