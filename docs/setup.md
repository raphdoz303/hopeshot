# HopeShot Setup Guide

Complete guide to get HopeShot running on your machine with Google Gemini AI integration.

---

## Prerequisites
- **Python 3.11+** (tested with 3.13.7)
- **Node.js 18+** (for Next.js)
- **Git** (for version control)
- **Google Cloud account** (for Gemini API access)
- **Google account** (for Google Sheets integration)

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

# Note: First run will download ML models (~500MB) for legacy transformers
# Test Gemini integration
py -c "import google.generativeai as genai; print('✅ Gemini library ready')"

# Start development server
py -m uvicorn main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

**Dependencies**:
- `fastapi>=0.68.0` - Web framework
- `uvicorn>=0.15.0` - ASGI server
- `python-dotenv>=0.19.0` - Environment variable management
- `aiohttp>=3.8.0` - Async HTTP client for concurrent API calls
- `google-generativeai>=0.3.0` - **NEW**: Google Gemini API client
- `google-api-python-client>=2.0.0` - Google Sheets API access
- `google-auth>=2.0.0` - Google authentication libraries
- `transformers>=4.21.0` - Hugging Face models (backup/legacy)
- `torch>=1.13.0` - PyTorch neural network backend (backup)
- `nltk>=3.8.0` - VADER sentiment analyzer (backup)
- `datasets>=2.0.0` - Model download support (backup)

### 3. Frontend Setup (Next.js/React)
```bash
# From project root
cd frontend

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

---

## API Configuration

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

## Verification

### Test Backend Endpoints
Visit these URLs in your browser:
- `http://localhost:8000/` - Root endpoint (should show v0.6.0)
- `http://localhost:8000/health` - System health check with Gemini status
- `http://localhost:8000/api/sources` - Source configuration with Gemini integration
- `http://localhost:8000/api/sources/test` - Source connectivity including Gemini

### Test Gemini Integration
```bash
# Test Gemini API connection
cd backend
py test_gemini.py

# Test Gemini analysis functionality  
py test_analysis.py

# Test complete pipeline
py test_full_pipeline.py

# Test Google Sheets integration
py test_sheets_gemini.py
```

### Test Frontend
- `http://localhost:3000/` - Homepage
- `http://localhost:3000/test` - API testing interface with Gemini analysis

### Test Complete System
```bash
# Test all integrations
curl http://localhost:8000/api/sources/test

# Test unified news with Gemini analysis (will take 30-60 seconds)
curl "http://localhost:8000/api/news?pageSize=5" 

# Test Gemini usage stats
curl http://localhost:8000/api/gemini/usage
```

**Expected Results**:
- All news sources should show success
- Gemini should show "connected successfully"
- Articles should include comprehensive `gemini_analysis` field
- Google Sheets should receive new rows with 37 columns of data
- Response should show `gemini_analyzed: true` and `sheets_logged: true`

---

## Development Workflow

### Starting Development Session
```bash
# Terminal 1: Backend  
cd backend
py -m uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Making Changes
1. Edit code files
2. Servers automatically restart (hot reload enabled)
3. Test changes in browser
4. Check Google Sheets for data logging
5. Monitor Gemini usage with test commands
6. Commit when feature is complete

---

## Troubleshooting

### Common Issues

**Gemini API Issues**:
- Verify API key is correct in `.env`
- Check quota usage: `py test_gemini.py`
- Ensure Google Cloud project has Gemini enabled
- Rate limit errors: Wait 2 minutes between large requests

**Google Sheets Issues**:
- Verify service account JSON file is in `backend/` directory
- Check that service account email has edit access to your sheet
- Ensure `GOOGLE_SHEETS_ID` matches your spreadsheet URL

**Python/pip not found**:
- Use `py` instead of `python`
- Use `py -m pip` instead of `pip`

**Package installation errors**:
- Update `requirements.txt` to use `>=` instead of `==` for version flexibility
- Some packages require specific Python versions

**CORS errors in browser**:
- Ensure backend CORS middleware allows `http://localhost:3000`
- Check that both servers are running

**Port conflicts**:
- Backend: Change `--port 8000` to another port
- Frontend: Next.js will auto-suggest alternative ports

**Slow first request**:
- Gemini analysis takes 30-60 seconds for batch processing
- This is normal for 100-article batches
- Legacy transformers models may download on first run (~500MB)

### Performance Monitoring

**Gemini Usage Tracking**:
```bash
# Check current usage
py -c "
from services.gemini_service import GeminiService
import asyncio
async def check():
    service = GeminiService()
    print(service.get_usage_stats())
asyncio.run(check())
"
```

**Google Sheets Verification**:
- Check your spreadsheet for new rows after running tests
- Verify all 37 columns are populated with analysis data
- Look for `analyzer_type: gemini` in the data

### Testing Comprehensive Analysis
```bash
# Test with diverse article types
py test_full_pipeline.py

# Expected: Different sentiment scores for positive vs negative articles
# Expected: Rich emotion analysis (hope, awe, gratitude, etc.)
# Expected: Geographic analysis and category detection
# Expected: Fact-checking readiness assessment
```

### Memory and Performance
- **Gemini requests**: 30-60 seconds for 100 articles (normal)
- **Memory usage**: ~1-2GB for full system (Gemini + legacy models)
- **Token tracking**: Exact usage displayed in test outputs
- **Rate limiting**: Conservative 2-minute intervals prevent quota issues

### Getting Help
- Check browser developer console for frontend errors
- Check terminal output for backend errors  
- Use the test page at `/test` to isolate API issues
- Monitor Google Sheets for data pipeline verification
- Check Gemini usage stats if experiencing rate limits

---

## Production Considerations

### Environment Variables
Ensure all required environment variables are set:
- `GEMINI_API_KEY` - Google Gemini API access
- `GOOGLE_SHEETS_ID` - Target spreadsheet ID
- `NEWS_API_KEY` - NewsAPI.org access
- `NEWSDATA_API_KEY` - NewsData.io access
- `AFP_CLIENT_ID`, `AFP_CLIENT_SECRET`, `AFP_USERNAME`, `AFP_PASSWORD` - AFP access

### Security
- Keep `gsheetapi_credentials.json` secure and never commit to version control
- Rotate API keys periodically
- Monitor usage to prevent quota violations
- Use environment-specific configuration files

### Scaling
- Current capacity: 72,000 articles/day
- Typical usage: ~5,000 articles/day
- 13x headroom for growth
- Google Sheets suitable for prototype; consider database for production

---

*Last updated: August 22, 2025*  
*Ready to build comprehensive AI-powered news analysis!*