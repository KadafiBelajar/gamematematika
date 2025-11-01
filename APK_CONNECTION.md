# 📱 Panduan Koneksi Cursor APK

Dokumen ini menjelaskan cara menghubungkan aplikasi Cursor APK (Android) dengan backend Flask game matematika.

## 🎯 Ringkasan

Cursor APK adalah aplikasi Android yang terhubung ke backend Flask untuk:
- Mengambil soal matematika (limit, turunan, integral)
- Mengirim jawaban untuk validasi
- Menyimpan progress pemain
- Menampilkan animasi karakter dan efek

## 🔌 Metode Koneksi

Ada 2 cara menghubungkan APK dengan backend:

### 1. Koneksi Lokal (WiFi yang Sama)

**Kapan digunakan:** Development/testing di jaringan yang sama

```
APK ──WiFi──> Backend Flask (192.168.x.x:5000)
```

**Langkah:**
1. Jalankan Flask: `python backend/app.py`
2. Cari IP lokal komputer:
   ```bash
   # Linux/Mac
   ifconfig | grep "inet "
   
   # Windows
   ipconfig
   ```
3. Di APK, masukkan: `http://192.168.x.x:5000`
4. Pastikan firewall mengizinkan koneksi port 5000

### 2. Koneksi Internet (Groupy/ngrok) ⭐ Rekomendasi

**Kapan digunakan:** Akses dari mana saja, testing production-like

```
APK ──Internet──> Groupy/ngrok ──> Backend Flask (localhost:5000)
```

**Langkah:** Lihat `QUICKSTART_GROUPY.md`

## ⚙️ Konfigurasi APK

### Di Aplikasi Cursor APK

1. Buka aplikasi
2. Tap icon **Settings** (⚙️) atau **Menu** (☰)
3. Cari **Backend URL** atau **Server Settings**
4. Masukkan URL sesuai metode koneksi:

   **Lokal:**
   ```
   http://192.168.1.100:5000
   ```
   
   **Groupy:**
   ```
   https://abc123xyz.groupy.io
   ```

5. Tap **Save** atau **Apply**
6. Restart aplikasi jika diperlukan

### Format URL yang Benar

✅ **Benar:**
```
https://abc123.groupy.io
http://192.168.1.100:5000
https://mathgame.ngrok.io
```

❌ **Salah:**
```
abc123.groupy.io          (tanpa https://)
http://localhost:5000      (localhost tidak bisa diakses dari APK)
192.168.1.100             (tanpa http:// dan port)
https://abc123.groupy.io/ (trailing slash bisa menyebabkan masalah)
```

## 🔍 Testing Koneksi

### 1. Test di Browser Smartphone

Sebelum menggunakan APK, test URL di browser smartphone:

```
https://abc123xyz.groupy.io
```

**Yang seharusnya muncul:**
- Halaman utama game matematika
- Tombol "Mulai Bermain", "Pilih Stage", dll.

**Jika error:**
- `Connection refused` → Backend tidak running
- `Site can't be reached` → URL salah atau Groupy tidak aktif
- `SSL error` → Coba gunakan HTTP untuk lokal, HTTPS untuk Groupy

### 2. Test API Endpoint

Test endpoint API di browser:

```
https://abc123xyz.groupy.io/api/question?level=1&stage=limit
```

**Response yang benar:**
```json
{
  "id": "limit_1_abc123",
  "latex": "\\lim_{x \\to 2} (x^2 + 3x)",
  "options": ["10", "8", "12", "6"],
  "options_display": ["10", "8", "12", "6"]
}
```

**Jika error:**
```json
{
  "error": "...",
  "detail": "..."
}
```
→ Cek log Flask untuk detail error

### 3. Test dari APK

Di aplikasi Cursor APK:

1. Buka aplikasi
2. Tap **Mulai Bermain**
3. Pilih **Stage** (Limit/Turunan/Integral)
4. Pilih **Level**
5. Permainan dimulai

**Indikator koneksi berhasil:**
- ✅ Soal matematika muncul
- ✅ HP bar terlihat
- ✅ Timer berjalan
- ✅ Jawaban bisa disubmit

**Jika gagal:**
- ❌ Loading terus-menerus → Cek URL
- ❌ "Connection Error" → Backend tidak terhubung
- ❌ "Server Error" → Cek log Flask

## 🐛 Troubleshooting

### Problem 1: APK Tidak Bisa Connect

**Gejala:**
- Loading screen terus-menerus
- Toast/snackbar: "Cannot connect to server"

**Solusi:**

1. **Cek backend Flask:**
   ```bash
   # Pastikan running
   python backend/app.py
   
   # Output yang diharapkan:
   # * Running on http://0.0.0.0:5000
   ```

2. **Cek Groupy/ngrok:**
   ```bash
   groupy http 5000
   
   # Pastikan status: online
   # Pastikan Forwarding URL valid
   ```

3. **Test URL di browser smartphone**
   - Buka browser
   - Akses URL yang sama dengan yang di APK
   - Pastikan halaman muncul

