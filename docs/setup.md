# HopeShot Setup Guide

Complete guide to get HopeShot running with SQLite database, Google Gemini AI integration, and multi-prompt A/B testing framework.

---

## Prerequisites
- **Python 3.11+** (tested with 3.13.7)
- **Node.js 18+** (for Next.js)
- **Git** (for version control)
- **Google Cloud account** (for Gemini API access)
- **Google account** (for Google Sheets integration)
- **SQLite** (built into Python - no separate installation needed)

---

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/hopeshot.git
cd hopeshot
```

### 2. Backend Setup (Python/FastAPI)
```bash
cd backend

# Install Python dependencies
py -m pip install -r requirements.txt

# Create SQLite database
py database_setup.py

# Migrate to multi-location support (if needed)
py database_migration.py

# Test database connection
py -c "from services.database_service import DatabaseService; db = DatabaseService(); print(db.test_connection())"

# Start development server
py -m uvicorn main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

**Dependencies**:
- `fastapi>=0.68.0` - Web framework
- `uvicorn>=0.15.0` - ASGI server
- `python-dotenv>=0.19.0` - Environment variable management
- `aiohttp>=3.8.0` - Async HTTP client for concurrent API calls
- `google-generativeai>=0.3.0` - Google Gemini API client
- `google-api-python-client>=2.0.0` - Google Sheets API access
- `google-auth>=2.0.0` - Google authentication libraries
- `pyyaml>=6.0.0` - YAML configuration file parsing for A/B testing
- `transformers>=4.21.0` - Hugging Face models (backup/legacy)
- `torch>=1.13.0` - PyTorch neural network backend (backup)
- `nltk>=3.8.0` - VADER sentiment analyzer (backup)
- `datasets>=2.0.0` - Model download support (backup)

### 3. Frontend Setup (Next.js/React)

#### New Development Workflow
```bash
# Frontend development with component testing
cd frontend
npm run dev

# Access component testing interface
http://localhost:3000/test-cards

# Access new explore page
http://localhost:3000/explore
```

#### Tailwind CSS v4 Configuration
The project uses Tailwind CSS v4 with CSS custom properties instead of traditional config files:

**Location**: `frontend/src/app/globals.css`
```css
:root {
  /* Sky & Growth Color Palette */
  --sky-50: #EAF6FF;
  --sky-500: #3BA3FF;
  --sky-700: #1D6FD1;
  --growth-50: #EAFBF1;
  --growth-500: #22C55E;
  /* ... additional colors */
}

/* Custom utility classes */
.bg-gradient-sky-growth { 
  background: linear-gradient(135deg, var(--sky-50), var(--growth-50));
}
```

#### Component Architecture
New components with standardized interfaces:
- `VerticalNewsCard.tsx` - Article display for explore grid
- `HorizontalHighlightCard.tsx` - Featured articles for homepage
- Both components use TypeScript interfaces and dynamic category colors

---

## Database Setup

### SQLite Database Creation
The database is automatically created when you run `database_setup.py`. This creates:

**Tables Created**:
- `articles` - Main article storage (40 columns matching Google Sheets schema)
- `categories` - Category definitions with metadata (name, description, color, emoji)
- `locations` - Hierarchical geographic data (country → region → continent)
- `article_categories` - Many-to-many junction table for article-category relationships
- `article_locations` - Many-to-many junction table for article-location relationships

**Database Features**:
- Auto-incrementing primary keys
- Foreign key constraints for data integrity
- Performance indexes on key lookup fields
- Junction tables for many-to-many relationships

### Viewing Database Content
**Option 1: DB Browser for SQLite (Recommended)**
1. Download from https://sqlitebrowser.org/
2. Open `backend/hopeshot_news.db`
3. Browse tables, run SQL queries, view relationships

**Option 2: API Endpoints**
- `http://localhost:8000/health` - Database statistics and top categories/locations
- `http://localhost:8000/api/sources` - Source info with database stats

**Option 3: VS Code Extension**
- Install "SQLite Viewer" extension
- Right-click `.db` file → "Open with SQLite Viewer"

---

## API Configuration

#### New API Endpoint Testing
```bash
# Test category API endpoint
curl http://localhost:8000/api/categories

# Expected response with 8 categories including filter_name, emoji, colors
```

