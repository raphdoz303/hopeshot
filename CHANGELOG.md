# 📝 Changelog

**All notable changes to HopeShot will be documented in this file.**

---

## [0.7.0] - 2025-08-25

### Added
- **Multi-Prompt A/B Testing Framework** with YAML-based configuration for systematic prompt optimization
- **Sequential Analysis Pipeline** - Each article analyzed by all active prompts for direct comparison
- **Enhanced Prompt Management** via `prompts.yaml` for easy experimentation without code changes
- **Comparative Data Collection** - Google Sheets logging with prompt version tracking for side-by-side analysis
- **Template-Based Prompt Generation** with dynamic article count and content insertion
- **Configuration-Driven Behavior** enabling rapid prompt iteration and performance evaluation

### Changed
- **Enhanced `/api/news` endpoint** - Now performs multi-prompt analysis with all active prompt versions
- **Unified Google Sheets pipeline** - Utilizes reserved columns for prompt version and name tracking
- **GeminiService architecture** - Supports dynamic prompt loading and sequential batch processing
- **API response structure** - Maintains backward compatibility while adding multi-prompt metadata

### Technical
- **YAML Configuration System** - Complete prompt management with active/inactive states and descriptions
- **Multi-Prompt Data Flow** - Articles → All Active Prompts → Comparative Analysis → Sheets Storage
- **Enhanced Rate Limiting** - Sequential processing maintains conservative API usage patterns
- **Prompt Version Tracking** - Full audit trail of which prompt generated each analysis

### Dependencies
- Added `pyyaml>=6.0.0` for YAML configuration file management

### Performance
- **2-3x analysis time increase** due to multi-prompt processing (expected trade-off for A/B testing)
- **Comparative data richness** - Multiple analyses per article enable systematic prompt optimization
- **Maintained rate limiting safety** - Conservative API usage despite increased analysis volume

### A/B Testing Capabilities
- **Easy prompt experimentation** - Edit YAML file to test new prompt variations
- **Direct comparison data** - Same articles analyzed by different prompts for quality assessment
- **Systematic optimization framework** - Foundation for identifying best-performing prompts for production

### Notes
- **Ready for prompt optimization** - System enables rapid iteration and performance comparison
- **DistilBERT preparation** - Comparative analysis will identify optimal prompt for training data collection
- **Production-ready architecture** - Multi-prompt framework scales to large-scale data collection needs

---

## [0.6.0] - 2025-08-22

### Added
- **Complete Google Gemini 2.5 Flash-Lite integration** with comprehensive sentiment analysis
- **Unified data architecture** - single Google Sheets pipeline for all news articles with rich metadata
- **37-column enhanced schema** capturing emotions, fact-checking, geographic, and content analysis
- **Advanced batch processing** - up to 100 articles per request with intelligent 2-minute pacing
- **Comprehensive rate limiting** with exact token tracking and hard stops to prevent API overages
- **Rich emotion detection** - hope, awe, gratitude, compassion, relief, joy with 0.0-1.0 scoring
- **Future-proofing metadata** - source credibility, fact-checking readiness, geographic analysis
- **Massive scale capacity** - 72,000 articles/day processing capability vs 5,000 daily need

### Changed
- **Simplified architecture** from dual-sheet to single-sheet approach due to abundant API capacity
- **Enhanced Google Sheets integration** to handle comprehensive 37-column analysis data
- **Optimized for batch efficiency** with 100-article processing vs previous 3-article batches
- **Conservative rate limiting** with 20% safety margins to guarantee no quota violations

### Technical
- **GeminiService architecture** - Complete service for large-batch article analysis with safety nets
- **Enhanced SheetsService** - Unified schema for rich metadata collection and future model training
- **Smart pacing system** - 2-minute intervals with exact token usage tracking
- **Robust error handling** - JSON parsing fallbacks and graceful degradation patterns

### Dependencies
- Added `google-generativeai>=0.3.0` for Gemini API access
- Updated environment configuration for Gemini API key management

### Performance
- **13x capacity headroom** - Can process entire daily news volume with massive safety margin
- **Efficient token usage** - Optimized prompts for comprehensive analysis within rate limits
- **Real-time data collection** - All articles generate training data for future custom models

### Notes
- **Prompt optimization needed** - Current prompts require refinement for consistent analysis quality
- **Complete training dataset** - Rich emotional analysis on ALL news types for better model development
- **Ready for scale** - Architecture supports full news volume with room for significant growth

---

## [0.5.0] - 2025-08-21

### Added
- **Complete Google Sheets integration** with service account authentication
- **Real-time data logging pipeline** - All `/api/news` calls automatically log articles to Google Sheets
- **Data flattening service** - Converts complex article + sentiment data into 25-column spreadsheet rows
- **Batch article logging** with error handling and graceful degradation
- **Enhanced API responses** - Added `sheets_logged` and `total_logged` metadata fields
- **Structured data collection** - 25 predefined columns including all sentiment metrics for analysis

### Changed
- **Enhanced `/api/news` endpoint** - Now includes automatic Google Sheets logging with full pipeline
- **Updated security configuration** - Protected Google Sheets credentials with enhanced .gitignore
- **Improved error handling** - Sheets logging failures don't impact API responses

