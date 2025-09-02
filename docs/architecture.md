# HopeShot Architecture

## Project Overview
HopeShot is a learning-first project with simple, modular components designed for easy understanding and extension. The system aggregates positive news from multiple sources using AI-powered sentiment analysis via Google Gemini API with multi-prompt A/B testing capabilities, logging comprehensive comparative data to Google Sheets for research and storing normalized application data in SQLite database with direct M49 code integration for hierarchical geographic filtering.

## Technology Stack
- **Frontend**: Next.js (React framework) with TypeScript and Tailwind CSS v4
- **Backend**: FastAPI (Python web framework) with Uvicorn ASGI server
- **Database**: SQLite with normalized schema and M49-based location junction tables
- **Authentication**: OAuth2 password grant (AFP), API key authentication (NewsAPI, NewsData), Service account (Google Sheets)
- **HTTP Client**: aiohttp for concurrent async requests
- **AI/ML**: Google Gemini 2.5 Flash-Lite with multi-prompt A/B testing framework
- **Configuration**: YAML-based prompt and source management for easy experimentation
- **Data Storage**: Dual strategy - SQLite for application data, Google Sheets for A/B testing research
- **UI System**: Custom Sky & Growth color palette with CSS variables
- **Geographic Standard**: UN M49 codes for location identification and hierarchical filtering
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
│   ├── setup.md                   # Installation and setup guide
│   └── parameters_reference.md    # TypeScript interfaces and parameter guide
├── frontend/                      # Next.js application
│   ├── services/                  # API service layer
│   │   └── api.ts                 # Centralized backend communication
│   ├── hooks/                     # Custom React hooks
│   │   └── useNews.ts             # News data management and filtering
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx           # Homepage with hero + top 3 articles
│   │   │   ├── explore/page.tsx   # News feed with real API integration
│   │   │   ├── test-cards/page.tsx # Component testing interface
│   │   │   └── globals.css        # Sky & Growth color palette + Tailwind
│   │   └── components/
│   │       └── VerticalNewsCard.tsx # Article card with dynamic category integration
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
│       ├── sheets_service.py      # Google Sheets integration with A/B tracking
│       └── database_service.py    # SQLite operations with M49 junction table support
└── scripts/                       # Utility scripts (empty)
```

## Enhanced Data Architecture with M49 Integration

### Database Schema (SQLite - Application Data)
```
articles (37 columns):
- Basic data: id, title, description, url_id, author, published_at, language, news_type, source_type
- Sentiment: uplift_score, sentiment_positive/negative/neutral, sentiment_confidence
- Emotions: hope, awe, gratitude, compassion, relief, joy (0.0-1.0 scores)
- Analysis: source_credibility, fact_checkable_claims, evidence_quality, controversy_level
- Geographic: geographical_impact_level (Global/Regional/National/Local only)
- A/B Testing: prompt_id, prompt_name
- Reserved: 3 columns for future expansion

categories:
- id, name, filter_name, emoji, description, color, accent, created_at

locations (M49 enhanced):
- id, name, m49_code, hierarchy_level (1-5), impact_level, parent_id, parent_m49_code
- iso_alpha2, iso_alpha3, emoji, aliases, created_at

article_categories (many-to-many):
- article_id, category_id

article_locations (M49 direct storage):
- article_id, m49_code
```

### M49 Geographic System
```
Direct M49 code storage with hierarchical relationships:
- World (001, level 1) → Asia (142, level 2) → Southeast Asia (035, level 3) → Vietnam (704, level 5)
- Junction table stores M49 codes directly from Gemini analysis
- Location names populated via JOIN queries for API responses
- Supports complex filtering: "Asia" filter includes all Asian countries and regions
```

### Standardized Category System
```
8 categories with clean naming and visual identity:
- science tech (🔬) - breakthroughs, inventions, space, AI, research, discoveries
- health (🩺) - medical progress, wellbeing, mental health, public health improvements  
- environment (🌱) - climate action, conservation, renewable energy, biodiversity recovery
- social progress (✊) - equality, inclusion, policy changes, social justice improvements
- education (🎓) - access to learning, teaching methods, scholarships, edtech
- human kindness (💖) - acts of generosity, rescues, donations, everyday hero stories
- diplomacy (🕊️) - peace agreements, negotiations, conflict resolution, cooperation between nations
- culture (🎭) - arts, heritage, creativity, festivals, inspiring cultural projects
```

### Data Pipeline Flow with M49 Integration
```
News APIs → Multi-Source Aggregation → Multi-Prompt Gemini Analysis → M49 Processing → Dual Storage
     ↓                ↓                          ↓                       ↓                ↓