4. **Cek URL di APK:**
   - Pastikan format benar (https:// untuk Groupy)
   - Tidak ada spasi atau typo
   - Tidak ada trailing slash

### Problem 2: CORS Error

**Gejala:**
- Console browser: "CORS policy blocked"
- APK: "Network error" atau "Access denied"

**Solusi:**

1. **Update Flask:**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **Cek konfigurasi CORS di backend/app.py:**
   ```python
   CORS(app, supports_credentials=True, resources={
       r"/api/*": {
           "origins": "*",
           "methods": ["GET", "POST", "OPTIONS"],
           "allow_headers": ["Content-Type", "Authorization"]
       }
   })
   ```

3. **Restart Flask server**

### Problem 3: Session/Progress Tidak Tersimpan

**Gejala:**
- Progress tidak save setelah menyelesaikan level
- Harus login terus-menerus

**Solusi:**

1. **Pastikan menggunakan HTTPS** (untuk Groupy)
   - HTTP tidak support secure cookies
   - Gunakan URL Groupy dengan HTTPS

2. **Cek cookie settings di APK**
   - Enable cookies/session storage
   - Allow third-party cookies (jika perlu)

3. **Gunakan koneksi yang konsisten**
   - Jangan ganti-ganti URL
   - Restart APK jika ganti URL

### Problem 4: Slow Response

**Gejala:**
- Soal loading lama
- Lag saat submit jawaban

**Solusi:**

1. **Cek koneksi internet:**
   - WiFi/data stabil?
   - Ping ke server: 
     ```bash
     ping abc123.groupy.io
     ```

2. **Cek performa Flask:**
   - Lihat log untuk response time
   - Restart jika terasa lambat

3. **Gunakan server lebih dekat:**
   - Groupy region settings
   - Atau deploy ke cloud (Vercel, Heroku)

### Problem 5: URL Groupy Berubah

**Gejala:**
- Setelah restart Groupy, APK tidak bisa connect lagi
- URL berubah dari `abc123` ke `xyz789`

**Solusi:**

**Temporary (Free):**
1. Copy URL baru dari Groupy
2. Update di APK settings
3. Restart APK

**Permanent (Berbayar):**
1. Upgrade Groupy account
2. Reserve custom subdomain:
   ```bash
   groupy http 5000 --subdomain=mathgame-yourname
   ```
3. URL tetap: `https://mathgame-yourname.groupy.io`

**Alternative (Recommended):**
1. Deploy ke cloud (Vercel, Heroku, Railway)
2. Gunakan custom domain
3. URL fixed, tidak perlu update lagi

## 📊 API Endpoints untuk APK

APK menggunakan endpoints berikut:

### GET `/api/question`

Mendapatkan soal baru

**Parameters:**
- `level` (int): Level 1-15
- `stage` (string): "limit", "turunan", atau "integral"

**Response:**
```json
{
  "id": "limit_1_abc123",
  "latex": "\\lim_{x \\to 2} (x^2 + 3x)",
  "options": ["10", "8", "12", "6"],
  "options_display": ["10", "8", "12", "6"]
}
```

### POST `/api/answer`

Submit jawaban

**Body:**
```json
{
  "question_id": "limit_1_abc123",
  "answer": "10",
  "stage_name": "limit",
  "level_num": 1
}
```

**Response:**
```json
{
  "correct": true,
  "canonical_answer": "10"
}
```

### POST `/api/level-complete`

Unlock level berikutnya (dipanggil saat Boss HP = 0)

**Body:**
```json
{
  "stage_name": "limit",
  "level_num": 1
}
```

**Response:**
```json
{
  "success": true,
  "message": "Level 2 telah terbuka!",
  "next_level": 2
}
```

## 🔐 Keamanan

### HTTPS Required

⚠️ **PENTING:** Untuk production, SELALU gunakan HTTPS!

- Groupy: Otomatis HTTPS ✅
- ngrok: Otomatis HTTPS ✅
- Lokal: Hanya HTTP (tidak aman untuk production) ⚠️

### Session Management

- Backend menggunakan Flask session dengan secret key
- Session disimpan di cookie (encrypted)
- Session timeout: default browser/APK

### Rate Limiting

**TODO:** Implementasi rate limiting untuk production

```python
# Contoh dengan Flask-Limiter
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route("/api/question")
@limiter.limit("10 per minute")
def api_get_question():
    ...
```

## 🚀 Production Deployment

Untuk production yang lebih stabil, pertimbangkan deploy ke:

### Option 1: Vercel (Recommended)

Lihat `DEPLOY_VERCEL.md`

### Option 2: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Option 3: Heroku

```bash
# Install Heroku CLI
# Buat Procfile:
echo "web: python backend/app.py" > Procfile

# Deploy
heroku create mathgame-app
git push heroku main
```

URL akan fixed dan tidak berubah-ubah!

## 📞 Support

Jika masih ada masalah:

1. **Cek dokumentasi:**
   - `GROUPY_CONNECTION_GUIDE.md` - Detail koneksi
   - `QUICKSTART_GROUPY.md` - Quick start guide

2. **Cek log:**
   - Flask: Terminal output
   - Groupy: Terminal output
   - APK: Logcat (Android Debug Bridge)

3. **Debug mode:**
   ```bash
   # Jalankan Flask dengan debug mode
   python backend/app.py
   # Debug sudah enabled by default
   ```

---

**Update:** 1 November 2025

**Selamat menggunakan Cursor APK! 🎉**
