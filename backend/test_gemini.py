import asyncio
from services.gemini_service import GeminiService

async def test_gemini():
    service = GeminiService()
    
    # Check usage before test
    stats = service.get_usage_stats()
    print(f"Usage before test: {stats}")
    
    # Test connection
    result = await service.test_connection()
    print(f"Test result: {result}")
    
    # Check usage after test
    stats = service.get_usage_stats()
    print(f"Usage after test: {stats}")

if __name__ == "__main__":
    asyncio.run(test_gemini())