NewsAPI        Deduplication         All Active Prompts          M49 Code Storage    SQLite (First Prompt)
NewsData   →   Priority Sort     →   Geographic Processing   →   Direct Junction   + GSheets (All Prompts)
AFP            Cross-Source          M49 Validation             Table Storage        A/B Testing Research
```

## Frontend Architecture

### Service Layer
- **ApiService**: Centralized backend communication with TypeScript interfaces and error handling
- **useNews() Hook**: Custom React hook managing articles, categories, filtering state, and API integration
- **Transformers**: Utility functions for data normalization, filtering, and sorting

### Component System
- **VerticalNewsCard**: Primary article display with dynamic category colors from API and impact level chips
- **HorizontalHighlightCard**: Featured article component for homepage with rank badges and category illustrations
- **ExplorePage**: News feed with real API integration, dynamic filtering, and responsive grid layout
- **HomePage**: Hero section with call-to-action and top 3 articles from database

### Design System
- **Sky & Growth Palette**: Custom color system with CSS variables for consistent branding
- **Dynamic Category Colors**: Each category has unique background, text, and accent colors from database
- **Impact Mapping**: Visual indicators for Global (🌍), Regional (🗺️), Local (📍) impact levels
- **Responsive Grid**: 1 column mobile, 2 columns tablet, 3 columns desktop

### State Management
- **Custom Hooks**: useNews() for data fetching, filtering, and error states
- **Real-time Filtering**: Interactive category and impact level selection with client-side filtering
- **API Integration**: Dynamic categories from database, articles from news endpoints with location data

## Service Architecture

### News Service Layer
- **NewsService**: Multi-source orchestrator with YAML-based configuration and priority system
- **BaseNewsClient**: Abstract base providing shared functionality for all clients
- **Client Implementations**: 
  - **NewsAPIClient**: Mainstream news sources with positive keyword filtering
  - **NewsDataClient**: Alternative/international sources with category filtering
  - **AFPClient**: Professional journalism with OAuth2 authentication

### Enhanced Analysis Layer with Direct M49 Integration
- **GeminiService**: Complete AI analysis service with YAML-based A/B testing framework and direct M49 code processing
- **YAML Configuration System**: `prompts.yaml` for easy prompt experimentation without code changes
- **Multi-Prompt Processing**: Each article analyzed by ALL active prompts for direct comparison
- **M49 Processing**: Direct storage of UN standard geographic codes without ID conversion
- **Conservative Rate Limiting**: Maintains API safety while processing multiple prompt variations

### Dual Storage Layer
- **DatabaseService**: SQLite operations with M49 junction table support and location name lookup
- **SheetsService**: Google Sheets integration with service account authentication and A/B testing metadata
- **Storage Strategy**: First prompt results to database (clean application data), all prompts to sheets (research data)
- **M49 Integration**: Direct code storage in junction tables with JOIN-based name resolution

## Design Patterns

### Architectural Patterns
- **Service-Oriented Architecture**: Clean separation between news, analysis, storage, and frontend services
- **Template Method**: BaseNewsClient defines common interface, clients implement specifics
- **Circuit Breaker**: Failed services don't impact others (graceful degradation)
- **M49 Direct Storage Pattern**: Junction tables store UN standard codes without ID conversion
- **Auto-Creation Pattern**: System grows organically as new data discovered
- **Dual Storage Pattern**: Different storage strategies for different use cases

### Database Patterns
- **Normalized Design**: Proper foreign keys and junction tables for data integrity
- **M49 Standard Integration**: UN geographic codes for unambiguous location identification
- **Direct Code Storage**: M49 codes stored without conversion overhead
- **Junction Table Optimization**: Many-to-many relationships with performance indexes
- **Hierarchical Querying**: Recursive queries for geographic filtering

### Frontend Patterns
- **Custom Hook Pattern**: useNews() encapsulates data fetching and state management
- **Service Layer Pattern**: API service centralized with TypeScript interfaces
- **Component Composition**: Reusable cards with props-driven customization
- **Dynamic Styling**: Category colors and styling from API data instead of hardcoded mappings

## API Architecture

### Core Endpoints with M49 Integration
- **GET /api/news** - Unified aggregation with multi-prompt analysis, M49 location processing, dual storage
- **GET /api/categories** - Dynamic category metadata for frontend filtering with visual identity
- **GET /api/sources** - Source configuration with database statistics including M49 relationships
- **GET /api/sources/test** - Health check for all services including M49 database connectivity
- **GET /health** - Comprehensive system health with M49 integration status

### Enhanced Response Structure with M49 Integration
```json
{
  "status": "success",
  "gemini_analyzed": true,
  "prompt_versions": ["v1_comprehensive"],
  "database_inserted": 2,
  "sheets_logged": true,
  "articles": [
    {
      "title": "Article Title",
      "gemini_analysis": {
        "categories": ["science tech", "health"],
        "geographical_impact_level": "Global",
        "geographical_impact_m49_codes": [840, 392],
        "geographical_impact_location_names": ["United States", "Japan"],
        "overall_hopefulness": 0.7
      }
    }
  ]
}
```

### M49 Geographic Integration
```json
{
  "categories": [
    {
      "id": 1,
      "name": "science tech",
      "filter_name": "Science & Tech", 
      "emoji": "🔬",
      "color": "#E6FBFF",
      "accent": "#00A7C4"
    }
  ]
}
```

## Database Architecture Details

### M49 Junction Table Relationships
```sql
-- Articles linked to M49 codes directly
SELECT a.title, l.name, l.m49_code, l.hierarchy_level
FROM articles a 
JOIN article_locations al ON a.id = al.article_id
JOIN locations l ON al.m49_code = l.m49_code;

