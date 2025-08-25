# HopeShot Architecture

## Project Overview
HopeShot is a learning-first project with simple, modular components designed for easy understanding and extension. The system aggregates positive news from multiple sources using AI-powered sentiment analysis via Google Gemini API with multi-prompt A/B testing capabilities, logging comprehensive comparative data to Google Sheets for research and algorithm improvement.

## Technology Stack
- **Frontend**: Next.js (React framework) with TypeScript and Tailwind CSS
- **Backend**: FastAPI (Python web framework) with Uvicorn ASGI server
- **Authentication**: OAuth2 password grant (AFP), API key authentication (NewsAPI, NewsData), Service account (Google Sheets)
- **HTTP Client**: aiohttp for concurrent async requests
- **AI/ML**: Google Gemini 2.5 Flash-Lite with multi-prompt A/B testing framework
- **Configuration**: YAML-based prompt management for easy experimentation
- **Data Storage**: Google Sheets for real-time comparative data collection with 37-column rich schema
- **Version Control**: Git + GitHub

## Project Structure
```
hopeshot/
├── README.md                      # Project overview
├── CHANGELOG.md                   # Version history  
├── .env.example                   # Environment variables template
├── .gitignore                     # Define files to ignore for Git
├── prompts.yaml                   # A/B testing prompt configurations
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
│   ├── main.py                    # FastAPI application with multi-prompt endpoints
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # API keys and configuration
│   ├── prompts.yaml               # A/B testing prompt configurations
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
│       ├── gemini_service.py      # Google Gemini API with multi-prompt A/B testing
│       └── sheets_service.py      # Google Sheets integration with comparative data logging
└── scripts/                       # Utility scripts (empty)
```

## Service Architecture

### Enhanced Data Pipeline Flow with A/B Testing
```
News APIs → News Service → Multi-Prompt Gemini Analysis → Comparative Google Sheets Storage
     ↓            ↓              ↓                               ↓
NewsAPI      Aggregation    All Active Prompts        Real-time A/B Testing Data
NewsData  → Deduplication → Sequential Analysis    →   Collection for Optimization
AFP          Priority Sort   Comparative Results        & Training Data Preparation
```

### News Service Layer
- **NewsService**: Multi-source orchestrator with priority system and concurrent fetching
- **BaseNewsClient**: Abstract base providing shared functionality for all clients
- **Client Implementations**: 
  - **NewsAPIClient**: Mainstream news sources with positive keyword filtering
  - **NewsDataClient**: Alternative/international sources with category filtering
  - **AFPClient**: Professional journalism with OAuth2 authentication and "inspiring" genre filter

### Multi-Prompt Analysis Layer
- **GeminiService**: Complete AI analysis service with YAML-based A/B testing framework
- **YAML Configuration System**: `prompts.yaml` for easy prompt experimentation without code changes
- **Sequential Multi-Prompt Processing**: Each article analyzed by ALL active prompts for direct comparison
- **Template-Based Prompt Generation**: Dynamic content insertion with configurable prompt structures
- **Conservative Rate Limiting**: Maintains API safety while processing multiple prompt variations

### Data Storage Layer
- **SheetsService**: Google Sheets integration with service account authentication and 37-column unified schema
- **Comparative Data Collection**: Multiple rows per article (one per prompt version) for A/B testing analysis
- **Prompt Version Tracking**: Enhanced metadata using reserved columns for systematic comparison
- **Unified Analysis Pipeline**: Single sheet architecture with rich prompt performance data

## Design Patterns

### Architectural Patterns
- **Template Method**: BaseNewsClient defines common interface, clients implement specifics
- **Service-Oriented Architecture**: Clean separation between news, analysis, and storage services
- **Circuit Breaker**: Failed services don't impact others (graceful degradation)
- **Pipeline Pattern**: Sequential processing through aggregation → multi-prompt analysis → comparative storage
- **Configuration-Driven Behavior**: YAML-based prompt management for experimental flexibility

### A/B Testing Patterns
- **Sequential Analysis Pattern**: Each article processed by all active prompts for direct comparison
- **Configuration-Based Experimentation**: YAML file enables rapid prompt iteration without deployment
- **Comparative Data Collection**: Multiple analysis results per article stored for systematic evaluation
- **Template-Based Content Generation**: Dynamic prompt creation with variable substitution

## API Architecture

### Core Endpoints
- **GET /api/news** - Unified aggregation with multi-prompt Gemini analysis and automatic comparative sheets logging
- **GET /api/sources** - Source configuration and priority information
- **GET /api/sources/test** - Health check for all news source connections
- **GET /api/news/afp** - Direct AFP testing endpoint
- **GET /health** - Comprehensive system health dashboard

