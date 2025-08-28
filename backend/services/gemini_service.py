import os
import asyncio
from typing import Dict, List, Any
from datetime import datetime, timedelta
import google.generativeai as genai
from dotenv import load_dotenv
import yaml
from pathlib import Path
import json

load_dotenv()

class GeminiService:
    def __init__(self):
        """Initialize Gemini 2.5 Flash-Lite service optimized for multi-prompt single requests"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini 2.5 Flash-Lite
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        # Rate limits
        self.requests_per_minute = 14
        self.requests_per_day = 900
        self.tokens_per_minute = 220000
        self.max_articles_per_batch = 100
        self.target_batch_interval = 120  # 2 minutes between different batches
        
        # Tracking
        self.current_minute = datetime.now().minute
        self.requests_this_minute = 0
        self.tokens_this_minute = 0
        self.daily_requests = 0
        self.last_request_time = None
        self.last_reset_date = datetime.now().date()
        
        print(f"🚀 Gemini 2.5 Flash-Lite configured: Multi-prompt single request mode")
        print(f"🔒 Safety limits: {self.requests_per_minute}/min, {self.requests_per_day}/day")

    def load_prompt_config(self) -> Dict[str, Any]:
        """Load prompt configurations from yaml file"""
        try:
            prompts_file = Path(__file__).parent.parent / 'prompts.yaml'
            with open(prompts_file, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                
            # Filter to only active prompts
            active_prompts = {
                version: details for version, details in config.items() 
                if details.get('active', False)
            }
            
            return active_prompts
            
        except Exception as e:
            print(f"⚠️ Failed to load prompts.yaml: {e}")
            return {}
    
    def _reset_counters_if_needed(self):
        """Reset minute and daily counters when time periods change"""
        now = datetime.now()
        current_minute = now.minute
        
        if current_minute != self.current_minute:
            self.current_minute = current_minute
            self.requests_this_minute = 0
            self.tokens_this_minute = 0
        
        today = now.date()
        if today > self.last_reset_date:
            self.daily_requests = 0
            self.last_reset_date = today

    def can_make_request(self, estimated_tokens: int = 10000) -> Dict[str, Any]:
        """Check if we can safely make a request with 2-minute pacing"""
        self._reset_counters_if_needed()
        now = datetime.now()
        
        # Check 2-minute interval pacing for different batches
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
            "seconds_until_next_allowed": max(0, self.target_batch_interval - (time_since_last or 0)) if time_since_last else 0
        }

    def record_request(self, actual_tokens: int):
        """Record a completed request"""
        self.requests_this_minute += 1
        self.tokens_this_minute += actual_tokens
        self.daily_requests += 1
        self.last_request_time = datetime.now()

    def _build_combined_prompt(self, articles: List[Dict], prompts: Dict[str, Any]) -> str:
        """Build a single prompt requesting analysis from all prompt versions"""
        article_count = len(articles)
        
        # Format articles once
        articles_text = "\n\nARTICLES TO ANALYZE:\n"
        for i, article in enumerate(articles):
            title = article.get('title', '')[:200]
            description = article.get('description', '')[:300]
            articles_text += f"\nArticle {i}:\nTitle: {title}\nDescription: {description}\n"
        
        # Build combined prompt
        prompt = f"""You will analyze {article_count} news articles using {len(prompts)} different analysis approaches. 
For each approach, you must return a JSON array with exactly {article_count} objects.

{articles_text}

Now analyze these articles using each approach below. Return your complete response as a single JSON object with this exact structure:
{{
    "version_key": [array of {article_count} analysis objects],
    "version_key2": [array of {article_count} analysis objects]
}}

