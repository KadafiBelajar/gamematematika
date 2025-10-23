@echo off
echo 🚀 Starting AI Text Platform...
echo ================================

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
pip show flask >nul 2>&1
if errorlevel 1 (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
    
    echo 📚 Downloading NLTK data...
    python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')"
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  No .env file found. Creating from example...
    copy .env.example .env
    echo 📝 Please edit .env file to add your API keys (optional)
)

REM Start the application
echo.
echo ✨ Starting application...
echo 📍 Access at: http://localhost:5000
echo 📊 API Docs: http://localhost:5000/api
echo.
echo Press Ctrl+C to stop the server
echo ================================

cd backend && python app.py