### Enhanced Response Structure with A/B Testing
```json
{
  "status": "success",
  "gemini_analyzed": true,
  "prompt_versions": ["v1_comprehensive", "v2_emotion_focused"],
  "analyzed_sources": ["newsapi", "newsdata", "afp"],
  "sheets_logged": true,
  "total_logged": 6,
  "gemini_stats": {
    "total_tokens_used": 2450,
    "total_batches_processed": 2,
    "prompt_versions_count": 2,
    "total_analyses": 6
  },
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
- **Gemini**: API key authentication with comprehensive rate limiting for multi-prompt processing

## Data Architecture

### Enhanced Google Sheets Schema with A/B Testing (37 Columns)
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

A/B Testing Tracking (3 columns - using reserved columns):
- reserved1: prompt_version (e.g., "v1_comprehensive")
- reserved2: prompt_name (e.g., "Current Comprehensive Analysis")
- reserved3: future expansion
```

### A/B Testing Data Flow
```
News Service → All Articles → Multi-Prompt Analysis → Comparative Metadata → Google Sheets (Multiple Rows Per Article)
```

### Scale and Capacity with A/B Testing
- **Gemini Capacity**: 72,000 articles/day (100 articles × 720 requests/day)
- **Multi-Prompt Overhead**: 2-3x processing time for comparative analysis
- **Actual Need**: ~5,000 articles/day from all sources
- **A/B Testing Headroom**: Still 4x capacity after multi-prompt overhead
- **Cost Safety**: Conservative rate limiting prevents quota violations during experimentation

## A/B Testing Framework

### YAML Configuration Structure
```yaml
v1_comprehensive:
  name: "Current Comprehensive Analysis"
  active: true
  description: "Detailed analysis with all fields - baseline version"
  prompt: |
    [Detailed prompt template with {article_count} variable substitution]

v2_emotion_focused:
  name: "Emotion-Focused Analysis" 
  active: true
  description: "Shorter prompt focused primarily on emotional scoring"
  prompt: |
    [Emotion-focused prompt template]

v3_experimental:
  name: "Experimental Prompt"
  active: false
  description: "Test prompt for new approaches"
  prompt: |
    [Test prompt - can be modified for experimentation]
```

### Comparative Analysis Process
1. **Configuration Loading**: Active prompts loaded from `prompts.yaml`
2. **Sequential Processing**: Each article analyzed by all active prompt versions
3. **Data Collection**: Separate Google Sheets rows for each prompt-article combination
4. **Performance Tracking**: Prompt version and name tracked in reserved columns
5. **Manual Evaluation**: Side-by-side comparison enables systematic prompt optimization

### Optimization Workflow
1. **Baseline Establishment**: Current prompt performance on diverse articles
2. **Experimental Variations**: New prompt versions tested against baseline
3. **Comparative Analysis**: Manual review of analysis quality across prompts
4. **Iterative Refinement**: Prompt modifications based on performance insights
5. **Production Selection**: Best-performing prompt used for large-scale data collection

## Frontend Architecture

### Component Design
- **StatusBanner**: Reusable status display with configurable props
  - Props: `status`, `message`, `emoji`
  - Variants: development, success, warning, error
  - Styling: Tailwind CSS with dynamic classes

### Testing Interface
- **Location**: `http://localhost:3000/test`
- **Purpose**: Visual testing of backend API endpoints with real-time multi-prompt data
- **Features**: 6 source-specific buttons, enhanced JSON display, comprehensive A/B testing results visualization

## Development Approach
1. **Documentation First** - Always document before coding
2. **Small Steps** - One feature at a time with testing
3. **Modular Design** - Each component has single responsibility
4. **Learning Focus** - Code optimized for understanding
5. **Data-Driven Experimentation** - A/B testing framework for systematic improvement
6. **Configuration-Driven Behavior** - YAML-based experimentation without code changes

## Current Status
- ✅ Complete multi-prompt A/B testing framework with YAML configuration
- ✅ Sequential analysis pipeline processing all active prompts per article
- ✅ Enhanced Google Sheets logging with prompt version tracking for comparative analysis
- ✅ Multi-source news aggregation (NewsAPI + NewsData active, AFP authenticated)
- ✅ Template-based prompt generation with dynamic content insertion
- ✅ Conservative rate limiting maintaining API safety during multi-prompt processing
- 🔄 Prompt optimization through systematic A/B testing (active experimentation phase)
- 📋 Production prompt selection based on comparative performance data (planned)

## Technical Debt
- **Legacy sentiment code**: Transformers-based analysis kept as backup but not actively used
- **Debug logging cleanup**: Temporary debug statements need removal for production
- **Manual prompt evaluation**: No automated quality scoring metrics yet implemented
- **Error monitoring**: Limited comprehensive logging dashboard for analysis quality tracking

## Scaling Considerations for A/B Testing
- **Multi-Prompt Processing**: 2-3x slower responses but enables systematic optimization
- **Data Storage**: Google Sheets suitable for A/B testing data; database migration needed for production scale
- **Analysis Quality**: Systematic A/B testing framework enables data-driven prompt optimization
- **DistilBERT Preparation**: Comparative analysis will identify optimal prompts for training data collection
- **User Interface**: Rich comparative analysis data ready for analytics dashboard and performance metrics

---
*Last updated: August 25, 2025*
*Architecture version: 0.7.0*