# Base class for all sentiment analyzers
# This defines the interface that all sentiment analyzers must implement

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseSentimentAnalyzer(ABC):
    """
    Abstract base class for sentiment analysis.
    All sentiment analyzers (VADER, Transformers, OpenAI) inherit from this.
    """
    
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of given text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict containing sentiment scores in standardized format
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if this analyzer is properly configured and ready to use.
        
        Returns:
            bool: True if analyzer is ready, False otherwise
        """
        pass
    
    def get_name(self) -> str:
        """Get the name of this analyzer."""
        return self.name