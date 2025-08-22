import os
import asyncio
from typing import Dict, List, Any
from datetime import datetime, timedelta
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        """Initialize Gemini 2.5 Flash-Lite service optimized for large batches"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini 2.5 Flash-Lite
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')  # Correct 2.5 Flash-Lite model
        
        # Optimized limits for 2-minute batch strategy
        self.requests_per_minute = 14  # Conservative safety margin
        self.requests_per_day = 900
        self.tokens_per_minute = 220000
        self.max_articles_per_batch = 100
        self.target_batch_interval = 120  # 2 minutes in seconds
        
        # Simple tracking
        self.current_minute = datetime.now().minute
        self.requests_this_minute = 0
        self.tokens_this_minute = 0
        self.daily_requests = 0
        self.last_request_time = None
        self.last_reset_date = datetime.now().date()
        
        print(f"🚀 Gemini 2.5 Flash-Lite configured: {self.max_articles_per_batch} articles/batch, 2min intervals")
        print(f"🔒 Safety limits: {self.requests_per_minute}/min, {self.requests_per_day}/day")

    def _reset_counters_if_needed(self):
        """Reset minute and daily counters when time periods change"""
        now = datetime.now()
        current_minute = now.minute
        
        # Reset minute counters
        if current_minute != self.current_minute:
            self.current_minute = current_minute
            self.requests_this_minute = 0
            self.tokens_this_minute = 0
            print(f"🔄 Minute reset: {current_minute:02d}")
        
        # Reset daily counters
        today = now.date()
        if today > self.last_reset_date:
            self.daily_requests = 0
            self.last_reset_date = today
            print(f"🔄 Daily reset: {today}")

    def can_make_request(self, estimated_tokens: int = 10000) -> Dict[str, Any]:
        """Check if we can safely make a request with 2-minute pacing"""
        self._reset_counters_if_needed()
        now = datetime.now()
        
        # Check 2-minute interval pacing
        time_since_last = None
        can_proceed_timing = True
        if self.last_request_time:
            time_since_last = (now - self.last_request_time).total_seconds()
            can_proceed_timing = time_since_last >= self.target_batch_interval
        
        # Check rate limits
        requests_ok = self.requests_this_minute < self.requests_per_minute
        tokens_ok = (self.tokens_this_minute + estimated_tokens) <= self.tokens_per_minute
        daily_ok = self.daily_requests < self.requests_per_day
        
        can_proceed = can_proceed_timing and requests_ok and tokens_ok and daily_ok
        
        return {
            "can_proceed": can_proceed,
            "time_since_last_request": time_since_last,
            "seconds_until_next_allowed": max(0, self.target_batch_interval - (time_since_last or 0)) if time_since_last else 0,
            "requests_remaining_this_minute": self.requests_per_minute - self.requests_this_minute,
            "tokens_remaining_this_minute": self.tokens_per_minute - self.tokens_this_minute,
            "requests_remaining_today": self.requests_per_day - self.daily_requests,
            "blocking_reason": self._get_blocking_reason(can_proceed_timing, requests_ok, tokens_ok, daily_ok)
        }

    def _get_blocking_reason(self, timing_ok: bool, requests_ok: bool, tokens_ok: bool, daily_ok: bool) -> str:
        """Identify why a request would be blocked"""
        if not timing_ok:
            return "2-minute interval not reached"
        elif not requests_ok:
            return "Per-minute request limit"
        elif not tokens_ok:
            return "Per-minute token limit"
        elif not daily_ok:
            return "Daily request limit"
        else:
            return "All checks passed"

    def record_request(self, actual_tokens: int):
        """Record a completed request with exact usage"""
        now = datetime.now()
        self.requests_this_minute += 1
        self.tokens_this_minute += actual_tokens
        self.daily_requests += 1
        self.last_request_time = now

    def _create_analysis_prompt(self, articles: List[Dict]) -> str:
        """Create optimized prompt for large batches (up to 100 articles)"""
        article_count = len(articles)
        
        prompt = f"""Analyze these {article_count} news articles for comprehensive emotional and contextual analysis. Return a JSON array with exactly {article_count} objects, one per article.

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

