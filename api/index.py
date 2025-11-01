"""
Vercel Serverless Function Entry Point untuk Flask App
"""
import sys
import os

print("[API INDEX] Starting serverless function...")
print(f"[API INDEX] Current directory: {os.path.dirname(os.path.abspath(__file__))}")

# Set Vercel environment variable BEFORE importing
os.environ['VERCEL'] = '1'

# Setup Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
backend_dir = os.path.join(parent_dir, 'backend')

print(f"[API INDEX] Parent dir: {parent_dir}")
print(f"[API INDEX] Backend dir: {backend_dir}")

sys.path.insert(0, parent_dir)
sys.path.insert(0, backend_dir)

# Import Flask app
print("[API INDEX] Importing Flask app...")
from app import app as flask_app

print("[API INDEX] Flask app imported successfully")
# Vercel Python runtime expects 'app' variable
# Flask app is already a WSGI application, so we can export it directly
app = flask_app