-- Hierarchical filtering: Asia includes all Asian countries
WITH RECURSIVE asia_hierarchy AS (
  SELECT id, name, m49_code, parent_id FROM locations WHERE m49_code = 142
  UNION ALL
  SELECT l.id, l.name, l.m49_code, l.parent_id
  FROM locations l
  JOIN asia_hierarchy ah ON l.parent_id = ah.id
)
SELECT DISTINCT a.title
FROM articles a
JOIN article_locations al ON a.id = al.article_id
JOIN asia_hierarchy ah ON al.m49_code = ah.m49_code;
```

### Direct M49 Storage Logic
```
1. Gemini Analysis Returns: 
   geographical_impact_location: ["840", "392"]  (M49 codes as strings)

2. GeminiService Processing:
   - Convert strings to integers: [840, 392]
   - Store in geographical_impact_m49_codes array
   - Look up location names: ["United States", "Japan"]

3. DatabaseService Storage:
   - Insert article into articles table (no M49 columns)
   - Insert into article_locations: (article_id=1, m49_code=840), (article_id=1, m49_code=392)

4. API Response:
   - JOIN article_locations with locations on m49_code
   - Return location names for display
```

## Frontend Service Architecture

### API Service Layer
- **ApiService Class**: Centralized HTTP client with TypeScript interfaces for all backend communication
- **Error Handling**: Consistent error patterns with logging and user-friendly messages
- **Type Safety**: Complete TypeScript interfaces matching backend response structures
- **Request Management**: Base URL configuration and request wrapper methods

### Custom Hook System
- **useNews()**: Manages articles, categories, loading states, and filtering logic
- **State Management**: Centralized state for selections, loading, and error handling
- **Filter Logic**: Client-side filtering by categories and impact levels
- **API Integration**: Automatic data fetching with refresh capabilities

### Component Architecture
- **Dynamic Category Integration**: Components receive category data as props instead of hardcoded mappings
- **Type-Safe Props**: All components use TypeScript interfaces for props validation
- **Modular Design**: Clean separation between data fetching, state management, and UI rendering
- **Reusable Components**: Cards work with any article data structure

## Development Approach
1. **Documentation First** - Always document before coding
2. **Modular Architecture** - Service layer separation enables independent updates
3. **Type Safety** - TypeScript interfaces prevent runtime errors and improve maintainability
4. **Real Data Integration** - Replace mock data with actual API connections
5. **Configuration-Driven Behavior** - YAML-based experimentation without code changes
6. **M49 Standard Compliance** - UN geographic codes for international compatibility

## Current Status (v0.11.0)
- ✅ Complete frontend-backend integration with real article data
- ✅ Dynamic category system with database-driven emoji and color display
- ✅ M49-based location storage with direct junction table architecture
- ✅ Modular service layer with TypeScript interfaces and error handling
- ✅ Working API integration with loading states and error boundaries
- ✅ Client-side filtering with real category data from backend
- ⚠️ M49 code accuracy issues in Gemini responses (Indonesia→Australia, Vietnam→Bulgaria)
- ⚠️ Location name lookup failures when M49 codes missing from database
- 📋 Backend filtering not implemented (frontend does client-side filtering)

## Technical Debt
- **Gemini M49 accuracy**: AI returns incorrect country codes requiring prompt refinement or validation
- **Incomplete M49 database**: Missing codes cause location name lookup failures
- **Client-side filtering**: Backend doesn't support category/impact filtering yet
- **Navigation system missing**: No header/menu to move between pages
- **Foreign key constraints disabled**: Simplified migration removed referential integrity
- **Error handling gaps**: Limited error states for M49 lookup failures

## Scaling Considerations with M49 Integration
- **Geographic Performance**: M49 codes enable efficient hierarchical queries
- **Database Joins**: Direct M49 storage eliminates lookup overhead during insertion
- **API Response Efficiency**: Location names populated via single JOIN query
- **Frontend Caching**: Categories and locations suitable for client-side caching
- **International Compatibility**: UN M49 standard supports global content expansion

## M49 Geographic Integration Details

### M49 Code Processing Flow
```
Gemini Response: "geographical_impact_location": ["840", "392"]
    ↓
