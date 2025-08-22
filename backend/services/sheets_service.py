import os
import json
from typing import Dict, List, Any
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

class SheetsService:
    def __init__(self):
        """Initialize Google Sheets service for Gemini analysis data"""
        self.credentials_file = 'gsheetapi_credentials.json'
        self.spreadsheet_id = os.getenv('GOOGLE_SHEETS_ID')
        
        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(f"Google Sheets credentials not found: {self.credentials_file}")
        
        if not self.spreadsheet_id:
            raise ValueError("GOOGLE_SHEETS_ID not found in environment variables")
        
        # Initialize Google Sheets API
        self.credentials = Credentials.from_service_account_file(
            self.credentials_file,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)
        
        print("📊 Google Sheets service initialized for unified Gemini analysis")

    def _flatten_article_with_gemini_analysis(self, article: Dict, gemini_analysis: Dict = None) -> Dict:
        """
        Flatten article + Gemini analysis into 37-column spreadsheet row
        Unified schema for all news with rich Gemini metadata
        """
        # Basic article data (9 columns)
        flattened = {
            'timestamp': datetime.now().isoformat(),
            'title': article.get('title', ''),
            'description': article.get('description', ''),
            'url': article.get('url', ''),
            'author': article.get('author', ''),
            'published_at': article.get('publishedAt', ''),
            'api_source': article.get('api_source', ''),
            'source_id': article.get('source', {}).get('id', ''),
            'source_name': article.get('source', {}).get('name', ''),
        }
        
        if gemini_analysis:
            # Gemini sentiment scores (5 columns)
            flattened.update({
                'uplift_score': gemini_analysis.get('overall_hopefulness', 0.0),
                'sentiment_positive': 1.0 if gemini_analysis.get('sentiment') == 'positive' else 0.0,
                'sentiment_negative': 1.0 if gemini_analysis.get('sentiment') == 'negative' else 0.0,
                'sentiment_neutral': 1.0 if gemini_analysis.get('sentiment') == 'neutral' else 0.0,
                'sentiment_confidence': gemini_analysis.get('confidence_score', 0.0),
            })
            
            # Gemini emotions (6 columns)
            emotions = gemini_analysis.get('emotions', {})
            flattened.update({
                'emotion_hope': emotions.get('hope', 0.0),
                'emotion_awe': emotions.get('awe', 0.0),
                'emotion_gratitude': emotions.get('gratitude', 0.0),
                'emotion_compassion': emotions.get('compassion', 0.0),
                'emotion_relief': emotions.get('relief', 0.0),
                'emotion_joy': emotions.get('joy', 0.0),
            })
            
            # Fact-checking metadata (3 columns)
            flattened.update({
                'source_credibility': gemini_analysis.get('source_credibility', ''),
                'fact_checkable_claims': gemini_analysis.get('fact_checkable_claims', ''),
                'evidence_quality': gemini_analysis.get('evidence_quality', ''),
            })
            
            # Content analysis (4 columns)
            flattened.update({
                'controversy_level': gemini_analysis.get('controversy_level', ''),
                'solution_focused': gemini_analysis.get('solution_focused', ''),
                'age_appropriate': gemini_analysis.get('age_appropriate', ''),
                'truth_seeking': gemini_analysis.get('truth_seeking', ''),
            })
            
            # Geographic data (4 columns)
            geographic_scope = gemini_analysis.get('geographic_scope', [])
            flattened.update({
                'geographic_scope': ', '.join(geographic_scope) if isinstance(geographic_scope, list) else str(geographic_scope),
                'country_focus': gemini_analysis.get('country_focus', ''),
                'local_focus': gemini_analysis.get('local_focus', ''),
                'geographic_relevance': gemini_analysis.get('geographic_relevance', ''),
            })
            
            # Enhanced analysis (3 columns)
            categories = gemini_analysis.get('categories', [])
            flattened.update({
                'categories': ', '.join(categories) if isinstance(categories, list) else str(categories),
                'reasoning': gemini_analysis.get('reasoning', ''),
                'analyzer_type': 'gemini',
            })
            
        else:
            # Fill with empty values when no Gemini analysis available
            empty_fields = [
                'uplift_score', 'sentiment_positive', 'sentiment_negative', 'sentiment_neutral', 'sentiment_confidence',
                'emotion_hope', 'emotion_awe', 'emotion_gratitude', 'emotion_compassion', 'emotion_relief', 'emotion_joy',
                'source_credibility', 'fact_checkable_claims', 'evidence_quality',
                'controversy_level', 'solution_focused', 'age_appropriate', 'truth_seeking',
                'geographic_scope', 'country_focus', 'local_focus', 'geographic_relevance',
                'categories', 'reasoning', 'analyzer_type'
            ]
            for field in empty_fields:
                flattened[field] = ''
        
        return flattened

    async def log_articles_with_gemini_analysis(self, articles_with_analysis: List[Dict]) -> Dict[str, Any]:
        """
        Log articles with their Gemini analysis to Google Sheets
        articles_with_analysis: List of {article: {...}, gemini_analysis: {...}}
        """
        try:
            if not articles_with_analysis:
                return {"status": "success", "logged_count": 0, "message": "No articles to log"}
            
            # Flatten all articles into spreadsheet rows
            rows = []
            for item in articles_with_analysis:
                article = item.get('article', {})
                analysis = item.get('gemini_analysis', {})
                flattened = self._flatten_article_with_gemini_analysis(article, analysis)
                # Convert to list in column order
                row = list(flattened.values())
                rows.append(row)
            
            # Append to sheet
            sheet_range = 'Sheet1!A:AK'  # 37 columns (A to AK)
            body = {'values': rows}
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=sheet_range,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logged_count = len(rows)
            print(f"📊 Logged {logged_count} articles with Gemini analysis to Google Sheets")
            
            return {
                "status": "success",
                "logged_count": logged_count,
                "total_articles": len(articles_with_analysis),
                "spreadsheet_id": self.spreadsheet_id
            }
            
        except Exception as e:
            print(f"❌ Google Sheets logging failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to log to Google Sheets: {str(e)}",
                "logged_count": 0
            }

    def create_header_row(self) -> Dict[str, Any]:
        """Create the header row for the unified Gemini analysis sheet"""
        headers = [
            # Basic article data (9)
            'timestamp', 'title', 'description', 'url', 'author', 'published_at', 
            'api_source', 'source_id', 'source_name',
            
            # Sentiment scores (5)
            'uplift_score', 'sentiment_positive', 'sentiment_negative', 'sentiment_neutral', 'sentiment_confidence',
            
            # Emotions (6)
            'emotion_hope', 'emotion_awe', 'emotion_gratitude', 'emotion_compassion', 'emotion_relief', 'emotion_joy',
            
            # Fact-checking (3)
            'source_credibility', 'fact_checkable_claims', 'evidence_quality',
            
            # Content analysis (4)
            'controversy_level', 'solution_focused', 'age_appropriate', 'truth_seeking',
            
            # Geographic (4)
            'geographic_scope', 'country_focus', 'local_focus', 'geographic_relevance',
            
            # Enhanced analysis (3)
            'categories', 'reasoning', 'analyzer_type',
            
            # Future expansion (3)
            'reserved1', 'reserved2', 'reserved3'
        ]
        
        try:
            # Clear existing content and add headers
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range='Sheet1!A:AZ'
            ).execute()
            
            # Add header row
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='Sheet1!A1:AN1',  # 40 columns for future expansion
                valueInputOption='RAW',
                body={'values': [headers]}
            ).execute()
            
            return {"status": "success", "message": f"Header row created with {len(headers)} columns"}
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create headers: {str(e)}"}