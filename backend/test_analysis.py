import asyncio
from services.gemini_service import GeminiService

async def test_usage_tracking():
    """Test to see what usage data Gemini provides"""
    service = GeminiService()
    
    print("=== Testing Gemini Usage Tracking ===")
    
    # Test 1: Simple request to check response structure
    print("\n1. Testing simple request...")
    try:
        response = service.model.generate_content("Hello world, please respond briefly.")
        
        print(f"Response type: {type(response)}")
        print(f"Response attributes: {[attr for attr in dir(response) if not attr.startswith('_')]}")
        
        if hasattr(response, 'usage_metadata'):
            print(f"✅ Usage metadata found: {response.usage_metadata}")
        else:
            print("❌ No usage_metadata attribute found")
            
        print(f"Response text: {response.text}")
        
    except Exception as e:
        print(f"Error in simple test: {e}")
    
    # Test 2: Full article analysis to check token usage
    print("\n2. Testing article analysis...")
    
    test_articles = [
        {
            "title": "Scientists develop new cancer treatment showing promising results",
            "description": "Researchers at Stanford University have created a breakthrough therapy that helped 90% of patients in early trials"
        },
        {
            "title": "Local community raises $50,000 for homeless shelter", 
            "description": "Neighbors came together to support families in need during the winter months"
        }
    ]
    
    # Check usage before
    usage_before = service.get_usage_stats()
    print(f"Usage before analysis: {usage_before}")
    
    # Run analysis
    result = await service.analyze_articles_batch(test_articles)
    
    # Check usage after
    usage_after = service.get_usage_stats()
    print(f"Usage after analysis: {usage_after}")
    
    print(f"\nAnalysis result status: {result['status']}")
    if result['status'] == 'success' and result['results']:
        print(f"First article analysis sample:")
        first_result = result['results'][0]
        for key, value in first_result.items():
            print(f"  {key}: {value}")

async def test_analysis():
    """Original analysis test"""
    await test_usage_tracking()

if __name__ == "__main__":
    asyncio.run(test_analysis())