### Technical
- **SheetsService architecture** - Modular Google Sheets integration ready for batch operations
- **Service account authentication** - Automated Google Sheets access without user intervention
- **Flat data schema** - Structured 25-column format for consistent sentiment analysis research
- **Real-time data pipeline** - News APIs → Sentiment Analysis → Google Sheets integration

### Dependencies
- Added `google-api-python-client>=2.0.0` for Google Sheets API access
- Added `google-auth>=2.0.0` and related authentication libraries

### Notes
- **Data collection active** - All API calls now generate research data for sentiment algorithm improvement
- **Neutral scoring confirmed** - Transformers models correctly return 0 for neutral business articles
- **Ready for analysis** - Complete data pipeline enables sentiment formula calibration

---

## [0.4.0] - 2025-08-20

### Added
- **Complete sentiment analysis system** using Transformers (Hugging Face)
- **Weighted emotion scoring** with custom uplift calculation (Hope×2.0, Awe×1.8, etc.)
- **Raw emotion tracking** - Store basic emotions (anger, fear, joy) + derived uplift emotions
- **Model-based confidence scoring** using actual transformer model confidence
- **Enhanced frontend test page** with 6 source-specific buttons for comprehensive testing
- **Sentiment integration** into `/api/news` endpoint for NewsAPI & NewsData articles

### Changed
- **Updated test page** - Complete rewrite with improved JSON display and source filtering
- **Enhanced API responses** - Articles now include `sentiment_analysis` and `uplift_score` fields
- **Improved response formatting** - Better visibility of source tracking and sentiment data

### Technical
- **Modular sentiment architecture** in `services/sentiment/` package
- **Dual-model analysis** - Separate sentiment and emotion detection models
- **Extensible analyzer pattern** - Ready for VADER, OpenAI, and custom AI integration
- **Source-specific analysis** - Only NewsAPI/NewsData articles analyzed (AFP uses built-in filters)

### Dependencies
- Added `transformers>=4.21.0` for sentiment/emotion models
- Added `torch>=1.13.0` for neural network backend
- Added `nltk>=3.8.0` for future VADER integration

### Notes
- **Scoring calibration needed** - Current uplift scores too high for neutral business news
- **AFP articles excluded** from sentiment analysis (relies on native filtering)
- **Models downloaded on first run** (~500MB initial download)

---

## [0.3.0] - 2024-08-19

### Added
- **Service-oriented architecture** with modular news clients
- **AFP integration** with OAuth2 password grant authentication
- **Multi-source orchestration** combining AFP + NewsAPI + NewsData
- **Priority system** for article ranking (AFP → NewsAPI → NewsData)  
- **Cross-source duplicate detection** with 70% word similarity algorithm
- **API source tracking** - articles include `api_source` field for quality analysis
- **Graceful degradation** - system works with any combination of available sources
- **Enhanced error reporting** with `sourcesUsed` and `sourcesFailed` arrays
- New endpoints: `/health`, `/api/sources`, `/api/sources/test`, `/api/news/afp`

### Changed
- **Replaced requests with aiohttp** for async HTTP calls
- **Refactored main.py** to use NewsService orchestrator
- **Updated /api/news** to aggregate from all available sources
- **Enhanced article metadata** with dual source tracking (API + publication)

### Technical
- **BaseNewsClient** abstract class for shared functionality
- **Concurrent API fetching** for improved performance  
- **OAuth2 token management** with automatic re-authentication
- **Cross-API response normalization** to unified article format

### Notes
- **AFP account activation pending** - authentication works, awaiting content access
- **Currently running on 2/3 sources** (NewsAPI + NewsData active)

---

## [0.2.0] - 2024-08-18

### Added
- Multi-source news integration (NewsAPI.org + NewsData.io)
- Service-oriented architecture with dedicated news clients
- Concurrent API fetching for improved performance
- Cross-API response normalization
- New endpoints: `/api/sources`, `/api/sources/test`
- Enhanced error handling with graceful source degradation
- Source-specific duplicate removal based on article titles

### Changed  
- Refactored `/api/news` to use unified news service
- Updated frontend test page with improved error display
- Enhanced API documentation with multi-source examples

### Technical
- Created `services/` package with modular news clients
- Added NewsData.io integration alongside existing NewsAPI
- Implemented async/await patterns for concurrent requests

---

## 🎉 [0.1.0] - 2024-08-17

### ✨ **Added**
- **Project Foundation**
  - Initial project setup with Git version control
  - Complete project documentation system in `docs/` folder
  - Professional development workflow established

- **Frontend Development**
  - **Next.js** frontend with TypeScript and Tailwind CSS
  - **StatusBanner** reusable React component with TypeScript interfaces
  - **Homepage** with HopeShot branding and dual status banners
  - **API testing interface** at `/test` route with interactive buttons

- **Backend Development**
  - **FastAPI** backend with CORS middleware
  - **Root endpoint** (`/`) returning API information
  - **Test endpoint** (`/api/test`) for connection verification

### 🔧 **Technical Improvements**
- **Frontend-backend communication** established via fetch API
- **Component-based architecture** with props-driven design
- **Async/await patterns** for API calls with loading states
- **Professional development setup** with hot reload on both stacks

### 📚 **Documentation**
- **README.md** with project overview and goals
- **Architecture documentation** with current structure
- **Inline code comments** for learning purposes