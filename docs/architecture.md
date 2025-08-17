# HopeShot Architecture

## Project Overview
HopeShot is designed as a learning-first project with simple, modular components that are easy to understand and extend.

## Technology Stack
- **Frontend**: Next.js (React framework) ✅ **Implemented**
  - TypeScript for type safety
  - Tailwind CSS for styling
  - Component-based architecture
- **Backend**: FastAPI (Python web framework)  ✅ **Implemented**
  - Uvicorn ASGI server
  - CORS middleware for cross-origin requests
  - Pydantic for data validation
- **AI/ML**: OpenAI API for sentiment analysis
- **Data Storage**: Google Sheets (for prototyping)
- **Version Control**: Git + GitHub ✅ **Active**

## Project Structure
hopeshot/
├── README.md                 # Project overview
├── CHANGELOG.md              # Version history
├── .env.example
├── docs/                     # Documentation
│   ├── api.md       
│   ├── architecture.md       # This file
│   └── setup.md    
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx      # Homepage component
│   │   │   └── test/         # API testing page
│   │   │       └── page.tsx  # Manual testing interface
│   │   └── components/       # Reusable React components
│   │       └── StatusBanner.tsx  # Status display component
│   ├── package.json          # Node.js dependencies
│   └── tailwind.config.js    # Styling configuration
├── backend/                  # FastAPI application
│   ├── main.py              # FastAPI app with endpoints
│   └── requirements.txt     # Python dependencies
└── scripts/                  # Utility scripts (empty)


## API Testing Strategy

### Manual Testing Interface
- **Location:** `http://localhost:3000/test`
- **Purpose:** Visual testing of backend API endpoints
- **Features:**
  - Interactive buttons for each endpoint
  - Real-time response display
  - Loading states and error handling

### Available Endpoints
- `GET /` - Root endpoint with basic API info
- `GET /api/test` - Connection test with sample data

### Development Servers
- **Frontend:** `npm run dev` on port 3000
- **Backend:** `py -m uvicorn main:app --reload --port 8000`


## Development Approach
1. **Documentation First** - Always document before coding
2. **Small Steps** - One feature at a time with testing
3. **Modular Design** - Each component has a single responsibility
4. **Learning Focus** - Code is optimized for understanding, not just performance

## Next Steps
- [x] Set up frontend structure (Next.js) ✅
- [x] Create first custom React component (StatusBanner) ✅
- [x] Implement component reusability and styling ✅
- [x] Set up backend structure (FastAPI) ✅
- [x] Create first API endpoints ✅
- [x] Build frontend-backend communication ✅
- [x] Create API testing interface ✅
- [ ] Integrate real news APIs
- [ ] Add sentiment analysis
- [ ] Connect to Google Sheets for data storage
---
*Created: 17/08/25*