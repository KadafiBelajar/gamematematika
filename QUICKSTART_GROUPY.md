# 🚀 Quick Start: Menghubungkan ke Cursor APK dengan Groupy

## Ringkasan Singkat

Panduan cepat untuk menghubungkan game matematika ini ke Cursor APK menggunakan Groupy dalam 5 menit!

## ⚡ Langkah Cepat

### 1️⃣ Install Dependencies (Sekali saja)

```bash
pip install -r requirements.txt
```

**Apa yang di-install?**
- Flask (web framework)
- flask-cors (untuk koneksi dari APK)
- sympy (untuk matematika simbolik)

### 2️⃣ Install Groupy

Pilih salah satu:

```bash
# Opsi 1: npm
npm install -g groupy

# Opsi 2: pip
pip install groupy

# Opsi 3: Download binary dari groupy.io
```

### 3️⃣ Jalankan Aplikasi

```bash
python backend/app.py
```

**Output yang diharapkan:**
```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

✅ **Aplikasi siap di port 5000!**

### 4️⃣ Buat Tunnel Groupy

Buka terminal baru:

```bash
groupy http 5000
```

**Output yang akan muncul:**
```
Session Status                online
Account                       [your-account] (Plan: Free)
Version                       2.x.x
Region                        [region]
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123xyz.groupy.io -> http://localhost:5000
```

🎉 **Copy URL HTTPS-nya:** `https://abc123xyz.groupy.io`

### 5️⃣ Konfigurasi Cursor APK

Di smartphone Anda:

1. Buka **Cursor APK**
2. Masuk ke **Settings** ⚙️
3. Cari **Backend URL** atau **Server URL**
4. Paste: `https://abc123xyz.groupy.io`
5. **Save**
6. Restart app jika perlu

### 6️⃣ Test!

Buka app dan coba bermain! 🎮

---

## 🔧 Alternatif: Menggunakan ngrok

Jika Groupy tidak tersedia, gunakan ngrok:

```bash
# Install
brew install ngrok  # Mac
choco install ngrok  # Windows

# Jalankan
ngrok http 5000
```

Copy URL forwarding yang muncul (contoh: `https://xyz.ngrok.io`)

---

## 📱 Testing Koneksi

### Test di Browser Smartphone

Sebelum menggunakan APK, test dulu di browser:

```
https://abc123xyz.groupy.io
```

Jika muncul halaman game matematika → ✅ **Koneksi Berhasil!**

### Test API Endpoint

```
https://abc123xyz.groupy.io/api/question?level=1&stage=limit
```

Jika muncul JSON dengan soal matematika → ✅ **API Berfungsi!**

---

## ⚠️ Troubleshooting

### ❌ Connection Refused
**Solusi:**
```bash
# Pastikan Flask running
python backend/app.py

# Pastikan Groupy/ngrok running
groupy http 5000
```

### ❌ CORS Error
**Solusi:** Sudah di-handle otomatis! Jika masih error:
```bash
# Update requirements
pip install -r requirements.txt --upgrade
```

### ❌ URL Berubah Setelah Restart
**Masalah:** Setiap kali restart Groupy, URL berubah

**Solusi:**
1. Gunakan subdomain custom (berbayar)
2. Atau update URL di APK setiap restart
3. Atau gunakan domain sendiri

---

## 🎯 Tips Pro

### 1. Simpan URL Groupy

Buat file untuk menyimpan URL terakhir:

```bash
echo "https://abc123xyz.groupy.io" > groupy-url.txt
```

### 2. Auto-Start Script

Buat file `start-with-groupy.sh`:

```bash
#!/bin/bash
echo "🚀 Starting Flask + Groupy..."
python backend/app.py &
sleep 3
groupy http 5000
```

Jalankan dengan:
```bash
chmod +x start-with-groupy.sh
./start-with-groupy.sh
```

### 3. Monitor Traffic

Groupy menyediakan web interface di:
```
http://127.0.0.1:4040
```

Buka di browser untuk melihat semua request yang masuk!

---

## 📊 Cara Kerja

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│ Cursor APK  │ HTTPS   │   Groupy    │  HTTP   │ Flask Server │
│ (Smartphone)│────────>│   Tunnel    │────────>│ (localhost)  │
│             │         │  (Internet) │         │   :5000      │
└─────────────┘         └─────────────┘         └──────────────┘
```

1. **Cursor APK** mengirim request ke URL Groupy
2. **Groupy** meneruskan ke Flask yang running di komputer Anda
3. **Flask** memproses dan mengirim response balik
4. **Groupy** meneruskan response ke APK

---

## 🔐 Keamanan

⚠️ **PENTING**: Aplikasi Anda akan publik di internet!

**Yang Sudah Aman:**
- ✅ HTTPS encryption (dari Groupy)
- ✅ CORS configured
- ✅ Session management

**Rekomendasi Tambahan:**
- 🔒 Tambahkan login/password
- 🔒 Rate limiting
- 🔒 Jangan share URL ke publik
- 🔒 Monitoring akses

---

## 📞 Butuh Bantuan?

1. **Dokumentasi Lengkap**: Baca `GROUPY_CONNECTION_GUIDE.md`
2. **Cek Log**: Lihat terminal Flask untuk error messages
3. **Test Local**: Pastikan `http://localhost:5000` berfungsi dulu

---

## ✅ Checklist

Sebelum mulai bermain:

- [ ] Flask installed (`pip install -r requirements.txt`)
- [ ] Groupy/ngrok installed
- [ ] Flask running (`python backend/app.py`)
- [ ] Groupy running (`groupy http 5000`)
- [ ] URL copied
- [ ] APK configured dengan URL
- [ ] Test di browser smartphone
- [ ] Ready to play! 🎮

---

**Selamat bermain! 🎉**

_Update: 1 November 2025_
