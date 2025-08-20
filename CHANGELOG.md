# 📝 Changelog

**All notable changes to HopeShot will be documented in this file.**

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