GeminiService Processing:
1. Parse strings to integers: [840, 392]
2. Store in analysis: geographical_impact_m49_codes: [840, 392]
3. Database lookup: ["United States", "Japan"]
4. Store in analysis: geographical_impact_location_names: ["United States", "Japan"]
    ↓
DatabaseService Storage:
- articles table: NO M49 columns (clean separation)
- article_locations: (article_id=1, m49_code=840), (article_id=1, m49_code=392)
    ↓
API Response:
- JOIN query populates location names for display
- Frontend receives: geographical_impact_location_names: ["United States", "Japan"]
```

### Hierarchical Query Capability
```
-- User filters by "Asia" in frontend
1. Find Asia: m49_code = 142, hierarchy_level = 2
2. Recursive query: Find all locations with parent relationships to Asia
3. Result: Vietnam (704), Japan (392), China (156), etc.
4. Article query: Return articles with ANY of these M49 codes in article_locations
```

## Known Issues & Quality Control

### Current M49 Integration Issues
- **Gemini Accuracy**: Returns wrong M49 codes (Indonesia→36 instead of 360, Vietnam→100 instead of 704)
- **Database Coverage**: Not all M49 codes exist in locations table causing lookup failures
- **Validation Gap**: No middleware to catch obviously incorrect codes before storage
- **Prompt Clarity**: Geographic instructions need specific M49 examples for better accuracy

### Data Quality Control Needs
- **M49 Validation Layer**: Check codes against known ranges before database storage
- **Location Database Completeness**: Import full UN M49 reference data
- **Gemini Prompt Enhancement**: Add correct M49 examples and validation instructions
- **Error Recovery**: Fallback mechanisms when location names can't be resolved

## Performance Optimizations

### Database Performance
- **M49 Indexes**: Direct indexing on m49_code for fast hierarchical queries
- **Junction Table Performance**: Composite indexes on (article_id, m49_code)
- **No ID Conversion Overhead**: Direct M49 storage eliminates lookup operations
- **Optimized JOIN Queries**: Single query populates all location names for API responses

### Frontend Performance
- **Service Layer Caching**: API service can cache category metadata
- **Component Optimization**: Dynamic category lookup with fallback handling
- **Client-Side Filtering**: Immediate response for filter interactions
- **Lazy Loading Ready**: Architecture supports pagination and infinite scroll

---
*Last updated: September 1, 2025*
*Architecture version: 0.11.0*


# HopeShot Architecture (Updated v0.12.0)

## Current Status (v0.12.0)
- ✅ Complete frontend-backend integration with real article data and geographic emoji display
- ✅ M49-based location emoji system with database JOIN lookup for flag display
- ✅ Geographic search filtering with case-insensitive location name matching
- ✅ Enhanced article card layout with consistent bottom-aligned footer and reorganized content hierarchy
- ✅ Memory-optimized Next.js configuration preventing development server crashes
- ✅ Dynamic category system with database-driven emoji and color display
- ⚠️ Client-side geographic filtering (backend filtering not implemented yet)
- ⚠️ Fresh API calls on page refresh instead of accumulated database articles
- 📋 Background collection service needed for continuous news gathering

## Enhanced Data Architecture with Geographic Display (Updated)

### Database Schema Enhancement (v0.12.0)
```
locations table (M49 enhanced):
- id, name, m49_code, hierarchy_level (1-5), impact_level, parent_id, parent_m49_code
- iso_alpha2, iso_alpha3, emoji, aliases, created_at
- emoji field: Contains flag emojis (🇺🇸, 🇹🇷) for visual display

