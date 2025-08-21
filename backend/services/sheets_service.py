import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class SheetsService:
    """Service for logging article data to Google Sheets"""
    
    def __init__(self):
        self.credentials_file = os.getenv('GOOGLE_SHEETS_CREDENTIALS', 'gsheetapi_credentials.json')
        self.sheet_id = os.getenv('GOOGLE_SHEETS_ID')
        self.service = None
        self._connect()
    
    def _connect(self):
        """Initialize Google Sheets API connection"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_file,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.service = build('sheets', 'v4', credentials=credentials)
            print("✅ Google Sheets service connected")
        except Exception as e:
            print(f"❌ Failed to connect to Google Sheets: {e}")
            self.service = None
    
    
    def flatten_article_data(self, article: Dict[str, Any]) -> List[Any]:
        """Convert article with sentiment data into flat row for sheets"""
        
        # Basic article fields
        timestamp = datetime.now().isoformat()
        title = article.get('title', '')
        description = article.get('description', '')
        url = article.get('url', '')
        author = article.get('author', '')
        published_at = article.get('publishedAt', '')
        api_source = article.get('api_source', '')
        
        # Source information
        source_info = article.get('source', {})
        source_id = source_info.get('id', '') if source_info else ''
        source_name = source_info.get('name', '') if source_info else ''
        
        # Sentiment analysis data (if available)
        sentiment = article.get('sentiment_analysis', {})
        uplift_score = article.get('uplift_score', 0.0)
        
        if sentiment:
            # Sentiment scores
            sentiment_scores = sentiment.get('sentiment', {})
            positive = sentiment_scores.get('positive', 0.0)
            negative = sentiment_scores.get('negative', 0.0)
            neutral = sentiment_scores.get('neutral', 0.0)
            confidence = sentiment.get('confidence', 0.0)
            
            # Raw emotions
            raw_emotions = sentiment.get('raw_emotions', {})
            anger = raw_emotions.get('anger', 0.0)
            disgust = raw_emotions.get('disgust', 0.0)
            fear = raw_emotions.get('fear', 0.0)
            joy = raw_emotions.get('joy', 0.0)
            sadness = raw_emotions.get('sadness', 0.0)
            surprise = raw_emotions.get('surprise', 0.0)
            
            # Uplift emotions
            uplift_emotions = sentiment.get('uplift_emotions', {})
            hope = uplift_emotions.get('hope', 0.0)
            gratitude = uplift_emotions.get('gratitude', 0.0)
            awe = uplift_emotions.get('awe', 0.0)
            relief = uplift_emotions.get('relief', 0.0)
            compassion = uplift_emotions.get('compassion', 0.0)
            
        else:
            # No sentiment data available
            positive = negative = neutral = confidence = 0.0
            anger = disgust = fear = joy = sadness = surprise = 0.0
            hope = gratitude = awe = relief = compassion = 0.0
        
        # Return flattened row
        return [
            timestamp, title, description, url, author, published_at,
            api_source, source_id, source_name, uplift_score,
            positive, negative, neutral, confidence,
            anger, disgust, fear, joy, sadness, surprise,
            hope, gratitude, awe, relief, compassion
        ]
    
    def get_sheet_headers(self) -> List[str]:
        """Define the column headers for our data sheet"""
        return [
            'timestamp', 'title', 'description', 'url', 'author', 'published_at',
            'api_source', 'source_id', 'source_name', 'uplift_score',
            'sentiment_positive', 'sentiment_negative', 'sentiment_neutral', 'sentiment_confidence',
            'emotion_anger', 'emotion_disgust', 'emotion_fear', 'emotion_joy', 
            'emotion_sadness', 'emotion_surprise',
            'uplift_hope', 'uplift_gratitude', 'uplift_awe', 'uplift_relief', 'uplift_compassion'
        ]
    
    def setup_sheet_headers(self, sheet_name: str = 'Sheet1') -> bool:
        """Add headers to the sheet if they don't exist"""
        if not self.service:
            print("❌ No Google Sheets connection")
            return False
        
        try:
            headers = self.get_sheet_headers()
            
            # Write headers to first row
            body = {'values': [headers]}
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=f'{sheet_name}!A1:Y1',  # A1 to Y1 (25 columns)
                valueInputOption='RAW',
                body=body
            ).execute()
            
            print(f"✅ Headers setup complete: {result.get('updatedCells', 0)} cells updated")
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup headers: {e}")
            return False
    
    def log_articles(self, articles: List[Dict[str, Any]], sheet_name: str = 'Sheet1') -> bool:
        """Log multiple articles to Google Sheets"""
        if not self.service:
            print("❌ No Google Sheets connection")
            return False
        
        if not articles:
            print("ℹ️ No articles to log")
            return True
        
        try:
            # Flatten all articles into rows
            rows = []
            for article in articles:
                flattened_row = self.flatten_article_data(article)
                rows.append(flattened_row)
            
            # Append all rows to sheet
            body = {'values': rows}
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range=f'{sheet_name}!A:Y',  # Append to columns A through Y
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            rows_added = result.get('updates', {}).get('updatedRows', 0)
            print(f"✅ Logged {rows_added} articles to Google Sheets")
            return True
            
        except Exception as e:
            print(f"❌ Failed to log articles: {e}")
            return False


if __name__ == "__main__":

    # Test article with sentiment data
    test_article = {
        'title': 'Medical Breakthrough Offers Hope',
        'description': 'Scientists discover new treatment...',
        'api_source': 'newsapi',
        'uplift_score': 0.65,
        'sentiment_analysis': {
            'sentiment': {'positive': 0.8, 'negative': 0.1, 'neutral': 0.1},
            'confidence': 0.9,
            'raw_emotions': {'joy': 0.3, 'anger': 0.1},
            'uplift_emotions': {'hope': 0.4, 'gratitude': 0.2}
        }
    }

    sheets_service = SheetsService()

    # Setup headers
    sheets_service.setup_sheet_headers()

    # Log test article
    sheets_service.log_articles([test_article])