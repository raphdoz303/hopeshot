# HopeShot Setup Guide

> **Purpose**: Installation steps, environment configuration, and development workflow setup

## Prerequisites
- **Python 3.11+** 
- **Node.js 18+**
- **Google Cloud account** (Gemini API)
- **Google account** (Sheets integration)

---

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/hopeshot.git
cd hopeshot
```

### 2. Backend Setup
```bash
cd backend
py -m pip install -r requirements.txt
py database_setup.py
py -m uvicorn main:app --reload --port 8000
```

**Key Dependencies**:
- `fastapi>=0.68.0` - Web framework
- `google-generativeai>=0.3.0` - Gemini API
- `google-api-python-client>=2.0.0` - Sheets API
- `pyyaml>=6.0.0` - A/B testing configuration
- `aiohttp>=3.8.0` - Async HTTP client

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

**Memory Optimization Required** (Windows PowerShell):
```powershell
# Clear cache before development
Remove-Item -Recurse -Force .next -ErrorAction SilentlyContinue

# Set memory allocation
$env:NODE_OPTIONS="--max-old-space-size=2048"
npm run dev
```

---

## API Configuration

### Google Gemini API
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create API key
3. Add to `backend/.env`: `GEMINI_API_KEY=your_key_here`

### Google Sheets Integration
1. Create spreadsheet at [Google Sheets](https://sheets.google.com)
2. Copy spreadsheet ID from URL
3. Create service account at [Google Cloud Console](https://console.cloud.google.com/)
4. Download JSON credentials → rename to `gsheetapi_credentials.json` → place in `backend/`
5. Share spreadsheet with service account email (Editor permissions)
6. Add to `.env`: `GOOGLE_SHEETS_ID=your_spreadsheet_id`

### News APIs (Optional)
**NewsAPI**: Sign up at https://newsapi.org/ → Add `NEWS_API_KEY=your_key`
**NewsData**: Sign up at https://newsdata.io/ → Add `NEWSDATA_API_KEY=your_key`
**AFP**: Contact AFP sales → Add all 4 credentials (CLIENT_ID, SECRET, USERNAME, PASSWORD)

---

## Configuration Files

### A/B Testing Setup
Create `backend/prompts.yaml`:
```yaml
v1_comprehensive:
  name: "Current Comprehensive Analysis"
  active: true
  description: "Detailed analysis with all fields - baseline version"
  prompt: |
    Analyze these {article_count} news articles...
    REQUIRED FORMAT for each article:
    {{
      "article_index": integer,
      "sentiment": "positive" | "negative" | "neutral",
      "categories": ["1 to 3 from: health, technology, environment..."],
      "geographical_impact_level": "Global" | "Regional" | "National" | "Local",
      "geographical_impact_location": ["Country names like USA, Vietnam"],
      "overall_hopefulness": float (0-1)
    }}
```

### Source Configuration
Create `backend/sources.yaml`:
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

## Verification & Testing

### Test Database Setup
```bash
cd backend
py database_setup.py
py -c "from services.database_service import DatabaseService; db = DatabaseService(); print(db.test_connection())"
```

### Test Complete System
```bash
# Start backend
py -m uvicorn main:app --reload --port 8000

# Test endpoints
curl "http://localhost:8000/health"
curl "http://localhost:8000/api/categories"
curl "http://localhost:8000/api/news?pageSize=2"

# Frontend (separate terminal)
cd frontend && npm run dev
# Visit: http://localhost:3000/explore
```

---

## Development Workflow

### Daily Development
```bash
# Terminal 1: Backend
cd backend && py -m uvicorn main:app --reload --port 8000

# Terminal 2: Frontend (with memory management)
cd frontend
Remove-Item -Recurse -Force .next -ErrorAction SilentlyContinue
$env:NODE_OPTIONS="--max-old-space-size=2048"
npm run dev
```

### Database Management
- **View data**: Use DB Browser for SQLite → open `backend/hopeshot_news.db`
- **Statistics**: Visit `http://localhost:8000/health`
- **Migration**: Run `py database_migration.py` when schema changes

---

## Troubleshooting

### Frontend Memory Issues
- Clear Next.js cache: `Remove-Item -Recurse -Force .next`
- Set memory limit: `$env:NODE_OPTIONS="--max-old-space-size=2048"`
- Close memory-intensive applications

### Database Issues
- **Locked database**: Close DB Browser, restart uvicorn
- **Categories not loading**: Check `/api/categories` endpoint
- **Missing M49 data**: Verify locations table has 278 rows

### API Connection Issues
- **Gemini**: Verify API key in `.env` file
- **Sheets**: Check service account permissions and spreadsheet sharing
- **News APIs**: Test individual sources via `/api/sources/test`

---

## Environment Variables (.env)
```bash
# Required
GEMINI_API_KEY=your_gemini_key
GOOGLE_SHEETS_ID=your_sheets_id

# Optional News Sources
NEWS_API_KEY=your_newsapi_key
NEWSDATA_API_KEY=your_newsdata_key
AFP_CLIENT_ID=your_afp_client
AFP_CLIENT_SECRET=your_afp_secret
AFP_USERNAME=your_afp_email
AFP_PASSWORD=your_afp_password

# Environment
ENVIRONMENT=development
```

---
*Setup version: 0.12.0*