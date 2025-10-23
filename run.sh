#!/bin/bash

echo "🚀 Starting AI Text Platform..."
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! pip show flask > /dev/null 2>&1; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    
    echo "📚 Downloading NLTK data..."
    python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp .env.example .env
    echo "📝 Please edit .env file to add your API keys (optional)"
fi

# Start the application
echo ""
echo "✨ Starting application..."
echo "📍 Access at: http://localhost:5000"
echo "📊 API Docs: http://localhost:5000/api"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"

cd backend && python app.py