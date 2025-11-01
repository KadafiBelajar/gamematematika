#!/bin/bash

# Script untuk menjalankan Flask app dengan Groupy tunnel
# Cara pakai: ./start-with-groupy.sh

echo "=========================================="
echo "🚀 Math Game - Groupy Connection Setup"
echo "=========================================="
echo ""

# Cek apakah virtual environment ada
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment tidak ditemukan!"
    echo "📦 Membuat virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment dibuat!"
fi

# Aktifkan virtual environment
echo "🔧 Mengaktifkan virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Memastikan dependencies terinstall..."
pip install -q -r requirements.txt

# Cek apakah groupy terinstall
if ! command -v groupy &> /dev/null; then
    echo ""
    echo "⚠️  Groupy belum terinstall!"
    echo "📥 Install dengan salah satu cara berikut:"
    echo "   npm install -g groupy"
    echo "   pip install groupy"
    echo ""
    echo "🔄 Atau gunakan ngrok sebagai alternatif:"
    echo "   ngrok http 5000"
    echo ""
    read -p "Tekan Enter untuk melanjutkan tanpa Groupy (hanya Flask)..."
    
    # Jalankan Flask saja
    echo ""
    echo "▶️  Menjalankan Flask server..."
    python backend/app.py
    exit 0
fi

# Jalankan Flask di background
echo "▶️  Menjalankan Flask server..."
python backend/app.py > flask.log 2>&1 &
FLASK_PID=$!

# Tunggu Flask siap
echo "⏳ Menunggu Flask siap..."
sleep 3

# Cek apakah Flask berjalan
if ! curl -s http://localhost:5000 > /dev/null; then
    echo "❌ Flask gagal start! Cek flask.log untuk detail."
    kill $FLASK_PID 2>/dev/null
    exit 1
fi

echo "✅ Flask berjalan di http://localhost:5000"
echo ""

# Jalankan Groupy
echo "🌐 Membuat Groupy tunnel..."
echo "=========================================="
echo ""
groupy http 5000

# Cleanup ketika script dihentikan
echo ""
echo "🛑 Menghentikan Flask server..."
kill $FLASK_PID 2>/dev/null
echo "✅ Selesai!"
