"""
AI Detector & Text Humanizer Platform
Backend API dengan Flask
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules
from ai_detector import detect_ai_text
from text_humanizer import humanize_text
from utils import handle_errors, rate_limit, validate_text_input, validate_language, log_api_call, APIError

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.urandom(24)
CORS(app)

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'id': 'Bahasa Indonesia',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch',
    'it': 'Italiano',
    'pt': 'Português',
    'ru': 'Русский',
    'ja': '日本語',
    'ko': '한국어',
    'zh': '中文',
    'ar': 'العربية',
    'hi': 'हिन्दी',
    'th': 'ไทย',
    'vi': 'Tiếng Việt',
    'tr': 'Türkçe',
    'pl': 'Polski',
    'nl': 'Nederlands',
    'sv': 'Svenska',
    'da': 'Dansk',
    'no': 'Norsk',
    'fi': 'Suomi',
    'cs': 'Čeština',
    'hu': 'Magyar',
    'el': 'Ελληνικά',
    'he': 'עברית',
    'uk': 'Українська',
    'ro': 'Română',
    'bg': 'Български',
    'hr': 'Hrvatski',
    'sk': 'Slovenčina',
    'sl': 'Slovenščina',
    'et': 'Eesti',
    'lv': 'Latviešu',
    'lt': 'Lietuvių',
    'ms': 'Bahasa Melayu',
    'tl': 'Tagalog',
    'sw': 'Kiswahili',
    'bn': 'বাংলা',
    'ta': 'தமிழ்',
    'te': 'తెలుగు',
    'ml': 'മലയാളം',
    'ur': 'اردو',
    'fa': 'فارسی',
    'ka': 'ქართული',
    'mn': 'Монгол',
    'ne': 'नेपाली',
    'si': 'සිංහල',
    'my': 'မြန်မာဘာသာ',
    'km': 'ភាសាខ្មែរ',
    'lo': 'ລາວ',
    'cy': 'Cymraeg',
    'eu': 'Euskara',
    'gl': 'Galego',
    'ca': 'Català',
    'is': 'Íslenska',
    'mt': 'Malti',
    'sq': 'Shqip',
    'mk': 'Македонски',
    'hy': 'Հայերեն',
    'az': 'Azərbaycan',
    'kk': 'Қазақ',
    'ky': 'Кыргызча',
    'uz': 'Oʻzbek',
    'tg': 'Тоҷикӣ',
    'tk': 'Türkmen'
}

# --- Routes ---

@app.route("/")
def index():
    """Main page"""
    return render_template("index.html", languages=SUPPORTED_LANGUAGES)

@app.route("/api/detect", methods=["POST"])
@handle_errors
@rate_limit(max_calls=30, window=60)  # 30 calls per minute
def api_detect():
    """API endpoint untuk AI text detection"""
    data = request.get_json()
    
    # Validate input
    text = validate_text_input(data.get('text', ''))
    language = validate_language(data.get('language'), SUPPORTED_LANGUAGES)
    
    # Detect AI text
    result = detect_ai_text(text, language)
    
    # Add timestamp
    result['timestamp'] = datetime.now().isoformat()
    
    # Log API call
    log_api_call('/api/detect', request, 200)
    
    return jsonify(result)

@app.route("/api/humanize", methods=["POST"])
@handle_errors
@rate_limit(max_calls=20, window=60)  # 20 calls per minute (more resource intensive)
def api_humanize():
    """API endpoint untuk text humanization"""
    data = request.get_json()
    
    # Validate input
    text = validate_text_input(data.get('text', ''))
    scope = data.get('scope', 'general')
    audience = data.get('audience', 'general')
    language = validate_language(data.get('language', 'en'), SUPPORTED_LANGUAGES)
    use_web_context = data.get('use_web_context', True)
    
    # Validate scope and audience
    valid_scopes = ['academic', 'business', 'general', 'email', 'creative', 'casual']
    valid_audiences = ['general', 'knowledgeable', 'expert']
    
    if scope not in valid_scopes:
        raise APIError(f'Invalid scope. Must be one of: {", ".join(valid_scopes)}')
    
    if audience not in valid_audiences:
        raise APIError(f'Invalid audience. Must be one of: {", ".join(valid_audiences)}')
    
    # Humanize text
    result = humanize_text(text, scope, audience, language, use_web_context)
    
    # Add timestamp
    result['timestamp'] = datetime.now().isoformat()
    
    # Log API call
    log_api_call('/api/humanize', request, 200)
    
    return jsonify(result)

@app.route("/api/process", methods=["POST"])
@handle_errors
@rate_limit(max_calls=15, window=60)  # 15 calls per minute (most resource intensive)
def api_process():
    """Combined API endpoint untuk detect dan humanize sekaligus"""
    data = request.get_json()
    
    # Validate input
    text = validate_text_input(data.get('text', ''))
    scope = data.get('scope', 'general')
    audience = data.get('audience', 'general')
    language = validate_language(data.get('language', 'en'), SUPPORTED_LANGUAGES)
    use_web_context = data.get('use_web_context', True)
    
    # Validate scope and audience
    valid_scopes = ['academic', 'business', 'general', 'email', 'creative', 'casual']
    valid_audiences = ['general', 'knowledgeable', 'expert']
    
    if scope not in valid_scopes:
        raise APIError(f'Invalid scope. Must be one of: {", ".join(valid_scopes)}')
    
    if audience not in valid_audiences:
        raise APIError(f'Invalid audience. Must be one of: {", ".join(valid_audiences)}')
    
    # First detect
    detection_result = detect_ai_text(text, language)
    
    # Then humanize
    humanize_result = humanize_text(text, scope, audience, language, use_web_context)
    
    # Combine results
    combined_result = {
        'detection': detection_result,
        'humanization': humanize_result,
        'timestamp': datetime.now().isoformat()
    }
    
    # Log API call
    log_api_call('/api/process', request, 200)
    
    return jsonify(combined_result)

@app.route("/api/languages", methods=["GET"])
def api_languages():
    """Get supported languages"""
    return jsonify({
        'languages': SUPPORTED_LANGUAGES,
        'total': len(SUPPORTED_LANGUAGES)
    })

@app.route("/api/scopes", methods=["GET"])
def api_scopes():
    """Get available scopes"""
    scopes = {
        'academic': {
            'name': 'Academic',
            'description': 'Formal, research-based writing with references',
            'icon': '🎓'
        },
        'business': {
            'name': 'Business',
            'description': 'Professional, concise, result-oriented',
            'icon': '💼'
        },
        'general': {
            'name': 'General',
            'description': 'Neutral, easy to understand, informative',
            'icon': '📝'
        },
        'email': {
            'name': 'Email',
            'description': 'Polite, direct, personal',
            'icon': '✉️'
        },
        'creative': {
            'name': 'Creative',
            'description': 'Expressive, imaginative, engaging',
            'icon': '🎨'
        },
        'casual': {
            'name': 'Casual',
            'description': 'Relaxed, conversational, friendly',
            'icon': '😊'
        }
    }
    return jsonify(scopes)

@app.route("/api/audiences", methods=["GET"])
def api_audiences():
    """Get available audiences"""
    audiences = {
        'general': {
            'name': 'General Public',
            'description': 'No specialized knowledge required',
            'icon': '👥'
        },
        'knowledgeable': {
            'name': 'Knowledgeable',
            'description': 'Basic understanding of the topic',
            'icon': '🧑‍🎓'
        },
        'expert': {
            'name': 'Expert',
            'description': 'Deep expertise in the field',
            'icon': '👨‍🔬'
        }
    }
    return jsonify(audiences)

@app.route("/api/health", methods=["GET"])
def api_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)