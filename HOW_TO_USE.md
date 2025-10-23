# Panduan Menggunakan Battle Screen UI

## 🎮 Cara Menjalankan Aplikasi

### 1. Install Dependencies (jika belum)
```bash
cd /workspace
pip3 install -r requirements.txt
```

### 2. Jalankan Server Flask
```bash
cd /workspace/backend
python3 app.py
```

Server akan berjalan di: `http://localhost:5000`

### 3. Akses Game
1. Buka browser
2. Akses `http://localhost:5000`
3. Pilih stage "Limit"
4. Pilih level yang ingin dimainkan

## 🎯 Gameplay

### Kontrol Utama
- **Mouse Click**: Pilih jawaban dan klik tombol SERANG
- **Enter Key**: Submit jawaban atau lanjut ke soal berikutnya
- **Heal Button**: Klik untuk restore HP (+25 HP, max 3x per level)

### Mekanik Battle
1. **Timer**: Anda punya 90 detik per soal
   - Hijau: >30 detik
   - Kuning: ≤30 detik
   - Merah berkedip: ≤10 detik

2. **Menjawab Soal**:
   - ✅ **Benar**: Boss kehilangan 10 HP + animasi serangan player
   - ❌ **Salah**: Player kehilangan 20 HP + animasi serangan boss
   - ⏱️ **Timeout**: Player kehilangan 5 HP + animasi serangan boss

3. **Heal System**:
   - 3 heal charges per level
   - Setiap heal +25 HP
   - Tidak bisa heal jika HP sudah penuh (100%)
   - Counter ditampilkan di button: "HEAL (3)"

4. **Kondisi Menang/Kalah**:
   - 🏆 **Victory**: Boss HP = 0
   - ☠️ **Defeat**: Player HP = 0

## 🎨 Fitur Visual

### Avatar Animations
- **Attacking**: Avatar bergetar + slash effect
- **Damaged**: Avatar flash merah
- **Glow**: Pulse effect berkelanjutan

### HP Bars
- **Smooth transitions**: Perubahan HP dengan animasi halus
- **Shine effect**: Kilau bergerak di dalam bar
- **Color coding**: Cyan (player) / Red (boss)
- **Angular design**: Bentuk futuristik dengan clip-path

### Background Effects
- **Stars**: Bintang berkedip
- **Particles**: 30 partikel cyan melayang
- **Gradient**: Purple-indigo-slate theme

### Question Panel
- **Glass morphism**: Background blur effect
- **Border glow**: Purple accent dengan glow
- **Icon**: Shield icon di header

### Answer Buttons
- **Crystal shape**: Bentuk angular dengan clip-path
- **Hover effect**: Naik + glow lebih terang
- **Selected state**: Scale up + glow maksimal
- **Stagger animation**: Muncul satu per satu

## 📱 Responsive Design

### Desktop (>1024px)
- Layout horizontal penuh
- Avatar besar (140x140px)
- 2-4 kolom answer grid

### Tablet (768-1024px)
- Avatar sedang (100x100px)
- Spacing lebih rapat
- 2 kolom answer grid

### Mobile (<768px)
- Layout vertikal
- Avatar di atas
- 1 kolom answer grid
- Heal button lebih kecil

## 🔧 Troubleshooting

### Animasi tidak muncul
- Pastikan browser support CSS animations
- Clear cache browser (Ctrl+Shift+Delete)
- Pastikan JavaScript enabled

### MathJax tidak render
- Check internet connection (MathJax load from CDN)
- Reload halaman (Ctrl+R)

### Heal button tidak berfungsi
- Pastikan HP tidak penuh (100%)
- Check apakah heal counter masih ada (>0)
- Refresh halaman untuk reset level

### Timer tidak jalan
- Check console browser untuk errors (F12)
- Pastikan JavaScript tidak di-block

## 🎨 Customization

### Mengubah Warna Theme

Edit `/workspace/static/style.css`:

```css
:root {
    --color-player: #00d4ff;      /* Warna player */
    --color-boss: #ff4b4b;        /* Warna boss */
    --color-accent: #a855f7;      /* Warna accent */
}
```

### Mengubah Durasi Timer

Edit `/workspace/static/main.js`:

```javascript
const startTimer = () => {
    let timerValue = 90; // Ubah angka ini
    // ...
}
```

### Mengubah Damage/Heal Amount

Edit `/workspace/static/main.js`:

```javascript
// Damage boss saat benar
applyDamageAndCheckStatus('boss', 10); // Ubah 10

// Damage player saat salah
applyDamageAndCheckStatus('player', 20); // Ubah 20

// Heal amount
const healAmount = 25; // Ubah 25

// Heal charges
let healCount = 3; // Ubah 3
```

## 📚 Files Structure

```
/workspace/
├── backend/
│   ├── app.py              # Flask server
│   ├── grader.py           # Answer checking
│   └── question_gen.py     # Question generator
├── templates/
│   └── main.html           # Battle screen HTML ⭐
├── static/
│   ├── style.css           # Battle screen CSS ⭐
│   └── main.js             # Battle screen JS ⭐
└── requirements.txt        # Dependencies
```

⭐ = File yang dimodifikasi untuk battle screen

## 🐛 Known Issues

1. **Safari iOS**: Animasi mungkin lebih lambat (hardware acceleration limited)
2. **Internet Explorer**: Tidak support (gunakan Chrome/Firefox/Edge)
3. **Very old browsers**: CSS clip-path mungkin tidak support

## 💡 Tips & Tricks

1. **Strategy**: Heal saat HP ≤50% untuk efisiensi maksimal
2. **Speed**: Gunakan Enter key untuk submit lebih cepat
3. **Focus**: Matikan distraksi, timer cepat habis!
4. **Practice**: Salah OK, yang penting belajar dari kesalahan

## 🎯 Next Features (Future)

- [ ] Sound effects untuk serangan
- [ ] Combo system (multiple correct answers)
- [ ] Special attacks (ultimate skills)
- [ ] Boss phase transitions
- [ ] Multiplayer mode
- [ ] Leaderboard system

---

**Selamat bermain dan semoga berhasil mengalahkan Calculus Demon!** 🎮⚔️🔥