"""
        
        # Add each prompt version
        for i, (version_key, config) in enumerate(prompts.items(), 1):
            prompt += f"\n=== APPROACH {i}: {version_key} ===\n"
            prompt += f"For the '{version_key}' key in your response:\n"
            
            # Use the prompt template from config, replacing variables
            template = config.get('prompt', '')
            # Extract just the format specification from the template
            if 'REQUIRED FORMAT' in template:
                format_start = template.find('REQUIRED FORMAT')
                format_end = template.find('Articles to analyze:') if 'Articles to analyze:' in template else len(template)
                format_spec = template[format_start:format_end].strip()
                prompt += format_spec + "\n"
            else:
                prompt += template.format(article_count=article_count) + "\n"
        
        prompt += f"\n\nRemember: Return a single JSON object with {len(prompts)} keys, each containing an array of {article_count} analysis objects."
        
        return prompt

    async def analyze_articles_batch(self, articles: List[Dict]) -> Dict[str, Any]:
        """Analyze articles with ALL active prompts in a single request"""
        try:
            if not articles:
                return {"status": "error", "message": "No articles provided"}
            
            # Load active prompts
            prompt_configs = self.load_prompt_config()
            if not prompt_configs:
                return {"status": "error", "message": "No active prompts found"}
            
            total_articles = len(articles)
            all_prompt_results = {}
            total_tokens_used = 0
            total_batches = 0
            
            print(f"📝 Loaded {len(prompt_configs)} active prompts: {list(prompt_configs.keys())}")
            print(f"🔄 Starting unified multi-prompt analysis: {len(prompt_configs)} prompts × {total_articles} articles in single request")
            
            # Process articles in batches
            for batch_start in range(0, total_articles, self.max_articles_per_batch):
                batch = articles[batch_start:batch_start + self.max_articles_per_batch]
                batch_size = len(batch)
                total_batches += 1
                
                # Estimate tokens (more for combined prompt)
                estimated_tokens = batch_size * 150 * len(prompt_configs) + 2000
                
                print(f"📦 Processing batch {total_batches}: {batch_size} articles with all {len(prompt_configs)} prompts")
                
                # Check rate limits
                status = self.can_make_request(estimated_tokens)
                if not status["can_proceed"]:
                    wait_time = status.get("seconds_until_next_allowed", 0)
                    if wait_time > 0:
                        print(f"⏰ Waiting {wait_time:.0f} seconds for rate limits...")
                        await asyncio.sleep(wait_time + 1)
                
                # Build combined prompt for all versions
                combined_prompt = self._build_combined_prompt(batch, prompt_configs)
                
                # Single API call for all prompts
                response = self.model.generate_content(combined_prompt)
                
                # Record usage
                actual_tokens = response.usage_metadata.total_token_count
                self.record_request(actual_tokens)
                total_tokens_used += actual_tokens
                
                # Parse multi-prompt response
                batch_results = self._parse_combined_response(response.text, prompt_configs, batch_size)
                
                # Merge batch results into all_prompt_results
                for version_key in prompt_configs.keys():
                    if version_key not in all_prompt_results:
                        all_prompt_results[version_key] = {
                            "results": [],
                            "config": prompt_configs[version_key],
                            "tokens_used": 0,
                            "articles_analyzed": 0
                        }
                    
                    version_results = batch_results.get(version_key, [])
                    all_prompt_results[version_key]["results"].extend(version_results)
                    all_prompt_results[version_key]["articles_analyzed"] = len(all_prompt_results[version_key]["results"])
                
                print(f"✅ Batch completed: {actual_tokens} tokens for all prompts combined")
            
            # Update token usage (distributed among prompts)
            tokens_per_prompt = total_tokens_used // len(prompt_configs) if prompt_configs else 0
            for version_key in all_prompt_results:
                all_prompt_results[version_key]["tokens_used"] = tokens_per_prompt
            
            return {
                "status": "success",
                "total_articles": total_articles,
                "prompt_versions": list(prompt_configs.keys()),
                "total_tokens_used": total_tokens_used,
                "total_batches_processed": total_batches,
                "results_by_prompt": all_prompt_results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Multi-prompt analysis failed: {str(e)}"
            }

    def _parse_combined_response(self, response_text: str, prompt_configs: Dict, expected_count: int) -> Dict[str, List[Dict]]:
        """Parse Gemini's combined multi-prompt response"""
        try:
            # Clean response
            clean_text = response_text.strip()
            if clean_text.startswith('```json'):
                clean_text = clean_text[7:]
            if clean_text.endswith('```'):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()
            
            # Parse JSON - should be {version1: [...], version2: [...]}
            parsed = json.loads(clean_text)
            
            if isinstance(parsed, dict):
                # Validate we have results for each prompt version
                results = {}
                for version_key in prompt_configs.keys():
                    if version_key in parsed:
                        version_results = parsed[version_key]
                        if isinstance(version_results, list):
                            results[version_key] = version_results
                        else:
                            results[version_key] = [version_results]
                    else:
                        # Fallback if version missing
                        results[version_key] = self._create_fallback_results(expected_count)
                
                return results
            else:
                # Unexpected format, create fallbacks
                return {
                    version_key: self._create_fallback_results(expected_count)
                    for version_key in prompt_configs.keys()
                }
                
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed: {e}")
            print(f"Raw response preview: {response_text[:500]}...")
            
            # Create fallback for all prompts
            return {
                version_key: self._create_fallback_results(expected_count)
                for version_key in prompt_configs.keys()
            }
    
    def _create_fallback_results(self, count: int) -> List[Dict]:
        """Create fallback results when parsing fails"""
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
        } for i in range(count)]

    async def test_connection(self) -> Dict[str, Any]:
        """Test Gemini connection"""
        try:
            response = self.model.generate_content("Respond with 'Connected' if working.")
            return {
                "status": "success",
                "message": "Gemini connected successfully",
                "response": response.text.strip()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection failed: {str(e)}"
            }

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        self._reset_counters_if_needed()
        return {
            "requests_today": self.daily_requests,
            "requests_remaining_today": max(0, self.requests_per_day - self.daily_requests),
            "can_make_request_now": self.can_make_request()["can_proceed"]
        }