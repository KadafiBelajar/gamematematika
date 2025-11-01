"""
Vercel Serverless Function Entry Point untuk Flask App
"""
import sys
import os

# Setup Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
backend_dir = os.path.join(parent_dir, 'backend')

sys.path.insert(0, parent_dir)
sys.path.insert(0, backend_dir)

# Set Vercel environment variable
os.environ['VERCEL'] = '1'

# Import Flask app
from app import app as flask_app

# Vercel Python runtime expects 'app' variable
# Flask app is already a WSGI application, so we can export it directly
app = flask_app
