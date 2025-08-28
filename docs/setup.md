# HopeShot Setup Guide

Complete guide to get HopeShot running on your machine with Google Gemini AI integration and multi-prompt A/B testing framework.

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

# Test YAML configuration
py -c "import yaml; print('✅ YAML library ready')"

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
- `pyyaml>=6.0.0` - **NEW**: YAML configuration file parsing for A/B testing
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

### Source Configuration Setup

1. **Configure News Sources**
   ```bash
   # Edit backend/sources.yaml to enable/disable sources
   # Set active: true/false for each source
   # Adjust quality_score and daily_limit as needed
   ```

2. **AFP Specific Configuration**
   - AFP uses "inspiring" genre filter (highly curated, ~4-10 articles/week)
   - To get more articles, consider:
     - Extending date range in `afp_client.py`: `"from": "now-30d"`
     - Removing genre filter (will require own quality filtering)
     - Enabling additional sources in `sources.yaml`

### Performance Optimization Note

The system now uses optimized multi-prompt analysis:
- All prompts analyzed in single request (~10 seconds total)
- 2-minute spacing only between different article batches
- To adjust prompt count, edit `prompts.yaml` and set `active: true/false`

---

## A/B Testing Configuration

### Create prompts.yaml File
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
      "article_index": 0,
      "sentiment": "positive/negative/neutral",
      "confidence_score": 0.85,
      "emotions": {{
        "hope": 0.8,
        "awe": 0.6,
        "gratitude": 0.4,
        "compassion": 0.7,
        "relief": 0.3,
        "joy": 0.5
      }},
      "categories": ["medical", "technology"],
      "source_credibility": "high",
      "fact_checkable_claims": "yes",
      "evidence_quality": "strong",
      "controversy_level": "low",
      "solution_focused": "yes",
      "age_appropriate": "all",
      "truth_seeking": "no",
      "geographic_scope": ["World"],
      "country_focus": "None",
      "local_focus": "None",
      "geographic_relevance": "primary",
      "overall_hopefulness": 0.75,
      "reasoning": "Brief 5-word summary"
    }}

    EMOTION FOCUS: hope, awe, gratitude, compassion, relief, joy (0.0-1.0)
    CATEGORIES: Suggest 1-3 organically (medical, tech, environment, social, etc.)
    REASONING: Maximum 5 words to minimize tokens

v2_emotion_focused:
  name: "Emotion-Focused Analysis" 
  active: true
  description: "Shorter prompt focused primarily on emotional scoring"
  prompt: |
    Analyze these {article_count} news articles focusing on emotional impact. Return JSON array with {article_count} objects.

    Focus on these emotions (0.0-1.0): hope, awe, gratitude, compassion, relief, joy
    
    Required format per article:
    {{
      "article_index": 0,
      "sentiment": "positive/negative/neutral",
      "confidence_score": 0.85,
      "emotions": {{
        "hope": 0.8,
        "awe": 0.6,
        "gratitude": 0.4,
        "compassion": 0.7,
        "relief": 0.3,
        "joy": 0.5
      }},
      "overall_hopefulness": 0.75,
      "reasoning": "Brief summary"
    }}

v3_experimental:
  name: "Experimental Prompt"
  active: false
  description: "Test prompt for experimentation"  
  prompt: |
    [Your experimental prompt here - modify as needed for testing]
```

---

## Verification

### Test Backend Endpoints
Visit these URLs in your browser:
- `http://localhost:8000/` - Root endpoint (should show v0.7.0)
- `http://localhost:8000/health` - System health check with A/B testing status
- `http://localhost:8000/api/sources` - Source configuration with multi-prompt information
- `http://localhost:8000/api/sources/test` - Source connectivity including Gemini A/B testing

### Test A/B Testing Framework
```bash
# Test YAML configuration loading
cd backend
py -c "
from services.gemini_service import GeminiService
service = GeminiService()
prompts = service.load_prompt_config()
print('Active prompts:', list(prompts.keys()))
for version, config in prompts.items():
    print(f'- {version}: {config.get(\"name\", \"Unknown\")}')
"

# Test Gemini API connection
py test_gemini.py

# Test multi-prompt analysis functionality  
py test_analysis.py

# Test complete pipeline with A/B testing
py test_full_pipeline.py

# Test Google Sheets integration with comparative data
py test_sheets_gemini.py
```

### Test Frontend
- `http://localhost:3000/` - Homepage
- `http://localhost:3000/test` - API testing interface with multi-prompt analysis results

### Test Complete Multi-Prompt System
```bash
# Test all integrations including A/B testing
curl http://localhost:8000/api/sources/test

# Test unified news with multi-prompt analysis (will take 60-120 seconds for 2 prompts)
curl "http://localhost:8000/api/news?pageSize=3" 

# Check Google Sheets for comparative data (should see 6 rows: 3 articles × 2 prompts)
```

**Expected Results**:
- All news sources should show success
- Gemini should show "Multi-prompt A/B testing framework ready"
- Articles should include comprehensive `gemini_analysis` field
- Google Sheets should receive multiple rows per article with prompt version tracking
- Response should show `prompt_versions: ["v1_comprehensive", "v2_emotion_focused"]`
- `sheets_logged: true` and `total_logged` should equal articles × active prompts

---

## A/B Testing Usage

