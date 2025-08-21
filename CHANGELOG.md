# 📝 Changelog

**All notable changes to HopeShot will be documented in this file.**

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