### Google Gemini API Setup
1. **Create Google Cloud Project** (if you don't have one)
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one

2. **Enable Gemini API**
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Click "Create API Key"
   - Select your Google Cloud project
   - Copy the API key

3. **Add to environment variables**:
   ```bash
   # Add to backend/.env
   GEMINI_API_KEY=your_api_key_here
   ```

### Google Sheets Integration
1. **Create a Google Sheet**
   - Go to [Google Sheets](https://sheets.google.com)
   - Create a new spreadsheet
   - Copy the spreadsheet ID from the URL
   - Example: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`

2. **Set up Service Account**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Navigate to APIs & Services > Credentials
   - Click "Create Credentials" > "Service Account"
   - Download the JSON credentials file
   - Rename it to `gsheetapi_credentials.json`
   - Place it in the `backend/` directory

3. **Share the Sheet**
   - Open your Google Sheet
   - Click "Share" button
   - Add the service account email (from the credentials file)
   - Give it "Editor" permissions

4. **Add to environment variables**:
   ```bash
   # Add to backend/.env
   GOOGLE_SHEETS_ID=your_spreadsheet_id_here
   ```

### NewsAPI.org
1. Sign up at https://newsapi.org/
2. Get your free API key (1000 requests/day)
3. Add to `.env`: `NEWS_API_KEY=your_key_here`

### NewsData.io
1. Sign up at https://newsdata.io/
2. Get your free API key (200 requests/day, 10 articles max)
3. Add to `.env`: `NEWSDATA_API_KEY=your_key_here`

### AFP (Agence France-Presse)
1. Contact AFP sales for API access
2. Requires content subscription for article access
3. Add all 4 credentials to `.env`:
   ```bash
   AFP_CLIENT_ID=your_client_id
   AFP_CLIENT_SECRET=your_client_secret
   AFP_USERNAME=your_email@example.com
   AFP_PASSWORD=your_password
   ```

---

## Configuration Files

### A/B Testing Configuration
Create `backend/prompts.yaml` with your prompt configurations:

```yaml
# prompts.yaml - A/B Testing Configuration
v1_comprehensive:
  name: "Current Comprehensive Analysis"
  active: true
  description: "Detailed analysis with all fields - baseline version"
  prompt: |
    Analyze these {article_count} news articles for comprehensive emotional and contextual analysis. Return a JSON array with exactly {article_count} objects, one per article.

    REQUIRED FORMAT for each article:
    {{
      "article_index": integer,
      "sentiment": "positive" | "negative" | "neutral",
      "confidence_score": float (0-1),
      "emotions": {{
        "hope": float (0-1),
        "awe": float (0-1),
        "gratitude": float (0-1),
        "compassion": float (0-1),
        "relief": float (0-1),
        "joy": float (0-1)
      }},
      "categories": ["1 to 3 from: health, technology, environment, education, social, human rights, scientific discovery"],
      "source_credibility": "high" | "medium" | "low",
      "fact_checkable_claims": "yes" | "no",
      "evidence_quality": "strong" | "moderate" | "weak",
      "controversy_level": "low" | "medium" | "high",
      "solution_focused": "yes" | "no",
      "age_appropriate": "all" | "adults",
      "truth_seeking": "yes" | "no",
      "geographical_impact_level": "Global" | "Regional" | "National" | "Local",
      "geographical_impact_location": ["Country names like USA, Vietnam, France"],
      "overall_hopefulness": float (0-1),
      "reasoning": "Explain top emotion + source credibility in max 15 words"
    }}

v2_precision:
  name: "Precision Analysis"
  active: true
  description: "Focused on accuracy and fact-checking"
  prompt: |
    [Similar format but emphasizing precision over emotion detection]

v3_empathy_depth:
  name: "Empathy-Focused Analysis"
  active: true
  description: "Deep emotional analysis with empathy focus"
  prompt: |
    [Similar format but emphasizing emotional depth and human impact]
```

### Source Configuration
The `backend/sources.yaml` file controls which news sources are active:

```yaml
afp:
  name: "Agence France-Presse"
  active: true
  configured: true
  priority: 1
  quality_score: 10
  daily_limit: 20

newsapi:
  name: "NewsAPI.org"
  active: false
  configured: true
  priority: 2
  quality_score: 5
  daily_limit: 10
```

---

## Verification

### Test Database Setup
```bash
cd backend

# Test database creation
py database_setup.py

# Test database service
py -c "
from services.database_service import DatabaseService
db = DatabaseService()
result = db.test_connection()
print('Database:', result['status'])
print('Tables:', result['stats'])
"
```

### Test All Services
```bash
# Test Gemini with geographic processing
py -c "
import asyncio
from services.gemini_service import GeminiService

async def test():
    gemini = GeminiService()
    result = await gemini.test_connection()
    print('Gemini:', result['status'])
    print('Database exists:', result['database_exists'])

asyncio.run(test())
"

# Test Google Sheets
py -c "
from services.sheets_service import SheetsService
sheets = SheetsService()
result = sheets.test_connection()
print('Sheets:', result['success'])
"
```

### Test Complete System
```bash
# Start backend server
py -m uvicorn main:app --reload --port 8000

# In another terminal, test endpoints
curl "http://localhost:8000/health"
curl "http://localhost:8000/api/sources/test"

# Test complete pipeline with dual storage
curl "http://localhost:8000/api/news?pageSize=2"
```

### Expected Results
- Database should show articles, categories, and locations being created
- Google Sheets should receive multiple rows per article (one per active prompt)
- Terminal should show auto-creation messages:
  ```
  Created new location: USA (country) with ID 3
  Created new category: social (ID: 1)
  Inserted article: [Title]... (ID: 15)
  Logged 6 articles to Google Sheets
  ```

---

## Development Workflow

### Starting Development Session
```bash
# Terminal 1: Backend with database support
cd backend
py -m uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Database Management
```bash
# View database statistics
curl "http://localhost:8000/health"

# Open database in DB Browser for SQLite
# File → Open Database → backend/hopeshot_news.db

# Run database migrations (when schema changes)
py database_migration.py
```

### A/B Testing Workflow
1. Edit `backend/prompts.yaml` to modify prompts or activate/deactivate versions
2. Run API calls to collect comparative data
3. Review Google Sheets for side-by-side prompt performance analysis
4. Check database for clean application data (first prompt only)
5. Iterate prompts based on quality comparison

---

## Troubleshooting

### Common Database Issues

**Database Locked Error**:
- Close DB Browser for SQLite if open
- Restart uvicorn server
- Check for multiple simultaneous API requests

**Categories Not Created**:
- Verify categories field in Gemini response is a list: `["social", "sport"]`
- Check terminal for "Created new category" messages
- Ensure connection reuse pattern is implemented

**Locations Not Auto-Created**:
- Check geographic fields in prompts.yaml match new schema
- Verify `geographical_impact_location` returns arrays: `["USA", "Japan"]`
- Monitor terminal for location creation messages

### Performance Issues

**Slow Multi-Prompt Analysis**:
- Expected: 2-3x slower than single prompt due to comprehensive analysis
- Reduce active prompts in prompts.yaml for faster testing
- 2-minute intervals between batches are normal for rate limiting

**Database Query Performance**:
- Junction table queries are indexed for performance
- Consider LIMIT clauses for large result sets
- SQLite handles thousands of articles efficiently

### A/B Testing Issues

**Prompts Not Loading**:
- Verify prompts.yaml syntax with online YAML validator
- Check `active: true` for prompts you want to test
- Monitor terminal for "Loaded X active prompts" messages

**Inconsistent Gemini Results**:
- Known issue: Score differences between single vs batch analysis
- Categories often default to "social" regardless of content type
- Geographic responses need validation improvements

---

## Production Considerations

### Environment Variables
Ensure all required environment variables are set in `backend/.env`:
- `GEMINI_API_KEY` - Google Gemini API access
- `GOOGLE_SHEETS_ID` - Target spreadsheet ID  
- `NEWS_API_KEY` - NewsAPI.org access (optional)
- `NEWSDATA_API_KEY` - NewsData.io access (optional)
- `AFP_CLIENT_ID`, `AFP_CLIENT_SECRET`, `AFP_USERNAME`, `AFP_PASSWORD` - AFP access (optional)

### Security
- Keep `gsheetapi_credentials.json` secure and never commit to version control
- Keep `hopeshot_news.db` in .gitignore for data protection
- Keep configuration files (`prompts.yaml`, `sources.yaml`) in version control
- Rotate API keys periodically

### Database Management
- **Current Setup**: SQLite suitable for development and single-user applications
- **Backup Strategy**: Database file can be copied for backups
- **Migration Path**: PostgreSQL recommended for multi-user production deployment
- **Connection Management**: Uses connection reuse pattern to prevent locks

### Scaling Considerations
- **Current Capacity**: ~24,000 articles/day with 3 active prompts and dual storage
- **Database Performance**: SQLite efficient for current scale
- **Geographic Hierarchy**: Simple inference mapping (consider external APIs for production)
- **A/B Testing Overhead**: 3x analysis time acceptable for research phase

---

## Database Features

### Auto-Creation System
The system automatically creates database entries as new content is discovered:

**Categories**: When Gemini identifies new categories, they're automatically added to the categories table
**Geographic Locations**: New countries/regions auto-created with proper hierarchical relationships
**Junction Relationships**: Articles automatically linked to relevant categories and locations

### Multi-Location Support
Articles can reference multiple locations for complex stories:
- USA-Japan collaboration → Both countries linked to article
- European policy → Multiple countries linked via region hierarchy
- Junction table queries enable sophisticated geographic filtering

### Geographic Hierarchy Example
```
Vietnam (discovered in article)
  ↓
Auto-creates: Vietnam (country) → Southeast Asia (region) → Asia (continent)
  ↓
Enables queries: "Articles about Vietnam", "Articles about Southeast Asia", "Articles about Asia"
```

---

## Known Issues & Future Improvements

### Immediate Issues to Address
- **Sheets logging**: May require debugging connection issues
- **Scoring inconsistencies**: Different results for single vs batch analysis
- **Category classification**: Prompts need refinement for accurate categorization
- **Timestamp handling**: Currently uses published_at instead of creation time

### Suggested Improvements
- **Geographic validation**: Pre-populate common countries for better accuracy
- **Prompt optimization**: Refine prompts for better sports/politics/health classification
- **RSS integration**: Add RSS sources to reduce AFP dependency
- **Duplicate detection**: Implement database-based deduplication for production

### Performance Optimizations
- **Connection pooling**: For concurrent user support
- **Database indexing**: Additional indexes for complex geographic queries
- **Prompt efficiency**: Shorter prompts for faster processing
- **Batch size tuning**: Optimize for API rate limits vs processing speed


### Development Environment Verification

#### Complete System Test
```bash
# 1. Backend health check with category system
curl http://localhost:8000/health

# 2. Category API functionality
curl http://localhost:8000/api/categories

# 3. Frontend development server
cd frontend && npm run dev

# 4. Component testing
http://localhost:3000/test-cards

# 5. Full application
http://localhost:3000/explore
```

### Troubleshooting Updates

#### Frontend Issues
**Tailwind CSS not working**:
- Ensure `globals.css` contains the CSS custom properties
- Restart frontend dev server after CSS changes
- Use browser dev tools to verify CSS variables are loaded

**Components not updating**:
- Hard refresh (Ctrl+Shift+R) to bypass cache
- Check browser console for JavaScript errors
- Verify TypeScript compilation is successful

**Categories not loading**:
- Check Network tab in browser dev tools for API calls
- Verify backend server is running on port 8000
- Check backend terminal for any database connection errors

#### Database Issues
**Categories API returns empty array**:
- Run `py check_db_schema.py` to verify categories table structure
- Ensure migration scripts completed successfully
- Check backend terminal for database service errors

**New columns not found**:
- Run `py update_categories_schema.py` to add missing columns
- Verify schema matches expected structure with filter_name and accent columns

### Production Considerations (Updated)

#### Environment Variables
No new environment variables required for frontend category system.

#### Database Schema
The categories table now includes additional columns for frontend integration:
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    filter_name TEXT,  -- NEW: Clean display name
    emoji TEXT,
    description TEXT,
    color TEXT,
    accent TEXT,       -- NEW: Accent color for selected states
    created_at TIMESTAMP
);
```

#### Frontend Build Process
```bash
# Production build with custom CSS variables
cd frontend
npm run build
npm start
```

### Known Issues & Solutions (v0.10.0)

#### Current Limitations
- **Mock Data**: Frontend components use mock articles, real API integration pending
- **Filter Functionality**: UI complete but doesn't query backend with selected filters
- **Navigation**: No header/menu system between homepage and explore page
- **Error Handling**: Basic console logging, no user-facing error states

#### Immediate Next Steps
1. Connect frontend components to real `/api/news` endpoint
2. Implement backend filtering by category and impact level
3. Add navigation header component
4. Implement loading states and error handling

#### Performance Notes
- Component rendering optimized for responsive grids
- CSS custom properties approach works reliably across browsers
- Category API calls suitable for frontend caching due to infrequent changes

---

---

*Last updated: August 29, 2025*  
*Ready for SQLite database integration with multi-location support and auto-creation capabilities!*