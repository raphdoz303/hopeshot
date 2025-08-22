import asyncio
from services.sheets_service import SheetsService

async def test_sheets_setup():
    sheets = SheetsService()
    
    # Test header creation
    result = sheets.create_header_row()
    print(f"Header creation: {result}")
    
    # Test with sample data
    sample_data = [{
        'article': {
            'title': 'Test Article',
            'description': 'Test description',
            'url': 'https://example.com',
            'api_source': 'test'
        },
        'gemini_analysis': {
            'sentiment': 'positive',
            'confidence_score': 0.8,
            'emotions': {'hope': 0.7, 'joy': 0.6},
            'categories': ['test'],
            'overall_hopefulness': 0.75
        }
    }]
    
    result = await sheets.log_articles_with_gemini_analysis(sample_data)
    print(f"Test logging: {result}")

if __name__ == "__main__":
    asyncio.run(test_sheets_setup())