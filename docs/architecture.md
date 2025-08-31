# HopeShot Architecture

## Project Overview
HopeShot is a learning-first project with simple, modular components designed for easy understanding and extension. The system aggregates positive news from multiple sources using AI-powered sentiment analysis via Google Gemini API with multi-prompt A/B testing capabilities, logging comprehensive comparative data to Google Sheets for research and storing normalized application data in SQLite database with auto-creation of categories and geographic hierarchies.

## Technology Stack
- **Frontend**: Next.js (React framework) with TypeScript and Tailwind CSS v4
- **Backend**: FastAPI (Python web framework) with Uvicorn ASGI server
- **Database**: SQLite with normalized schema and junction tables for relationships
- **Authentication**: OAuth2 password grant (AFP), API key authentication (NewsAPI, NewsData), Service account (Google Sheets)
- **HTTP Client**: aiohttp for concurrent async requests
- **AI/ML**: Google Gemini 2.5 Flash-Lite with multi-prompt A/B testing framework
- **Configuration**: YAML-based prompt and source management for easy experimentation
- **Data Storage**: Dual strategy - SQLite for application data, Google Sheets for A/B testing research
- **UI System**: Custom Sky & Growth color palette with CSS variables
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
│   │   │   ├── page.tsx           # Homepage with hero + top 3 articles
│   │   │   ├── explore/page.tsx   # News feed with dynamic filtering
│   │   │   ├── test-cards/page.tsx # Component testing interface
│   │   │   └── globals.css        # Sky & Growth color palette + Tailwind
│   │   └── components/
│   │       ├── VerticalNewsCard.tsx # Article card for explore grid
│   │       └── HorizontalHighlightCard.tsx # Featured article for homepage
│   ├── package.json               # Node.js dependencies
│   └── tailwind.config.js         # Tailwind configuration (unused in v4)
├── backend/
│   ├── main.py                    # FastAPI application with dual storage endpoints
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # API keys and configuration (gitignored)
│   ├── prompts.yaml               # A/B testing prompt configurations
│   ├── sources.yaml               # News source configuration with ethical limits
│   ├── hopeshot_news.db          # SQLite database (gitignored)
│   ├── gsheetapi_credentials.json # Google Sheets service account (gitignored)
│   ├── database_setup.py          # SQLite schema creation script
│   ├── database_migration.py      # Schema migration utilitiesy
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
- id, name, filter_name, emoji, description, color, accent, created_at

locations (hierarchical):
- id, name, level (country/region/continent), parent_id, created_at

article_categories (many-to-many):
- article_id, category_id

article_locations (many-to-many):
- article_id, location_id
```

### Standardized Category System
```
8 categories with clean naming and visual identity:
- science tech (🔬) - breakthroughs, inventions, space, AI, research, discoveries
- health (🩺) - medical progress, wellbeing, mental health, public health improvements  
- environment (🌱) - climate action, conservation, renewable energy, biodiversity recovery
- social progress (✊) - equality, inclusion, policy changes, social justice improvements
- education (📚) - access to learning, teaching methods, scholarships, edtech
- human kindness (🤝) - acts of generosity, rescues, donations, everyday hero stories
- diplomacy (🕊️) - peace agreements, negotiations, conflict resolution, cooperation between nations
- culture (🎨) - arts, heritage, creativity, festivals, inspiring cultural projects
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

## Frontend Architecture

### Component System
- **VerticalNewsCard**: Primary article display component with category colors, impact chips, and metadata
- **HorizontalHighlightCard**: Featured article component for homepage with rank badges and category illustrations
- **ExplorePage**: News feed with dynamic category filtering and responsive grid layout
- **HomePage**: Hero section with call-to-action and top 3 articles from last 7 days

### Design System
- **Sky & Growth Palette**: Custom color system with CSS variables for consistent branding
- **Category Colors**: Each category has unique background, text, and accent colors plus emoji
- **Impact Mapping**: Visual indicators for Global (🌍), Regional (🗺️), Local (📍) impact levels
- **Responsive Grid**: 1 column mobile, 2 columns tablet, 3 columns desktop

### State Management
- **React Hooks**: useState and useEffect for component state and API calls
- **Dynamic Filtering**: Interactive category and impact level selection with visual feedback
- **API Integration**: Fetch categories from database, articles from news endpoints

## Service Architecture

### News Service Layer
- **NewsService**: Multi-source orchestrator with YAML-based configuration and priority system
- **BaseNewsClient**: Abstract base providing shared functionality for all clients
- **Client Implementations**: 
  - **NewsAPIClient**: Mainstream news sources with positive keyword filtering
  - **NewsDataClient**: Alternative/international sources with category filtering
  - **AFPClient**: Professional journalism with OAuth2 authentication

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

### Enhanced Response Structure with Frontend Support
```json
{
  "status": "success",
  "categories": [
    {
      "id": 1,
      "name": "science tech",
      "filter_name": "Science & Tech", 
      "emoji": "🔬",
      "description": "breakthroughs, inventions, space, AI, research, discoveries",
      "color": "#E6FBFF",
      "accent": "#00A7C4"
    }
  ],
  "total": 8
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

## Current Status (v0.10.0)
- ✅ Complete frontend architecture with responsive design
- ✅ Dynamic category system with database integration
- ✅ Sky & Growth color palette implementation
- ✅ Component-based architecture with reusable cards
- ✅ Homepage with hero section and featured articles
- ✅ Explore page with interactive filtering UI
- ✅ Standardized 8-category system with visual identity
- 🔄 Mock data used for UI development (ready for API integration)
- 📋 Filter interactions implemented but not connected to backend queries

## Technical Debt
- **Mock data dependency**: Frontend components need real API integration
- **Filter functionality gap**: UI exists but doesn't query backend with selections
- **Navigation system missing**: No header/menu to move between pages
- **Error handling incomplete**: Limited error states for API failures
- **Loading states absent**: No spinners or skeleton screens during API calls
- **Category color duplication**: Color mapping repeated across components

## Scaling Considerations with Frontend Integration
- **Component Performance**: React rendering optimization for large article lists
- **API Response Caching**: Consider frontend caching for category metadata
- **Responsive Design**: Tested on mobile/tablet/desktop breakpoints
- **Accessibility**: Proper ARIA labels for screen readers, keyboard navigation
- **SEO Considerations**: Server-side rendering for article content

## User Experience Design
- **2010s Internet Aesthetic**: Clean, readable design with subtle gradients and clear typography
- **Ethical Attention Design**: No infinite scroll, clear pagination, time-spent awareness
- **Positive Focus**: Optimistic color palette, hopeful messaging, constructive content curation
- **Information Hierarchy**: Clear visual hierarchy with impact levels, categories, and metadata
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