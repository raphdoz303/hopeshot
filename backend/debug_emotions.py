# Enhanced debug to get ALL emotion scores
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transformers import pipeline

def debug_emotion_model_full():
    """Get ALL emotion scores, not just the top one."""
    print("🔍 Debugging Emotion Detection - Getting ALL Scores")
    print("=" * 60)
    
    # Initialize emotion model
    emotion_pipeline = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base", 
        device=-1,
        return_all_scores=True  # This should give us ALL emotions!
    )
    
    test_texts = [
        "Scientists develop breakthrough cancer treatment that shows incredible promise",
        "Community comes together to help flood victims with amazing generosity",
        "Amazing discovery brings hope for the future"
    ]
    
    for text in test_texts:
        print(f"\\n🧪 Testing: '{text}'")
        print("-" * 40)
        
        # Get ALL emotion scores
        emotion_results = emotion_pipeline(text)
        
        if isinstance(emotion_results, list) and len(emotion_results) > 0:
            emotions = emotion_results[0]  # First (and only) result
            
            print("📊 All emotion scores:")
            for emotion in emotions:
                label = emotion['label']
                score = round(emotion['score'], 3)
                print(f"  {label}: {score}")
                
            # Find highest scoring positive emotions
            positive_emotions = [e for e in emotions if e['score'] > 0.1]
            print(f"\\n✨ Emotions > 0.1: {len(positive_emotions)}")

if __name__ == "__main__":
    debug_emotion_model_full()