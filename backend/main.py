# Main FastAPI application for HopeShot backend

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI application instance
app = FastAPI(
    title="HopeShot API",
    description="Backend API for the HopeShot positive news app",
    version="0.1.0"
)

# Add CORS middleware so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your first API endpoint
@app.get("/")
async def read_root():
    return {
        "message": "Hello from HopeShot backend! 🌟",
        "status": "running",
        "version": "0.1.0"
    }

# Test endpoint for frontend-backend connection
@app.get("/api/test")
async def test_connection():
    return {
        "message": "Backend connection successful!",
        "data": {
            "timestamp": "2024-01-01",
            "backend_status": "healthy"
        }
    }