### Basic Usage
1. **Edit prompts.yaml** - Modify prompt text, add new versions, or activate/deactivate prompts
2. **Run API calls** - Each article will be analyzed by all active prompts
3. **Review Google Sheets** - See side-by-side comparison of different prompt analyses for identical articles
4. **Iterate and improve** - Refine prompts based on quality comparison

### Systematic Optimization Workflow
1. **Establish baseline** - Start with one proven prompt as baseline
2. **Create variations** - Add experimental prompts with `active: true`
3. **Collect comparative data** - Run `/api/news` with diverse articles
4. **Evaluate quality** - Review Google Sheets for analysis quality comparison
5. **Select best prompts** - Identify highest-performing prompts for production use

### Configuration Management
```bash
# Activate a new prompt for testing
# Edit prompts.yaml: change "active: false" to "active: true"

# Test specific prompt combinations
# Deactivate prompts you don't want to test by setting "active: false"

# Add new experimental prompts
# Copy existing prompt structure and modify content
```

---

## Development Workflow

### Starting Development Session
```bash
# Terminal 1: Backend with A/B testing 
cd backend
py -m uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Making Changes to Prompts
1. Edit `backend/prompts.yaml` file
2. No server restart required - configuration loads dynamically
3. Test changes with new API calls
4. Check Google Sheets for comparative analysis results
5. Monitor token usage and processing time

### Making Code Changes
1. Edit code files
2. Servers automatically restart (hot reload enabled)
3. Test changes in browser
4. Verify A/B testing functionality with test commands
5. Commit when feature is complete

---

## Troubleshooting

### Common Issues

**YAML Configuration Issues**:
- Verify `prompts.yaml` is in the `backend/` directory
- Check YAML syntax with online validator if getting parsing errors
- Ensure proper indentation (spaces, not tabs)
- Verify `active: true` for prompts you want to test

**Multi-Prompt Processing Slow**:
- Expected behavior: 2-3x slower than single prompt
- Each active prompt processes all articles sequentially
- 2-minute intervals between batches for rate limiting
- Disable unused prompts to improve performance

**Google Sheets Missing Comparative Data**:
- Check that multiple rows appear per article (one per active prompt)
- Verify `reserved1` and `reserved2` columns show prompt versions and names
- Ensure service account has edit permissions
- Check for sheets logging errors in API response

**Prompt Not Loading**:
- Verify prompt is set to `active: true` in YAML
- Check terminal output for YAML loading messages
- Test prompt loading with: `py -c "from services.gemini_service import GeminiService; print(GeminiService().load_prompt_config())"`

**Rate Limiting Issues**:
- Multi-prompt analysis uses 2x+ API calls
- Wait times are normal and protect against quota violations
- Monitor usage with test scripts
- Consider reducing number of active prompts for faster testing

### A/B Testing Verification

**Check Prompt Loading**:
```bash
py -c "
from services.gemini_service import GeminiService
service = GeminiService()
prompts = service.load_prompt_config()
print('✅ Loaded prompts:', list(prompts.keys()))
"
```

**Verify Comparative Data in Sheets**:
- Look for multiple rows per article
- Check `reserved1` column for prompt versions (e.g., "v1_comprehensive")
- Check `reserved2` column for prompt names (e.g., "Current Comprehensive Analysis")
- Same article should have different analysis results from different prompts

**Monitor Multi-Prompt Processing**:
```bash
# Watch terminal output during API calls for:
# - "📝 Loaded X active prompts: [list]"
# - "🔄 Starting multi-prompt analysis: X prompts × Y articles"
# - "📋 Analyzing with [prompt_version]: [prompt_name]"
# - "✅ [prompt_version] completed: X articles, Y tokens"
```

### Performance Optimization

**Prompt Efficiency**:
- Shorter prompts use fewer tokens and process faster
- Remove unnecessary fields from prompts you're testing
- Focus on specific aspects you want to optimize

**Active Prompt Management**:
- Only keep prompts active that you're actively comparing
- Disable experimental prompts when not testing: `active: false`
- Use 2-3 active prompts maximum for regular development

**Batch Size Optimization**:
- Smaller `pageSize` values process faster for testing
- Use `pageSize=1` for rapid prompt iteration
- Use larger batches for comprehensive data collection

### Getting Help
- Check browser developer console for frontend errors
- Check terminal output for backend errors and A/B testing logs
- Use the test page at `/test` to isolate API issues
- Monitor Google Sheets for comparative data verification
- Check Gemini usage stats if experiencing rate limits
- Verify YAML syntax if prompts aren't loading

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
- Keep `prompts.yaml` in version control for collaborative prompt development
- Rotate API keys periodically
- Monitor usage to prevent quota violations with multi-prompt processing

### Scaling for Production
- **Current capacity**: ~24,000 articles/day with 2 active prompts
- **A/B testing overhead**: 2-3x processing time for comparative analysis
- **Production strategy**: Use A/B testing to identify best prompt, then single-prompt for scale
- **Data collection**: Multi-prompt comparative data enables systematic optimization

### A/B Testing Best Practices
- **Start with baseline**: Keep one proven prompt as control group
- **Systematic changes**: Modify one aspect at a time for clear comparison
- **Sufficient data**: Test prompts on diverse article types and topics
- **Quality criteria**: Develop consistent evaluation standards
- **Documentation**: Track prompt changes and performance insights

---

*Last updated: August 25, 2025*  
*Ready for multi-prompt A/B testing and systematic prompt optimization!*