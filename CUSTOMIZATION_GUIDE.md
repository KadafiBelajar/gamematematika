# 🎨 Panduan Kustomisasi Game Battle Screen

Dokumen ini menjelaskan cara mengkustomisasi tampilan, karakter, dan sound game Battle Screen.

## 📋 Daftar Isi

1. [Kustomisasi Karakter](#kustomisasi-karakter)
2. [Kustomisasi Sound](#kustomisasi-sound)
3. [Konfigurasi Lengkap](#konfigurasi-lengkap)
4. [Tips & Trik](#tips--trik)

---

## 🎭 Kustomisasi Karakter

### Format File yang Didukung

- **GIF** - Animasi bergerak (recommended untuk animasi)
- **WebP** - Format modern dengan ukuran kecil dan transparent background
- **PNG** - Gambar statis dengan transparent background
- **JPG** - Gambar statis (tidak support transparent)

### Ukuran Rekomendasi

- Dimensi: **150x150 pixel** (atau aspect ratio 1:1)
- Ukuran file: **< 500 KB** per gambar
- Background: **Transparent** untuk hasil terbaik

### 3 Animasi yang Dibutuhkan

Untuk setiap karakter (Player dan Boss), Anda perlu 3 jenis animasi:

1. **Idle** - Karakter dalam kondisi diam
   - Contoh: Karakter bernapas, mata berkedip, rambut bergerak
   
2. **Attack** - Karakter sedang menyerang
   - Contoh: Ayunan pedang, tembakan energi, pukulan
   - Durasi: 0.5 detik (500ms)
   
3. **Hit** - Karakter terkena serangan
   - Contoh: Karakter mundur, terguncang, efek damage
   - Durasi: 0.5 detik (500ms)

### Cara Mengganti Karakter

#### Opsi 1: Menggunakan File Custom

1. Siapkan 6 gambar total:
   ```
   Player:
   - idle.gif
   - attack.gif
   - hit.gif
   
   Boss:
   - idle.gif
   - attack.gif
   - hit.gif
   ```

2. Letakkan file di folder yang tepat:
   ```
   /static/assets/characters/player/idle.gif
   /static/assets/characters/player/attack.gif
   /static/assets/characters/player/hit.gif
   
   /static/assets/characters/boss/idle.gif
   /static/assets/characters/boss/attack.gif
   /static/assets/characters/boss/hit.gif
   ```

3. File akan otomatis dimuat! Tidak perlu edit kode.

#### Opsi 2: Menggunakan Path Custom

Jika Anda ingin menyimpan file di lokasi lain, edit file **`/static/assets-config.js`**:

```javascript
player: {
    idle: {
        image: '/path/to/your/player-idle.gif',  // Ganti path di sini
        width: 150,
        height: 150
    },
    attack: {
        image: '/path/to/your/player-attack.gif',
        width: 150,
        height: 150,
        duration: 500  // Durasi animasi dalam milidetik
    },
    hit: {
        image: '/path/to/your/player-hit.webp',  // Bisa pakai .webp juga
        width: 150,
        height: 150,
        duration: 500
    }
}
```

### Mengubah Ukuran Karakter

Edit `width` dan `height` di **`assets-config.js`**:

```javascript
player: {
    idle: {
        image: '/static/assets/characters/player/idle.gif',
        width: 200,   // Ubah dari 150 ke 200
        height: 200   // Karakter jadi lebih besar
    }
}
```

### Mengubah Durasi Animasi

```javascript
player: {
    attack: {
        image: '/static/assets/characters/player/attack.gif',
        width: 150,
        height: 150,
        duration: 800  // Animasi jadi lebih lama (dari 500ms ke 800ms)
    }
}
```

---

## 🔊 Kustomisasi Sound

### Format File yang Didukung

- **MP3** - Recommended untuk kompatibilitas terbaik
- **WAV** - Kualitas tinggi tapi ukuran besar
- **OGG** - Format alternatif

### Jenis Sound yang Bisa Dikustomisasi

| Sound | Deskripsi | Kapan Diputar |
|-------|-----------|---------------|
| `background-music.mp3` | Musik latar utama | Saat game dimulai |
| `player-attack.mp3` | Suara player menyerang | Player jawab benar |
| `boss-attack.mp3` | Suara boss menyerang | Player jawab salah/timeout |
| `player-hit.mp3` | Suara player kena damage | Player kehilangan HP |
| `boss-hit.mp3` | Suara boss kena damage | Boss kehilangan HP |
| `heal.mp3` | Suara heal | Tekan tombol Heal |
| `correct.mp3` | Suara jawaban benar | Jawaban benar |
| `wrong.mp3` | Suara jawaban salah | Jawaban salah |
| `victory.mp3` | Suara menang | Boss dikalahkan |
| `defeat.mp3` | Suara kalah | Player kalah |
| `timer-warning.mp3` | Peringatan waktu | 10 detik terakhir |

### Cara Mengganti Sound

1. Siapkan file audio dengan nama yang sesuai tabel di atas

2. Letakkan di folder `/static/assets/sounds/`

3. Sound otomatis dimuat!

### Mengatur Volume Sound

Edit **`/static/assets-config.js`**:

```javascript
sounds: {
    backgroundMusic: {
        src: '/static/assets/sounds/background-music.mp3',
        volume: 0.3,    // 0.0 (mute) - 1.0 (max)
        loop: true,     // true = berulang terus
        enabled: true   // false = disable sound ini
    },
    
    playerAttack: {
        src: '/static/assets/sounds/player-attack.mp3',
        volume: 0.7,    // Naikin volume jadi 70%
        enabled: true
    },
    
    timerWarning: {
        src: '/static/assets/sounds/timer-warning.mp3',
        volume: 0.1,    // Pelan aja biar gak kaget
        enabled: false  // Nonaktifkan sound ini
    }
}
```

### Disable Semua Sound

Ubah semua `enabled: false` atau set `volume: 0`.

---

## ⚙️ Konfigurasi Lengkap

### File Konfigurasi Utama

**Lokasi:** `/static/assets-config.js`

Ini adalah file yang mengontrol semua aset. Struktur lengkapnya:

```javascript
const ASSETS_CONFIG = {
    // Karakter Player
    player: {
        idle: { image: '...', width: 150, height: 150 },
        attack: { image: '...', width: 150, height: 150, duration: 500 },
        hit: { image: '...', width: 150, height: 150, duration: 500 },
        useFallback: true  // true = pakai SVG default jika gambar gagal load
    },
    
    // Karakter Boss
    boss: {
        idle: { image: '...', width: 150, height: 150 },
        attack: { image: '...', width: 150, height: 150, duration: 500 },
        hit: { image: '...', width: 150, height: 150, duration: 500 },
        useFallback: true
    },
    
    // Sound Effects
    sounds: {
        backgroundMusic: { src: '...', volume: 0.3, loop: true, enabled: true },
        playerAttack: { src: '...', volume: 0.5, enabled: true },
        // ... (11 sounds total)
    },
    
    // Pengaturan Global
    settings: {
        preloadAssets: true,    // Preload semua aset saat halaman dimuat
        showErrors: true,       // Tampilkan error di console
        usePlaceholder: true    // Gunakan placeholder saat loading
    }
};
```

### Responsive Design

Game sudah responsive untuk:
- 📱 **Mobile Portrait** (320px - 480px)
- 📱 **Mobile Landscape** (481px - 767px)
- 📱 **Tablet** (768px - 1023px)
- 💻 **Laptop** (1024px - 1439px)
- 🖥️ **Desktop** (1440px+)

Tidak perlu konfigurasi tambahan!

---

## 💡 Tips & Trik

### 1. Membuat Animasi GIF

**Tools Recommended:**
- [Aseprite](https://www.aseprite.org/) - Pixel art animation (paid)
- [Piskel](https://www.piskelapp.com/) - Free online pixel art
- [Ezgif](https://ezgif.com/) - Free GIF editor online

**Langkah-langkah:**
1. Buat frame-by-frame animation
2. Export sebagai GIF
3. Optimize ukuran file (< 500 KB)
4. Pastikan background transparan

### 2. Convert ke WebP

WebP biasanya 30% lebih kecil dari PNG/GIF dengan kualitas sama.

**Online Converter:**
- https://cloudconvert.com/gif-to-webp
- https://convertio.co/gif-webp/

### 3. Membuat/Edit Sound Effect

**Free Tools:**
- [Audacity](https://www.audacityteam.org/) - Audio editor gratis
- [LMMS](https://lmms.io/) - Music production

**Free Sound Libraries:**
- [Freesound.org](https://freesound.org/)
- [Zapsplat](https://www.zapsplat.com/)
- [Mixkit](https://mixkit.co/free-sound-effects/)

### 4. Testing

Setelah mengganti aset:
1. Buka browser
2. Tekan **F12** untuk buka Developer Console
3. Refresh halaman (Ctrl+F5)
4. Cek di console apakah ada error
5. Test semua animasi:
   - Idle: karakter harus tampil
   - Attack: jawab soal dengan benar
   - Hit: jawab soal salah atau waktu habis
   - Sound: aktifkan/test semua suara

### 5. Optimisasi Performance

- Gunakan gambar dengan resolusi wajar (jangan terlalu besar)
- Compress GIF/WebP sebelum dipakai
- Gunakan MP3 dengan bitrate 128-192 kbps untuk sound
- Enable preload di `settings.preloadAssets: true`

### 6. Fallback ke SVG Default

Jika Anda tidak punya custom image, sistem akan otomatis pakai icon SVG default yang sudah ada. Set `useFallback: true` di config.

### 7. Debug

Jika ada masalah:

```javascript
// Di assets-config.js, aktifkan debug mode
settings: {
    showErrors: true  // Tampilkan error di console
}
```

Buka console (F12) dan lihat pesan error.

---

## 🎯 Contoh Konfigurasi

### Karakter Pixel Art Style

```javascript
player: {
    idle: {
        image: '/static/assets/characters/player/warrior-idle.gif',
        width: 120,
        height: 120
    },
    attack: {
        image: '/static/assets/characters/player/warrior-attack.gif',
        width: 140,  // Lebih besar saat attack
        height: 140,
        duration: 600
    },
    hit: {
        image: '/static/assets/characters/player/warrior-hit.gif',
        width: 120,
        height: 120,
        duration: 400
    }
}
```

### Sound 8-bit Retro Style

```javascript
sounds: {
    backgroundMusic: {
        src: '/static/assets/sounds/8bit-theme.mp3',
        volume: 0.2,
        loop: true,
        enabled: true
    },
    correct: {
        src: '/static/assets/sounds/coin.mp3',
        volume: 0.6,
        enabled: true
    },
    wrong: {
        src: '/static/assets/sounds/error.mp3',
        volume: 0.5,
        enabled: true
    }
}
```

---

## 📞 Troubleshooting

### Problem: Gambar tidak muncul

**Solusi:**
1. Cek path file di `assets-config.js` (case-sensitive!)
2. Pastikan file benar-benar ada di folder
3. Cek console (F12) untuk error messages
4. Pastikan format file didukung (GIF, WebP, PNG, JPG)

### Problem: Sound tidak keluar

**Solusi:**
1. Pastikan file format MP3
2. Cek `enabled: true` di config
3. Background music butuh user interaction (klik/ketik dulu)
4. Cek volume di config
5. Pastikan browser tidak mute/volume rendah

### Problem: Animasi terlalu cepat/lambat

**Solusi:**
```javascript
attack: {
    duration: 1000  // Ubah durasi (dalam milidetik)
}
```

### Problem: Gambar terlalu besar/kecil

**Solusi:**
```javascript
idle: {
    width: 200,   // Ubah ukuran
    height: 200
}
```

---

## 📚 Resource Tambahan

### Free Asset Sources

**Gambar/Sprites:**
- [itch.io](https://itch.io/game-assets/free) - Ribuan free game assets
- [OpenGameArt.org](https://opengameart.org/) - Open source game art
- [Kenney.nl](https://www.kenney.nl/assets) - High quality free assets

**Sounds:**
- [Freesound.org](https://freesound.org/) - Community sound library
- [Zapsplat](https://www.zapsplat.com/) - Free sound effects
- [OpenGameArt Audio](https://opengameart.org/art-search-advanced?keys=&field_art_type_tid%5B%5D=13)

**Music:**
- [Incompetech](https://incompetech.com/music/royalty-free/) - Free background music
- [FreePD](https://freepd.com/) - Public domain music

---

**Selamat Mengkustomisasi! 🎮✨**

Jika ada pertanyaan, cek console browser (F12) untuk error messages atau baca kembali dokumentasi ini.
