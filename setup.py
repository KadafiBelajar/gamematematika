#!/usr/bin/env python3
"""
Setup script untuk AI Text Platform
Menginstall dependencies dan melakukan setup awal
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n📌 {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} - Berhasil!")
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Gagal!")
        print(f"Error: {e}")
        return False
    return True

def main():
    print("🚀 AI Text Platform Setup")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ diperlukan!")
        sys.exit(1)
    else:
        print(f"✅ Python {python_version.major}.{python_version.minor} terdeteksi")
    
    # Update pip
    if not run_command("pip install --upgrade pip", "Update pip"):
        return
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Install Python dependencies"):
        return
    
    # Download NLTK data
    print("\n📌 Download NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('wordnet', quiet=True)
        print("✅ NLTK data - Berhasil!")
    except Exception as e:
        print(f"❌ NLTK data - Gagal! Error: {e}")
    
    # Download spaCy model
    print("\n📌 Download spaCy language model...")
    try:
        run_command("python -m spacy download en_core_web_sm", "Download spaCy English model")
    except:
        print("⚠️  spaCy model gagal didownload, beberapa fitur mungkin terbatas")
    
    # Create .env file if not exists
    if not os.path.exists('.env'):
        print("\n📌 Membuat file .env...")
        try:
            with open('.env.example', 'r') as example:
                with open('.env', 'w') as env:
                    env.write(example.read())
            print("✅ File .env dibuat! Silakan edit dengan API keys Anda")
        except:
            print("⚠️  Tidak dapat membuat .env file")
    
    # Platform specific setup
    system = platform.system()
    if system == "Windows":
        print("\n💡 Tips untuk Windows:")
        print("   - Gunakan PowerShell atau Command Prompt sebagai Administrator")
        print("   - Install Visual C++ Build Tools jika ada error")
    elif system == "Darwin":  # macOS
        print("\n💡 Tips untuk macOS:")
        print("   - Pastikan Xcode Command Line Tools terinstall")
        print("   - brew install python3 untuk Python terbaru")
    elif system == "Linux":
        print("\n💡 Tips untuk Linux:")
        print("   - Gunakan virtual environment untuk isolasi dependencies")
        print("   - sudo apt-get install python3-dev untuk Ubuntu/Debian")
    
    print("\n" + "=" * 50)
    print("✨ Setup selesai!")
    print("\nUntuk menjalankan aplikasi:")
    print("  cd backend")
    print("  python app.py")
    print("\nAplikasi akan berjalan di http://localhost:5000")
    print("\n⚠️  Catatan: Beberapa fitur memerlukan API keys")
    print("Edit file .env untuk menambahkan API keys jika diperlukan")

if __name__ == "__main__":
    main()