Articles to analyze:
"""
        
        for i, article in enumerate(articles):
            title = article.get('title', '')[:200]  # Truncate very long titles
            description = article.get('description', '')[:300]  # Truncate long descriptions
            prompt += f"\nArticle {i}:\nTitle: {title}\nDescription: {description}\n"
            
        prompt += f"\nReturn JSON array with exactly {article_count} analysis objects. Keep responses concise."
        return prompt

    async def analyze_articles_batch(self, articles: List[Dict]) -> Dict[str, Any]:
        """
        Analyze articles in optimized 100-article batches with 2-minute pacing
        """
        try:
            if not articles:
                return {"status": "error", "message": "No articles provided"}
            
            total_articles = len(articles)
            all_results = []
            total_tokens_used = 0
            batch_number = 0
            
            # Process in batches of up to 100 articles
            for i in range(0, total_articles, self.max_articles_per_batch):
                batch = articles[i:i + self.max_articles_per_batch]
                batch_size = len(batch)
                batch_number += 1
                
                # Estimate tokens (conservative: 80 tokens per article + 1000 for prompt)
                estimated_tokens = batch_size * 80 + 1000
                
                print(f"📋 Preparing batch {batch_number}: {batch_size} articles")
                
                # Check if we can make this request
                status = self.can_make_request(estimated_tokens)
                if not status["can_proceed"]:
                    wait_time = status.get("seconds_until_next_allowed", 0)
                    if wait_time > 0 and status["blocking_reason"] == "2-minute interval not reached":
                        print(f"⏰ Waiting {wait_time:.0f} seconds for 2-minute interval...")
                        await asyncio.sleep(wait_time + 1)  # +1 second buffer
                        
                        # Re-check after waiting
                        status = self.can_make_request(estimated_tokens)
                    
                    if not status["can_proceed"]:
                        return {
                            "status": "partial_success",
                            "message": f"Rate limit reached after {len(all_results)} articles",
                            "blocking_reason": status["blocking_reason"],
                            "processed_articles": len(all_results),
                            "total_articles": total_articles,
                            "total_tokens_used": total_tokens_used,
                            "results": all_results
                        }
                
                print(f"🚀 Sending batch {batch_number} to Gemini ({batch_size} articles, ~{estimated_tokens} tokens)")
                
                # Make the request
                prompt = self._create_analysis_prompt(batch)
                response = self.model.generate_content(prompt)
                
                # Record exact usage
                actual_tokens = response.usage_metadata.total_token_count
                self.record_request(actual_tokens)
                total_tokens_used += actual_tokens
                
                # Parse results
                batch_results = self._parse_gemini_response(response.text, batch)
                all_results.extend(batch_results)
                
                tokens_per_article = actual_tokens / batch_size
                print(f"✅ Batch {batch_number} completed: {batch_size} articles, {actual_tokens} tokens ({tokens_per_article:.0f}/article)")
            
            return {
                "status": "success",
                "processed_articles": len(all_results),
                "total_articles": total_articles,
                "total_tokens_used": total_tokens_used,
                "average_tokens_per_article": total_tokens_used / len(all_results) if all_results else 0,
                "batches_processed": batch_number,
                "results": all_results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Analysis failed: {str(e)}"
            }

    def _parse_gemini_response(self, response_text: str, original_articles: List[Dict]) -> List[Dict]:
        """Parse Gemini's JSON response with robust error handling"""
        import json
        
        try:
            # Clean response text
            clean_text = response_text.strip()
            if clean_text.startswith('```json'):
                clean_text = clean_text[7:]
            if clean_text.endswith('```'):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()
            
            # Parse JSON
            parsed = json.loads(clean_text)
            if isinstance(parsed, list):
                return parsed
            else:
                return [parsed]
                
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed: {e}")
            print(f"Raw response preview: {response_text[:200]}...")
            
            # Fallback: create default responses
            return [{
                "article_index": i,
                "sentiment": "neutral",
                "confidence_score": 0.5,
                "emotions": {"hope": 0.0, "awe": 0.0, "gratitude": 0.0, "compassion": 0.0, "relief": 0.0, "joy": 0.0},
                "categories": ["unknown"],
                "source_credibility": "medium",
                "fact_checkable_claims": "unknown",
                "evidence_quality": "moderate",
                "controversy_level": "low",
                "solution_focused": "unknown",
                "age_appropriate": "all",
                "truth_seeking": "no",
                "geographic_scope": ["Unknown"],
                "country_focus": "None",
                "local_focus": "None",
                "geographic_relevance": "minimal",
                "overall_hopefulness": 0.0,
                "reasoning": "Parsing failed"
            } for i in range(len(original_articles))]

    async def test_connection(self) -> Dict[str, Any]:
        """Test Gemini 2.5 Flash-Lite connection"""
        try:
            response = self.model.generate_content("Hello! Please respond with 'Gemini 2.5 Flash-Lite connected' if you can hear me.")
            
            return {
                "status": "success",
                "message": "Gemini 2.5 Flash-Lite connected successfully",
                "response": response.text.strip(),
                "model": "gemini-2.0-flash-exp"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Gemini connection failed: {str(e)}"
            }

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        self._reset_counters_if_needed()
        now = datetime.now()
        
        time_since_last = None
        if self.last_request_time:
            time_since_last = (now - self.last_request_time).total_seconds()
        
        return {
            "requests_today": self.daily_requests,
            "requests_remaining_today": max(0, self.requests_per_day - self.daily_requests),
            "requests_this_minute": self.requests_this_minute,
            "tokens_this_minute": self.tokens_this_minute,
            "seconds_since_last_request": time_since_last,
            "can_make_request_now": self.can_make_request()["can_proceed"],
            "max_articles_per_batch": self.max_articles_per_batch
        }