article_locations (M49 direct storage):
- article_id, m49_code
- Direct M49 code storage enables efficient emoji lookup via JOIN
```

### Geographic Display Data Flow (NEW)
```
API Request → Database Query → M49 JOIN → Emoji Population → Frontend Display
     ↓              ↓               ↓             ↓              ↓
/api/news    article_locations   locations    name + emoji    Flag emojis in cards
             Junction table      table JOIN   arrays returned  🇹🇷 🇺🇸 display
```

## Frontend Architecture Updates (v0.12.0)

### Enhanced Component System
- **VerticalNewsCard**: Redesigned layout with M49 flag emoji display, consistent footer alignment, placeholder emoji for missing categories
- **Geographic Search Integration**: Real-time filtering by location name with search bar positioned right of impact level buttons
- **Memory-Optimized Configuration**: Next.js webpack settings preventing development crashes
- **Layout Optimization**: Flexbox architecture ensuring footer alignment regardless of content length

### Enhanced Service Layer (Updated)
- **useNews() Hook**: Added geographic search state management and enhanced filtering logic
- **Geographic Filtering**: Client-side search matching geographical_impact_location_names arrays
- **Interface Standardization**: Shared TypeScript interfaces across components preventing type conflicts

### Design System Updates (v0.12.0)
- **Geographic Display Pattern**: M49 flag emojis in grey background chips replacing redundant impact level display
- **Content Hierarchy**: Geography section (flags + categories) → Title → Description → Footer
- **Placeholder System**: 📰 emoji for articles without categories via getCategoryData fallback
- **Responsive Layout**: Consistent card height and footer alignment across all screen sizes

## Enhanced Geographic Integration (v0.12.0)

### M49 Emoji Display System (NEW)
```
Database Query Flow:
1. Article has M49 codes: [792, 840] (Turkey, USA)
2. JOIN locations table: SELECT name, emoji WHERE m49_code IN (792, 840)
3. Returns: names=["Türkiye", "United States"], emojis=["🇹🇷", "🇺🇸"]
4. Frontend displays: Flag emojis in grey background with location name tooltips
```

### Geographic Search Architecture
```
User Input: "turkey" → Filter Logic → Location Name Matching → Filtered Results
     ↓               ↓                     ↓                      ↓
