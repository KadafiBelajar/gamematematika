# Panduan Koneksi Cursor APK dengan Groupy

## Apa itu Groupy?

Groupy adalah layanan tunneling yang memungkinkan aplikasi lokal Anda dapat diakses dari internet secara publik. Ini berguna untuk menghubungkan aplikasi Flask yang berjalan di komputer lokal Anda dengan Cursor APK (aplikasi mobile).

## Mengapa Menggunakan Groupy?

- **Akses Publik**: Aplikasi Flask lokal Anda dapat diakses dari smartphone/APK melalui internet
- **Tidak Perlu Port Forwarding**: Tidak perlu konfigurasi router yang rumit
- **HTTPS Otomatis**: Groupy menyediakan URL HTTPS yang aman
- **Mudah Digunakan**: Setup cepat dan sederhana

## Langkah-langkah Koneksi

### 1. Install Groupy CLI

Pertama, install Groupy CLI tool di komputer Anda:

```bash
# Menggunakan npm
npm install -g groupy

# Atau menggunakan pip
pip install groupy
```

### 2. Jalankan Aplikasi Flask

Pastikan aplikasi Flask berjalan di port 5000 (default):

```bash
# Aktifkan virtual environment
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# Jalankan aplikasi
python backend/app.py
```

Aplikasi akan berjalan di `http://127.0.0.1:5000`

### 3. Buat Tunnel dengan Groupy

Buka terminal baru dan jalankan Groupy untuk membuat tunnel ke aplikasi Anda:

```bash
groupy http 5000
```

Atau dengan opsi custom subdomain (jika tersedia):

```bash
groupy http 5000 --subdomain=math-game-your-name
```

### 4. Dapatkan URL Publik

Setelah menjalankan perintah Groupy, Anda akan mendapatkan URL publik seperti:

```
https://abc123.groupy.io
```

atau (dengan custom subdomain):

```
https://math-game-your-name.groupy.io
```

**SIMPAN URL INI!** URL ini yang akan digunakan di Cursor APK.

### 5. Konfigurasi Cursor APK

Di aplikasi Cursor APK:

1. Buka **Settings/Pengaturan**
2. Cari bagian **Server URL** atau **Backend URL**
3. Masukkan URL Groupy yang Anda dapatkan (contoh: `https://abc123.groupy.io`)
4. Simpan konfigurasi
5. Restart aplikasi APK jika diperlukan

### 6. Testing Koneksi

Test koneksi dengan membuka URL di browser smartphone Anda:

```
https://abc123.groupy.io
```

Jika berhasil, Anda akan melihat halaman utama game matematika.

## Tips Penggunaan

### Keep Alive

Groupy tunnel akan tetap aktif selama terminal tetap terbuka. Untuk menjaga tunnel tetap hidup:

```bash
# Jalankan di background dengan screen/tmux (Linux/Mac)
screen -S groupy-tunnel
groupy http 5000
# Tekan Ctrl+A lalu D untuk detach

# Atau gunakan nohup
nohup groupy http 5000 &
```

### Domain Custom (Opsional)

Jika Anda memiliki domain sendiri:

```bash
groupy http 5000 --hostname=api.yourdomain.com
```

### Keamanan

⚠️ **PENTING**: Karena aplikasi Anda akan publik di internet:

1. **Gunakan HTTPS**: Groupy menyediakan ini secara default
2. **Tambahkan Authentication**: Pertimbangkan menambahkan login/password
3. **Rate Limiting**: Batasi request dari IP tertentu
4. **Jangan Share URL**: Hanya bagikan URL ke pengguna yang dipercaya

## Alternatif Groupy

Jika Groupy tidak tersedia, Anda bisa menggunakan alternatif:

### ngrok
```bash
ngrok http 5000
```

### localtunnel
```bash
npx localtunnel --port 5000
```

### cloudflared (Cloudflare Tunnel)
```bash
cloudflared tunnel --url http://localhost:5000
```

## Troubleshooting

### Error: Connection Refused

**Masalah**: Cursor APK tidak bisa connect

**Solusi**:
1. Pastikan aplikasi Flask masih berjalan (`python backend/app.py`)
2. Pastikan Groupy tunnel masih aktif
3. Cek URL yang dimasukkan di APK sudah benar (harus HTTPS)
4. Cek firewall tidak memblokir koneksi

### Error: CORS

**Masalah**: Browser/APK menampilkan error CORS

**Solusi**: Sudah ditangani di konfigurasi Flask (lihat `backend/app.py`)

### Error: Session/Cookie Issues

**Masalah**: Login atau progress tidak tersimpan

**Solusi**:
1. Pastikan cookie diaktifkan di browser/APK
2. Gunakan HTTPS (bukan HTTP)
3. Check `app.secret_key` sudah di-set

### Tunnel Disconnect

**Masalah**: Koneksi terputus setelah beberapa waktu

**Solusi**:
1. Jalankan Groupy di screen/tmux session
2. Atau restart tunnel: `groupy http 5000`
3. Update URL di APK dengan URL baru jika berubah

## Contoh Workflow Lengkap

```bash
# Terminal 1: Jalankan Flask
cd /workspace
source venv/bin/activate
python backend/app.py

# Terminal 2: Jalankan Groupy
groupy http 5000

# Output:
# Session Status: online
# Forwarding: https://abc123.groupy.io -> http://localhost:5000
```

Kemudian di Cursor APK:
1. Setting → Backend URL → `https://abc123.groupy.io`
2. Save dan restart
3. Mulai bermain!

## Monitoring

Untuk melihat log request yang masuk:

```bash
# Di terminal Flask, Anda akan melihat:
127.0.0.1 - - [01/Nov/2025 10:15:30] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [01/Nov/2025 10:15:35] "GET /api/question?level=1&stage=limit HTTP/1.1" 200 -
```

Di terminal Groupy:
```bash
HTTP Requests
-------------
GET /               200 OK
GET /api/question   200 OK
POST /api/answer    200 OK
```

## Support

Jika masih ada masalah:
1. Cek log di terminal Flask untuk error
2. Cek log di terminal Groupy untuk koneksi
3. Test URL Groupy di browser desktop dulu sebelum di APK
4. Pastikan internet connection stabil di smartphone

---

**Update Terakhir**: 1 November 2025
