"""
Utility functions untuk AI Text Platform
"""

import os
import logging
from functools import wraps
from flask import jsonify
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom API Error class"""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        rv['status_code'] = self.status_code
        return rv

def handle_errors(f):
    """Decorator untuk handle errors di API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIError as e:
            response = jsonify(e.to_dict())
            response.status_code = e.status_code
            return response
        except Exception as e:
            logger.error(f"Unhandled error in {f.__name__}: {str(e)}", exc_info=True)
            response = jsonify({
                'error': 'Internal server error',
                'message': str(e) if os.getenv('FLASK_DEBUG') else 'An unexpected error occurred'
            })
            response.status_code = 500
            return response
    return decorated_function

def rate_limit(max_calls=10, window=60):
    """Simple rate limiting decorator"""
    calls = {}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client IP (simplified, in production use proper method)
            client_id = 'default'  # In production, get from request.remote_addr
            
            current_time = time.time()
            if client_id not in calls:
                calls[client_id] = []
            
            # Remove old calls outside window
            calls[client_id] = [call_time for call_time in calls[client_id] 
                               if current_time - call_time < window]
            
            if len(calls[client_id]) >= max_calls:
                raise APIError('Rate limit exceeded. Please try again later.', 429)
            
            calls[client_id].append(current_time)
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def validate_text_input(text, min_length=10, max_length=50000):
    """Validate text input"""
    if not text or not isinstance(text, str):
        raise APIError('Text is required and must be a string', 400)
    
    text = text.strip()
    if len(text) < min_length:
        raise APIError(f'Text must be at least {min_length} characters long', 400)
    
    if len(text) > max_length:
        raise APIError(f'Text must not exceed {max_length} characters', 400)
    
    return text

def validate_language(language, supported_languages):
    """Validate language code"""
    if language and language not in supported_languages:
        raise APIError(
            f'Unsupported language: {language}. Supported languages: {", ".join(supported_languages.keys())}',
            400
        )
    return language

def get_client_info(request):
    """Get client information from request"""
    return {
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'referer': request.headers.get('Referer', 'Direct'),
        'timestamp': time.time()
    }

def log_api_call(endpoint, request, response_status):
    """Log API calls for monitoring"""
    client_info = get_client_info(request)
    logger.info(f"API Call: {endpoint} - Status: {response_status} - Client: {client_info['ip']}")

# Cache implementation (simple in-memory cache)
class SimpleCache:
    def __init__(self, ttl=300):  # 5 minutes default TTL
        self.cache = {}
        self.ttl = ttl
    
    def get(self, key):
        """Get value from cache"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key, value):
        """Set value in cache"""
        self.cache[key] = (value, time.time())
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()

# Create cache instance
cache = SimpleCache()

def cached(ttl=300):
    """Caching decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{f.__name__}_{str(args)}_{str(kwargs)}"
            
            # Check cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = f(*args, **kwargs)
            cache.set(cache_key, result)
            return result
        
        return decorated_function
    return decorator