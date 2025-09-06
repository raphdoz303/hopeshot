# 📝 Changelog

**All notable changes to HopeShot will be documented in this file.**

---

## [0.13.0] - 2025-09-06

### Added
- **Modular deduplication service** with URL exact matching and title similarity detection (80% threshold)
- **Performance-optimized duplicate detection** using 30-day comparison window for scalability
- **Database-driven content endpoint** (`/api/articles`) for accumulated articles without fresh API calls
- **Frontend database integration** with `getArticles()` method and updated useNews hook
- **Fresh news collection option** via `fetchFreshNews()` for manual content updates
- **Deduplication analytics** tracking comparison scope and detection effectiveness

### Changed
- **Primary content source** from fresh API calls to accumulated database articles for better performance
- **Article insertion pipeline** now includes automatic duplicate detection before database storage
- **Frontend data flow** prioritizes database content with optional fresh content collection

### Fixed
- **Database column name compatibility** between deduplication service and actual schema (url_id)
- **Integration approach** using minimal changes to preserve existing working functionality

### Technical
- **DeduplicationService**: Two-tier detection with URL matching (fast) and title similarity (comprehensive)
- **Performance Optimization**: 30-day window reduces comparison overhead as database scales
- **Modular Architecture**: Reusable deduplication service across multiple endpoints

---

## [0.12.0] - 2025-09-02

### Added
- **Geographic emoji display** using database location.emoji field via M49 JOIN queries
- **Geographic search filtering** with case-insensitive location name matching
- **Enhanced location data integration** with backend emoji lookup function
- **Memory-optimized Next.js configuration** preventing development server crashes
- **Placeholder emoji system** for articles without categories using 📰 fallback

### Changed
- **Article card geography display** from impact badges to M49 flag emojis in grey chips
- **Category emoji positioning** moved to top section below geographic information
- **Frontend filtering architecture** enhanced with geographic search alongside category/impact filters

### Fixed
- **Node.js memory allocation crashes** through Next.js webpack optimization
- **TypeScript interface mismatches** between api.ts and components
- **Card layout inconsistencies** with bottom-aligned footer using flexbox

### Technical
- **M49 Emoji Integration**: get_location_names_and_emojis_by_m49() dual lookup function
- **Memory Configuration**: Next.js webpack optimization with reduced parallelism
- **Interface Standardization**: Shared TypeScript interfaces across components

---

## [0.11.0] - 2025-09-01

### Added
- **Complete frontend-backend integration** with real news articles
- **Modular API service layer** with centralized backend communication
- **Custom React hook system** (useNews) for data fetching and filtering
- **Direct M49 code integration** using UN standard geographic codes
- **Dynamic category system** with real-time emoji/color display from database

### Changed
- **Database schema architecture** to direct M49 code storage in junction tables
- **Frontend data flow** from mock articles to real API integration

### Fixed
- **Category emoji display issues** by connecting components to database
- **Memory allocation crashes** through cache clearing strategies
- **Foreign key constraint errors** using simplified migration approach

### Technical
- **M49 Direct Storage**: article_locations(article_id, m49_code) without conversion
- **Service Layer Pattern**: ApiService class with error handling and type safety

---

## [0.10.0] - 2025-08-30

### Added
- **Complete frontend architecture** with Next.js and TypeScript
- **Dynamic category system** fetching from database API instead of hardcoded values
- **Sky & Growth color palette** implemented via CSS variables
- **Responsive component library** with VerticalNewsCard and HorizontalHighlightCard
- **Interactive filtering interface** with category/impact selection

### Changed
- **Category system** from auto-generated to 8 standardized categories with visual identity
- **Frontend styling** from Tailwind config to CSS variables for v4 compatibility

### Fixed
- **Database service connection handling** for get_all_categories method
- **Tailwind CSS v4 compatibility** by switching to CSS custom properties

---

## [0.9.0] - 2025-08-29

### Added
- **Complete SQLite database integration** with normalized schema
- **Multi-location junction table architecture** for complex geographic relationships
- **Auto-creation system** for categories and locations with hierarchical relationships
- **Dual storage pipeline** - SQLite for app data, Google Sheets for A/B testing

### Changed
- **Geographic schema simplification** from 4 fields to 2 fields
- **DatabaseService architecture** with junction tables for many-to-many relationships

### Fixed
- **Database locking issues** through connection reuse patterns

---

## [0.8.0] - 2025-08-28

### Added
- **YAML-based source configuration** for dynamic news source management
- **Combined multi-prompt analysis** - All A/B test prompts in single Gemini request

### Fixed
- **AFP integration** - Corrected response parsing from data.documents to data.response.docs
- **Multi-prompt performance** - Reduced analysis time from 2+ minutes to ~10 seconds

---

## [0.7.0] - 2025-08-25

### Added
- **Multi-Prompt A/B Testing Framework** with YAML configuration
- **Sequential Analysis Pipeline** for direct prompt comparison
- **Comparative Data Collection** in Google Sheets with version tracking

### Changed
- **Enhanced `/api/news` endpoint** with multi-prompt analysis
- **GeminiService architecture** supports dynamic prompt loading

---

## [0.6.0] - 2025-08-22

### Added
- **Google Gemini 2.5 Flash-Lite integration** with comprehensive sentiment analysis
- **37-column enhanced schema** for emotions, fact-checking, geographic analysis
- **Advanced batch processing** up to 100 articles per request
- **Rich emotion detection** with 0.0-1.0 scoring

### Changed
- **Simplified architecture** from dual-sheet to single-sheet approach

---

## [0.5.0] - 2025-08-21

### Added
- **Google Sheets integration** with service account authentication
- **Real-time data logging pipeline** for all API calls
- **Structured 25-column data collection** for sentiment analysis research

---

## [0.4.0] - 2025-08-20

### Added
- **Complete sentiment analysis system** using Transformers (Hugging Face)
- **Weighted emotion scoring** with custom uplift calculation
- **Model-based confidence scoring** using transformer confidence

### Dependencies
- Added transformers, torch, nltk for sentiment analysis

---

## [0.3.0] - 2024-08-19

### Added
- **Service-oriented architecture** with modular news clients
- **AFP integration** with OAuth2 authentication
- **Multi-source orchestration** with priority system and duplicate detection

### Changed
- **Replaced requests with aiohttp** for async HTTP calls

---

## [0.2.0] - 2024-08-18

### Added
- **Multi-source news integration** (NewsAPI + NewsData)
- **Concurrent API fetching** for improved performance
- **Cross-API response normalization**

---

## [0.1.0] - 2024-08-17

### Added
- **Project foundation** with Next.js frontend and FastAPI backend
- **Component-based architecture** with TypeScript interfaces
- **Professional development workflow** with documentation system

---
*Changelog version: 0.12.0*