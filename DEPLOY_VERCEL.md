# 🚀 Panduan Deploy Game Matematika ke Vercel (GRATIS)

## 📋 Prerequisites

1. **Akun GitHub** (gratis) - https://github.com
2. **Akun Vercel** (gratis) - https://vercel.com (login dengan GitHub)

## ✅ File yang Sudah Disiapkan

✅ `vercel.json` - Konfigurasi routing dan build  
✅ `api/index.py` - Entry point untuk serverless function  
✅ `requirements.txt` - Dependencies  
✅ `.vercelignore` - File yang diabaikan saat deploy  
✅ `.gitignore` - File yang tidak di-commit

## 🎯 Langkah Deployment (Cara Termudah)

### **Langkah 1: Push Kode ke GitHub**

```bash
# Jika belum ada Git repository
git init

# Tambahkan semua file
git add .

# Commit
git commit -m "Prepare for Vercel deployment"

# Buat repository baru di GitHub (via web)
# Lalu hubungkan:
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

### **Langkah 2: Deploy di Vercel Dashboard**

1. **Login ke Vercel**
   - Kunjungi https://vercel.com
   - Klik "Sign Up" → Login dengan GitHub

2. **Import Project**
   - Klik **"Add New..."** → **"Project"**
   - Klik **"Import Git Repository"**
   - Pilih repository GitHub Anda
   - Atau paste URL: `https://github.com/USERNAME/REPO_NAME`

3. **Konfigurasi Project**
   - **Framework Preset**: **"Other"** (atau biarkan auto-detect)
   - **Root Directory**: Biarkan **kosong**
   - **Build Command**: **Kosongkan**
   - **Output Directory**: **Kosongkan**
   - **Install Command**: Biarkan default

4. **Deploy!**
   - Klik **"Deploy"**
   - Tunggu 2-5 menit
   - Setelah selesai, dapatkan URL: `https://your-project.vercel.app`

## 🔧 Penjelasan File Konfigurasi

### `vercel.json`
- `builds`: Menggunakan Python runtime untuk `api/index.py`
- `routes`: Route `/static/*` untuk static files, lainnya ke Flask
- `env`: Set `VERCEL=1` untuk deteksi environment
- `functions`: Limit function timeout 10 detik (free tier)

### `api/index.py`
- Setup Python path
- Import Flask app dari `backend/app.py`
- Export sebagai WSGI application untuk Vercel

### `backend/app.py` (Otomatis Terdeteksi)
- Deteksi Vercel environment via `VERCEL` env var
- Otomatis adjust path untuk template dan static files

## ⚠️ Catatan Penting

### 1. Session Storage
- Vercel serverless = stateless
- Session di memory (mungkin hilang saat cold start)
- **Solusi**: Pertimbangkan database (Upstash Redis gratis) atau localStorage

### 2. Function Timeout
- Free tier: **10 detik** per function
- Pastikan generate question tidak terlalu lama

### 3. Cold Start
- Function pertama kali: ~1-3 detik (cold start)
- Setelah warm: cepat

## 🔍 Troubleshooting

### Error: Module not found
**Check:**
- Struktur folder sesuai (api/, backend/, templates/, static/)
- `api/index.py` path setup benar
- Semua dependencies ada di `requirements.txt`

### Error: Template not found
**Solusi:**
- Check `backend/app.py` sudah detect Vercel environment
- Pastikan template files ada di `templates/`

### Static files tidak muncul
**Solusi:**
- Check `vercel.json` route `/static/*` sudah ada
- Pastikan file ada di `static/`

## 🔄 Update Setelah Deploy

- Push ke GitHub → Vercel **auto-deploy** (jika connected)
- Atau: `vercel --prod` (jika pakai CLI)

## 📝 Checklist Sebelum Deploy

- [ ] Kode sudah di-commit ke Git
- [ ] Repository sudah di-push ke GitHub
- [ ] `requirements.txt` lengkap
- [ ] `vercel.json` sudah dikonfigurasi
- [ ] `api/index.py` sudah dibuat
- [ ] Test lokal berjalan baik

## 🎉 Selesai!

Setelah deploy, game Anda akan tersedia di:
```
https://your-project-name.vercel.app
```

Bagikan URL ini untuk mengakses game dari mana saja! 🌐

---

**Tips:** Check logs di Vercel dashboard jika ada masalah.
