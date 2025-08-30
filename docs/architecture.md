# HopeShot Architecture

## Project Overview
HopeShot is a learning-first project with simple, modular components designed for easy understanding and extension. The system aggregates positive news from multiple sources using AI-powered sentiment analysis via Google Gemini API with multi-prompt A/B testing capabilities, logging comprehensive comparative data to Google Sheets for research and storing normalized application data in SQLite database with auto-creation of categories and geographic hierarchies.

## Technology Stack
- **Frontend**: Next.js (React framework) with TypeScript and Tailwind CSS
- **Backend**: FastAPI (Python web framework) with Uvicorn ASGI server
- **Database**: SQLite with normalized schema and junction tables for relationships
- **Authentication**: OAuth2 password grant (AFP), API key authentication (NewsAPI, NewsData), Service account (Google Sheets)
- **HTTP Client**: aiohttp for concurrent async requests
- **AI/ML**: Google Gemini 2.5 Flash-Lite with multi-prompt A/B testing framework
- **Configuration**: YAML-based prompt and source management for easy experimentation
- **Data Storage**: Dual strategy - SQLite for application data, Google Sheets for A/B testing research
- **Version Control**: Git + GitHub

## Project Structure
```
hopeshot/
├── README.md                      # Project overview
├── CHANGELOG.md                   # Version history  
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
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
│   ├── main.py                    # FastAPI application with dual storage endpoints
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # API keys and configuration (gitignored)
│   ├── prompts.yaml               # A/B testing prompt configurations
│   ├── sources.yaml               # News source configuration with ethical limits
│   ├── hopeshot_news.db          # SQLite database (gitignored)
│   ├── gsheetapi_credentials.json # Google Sheets service account (gitignored)
│   ├── database_setup.py          # SQLite schema creation script
│   ├── database_migration.py      # Schema migration utilities
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
│       ├── gemini_service.py      # Multi-prompt analysis with geographic auto-creation
│       ├── sheets_service.py      # Google Sheets integration with A/B tracking
│       └── database_service.py    # SQLite operations with junction table support
└── scripts/                       # Utility scripts (empty)
```

## Enhanced Data Architecture with Dual Storage

### Database Schema (SQLite - Application Data)
```
articles (40 columns):
- Basic data: id, title, description, url_id, author, published_at, language, news_type, source_type
- Sentiment: uplift_score, sentiment_positive/negative/neutral, sentiment_confidence
- Emotions: hope, awe, gratitude, compassion, relief, joy (0.0-1.0 scores)
- Analysis: source_credibility, fact_checkable_claims, evidence_quality, controversy_level
- Geographic: geographical_impact_level (Global/Regional/National/Local)
- A/B Testing: prompt_id, prompt_name
- Reserved: 3 columns for future expansion

categories:
- id, name, description, color, emoji, created_at

locations (hierarchical):
- id, name, level (country/region/continent), parent_id, created_at

article_categories (many-to-many):
- article_id, category_id

article_locations (many-to-many):
- article_id, location_id
```

### Data Pipeline Flow with Dual Storage
```
News APIs → Multi-Source Aggregation → Multi-Prompt Gemini Analysis → Dual Storage
     ↓                ↓                          ↓                         ↓
NewsAPI        Deduplication         All Active Prompts          SQLite (First Prompt)
NewsData   →   Priority Sort     →   Geographic Processing   →   + GSheets (All Prompts)
AFP            Cross-Source          Auto-Creation Logic         A/B Testing Research
```

### Geographic Hierarchy Auto-Creation
```
Gemini Response: "geographical_impact_location": ["Vietnam", "Japan"]
    ↓
System Processing:
1. Vietnam → Create: Vietnam (country) → Southeast Asia (region) → Asia (continent)
2. Japan → Create: Japan (country) → East Asia (region) → Asia (continent)
    ↓
Database Storage:
- locations table: Vietnam (id=5), Japan (id=6), Southeast Asia (id=2), etc.
- article_locations: article_id=1, location_id=5 AND article_id=1, location_id=6
    ↓
Query Capability:
- "Articles about Vietnam": Direct match
- "Articles about Japan": Direct match  
- "Articles about Asia": Includes both Vietnam and Japan articles via hierarchy
```

## Service Architecture

### News Service Layer
- **NewsService**: Multi-source orchestrator with YAML-based configuration and priority system
- **BaseNewsClient**: Abstract base providing shared functionality for all clients
- **Client Implementations**: 
  - **NewsAPIClient**: Mainstream news sources with positive keyword filtering
  - **NewsDataClient**: Alternative/international sources with category filtering
  - **AFPClient**: Professional journalism with OAuth2 authentication (inspiring filter removed)

