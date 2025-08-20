# Transformers-based sentiment and emotion analyzer
# Uses Hugging Face models for both sentiment analysis and emotion detection

from typing import Dict, Any
import logging
from transformers import pipeline
from .base_analyzer import BaseSentimentAnalyzer

class TransformersAnalyzer(BaseSentimentAnalyzer):
    """
    Sentiment and emotion analyzer using Hugging Face Transformers.
    Primary analyzer that provides both sentiment scores and emotional analysis.
    """
    
    def __init__(self):
        super().__init__("transformers")
        self.sentiment_pipeline = None
        self.emotion_pipeline = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize the Transformers models. This might take a moment on first run."""
        try:
            # Sentiment analysis model (positive/negative classification)
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1  # Use CPU (change to 0 for GPU if available)
            )
            
            # Emotion detection model - NOW WITH return_all_scores=True
            self.emotion_pipeline = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                device=-1,  # Use CPU
                return_all_scores=True  # Get ALL emotion scores, not just top one
            )
            
            logging.info("✅ Transformers models loaded successfully")
            
        except Exception as e:
            logging.error(f"❌ Failed to initialize Transformers models: {e}")
            self.sentiment_pipeline = None
            self.emotion_pipeline = None
    
    def is_available(self) -> bool:
        """Check if both models are loaded and ready."""
        return self.sentiment_pipeline is not None and self.emotion_pipeline is not None
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze both sentiment and emotions of the given text.
        
        Args:
            text (str): Text to analyze (article title + description)
            
        Returns:
            Dict with sentiment scores, emotions, and calculated uplift score
        """
        if not self.is_available():
            return self._create_error_response("Models not available")
        
        if not text or not text.strip():
            return self._create_error_response("Empty text provided")
        
        try:
            # Get basic sentiment (positive/negative)
            sentiment_result = self.sentiment_pipeline(text[:512])  # Limit text length
            
            # Get emotions (now returns ALL emotion scores)
            emotion_results = self.emotion_pipeline(text[:512])
            
            # Process results
            return self._process_results(sentiment_result, emotion_results)
            
        except Exception as e:
            logging.error(f"❌ Transformers analysis failed: {e}")
            return self._create_error_response(f"Analysis failed: {str(e)}")
    
    def _process_results(self, sentiment_result, emotion_results) -> Dict[str, Any]:
        """
        Process and combine sentiment and emotion results into our standard format.
        """
        # Convert sentiment to our format
        sentiment_scores = self._convert_sentiment(sentiment_result)
        
        # Convert emotions to our format  
        emotion_scores = self._convert_emotions(emotion_results)
        
        # Extract raw emotions from transformer model
        raw_emotions = self._extract_raw_emotions(emotion_results)
        
        # Calculate uplift score using your weighted system
        uplift_score = self._calculate_uplift_score(emotion_scores, sentiment_scores)
        
        # Calculate confidence (we'll improve this)
        confidence = self._calculate_confidence(sentiment_result, emotion_results)
        
        return {
            "sentiment": sentiment_scores,
            "confidence": round(confidence, 3),
            "raw_emotions": raw_emotions,  # NEW: Raw transformer emotions
            "uplift_emotions": emotion_scores,
            "uplift_score": round(uplift_score, 3),
            "analyzer": self.name
        }
    
    def _extract_raw_emotions(self, emotion_results) -> Dict[str, float]:
        """Extract raw emotion scores from transformer model."""
        raw_emotions = {}
        
        if emotion_results and len(emotion_results) > 0:
            all_emotions = emotion_results[0] if isinstance(emotion_results[0], list) else emotion_results
            
            for emotion_data in all_emotions:
                emotion_name = emotion_data['label'].lower()
                score = round(emotion_data['score'], 3)
                raw_emotions[emotion_name] = score
        
        return raw_emotions
    
    def _calculate_confidence(self, sentiment_result, emotion_results) -> float:
        """Calculate confidence using actual model confidence scores."""
        # Get sentiment model confidence
        sentiment_confidence = sentiment_result[0]['score']
        
        # Get emotion model confidence (highest scoring emotion)
        emotion_confidence = 0.0
        if emotion_results and len(emotion_results) > 0:
            all_emotions = emotion_results[0] if isinstance(emotion_results[0], list) else emotion_results
            emotion_confidence = max(emotion['score'] for emotion in all_emotions)
        
        # Average the two model confidences
        return (sentiment_confidence + emotion_confidence) / 2
    
    def _convert_sentiment(self, sentiment_result) -> Dict[str, float]:
        """Convert Transformers sentiment to our positive/negative/neutral format."""
        result = sentiment_result[0]
        label = result['label'].upper()
        score = result['score']
        
        if label == 'POSITIVE':
            return {"positive": round(score, 3), "negative": round(1-score, 3), "neutral": 0.0}
        else:  # NEGATIVE
            return {"positive": round(1-score, 3), "negative": round(score, 3), "neutral": 0.0}
    
    def _convert_emotions(self, emotion_results) -> Dict[str, float]:
        """Convert Transformers emotions to our uplift emotions format."""
        # The model returns: [anger, disgust, fear, joy, neutral, sadness, surprise]
        # We need to map these to our uplift emotions
        
        if not emotion_results or len(emotion_results) == 0:
            return self._get_empty_emotions()
        
        # Get all emotion scores from the first result
        all_emotions = emotion_results[0] if isinstance(emotion_results[0], list) else emotion_results
        
        # Initialize our uplift emotions
        uplift_emotions = {
            'joy': 0.0,
            'hope': 0.0, 
            'gratitude': 0.0,
            'awe': 0.0,
            'relief': 0.0,
            'compassion': 0.0
        }
        
        # Extract scores from model results
        model_scores = {}
        for emotion_data in all_emotions:
            emotion_name = emotion_data['label'].lower()
            score = emotion_data['score']
            model_scores[emotion_name] = score
        
        # Map direct emotions
        uplift_emotions['joy'] = model_scores.get('joy', 0.0)
        uplift_emotions['awe'] = model_scores.get('surprise', 0.0)
        
        # Derive complex emotions from combinations
        # Hope = joy + (1 - fear) + surprise, normalized
        hope_score = (
            model_scores.get('joy', 0.0) * 0.4 +
            (1 - model_scores.get('fear', 0.0)) * 0.3 +
            model_scores.get('surprise', 0.0) * 0.3
        )
        uplift_emotions['hope'] = min(hope_score, 1.0)
        
        # Relief = (1 - sadness) + (1 - fear), normalized  
        relief_score = (
            (1 - model_scores.get('sadness', 0.0)) * 0.5 +
            (1 - model_scores.get('fear', 0.0)) * 0.5
        )
        uplift_emotions['relief'] = min(relief_score - 0.5, 1.0) if relief_score > 0.5 else 0.0
        
        # Gratitude = joy + (1 - anger), representing social positivity
        gratitude_score = (
            model_scores.get('joy', 0.0) * 0.6 +
            (1 - model_scores.get('anger', 0.0)) * 0.4
        )
        uplift_emotions['gratitude'] = min(gratitude_score, 1.0)
        
        # Compassion = joy + (1 - disgust) + (1 - anger), representing care for others
        compassion_score = (
            model_scores.get('joy', 0.0) * 0.4 +
            (1 - model_scores.get('disgust', 0.0)) * 0.3 +
            (1 - model_scores.get('anger', 0.0)) * 0.3
        )
        uplift_emotions['compassion'] = min(compassion_score, 1.0)
        
        # Round all scores to 3 decimal places
        for emotion in uplift_emotions:
            uplift_emotions[emotion] = round(uplift_emotions[emotion], 3)
        
        return uplift_emotions
    
    def _get_empty_emotions(self) -> Dict[str, float]:
        """Return empty emotions dict."""
        return {
            'joy': 0.0, 'hope': 0.0, 'gratitude': 0.0,
            'awe': 0.0, 'relief': 0.0, 'compassion': 0.0
        }
    
    def _calculate_uplift_score(self, emotions: Dict[str, float], sentiment: Dict[str, float]) -> float:
        """
        Calculate weighted uplift score using your emotion weighting system.
        
        Weights:
        - Hope: ×2.0 (strongest: future-oriented good news)
        - Awe: ×1.8 (breakthroughs, discoveries)  
        - Gratitude: ×1.5 (kindness, social cohesion)
        - Compassion: ×1.5 (humanitarian help)
        - Relief: ×1.0 (neutral baseline)
        - Joy: ×0.7 (positive but often trivial)
        """
        weights = {
            'hope': 2.0,
            'awe': 1.8, 
            'gratitude': 1.5,
            'compassion': 1.5,
            'relief': 1.0,
            'joy': 0.7
        }
        
        # Calculate weighted emotion score
        weighted_emotion_sum = 0.0
        total_weight = 0.0
        
        for emotion, score in emotions.items():
            if emotion in weights:
                weighted_emotion_sum += score * weights[emotion]
                total_weight += weights[emotion]
        
        # Average weighted emotion score
        emotion_component = weighted_emotion_sum / total_weight if total_weight > 0 else 0.0
        
        # Combine with basic sentiment (70% emotions, 30% sentiment)
        sentiment_component = sentiment['positive'] * 0.3
        emotion_component = emotion_component * 0.7
        
        return emotion_component + sentiment_component
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error response."""
        return {
            "sentiment": {"positive": 0.0, "negative": 0.0, "neutral": 1.0},
            "confidence": 0.0,
            "uplift_emotions": {
                "joy": 0.0, "hope": 0.0, "gratitude": 0.0, 
                "awe": 0.0, "relief": 0.0, "compassion": 0.0
            },
            "uplift_score": 0.0,
            "analyzer": self.name,
            "error": error_message
        }