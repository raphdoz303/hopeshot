# HopeShot Setup Guide

Complete guide to get HopeShot running on your machine.

---

## Prerequisites
- **Python 3.11+** (tested with 3.13.7)
- **Node.js 18+** (for Next.js)
- **Git** (for version control)

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

# Note: First run will download ML models (~500MB)
# Test sentiment analysis installation
py -c "import transformers; import torch; print('✅ Sentiment analysis ready')"

# Start development server
py -m uvicorn main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

**Dependencies**:
- `fastapi>=0.68.0` - Web framework
- `uvicorn>=0.15.0` - ASGI server
- `python-dotenv>=0.19.0` - Environment variable management
- `aiohttp>=3.8.0` - Async HTTP client for concurrent API calls
- `transformers>=4.21.0` - Hugging Face sentiment + emotion models
- `torch>=1.13.0` - PyTorch neural network backend
- `nltk>=3.8.0` - VADER sentiment analyzer (future use)
- `datasets>=2.0.0` - Model download support

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

## News API Configuration

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
- `http://localhost:8000/` - Root endpoint
- `http://localhost:8000/health` - System health check
- `http://localhost:8000/api/sources` - Source configuration
- `http://localhost:8000/api/sources/test` - Source connectivity

### Test Frontend
- `http://localhost:3000/` - Homepage
- `http://localhost:3000/test` - API testing interface

### Test Multi-Source System
```bash
# Test source availability
curl http://localhost:8000/api/sources

# Test source connections
curl http://localhost:8000/api/sources/test

# Test unified news aggregation (currently 2/3 sources active)
curl "http://localhost:8000/api/news?pageSize=5" 

# Test specific source (for debugging)
curl http://localhost:8000/api/news/afp?pageSize=2
```

**Expected Results**:
- NewsAPI + NewsData should show success
- AFP should authenticate successfully but return 0 articles (pending subscription)
- Articles should include `api_source` field
- Response should show `sourcesUsed` and `sourcesFailed` arrays

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
4. Commit when feature is complete

---

## Troubleshooting

### Common Issues

**Python/pip not found**:
- Use `py` instead of `python`
- Use `py -m pip` instead of `pip`

**Package installation errors**:
- Update `requirements.txt` to use `>=` instead of `==` for version flexibility

**CORS errors in browser**:
- Ensure backend CORS middleware allows `http://localhost:3000`
- Check that both servers are running

**Port conflicts**:
- Backend: Change `--port 8000` to another port
- Frontend: Next.js will auto-suggest alternative ports

### Getting Help
- Check browser developer console for frontend errors
- Check terminal output for backend errors  
- Use the test page at `/test` to isolate API issues


## Testing Sentiment Analysis
bash# Test sentiment service directly
py test_sentiment.py

### Test API integration
curl "http://localhost:8000/api/news?pageSize=3"

Expected: Articles include sentiment_analysis field with uplift_score

### Updated Frontend Testing
Visit http://localhost:3000/test for enhanced testing interface:

Test API Health - Basic connectivity check
Test All Sources - Source configuration and connectivity
Get Unified News - Multi-source news with sentiment analysis
Test NewsAPI Only - Filtered NewsAPI results
Test NewsData Only - Filtered NewsData results
Test AFP Only - Direct AFP endpoint testing

### Troubleshooting Sentiment Analysis:

Slow first request: Models downloading (~2-3 minutes initial setup)
High memory usage: Transformers models require ~1GB RAM
Missing sentiment data: Check that articles are from NewsAPI/NewsData (not AFP)

---

*Last updated: August 20, 2025*  
*Ready to build something amazing!*