### Enhanced Analysis Layer with Auto-Creation
- **GeminiService**: Complete AI analysis service with YAML-based A/B testing framework and geographic auto-creation
- **YAML Configuration System**: `prompts.yaml` for easy prompt experimentation without code changes
- **Multi-Prompt Processing**: Each article analyzed by ALL active prompts for direct comparison
- **Geographic Processing**: Auto-creates location hierarchies and converts names to database IDs
- **Conservative Rate Limiting**: Maintains API safety while processing multiple prompt variations

### Dual Storage Layer
- **DatabaseService**: SQLite operations with junction table support and auto-creation logic
- **SheetsService**: Google Sheets integration with service account authentication and A/B testing metadata
- **Storage Strategy**: First prompt results to database (clean application data), all prompts to sheets (research data)
- **Connection Management**: Reused connections prevent database locks during bulk operations

## Design Patterns

### Architectural Patterns
- **Service-Oriented Architecture**: Clean separation between news, analysis, and storage services
- **Template Method**: BaseNewsClient defines common interface, clients implement specifics
- **Circuit Breaker**: Failed services don't impact others (graceful degradation)
- **Junction Table Pattern**: Many-to-many relationships for categories and locations
- **Auto-Creation Pattern**: System grows organically as new data discovered
- **Dual Storage Pattern**: Different storage strategies for different use cases

### Database Patterns
- **Normalized Design**: Proper foreign keys and junction tables for data integrity
- **Hierarchical Data**: Parent-child relationships for geographic data with recursive queries
- **Auto-Creation Logic**: Dynamic schema population as content discovered
- **Connection Reuse**: Prevents database locks during bulk operations
- **Junction Tables**: Many-to-many relationships for complex article categorization

### A/B Testing Patterns
- **Configuration-Driven Experimentation**: YAML-based prompt management without deployment
- **Comparative Data Collection**: Multiple analysis results per article for systematic evaluation
- **Template-Based Content Generation**: Dynamic prompt creation with variable substitution
- **Dual Storage Research**: All prompts to sheets, best prompt to database

## API Architecture

### Core Endpoints with Dual Storage
- **GET /api/news** - Unified aggregation with multi-prompt analysis, dual storage (database + sheets)
- **GET /api/sources** - Source configuration with database statistics
- **GET /api/sources/test** - Health check for all services including database connectivity
- **GET /api/news/afp** - Direct AFP testing endpoint
- **GET /health** - Comprehensive system health with database and A/B testing status

### Enhanced Response Structure with Database Integration
```json
{
  "status": "success",
  "gemini_analyzed": true,
  "prompt_versions": ["v1_comprehensive", "v2_precision", "v3_empathy_depth"],
  "database_inserted": 2,
  "sheets_logged": true,
  "total_logged": 6,
  "duplicate_count": 0,
  "gemini_stats": {
    "total_tokens_used": 3429,
    "total_batches_processed": 1,
    "prompt_versions_count": 3,
    "total_analyses": 6
  }
}
```

### Authentication Systems
- **NewsAPI**: Simple API key authentication
- **NewsData**: API key with query parameters
- **AFP**: OAuth2 password grant with automatic token management (5-hour expiry)
- **Google Sheets**: Service account with JSON credentials file
- **Gemini**: API key authentication with comprehensive rate limiting for multi-prompt processing
- **SQLite**: Local file-based database with connection pooling

## Database Architecture Details

### Junction Table Relationships
```sql
-- Articles can have multiple categories
SELECT a.title, c.name as category
FROM articles a 
JOIN article_categories ac ON a.id = ac.article_id
JOIN categories c ON ac.category_id = c.id;

-- Articles can reference multiple locations
SELECT a.title, l.name as location, l.level
FROM articles a
JOIN article_locations al ON a.id = al.article_id  
JOIN locations l ON al.location_id = l.id;

-- Geographic hierarchy queries
SELECT child.name as country, parent.name as region, grandparent.name as continent
FROM locations child
LEFT JOIN locations parent ON child.parent_id = parent.id
LEFT JOIN locations grandparent ON parent.parent_id = grandparent.id
WHERE child.level = 'country';
```

### Auto-Creation Logic Flow
```
1. Gemini Analysis Returns: 
   categories: ["social", "human rights"]
   geographical_impact_location: ["USA", "Japan"]

2. Category Auto-Creation:
   - Check if "social" exists → Create if not
   - Check if "human rights" exists → Create if not
   - Link article to both categories via junction table

3. Location Auto-Creation:
   - USA → North America → Americas (create full hierarchy)
   - Japan → East Asia → Asia (create full hierarchy)
   - Link article to both countries via junction table

4. Result:
   - Article appears in "social" and "human rights" category filters
   - Article appears in "USA", "Japan", "North America", "East Asia", "Americas", "Asia" location filters
```