Search bar     Case-insensitive     "Türkiye".includes("turkey")   Articles displayed
input          toLowerCase()        location name matching          matching search
```

## Service Architecture Updates (v0.12.0)

### Enhanced Database Service Layer
- **get_location_names_and_emojis_by_m49()**: Dual data lookup function returning both names and emojis via single query
- **Memory-Efficient Queries**: Single JOIN query fetches all required location display data
- **Fallback Handling**: Default emoji (🌍) when database emoji field is null

### Frontend Service Integration
- **Geographic State Management**: geographicSearch state integrated with existing filter architecture
- **Enhanced Filtering Logic**: Triple filter combination (category + impact + geographic) with client-side processing
- **Interface Consistency**: Shared TypeScript interfaces prevent component type mismatches

## Technical Architecture Patterns (Updated)

### Geographic Display Patterns (NEW)
- **Database-Driven Emoji Display**: Flag emojis sourced from database instead of hardcoded mappings
- **M49 JOIN Optimization**: Single query retrieves both location names and emojis efficiently
- **Component Interface Sharing**: TypeScript interfaces imported from services/api.ts across all components
- **Flexible Content Layout**: Flexbox architecture adapts to variable content while maintaining footer alignment

### Memory Management Patterns (NEW)
- **Next.js Optimization**: Webpack configuration reducing parallel processing and memory allocation
- **Development Workflow**: Cache clearing and memory allocation strategies for sustainable frontend development
- **Resource Monitoring**: Configuration settings preventing Node.js memory crashes during component iteration

## Development Environment Architecture (Updated v0.12.0)

### Frontend Development Optimization
```
Memory Management Workflow:
1. Clear Next.js cache before sessions
2. Set Node.js memory allocation to 2048MB
3. Use optimized webpack configuration
4. Monitor resource usage during development
```

### Geographic Development Patterns
```
Component Development Flow:
1. Backend provides M49 codes and location data
2. Database JOIN populates emoji fields via API
3. Frontend components consume enhanced data structure
4. TypeScript interfaces ensure type safety across layers
```

## Performance Optimizations (Updated)

### Geographic Display Performance (NEW)
- **Single Query Efficiency**: Combined name and emoji lookup eliminates multiple database calls
- **Client-Side Search**: Immediate geographic filtering response without backend roundtrips
- **M49 Index Performance**: Direct M49 code indexing enables fast location emoji lookup
- **Component Rendering**: Optimized card layout prevents layout thrashing with consistent dimensions

### Development Environment Performance (NEW)
- **Memory Usage Reduction**: Next.js configuration reduces development server resource consumption by ~60%
- **Cache Management**: Automated cache clearing prevents memory accumulation during development sessions
- **Build Optimization**: Webpack settings eliminate unnecessary parallel processing overhead

## Known Technical Debt (Updated v0.12.0)

### Geographic System Limitations
- **Client-Side Filtering**: Geographic search processed in frontend requiring all articles loaded
- **Search Precision**: Basic substring matching without fuzzy search or location suggestions
- **No Search Validation**: Accepts any search term without geographic context verification
- **Backend Filtering Gap**: Server-side geographic filtering not implemented yet

### Memory Management Requirements
- **Configuration Dependency**: Next.js optimization required for stable development environment
- **Manual Cache Management**: Developers must clear cache manually to prevent memory issues
- **Resource Monitoring**: Development requires attention to system resource usage

### Interface Management Complexity
- **Shared Interface Coordination**: Changes to GeminiAnalysis interface require updates across multiple files
- **Type Safety Overhead**: Enhanced TypeScript interfaces increase import complexity
- **Component Interface Dependencies**: VerticalNewsCard depends on shared interfaces from api.ts