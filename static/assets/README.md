# 📁 Panduan Folder Aset

Folder ini berisi semua aset (gambar dan suara) untuk game Battle Screen.

## 📂 Struktur Folder

```
assets/
├── characters/
│   ├── player/          # Aset karakter pemain
│   │   ├── idle.gif     # Animasi idle (diam)
│   │   ├── attack.gif   # Animasi menyerang
│   │   └── hit.gif      # Animasi kena serangan
│   └── boss/            # Aset karakter boss
│       ├── idle.gif     # Animasi idle (diam)
│       ├── attack.gif   # Animasi menyerang
│       └── hit.gif      # Animasi kena serangan
└── sounds/              # Sound effects dan musik
    ├── background-music.mp3    # Musik latar
    ├── player-attack.mp3       # Suara player menyerang
    ├── boss-attack.mp3         # Suara boss menyerang
    ├── player-hit.mp3          # Suara player kena damage
    ├── boss-hit.mp3            # Suara boss kena damage
    ├── heal.mp3                # Suara heal
    ├── correct.mp3             # Suara jawaban benar
    ├── wrong.mp3               # Suara jawaban salah
    ├── victory.mp3             # Suara menang
    ├── defeat.mp3              # Suara kalah
    └── timer-warning.mp3       # Suara peringatan timer
```

## 🎨 Cara Mengganti Gambar Karakter

### Format yang Didukung:
- **GIF** (animasi bergerak)
- **WebP** (dengan transparent background)
- **PNG** (gambar statis dengan transparent background)
- **JPG** (gambar statis)

### Ukuran Rekomendasi:
- Lebar: 150-200 pixel
- Tinggi: 150-200 pixel
- Aspect Ratio: 1:1 (persegi) atau sesuai kebutuhan

### Langkah-langkah:
1. Siapkan 3 gambar untuk setiap karakter:
   - `idle.gif` - Karakter dalam kondisi diam
   - `attack.gif` - Karakter sedang menyerang
   - `hit.gif` - Karakter kena serangan

2. Pastikan gambar memiliki **transparent background** untuk hasil terbaik

3. Letakkan gambar di folder yang sesuai:
   - Player: `/static/assets/characters/player/`
   - Boss: `/static/assets/characters/boss/`

4. Gambar akan otomatis dimuat saat game dijalankan!

### Tips:
- Gunakan GIF untuk animasi bergerak yang smooth
- Gunakan WebP untuk ukuran file lebih kecil dengan kualitas tinggi
- Pastikan background transparan agar terlihat profesional
- Durasi animasi yang disarankan: 0.5 detik (500ms)

## 🔊 Cara Mengganti Sound Effect

### Format yang Didukung:
- **MP3** (recommended)
- **WAV**
- **OGG**

### Ukuran File:
- Sound effect: < 500 KB
- Background music: < 5 MB

### Langkah-langkah:
1. Siapkan file audio dengan nama yang sesuai (lihat struktur folder di atas)

2. Letakkan file di folder `/static/assets/sounds/`

3. Sound akan otomatis dimuat saat game dijalankan!

### Tips:
- Gunakan MP3 untuk kompatibilitas terbaik
- Normalkan volume audio agar tidak terlalu keras/pelan
- Background music sebaiknya di-loop (berulang)
- Sound effect sebaiknya pendek (1-2 detik)

## ⚙️ Kustomisasi Lanjutan

Jika Anda ingin mengubah path file, ukuran gambar, atau volume suara, edit file:

**`/static/assets-config.js`**

Contoh:
```javascript
player: {
    idle: {
        image: '/static/assets/characters/player/idle.gif',
        width: 150,   // Ubah ukuran di sini
        height: 150
    },
    // ...
}

sounds: {
    backgroundMusic: {
        src: '/static/assets/sounds/background-music.mp3',
        volume: 0.3,  // Ubah volume di sini (0.0 - 1.0)
        // ...
    }
}
```

## 🎯 Contoh Aset

Untuk mendapatkan aset contoh (gambar dan suara), Anda bisa:
1. Membuat sendiri menggunakan software seperti:
   - **Gambar**: Aseprite, Piskel, Photoshop, GIMP
   - **Sound**: Audacity, FL Studio, atau download dari freesound.org

2. Download dari website free assets:
   - **Gambar**: itch.io, opengameart.org, kenney.nl
   - **Sound**: freesound.org, zapsplat.com, mixkit.co

## ❓ Troubleshooting

### Gambar tidak muncul?
- Cek apakah path file sudah benar di `assets-config.js`
- Pastikan nama file sama persis (case-sensitive)
- Cek console browser (F12) untuk error messages

### Sound tidak keluar?
- Pastikan format file didukung (MP3 recommended)
- Cek volume di `assets-config.js`
- Background music membutuhkan user interaction untuk mulai (klik atau tekan tombol)
- Cek apakah browser memblok autoplay

### Gambar terlalu besar/kecil?
- Edit ukuran di `assets-config.js` pada property `width` dan `height`
- Atau resize gambar aslinya

## 📝 Catatan Penting

1. **Fallback**: Jika gambar tidak ditemukan, sistem akan otomatis menggunakan icon SVG default
2. **Performance**: Gunakan gambar dengan ukuran yang wajar (< 500 KB per file)
3. **Copyright**: Pastikan Anda memiliki hak untuk menggunakan aset yang Anda masukkan
4. **Testing**: Selalu test di browser setelah mengganti aset

---

Selamat berkreasi! 🎮✨
