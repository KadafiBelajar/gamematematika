# Math Limit Game

Proyek game matematika sederhana untuk belajar konsep limit, turunan, dan integral. Dibuat dengan Python (Flask) dan HTML/CSS/JavaScript.

## ?? Fitur

- **3 Stage:** Limit, Turunan (Derivative), dan Integral
- **15 Level per Stage** dengan tingkat kesulitan yang meningkat
- **Battle System** dengan animasi karakter dan efek serangan
- **Learn Mode** untuk belajar konsep matematika
- **Progress System** yang menyimpan kemajuan pemain
- **Mobile Support** - Bisa diakses dari Cursor APK

## ?? Cara Menjalankan Proyek

### Lokal (Browser Desktop)

1.  **Buat Lingkungan Virtual (Virtual Environment)**
    
    ```bash
    python -m venv venv
    ```

2.  **Aktifkan Lingkungan Virtual**
    
    Di Windows:
    ```bash
    venv\Scripts\activate
    ```
    
    Di Linux/Mac:
    ```bash
    source venv/bin/activate
    ```
    
3.  **Install Dependensi**
    
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi**
    
    ```bash
    python backend/app.py
    ```

5.  **Buka di Browser**
    
    Kunjungi `http://127.0.0.1:5000`

### ?? Koneksi dengan Cursor APK

Untuk menghubungkan aplikasi ini dengan Cursor APK (Android), gunakan Groupy untuk membuat tunnel:

#### Quick Start

```bash
# Jalankan Flask
python backend/app.py

# Terminal baru: Jalankan Groupy
groupy http 5000

# Copy URL yang muncul (contoh: https://abc123.groupy.io)
# Masukkan URL tersebut ke Cursor APK Settings
```

#### Script Otomatis

```bash
./start-with-groupy.sh
```

?? **Dokumentasi Lengkap:**
- [Quick Start Groupy](QUICKSTART_GROUPY.md) - Panduan cepat 5 menit
- [Panduan Koneksi Groupy](GROUPY_CONNECTION_GUIDE.md) - Dokumentasi lengkap
- [APK Connection](APK_CONNECTION.md) - Troubleshooting & API endpoints

## ?? Dokumentasi Lainnya

- [Deploy ke Vercel](DEPLOY_VERCEL.md)
- [Customization Guide](CUSTOMIZATION_GUIDE.md)
- [How to Use](HOW_TO_USE.md)
- [Update Log](UPDATE_LOG.md)

## ??? Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Math Engine:** SymPy
- **Mobile:** Cursor APK (Android)
- **Tunneling:** Groupy / ngrok

## ?? Requirements

- Python 3.7+
- Flask
- flask-cors (untuk APK connection)
- SymPy
- Groupy atau ngrok (untuk mobile access)
