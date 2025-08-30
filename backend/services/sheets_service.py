# services/sheets_service.py
import os
import json
from typing import List, Dict, Any, Optional
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv

class SheetsService:
    def __init__(self):
        """Initialize Google Sheets service with service account authentication"""
        load_dotenv()
        self.credentials_file = os.getenv('GOOGLE_SHEETS_CREDENTIALS', 'gsheetapi_credentials.json')
        self.spreadsheet_id = os.getenv('GOOGLE_SHEETS_ID')
        self.service = None
        
        if not self.spreadsheet_id:
            raise ValueError("GOOGLE_SHEETS_ID environment variable not set")
        
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Sheets API using service account"""
        try:
            # Define the scopes
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            
            # Load credentials from JSON file
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_file, 
                scopes=SCOPES
            )
            
            # Build the service
            self.service = build('sheets', 'v4', credentials=credentials)
            print("Google Sheets authenticated successfully")
            
        except Exception as e:
            print(f"Google Sheets authentication failed: {e}")
            raise

    def flatten_article_for_sheets(self, article: Dict[str, Any], gemini_analysis: Dict[str, Any], 
                                 prompt_version: str = None, prompt_name: str = None) -> List[Any]:
        """
        Convert article + analysis data into flat row for Google Sheets
        Handles new geographic array format and 40-column schema
        """
        
        # Extract emotions
        emotions = gemini_analysis.get('emotions', {})
        
        # Handle geographic arrays - convert to string for sheets storage
        geographical_impact_level = gemini_analysis.get('geographical_impact_level', '')
        geographical_impact_location = gemini_analysis.get('geographical_impact_location_names', [])
        
        # Convert location array to comma-separated string
        if isinstance(geographical_impact_location, list):
            location_str = ', '.join(geographical_impact_location)
        else:
            location_str = str(geographical_impact_location) if geographical_impact_location else ''
        
        # Build the flattened row (40 columns matching updated GSheets schema)
        row = [
            # Basic Article Data (12 columns)
            article.get('publishedAt', ''),           # timestamp
            article.get('title', ''),                 # title  
            article.get('description', ''),           # description
            article.get('url', ''),                   # Url_ID
            article.get('author', ''),                # Author
            article.get('publishedAt', ''),           # Published_at
            article.get('language', 'en'),            # Language
            article.get('news_type', 'article'),      # News_Type  
            article.get('source_type', 'api'),        # Source_Type
            article.get('source', {}).get('name', ''), # Source_Name
            article.get('source', {}).get('id', ''),   # Source_ID
            article.get('api_source', ''),            # Original_Source
            
            # Sentiment Analysis (5 columns)
            gemini_analysis.get('overall_hopefulness', 0.0),  # uplift_score
            1 if gemini_analysis.get('sentiment') == 'positive' else 0,  # sentiment_positive
            1 if gemini_analysis.get('sentiment') == 'negative' else 0,  # sentiment_negative  
            1 if gemini_analysis.get('sentiment') == 'neutral' else 0,   # sentiment_neutral
            gemini_analysis.get('confidence_score', 0.0),    # sentiment_confidence
            
            # Target Emotions (6 columns)
            emotions.get('hope', 0.0),                # emotion_hope
            emotions.get('awe', 0.0),                 # emotion_awe
            emotions.get('gratitude', 0.0),           # emotion_gratitude
            emotions.get('compassion', 0.0),          # emotion_compassion
            emotions.get('relief', 0.0),              # emotion_relief
            emotions.get('joy', 0.0),                 # emotion_joy
            
            # Fact-checking Readiness (3 columns)
            gemini_analysis.get('source_credibility', ''),   # source_credibility
            gemini_analysis.get('fact_checkable_claims', ''), # fact_checkable_claims
            gemini_analysis.get('evidence_quality', ''),     # evidence_quality
            
            # Content Analysis (4 columns)
            gemini_analysis.get('controversy_level', ''),    # controversy_level
            gemini_analysis.get('solution_focused', ''),     # solution_focused
            gemini_analysis.get('age_appropriate', ''),      # age_appropriate
            gemini_analysis.get('truth_seeking', ''),        # truth_seeking
            
            # Geographic Analysis (2 columns) - UPDATED FIELDS
            geographical_impact_level,                # geographical_impact_level
            location_str,                            # geographical_impact_location (converted from array)
            
            # Enhanced Metadata (3 columns)
            self._format_categories(gemini_analysis.get('categories', [])), # categories
            gemini_analysis.get('reasoning', ''),            # reasoning
            gemini_analysis.get('analyzer_type', 'gemini'),  # analyzer_type
            
            # A/B Testing Tracking (3 columns)
            prompt_version or '',                     # Prompt_ID
            prompt_name or '',                        # Prompt_Name
            
            # Reserved fields for future expansion (3 columns)
            '',                                       # reserved1
            '',                                       # reserved2  
            '',                                       # reserved3
        ]
        
        return row

    def _format_categories(self, categories: List[str]) -> str:
        """Format categories list as JSON string for storage"""
        if isinstance(categories, list):
            return json.dumps(categories)
        elif isinstance(categories, str):
            return categories
        else:
            return '[]'

    async def log_articles_with_gemini_analysis(self, articles_with_analysis: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Log articles with their Gemini analysis to Google Sheets
        Expected format: [{"article": {...}, "gemini_analysis": {...}}, ...]
        This is the method main.py is calling
        """
        try:
            if not articles_with_analysis:
                return {"status": "success", "logged_count": 0, "message": "No articles to log"}
            
            # Convert to rows format
            rows = []
            for item in articles_with_analysis:
                article = item.get('article', {})
                analysis = item.get('gemini_analysis', {})
                
                # Extract prompt info from analysis
                prompt_version = analysis.get('prompt_version', '')
                prompt_name = analysis.get('prompt_name', '')
                
                # Flatten to sheet row
                row = self.flatten_article_for_sheets(article, analysis, prompt_version, prompt_name)
                rows.append(row)
            
            # Append to sheet
            sheet_range = 'Sheet1!A:AN'  # 40 columns (A to AN)
            body = {
                'values': rows,
                'majorDimension': 'ROWS'
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=sheet_range,
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            updates = result.get('updates', {})
            updated_rows = updates.get('updatedRows', 0)
            
            print(f"Logged {updated_rows} articles to Google Sheets")
            
            return {
                "status": "success",
                "logged_count": updated_rows,
                "total_articles": len(articles_with_analysis),
                "spreadsheet_id": self.spreadsheet_id
            }
            
        except Exception as e:
            print(f"Error logging to Google Sheets: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to log to Google Sheets: {str(e)}",
                "logged_count": 0
            }

    def log_articles_batch(self, articles: List[Dict[str, Any]], prompt_version: str = None, prompt_name: str = None) -> Dict[str, Any]:
        """
        Legacy method - now calls the main logging method
        """
        # Convert to expected format
        articles_with_analysis = []
        for article in articles:
            # Assume gemini_analysis is attached to article
            analysis = article.get('gemini_analysis', {})
            articles_with_analysis.append({
                'article': article,
                'gemini_analysis': analysis
            })
        
        import asyncio
        return asyncio.run(self.log_articles_with_gemini_analysis(articles_with_analysis))

    def get_existing_urls(self) -> set:
        """
        Get all existing URLs from Google Sheets for deduplication
        Returns set of URLs that already exist
        """
        try:
            # Read the URL column (column D - Url_ID)
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range="Sheet1!D:D"
            ).execute()
            
            values = result.get('values', [])
            
            # Extract URLs, skip header row
            existing_urls = set()
            for row in values[1:]:  # Skip header
                if row and row[0]:  # Check if URL exists and is not empty
                    existing_urls.add(row[0])
            
            print(f"Found {len(existing_urls)} existing URLs in sheets")
            return existing_urls
            
        except Exception as e:
            print(f"Error reading existing URLs: {e}")
            return set()

    def test_connection(self) -> Dict[str, Any]:
        """Test Google Sheets connection and return status"""
        try:
            # Try to get spreadsheet metadata
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            title = sheet_metadata.get('properties', {}).get('title', 'Unknown')
            sheets = sheet_metadata.get('sheets', [])
            sheet_count = len(sheets)
            
            return {
                "success": True,
                "message": f"Connected to '{title}' with {sheet_count} sheets",
                "spreadsheet_title": title,
                "sheet_count": sheet_count,
                "schema_version": "v3.0_multi_location"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}"
            }

    def create_header_row(self) -> Dict[str, Any]:
        """Create the header row for the unified multi-location analysis sheet"""
        headers = [
            # Basic article data (12)
            'timestamp', 'title', 'description', 'url_id', 'author', 'published_at', 
            'language', 'news_type', 'source_type', 'source_name', 'source_id', 'original_source',
            
            # Sentiment scores (5)
            'uplift_score', 'sentiment_positive', 'sentiment_negative', 'sentiment_neutral', 'sentiment_confidence',
            
            # Emotions (6)
            'emotion_hope', 'emotion_awe', 'emotion_gratitude', 'emotion_compassion', 'emotion_relief', 'emotion_joy',
            
            # Fact-checking (3)
            'source_credibility', 'fact_checkable_claims', 'evidence_quality',
            
            # Content analysis (4)
            'controversy_level', 'solution_focused', 'age_appropriate', 'truth_seeking',
            
            # Geographic (2) - Updated schema
            'geographical_impact_level', 'geographical_impact_location',
            
            # Enhanced analysis (3)
            'categories', 'reasoning', 'analyzer_type',
            
            # A/B Testing (2)
            'prompt_id', 'prompt_name',
            
            # Future expansion (3)
            'reserved1', 'reserved2', 'reserved3'
        ]
        
        try:
            # Clear existing content and add headers
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range='Sheet1!A:AN'
            ).execute()
            
            # Add header row
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='Sheet1!A1:AN1',  # 40 columns
                valueInputOption='RAW',
                body={'values': [headers]}
            ).execute()
            
            return {"status": "success", "message": f"Header row created with {len(headers)} columns"}
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create headers: {str(e)}"}