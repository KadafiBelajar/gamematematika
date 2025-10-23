"""
Text Humanizer Module
Mengubah teks menjadi gaya penulisan yang lebih natural dan sesuai konteks
"""

import openai
import anthropic
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
import random
from typing import Dict, List, Optional, Tuple
import nltk
from textstat import flesch_reading_ease
import json
import os

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

class TextHumanizer:
    def __init__(self):
        """Initialize Text Humanizer dengan berbagai style dan tone"""
        self.scopes = {
            'academic': {
                'description': 'Formal, penelitian-based, dengan referensi',
                'characteristics': ['formal', 'objective', 'evidence-based', 'structured'],
                'vocabulary_level': 'advanced',
                'sentence_complexity': 'complex'
            },
            'business': {
                'description': 'Profesional, ringkas, berorientasi hasil',
                'characteristics': ['professional', 'concise', 'action-oriented', 'clear'],
                'vocabulary_level': 'professional',
                'sentence_complexity': 'moderate'
            },
            'general': {
                'description': 'Netral, mudah dipahami, informatif',
                'characteristics': ['clear', 'informative', 'balanced', 'accessible'],
                'vocabulary_level': 'standard',
                'sentence_complexity': 'moderate'
            },
            'email': {
                'description': 'Sopan, langsung, personal',
                'characteristics': ['polite', 'direct', 'personal', 'actionable'],
                'vocabulary_level': 'standard',
                'sentence_complexity': 'simple'
            },
            'creative': {
                'description': 'Ekspresif, imajinatif, engaging',
                'characteristics': ['expressive', 'imaginative', 'engaging', 'varied'],
                'vocabulary_level': 'varied',
                'sentence_complexity': 'varied'
            },
            'casual': {
                'description': 'Santai, conversational, friendly',
                'characteristics': ['relaxed', 'conversational', 'friendly', 'natural'],
                'vocabulary_level': 'simple',
                'sentence_complexity': 'simple'
            }
        }
        
        self.audiences = {
            'general': {
                'description': 'Audiens umum tanpa pengetahuan khusus',
                'knowledge_level': 'basic',
                'formality': 'neutral',
                'technical_terms': 'minimal'
            },
            'knowledgeable': {
                'description': 'Audiens dengan pemahaman dasar topik',
                'knowledge_level': 'intermediate',
                'formality': 'semi-formal',
                'technical_terms': 'moderate'
            },
            'expert': {
                'description': 'Audiens dengan keahlian mendalam',
                'knowledge_level': 'advanced',
                'formality': 'formal',
                'technical_terms': 'extensive'
            }
        }
        
        # Variation patterns untuk membuat teks lebih natural
        self.variation_patterns = {
            'sentence_starters': {
                'academic': ['Furthermore,', 'Moreover,', 'It is evident that', 'Research indicates that', 'Studies show that'],
                'business': ['Additionally,', 'It\'s important to note that', 'Our analysis shows', 'Moving forward,'],
                'general': ['Also,', 'In addition,', 'It\'s worth noting that', 'Interestingly,'],
                'casual': ['Plus,', 'Oh, and', 'By the way,', 'You know what?', 'Actually,']
            },
            'transitions': {
                'contrast': ['However,', 'On the other hand,', 'Nevertheless,', 'In contrast,'],
                'addition': ['Furthermore,', 'Additionally,', 'Moreover,', 'Also,'],
                'conclusion': ['Therefore,', 'In conclusion,', 'Thus,', 'As a result,']
            }
        }
        
        # Initialize APIs if available
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY
        if ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
    
    def search_web_context(self, topic: str, num_results: int = 3) -> List[Dict]:
        """Search web untuk mendapatkan konteks terkini"""
        contexts = []
        
        try:
            # Google search
            for url in search(topic, num_results=num_results):
                try:
                    response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract text content
                    paragraphs = soup.find_all('p')
                    content = ' '.join([p.get_text() for p in paragraphs[:5]])
                    
                    if content:
                        contexts.append({
                            'url': url,
                            'content': content[:500],  # Limit content
                            'title': soup.title.string if soup.title else ''
                        })
                except Exception as e:
                    print(f"Error fetching {url}: {e}")
                    
        except Exception as e:
            print(f"Search error: {e}")
        
        return contexts
    
    def humanize_text(self, 
                     text: str, 
                     scope: str = 'general', 
                     audience: str = 'general',
                     language: str = 'en',
                     use_web_context: bool = True) -> Dict[str, any]:
        """
        Humanize text dengan style dan audience yang ditentukan
        """
        result = {
            'original_text': text,
            'humanized_text': '',
            'scope': scope,
            'audience': audience,
            'language': language,
            'web_contexts': [],
            'modifications': []
        }
        
        # Validate inputs
        if scope not in self.scopes:
            scope = 'general'
        if audience not in self.audiences:
            audience = 'general'
        
        # Get web context if enabled
        if use_web_context:
            # Extract main topic from text
            topic = self._extract_topic(text)
            result['web_contexts'] = self.search_web_context(topic)
        
        # Apply humanization techniques
        humanized_text = text
        
        # 1. Adjust vocabulary and complexity
        humanized_text = self._adjust_vocabulary(humanized_text, scope, audience)
        
        # 2. Add natural variations
        humanized_text = self._add_variations(humanized_text, scope)
        
        # 3. Adjust tone and style
        humanized_text = self._adjust_tone(humanized_text, scope, audience)
        
        # 4. Incorporate web context if available
        if result['web_contexts']:
            humanized_text = self._incorporate_context(humanized_text, result['web_contexts'])
        
        # 5. Final polish with AI if available
        if OPENAI_API_KEY or ANTHROPIC_API_KEY:
            humanized_text = self._ai_polish(humanized_text, scope, audience, language)
        
        result['humanized_text'] = humanized_text
        result['modifications'] = self._track_modifications(text, humanized_text)
        
        return result
    
    def _extract_topic(self, text: str) -> str:
        """Extract main topic from text for web search"""
        # Simple implementation - can be enhanced with NLP
        sentences = nltk.sent_tokenize(text)
        if sentences:
            # Get first sentence and extract key words
            words = nltk.word_tokenize(sentences[0])
            pos_tags = nltk.pos_tag(words)
            
            # Extract nouns and important words
            keywords = [word for word, pos in pos_tags if pos.startswith('NN') or pos.startswith('VB')]
            return ' '.join(keywords[:5])
        
        return text[:50]
    
    def _adjust_vocabulary(self, text: str, scope: str, audience: str) -> str:
        """Adjust vocabulary based on scope and audience"""
        # Implement vocabulary adjustment logic
        scope_config = self.scopes[scope]
        audience_config = self.audiences[audience]
        
        # For now, simple implementation
        # In production, use more sophisticated NLP techniques
        
        if scope == 'academic' and audience == 'expert':
            # Use more technical terms
            replacements = {
                'use': 'utilize',
                'show': 'demonstrate',
                'find': 'discover',
                'think': 'hypothesize'
            }
        elif scope == 'casual' and audience == 'general':
            # Use simpler terms
            replacements = {
                'utilize': 'use',
                'demonstrate': 'show',
                'hypothesis': 'idea',
                'methodology': 'method'
            }
        else:
            replacements = {}
        
        for old, new in replacements.items():
            text = re.sub(r'\b' + old + r'\b', new, text, flags=re.IGNORECASE)
        
        return text
    
    def _add_variations(self, text: str, scope: str) -> str:
        """Add natural variations to make text more human-like"""
        sentences = nltk.sent_tokenize(text)
        
        if scope in self.variation_patterns['sentence_starters']:
            starters = self.variation_patterns['sentence_starters'][scope]
            
            # Randomly add sentence starters
            for i in range(1, len(sentences), 3):  # Every third sentence
                if random.random() > 0.5:
                    sentences[i] = random.choice(starters) + ' ' + sentences[i]
        
        return ' '.join(sentences)
    
    def _adjust_tone(self, text: str, scope: str, audience: str) -> str:
        """Adjust tone based on scope and audience"""
        if scope == 'casual':
            # Add contractions
            contractions = {
                'do not': "don't",
                'cannot': "can't",
                'will not': "won't",
                'it is': "it's",
                'that is': "that's"
            }
            for full, short in contractions.items():
                text = text.replace(full, short)
        
        elif scope == 'academic':
            # Remove contractions
            expansions = {
                "don't": 'do not',
                "can't": 'cannot',
                "won't": 'will not',
                "it's": 'it is',
                "that's": 'that is'
            }
            for short, full in expansions.items():
                text = text.replace(short, full)
        
        return text
    
    def _incorporate_context(self, text: str, contexts: List[Dict]) -> str:
        """Incorporate web context to make text more current and relevant"""
        # Simple implementation - enhance with better NLP
        if contexts:
            # Add a contextual reference
            context_ref = f"\n\nBased on recent information from {contexts[0]['title']}, "
            text = text + context_ref + "this aligns with current understanding in the field."
        
        return text
    
    def _ai_polish(self, text: str, scope: str, audience: str, language: str) -> str:
        """Use AI to polish the text if API is available"""
        prompt = f"""
        Please rewrite the following text in {language} language with these specifications:
        - Scope: {scope} ({self.scopes[scope]['description']})
        - Audience: {audience} ({self.audiences[audience]['description']})
        - Make it sound natural and human-written
        - Maintain the original meaning
        - Add appropriate variations and nuances
        
        Text: {text}
        """
        
        try:
            if OPENAI_API_KEY:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return response.choices[0].message.content
            
            elif ANTHROPIC_API_KEY:
                response = self.anthropic_client.messages.create(
                    model="claude-3-opus-20240229",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000
                )
                return response.content[0].text
        except Exception as e:
            print(f"AI polish error: {e}")
        
        return text
    
    def _track_modifications(self, original: str, modified: str) -> List[str]:
        """Track what modifications were made"""
        modifications = []
        
        # Check length difference
        len_diff = len(modified) - len(original)
        if len_diff > 0:
            modifications.append(f"Text expanded by {len_diff} characters")
        elif len_diff < 0:
            modifications.append(f"Text reduced by {-len_diff} characters")
        
        # Check readability change
        try:
            orig_score = flesch_reading_ease(original)
            mod_score = flesch_reading_ease(modified)
            if abs(orig_score - mod_score) > 5:
                modifications.append(f"Readability adjusted from {orig_score:.1f} to {mod_score:.1f}")
        except:
            pass
        
        return modifications

# Singleton instance
humanizer = TextHumanizer()

def humanize_text(text: str, scope: str = 'general', audience: str = 'general', 
                  language: str = 'en', use_web_context: bool = True) -> Dict:
    """Public API untuk humanize text"""
    return humanizer.humanize_text(text, scope, audience, language, use_web_context)