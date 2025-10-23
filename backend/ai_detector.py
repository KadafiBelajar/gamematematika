"""
AI Text Detector Module
Mendeteksi apakah teks ditulis oleh AI atau manusia dengan dukungan multi-bahasa
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from typing import Dict, List, Tuple
import langdetect
from langdetect import detect_langs
import pycld3 as cld3
import re
from textstat import flesch_reading_ease, automated_readability_index
import nltk
from collections import Counter
import math

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

class AITextDetector:
    def __init__(self):
        """Initialize AI Text Detector dengan multiple model untuk akurasi tinggi"""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load pre-trained models untuk deteksi AI
        self.models = {}
        self.tokenizers = {}
        
        # Model utama untuk deteksi AI text
        model_names = [
            "Hello-SimpleAI/chatgpt-detector-roberta",
            "umm-maybe/AI-image-detector",
        ]
        
        for model_name in model_names:
            try:
                self.tokenizers[model_name] = AutoTokenizer.from_pretrained(model_name)
                self.models[model_name] = AutoModelForSequenceClassification.from_pretrained(model_name).to(self.device)
                self.models[model_name].eval()
            except Exception as e:
                print(f"Warning: Could not load model {model_name}: {e}")
    
    def detect_language(self, text: str) -> Dict[str, float]:
        """Deteksi bahasa dari teks dengan multiple library untuk akurasi"""
        languages = {}
        
        # Menggunakan langdetect
        try:
            detected_langs = detect_langs(text)
            for lang in detected_langs:
                languages[lang.lang] = lang.prob
        except:
            pass
        
        # Menggunakan pycld3
        try:
            is_reliable, text_bytes_found, details = cld3.get_language(text)
            if is_reliable:
                lang_code = details[0][0]
                confidence = details[0][2] / 100.0
                if lang_code not in languages:
                    languages[lang_code] = confidence
        except:
            pass
        
        return languages
    
    def extract_features(self, text: str) -> Dict[str, float]:
        """Extract linguistic features untuk analisis AI detection"""
        features = {}
        
        # Basic statistics
        sentences = nltk.sent_tokenize(text)
        words = nltk.word_tokenize(text)
        
        features['avg_sentence_length'] = np.mean([len(nltk.word_tokenize(s)) for s in sentences]) if sentences else 0
        features['std_sentence_length'] = np.std([len(nltk.word_tokenize(s)) for s in sentences]) if len(sentences) > 1 else 0
        
        # Vocabulary diversity
        unique_words = set(word.lower() for word in words if word.isalpha())
        features['vocabulary_diversity'] = len(unique_words) / len(words) if words else 0
        
        # Readability scores
        try:
            features['flesch_reading_ease'] = flesch_reading_ease(text)
            features['automated_readability_index'] = automated_readability_index(text)
        except:
            features['flesch_reading_ease'] = 0
            features['automated_readability_index'] = 0
        
        # POS tag distribution
        pos_tags = nltk.pos_tag(words)
        pos_counts = Counter(tag for word, tag in pos_tags)
        total_tags = sum(pos_counts.values())
        
        for tag in ['NN', 'VB', 'JJ', 'RB']:  # Noun, Verb, Adjective, Adverb
            features[f'pos_{tag}_ratio'] = sum(v for k, v in pos_counts.items() if k.startswith(tag)) / total_tags if total_tags > 0 else 0
        
        # Punctuation patterns
        punctuation_counts = Counter(char for char in text if char in '.,!?;:')
        features['punctuation_diversity'] = len(punctuation_counts) / len(text) if text else 0
        
        # Repetition patterns
        bigrams = list(zip(words[:-1], words[1:]))
        repeated_bigrams = sum(1 for i in range(len(bigrams)-1) if bigrams[i] == bigrams[i+1])
        features['bigram_repetition'] = repeated_bigrams / len(bigrams) if bigrams else 0
        
        return features
    
    def detect_ai_text(self, text: str, language: str = None) -> Dict[str, any]:
        """
        Deteksi apakah teks ditulis oleh AI
        Returns: Dictionary dengan confidence score dan analisis detail
        """
        results = {
            'is_ai_generated': False,
            'confidence': 0.0,
            'language': {},
            'model_scores': {},
            'feature_analysis': {},
            'explanation': []
        }
        
        # Deteksi bahasa jika tidak disediakan
        if not language:
            results['language'] = self.detect_language(text)
            language = max(results['language'].items(), key=lambda x: x[1])[0] if results['language'] else 'en'
        else:
            results['language'] = {language: 1.0}
        
        # Extract linguistic features
        features = self.extract_features(text)
        results['feature_analysis'] = features
        
        # Analisis dengan berbagai model
        scores = []
        
        for model_name, model in self.models.items():
            try:
                inputs = self.tokenizers[model_name](
                    text, 
                    return_tensors="pt", 
                    truncation=True, 
                    max_length=512,
                    padding=True
                ).to(self.device)
                
                with torch.no_grad():
                    outputs = model(**inputs)
                    probs = torch.softmax(outputs.logits, dim=-1)
                    ai_prob = probs[0][1].item()  # Assuming index 1 is AI-generated
                    
                results['model_scores'][model_name] = ai_prob
                scores.append(ai_prob)
            except Exception as e:
                print(f"Error with model {model_name}: {e}")
        
        # Heuristic analysis berdasarkan features
        heuristic_score = self._calculate_heuristic_score(features)
        scores.append(heuristic_score)
        results['model_scores']['heuristic_analysis'] = heuristic_score
        
        # Calculate final confidence
        if scores:
            results['confidence'] = np.mean(scores)
            results['is_ai_generated'] = results['confidence'] > 0.5
        
        # Generate explanation
        results['explanation'] = self._generate_explanation(results)
        
        return results
    
    def _calculate_heuristic_score(self, features: Dict[str, float]) -> float:
        """Calculate AI probability based on linguistic features"""
        score = 0.5  # Base score
        
        # AI text cenderung memiliki:
        # - Sentence length yang lebih konsisten (std lebih rendah)
        if features.get('std_sentence_length', 10) < 5:
            score += 0.1
        
        # - Vocabulary diversity yang moderat (tidak terlalu tinggi/rendah)
        vocab_div = features.get('vocabulary_diversity', 0.5)
        if 0.3 < vocab_div < 0.6:
            score += 0.1
        
        # - Readability score yang konsisten
        flesch = features.get('flesch_reading_ease', 50)
        if 40 < flesch < 70:
            score += 0.1
        
        # - Balanced POS tag distribution
        noun_ratio = features.get('pos_NN_ratio', 0)
        verb_ratio = features.get('pos_VB_ratio', 0)
        if abs(noun_ratio - verb_ratio) < 0.1:
            score += 0.1
        
        # - Low bigram repetition
        if features.get('bigram_repetition', 0.1) < 0.05:
            score += 0.1
        
        return min(max(score, 0), 1)
    
    def _generate_explanation(self, results: Dict) -> List[str]:
        """Generate human-readable explanation of the detection results"""
        explanations = []
        
        if results['is_ai_generated']:
            explanations.append(f"Teks ini kemungkinan {results['confidence']*100:.1f}% dihasilkan oleh AI.")
        else:
            explanations.append(f"Teks ini kemungkinan {(1-results['confidence'])*100:.1f}% ditulis oleh manusia.")
        
        # Language detection
        main_lang = max(results['language'].items(), key=lambda x: x[1])[0] if results['language'] else 'unknown'
        explanations.append(f"Bahasa utama: {main_lang}")
        
        # Feature analysis insights
        features = results['feature_analysis']
        if features.get('vocabulary_diversity', 0) < 0.2:
            explanations.append("Kosakata yang digunakan cukup repetitif.")
        elif features.get('vocabulary_diversity', 0) > 0.7:
            explanations.append("Kosakata yang digunakan sangat bervariasi.")
        
        if features.get('std_sentence_length', 10) < 3:
            explanations.append("Panjang kalimat sangat konsisten (ciri khas AI).")
        
        return explanations

# Singleton instance
detector = AITextDetector()

def detect_ai_text(text: str, language: str = None) -> Dict:
    """Public API untuk deteksi AI text"""
    return detector.detect_ai_text(text, language)