## Development Approach
1. **Documentation First** - Always document before coding
2. **Small Steps** - One feature at a time with testing
3. **Modular Design** - Each component has single responsibility
4. **Learning Focus** - Code optimized for understanding
5. **Data-Driven Experimentation** - A/B testing framework for systematic improvement
6. **Configuration-Driven Behavior** - YAML-based experimentation without code changes
7. **Database-Driven Architecture** - Normalized data with proper relationships

## Current Status (v0.9.0)
- ✅ Complete SQLite database integration with normalized schema and auto-creation
- ✅ Multi-location junction table architecture supporting complex geographic relationships
- ✅ Dual storage pipeline (SQLite for app data, Sheets for A/B testing research)
- ✅ Multi-prompt A/B testing framework with YAML configuration
- ✅ Geographic hierarchy auto-generation with parent-child relationships
- ✅ Category auto-creation with many-to-many article relationships
- ✅ Connection management preventing database locks during bulk operations
- 🔄 Multi-source news aggregation (AFP active, NewsAPI/NewsData configurable)
- 📋 Prompt optimization needed for better category classification and geographic accuracy

## Technical Debt
- **Geographic inference**: Simple country-to-region mapping needs external API integration
- **Connection management**: Could use connection pooling for production scale
- **Schema evolution**: Backward compatibility approach keeps old columns
- **Error handling**: Enhanced logging needed for production debugging
- **Prompt quality**: Category classification needs refinement for accuracy

## Scaling Considerations with Database Integration
- **Database Performance**: SQLite suitable for single-user applications, PostgreSQL for production
- **Multi-Location Processing**: Junction table queries optimized with indexes
- **Auto-Creation Overhead**: Minimal impact due to efficient existence checking
- **A/B Testing Scale**: 3x analysis time acceptable for research phase
- **Storage Strategy**: Database for application queries, sheets for research analysis

## Geographic Hierarchy System

### Country-to-Region Inference Mapping
```python
country_to_region = {
    'Vietnam': 'Southeast Asia',
    'United States': 'North America',
    'USA': 'North America', 
    'France': 'Europe',
    'Germany': 'Europe',
    'Japan': 'East Asia',
    'China': 'East Asia',
    'Brazil': 'South America',
    'Nigeria': 'Africa',
    'Australia': 'Oceania',
    'India': 'South Asia',
    'Canada': 'North America'
}

region_to_continent = {
    'Southeast Asia': 'Asia',
    'East Asia': 'Asia',
    'South Asia': 'Asia',
    'North America': 'Americas',
    'South America': 'Americas',
    'Europe': 'Europe',
    'Africa': 'Africa',
    'Oceania': 'Oceania'
}
```

### Query Capabilities
- **Country-specific**: "Show articles about Vietnam"
- **Regional**: "Show articles about Southeast Asia" (includes Vietnam, Thailand, etc.)
- **Continental**: "Show articles about Asia" (includes all Asian countries)
- **Multi-country stories**: USA-Japan collaboration appears in both country filters

## Known Issues & Improvement Areas

### Immediate Issues (Identified in Testing)
- **Scoring inconsistencies**: Different results when analyzing 1 article vs 20 articles with same prompt
- **Category classification accuracy**: Sports articles incorrectly classified as "social, human rights"
- **Geographic response quality**: Mixed specificity (e.g., "Africa, Madagascar, Morocco" instead of just countries)
- **Duplicate detection**: Same articles sent repeatedly to Gemini (good for testing, needs fixing for production)
- **Timestamp handling**: Currently uses published_at instead of creation timestamp

### Prompt Optimization Needs
- **Category refinement**: Improve classification accuracy for sports, politics, health content
- **Geographic specificity**: Ensure responses contain only countries with proper region assignment
- **Score calibration**: Address inconsistencies between single and batch analysis
- **Template standardization**: Ensure consistent prompt formatting across all versions

### Production Readiness Improvements
- **Database connection pooling**: For concurrent user support
- **External geographic API**: Replace inference mapping with authoritative data
- **Advanced duplicate detection**: Fuzzy matching beyond URL and title similarity
- **Error monitoring**: Comprehensive logging for production debugging
- **Performance monitoring**: Query optimization and response time tracking

---
*Last updated: August 29, 2025*
*Architecture version: 0.9.0*