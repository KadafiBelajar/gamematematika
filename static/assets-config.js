// ==========================================
// KONFIGURASI ASET - MUDAH DIKUSTOMISASI
// ==========================================
// Anda dapat mengubah path gambar dan suara di sini
// Support: GIF, WebP (dengan transparent background), PNG, JPG

const ASSETS_CONFIG = {
    // ==========================================
    // KARAKTER PLAYER
    // ==========================================
    player: {
        // Animasi idle (karakter diam)
        idle: {
            image: '/public/assets/characters/player/idle.gif',  // atau .webp, .png
            width: 150,   // lebar dalam pixel
            height: 150   // tinggi dalam pixel
        },
        
        // Animasi saat menyerang
        attack: {
            image: '/public/assets/characters/player/attack.gif',
            width: 150,
            height: 150,
            duration: 500  // durasi animasi dalam milidetik
        },
        
        // Animasi saat kena serangan
        hit: {
            image: '/public/assets/characters/player/hit.gif',
            width: 150,
            height: 150,
            duration: 500
        },
        
        // Fallback jika gambar tidak ditemukan (gunakan SVG default)
        useFallback: true
    },
    
    // ==========================================
    // KARAKTER BOSS
    // ==========================================
    boss: {
        // Animasi idle (boss diam)
        idle: {
            image: '/public/assets/characters/boss/idle.gif',
            width: 150,
            height: 150
        },
        
        // Animasi saat menyerang
        attack: {
            image: '/public/assets/characters/boss/attack.gif',
            width: 150,
            height: 150,
            duration: 500
        },
        
        // Animasi saat kena serangan
        hit: {
            image: '/public/assets/characters/boss/hit.gif',
            width: 150,
            height: 150,
            duration: 500
        },
        
        // Fallback jika gambar tidak ditemukan
        useFallback: true
    },
    
    // ==========================================
    // SOUND EFFECTS
    // ==========================================
    sounds: {
        // Background music (main theme)
        backgroundMusic: {
            src: '/public/assets/sounds/background-music.mp3',
            volume: 0.3,    // volume 0.0 - 1.0
            loop: true,     // apakah musik berulang
            enabled: true   // enable/disable musik
        },
        
        // Sound effect saat player menyerang
        playerAttack: {
            src: '/public/assets/sounds/player-attack.MP3',
            volume: 0.5,
            enabled: true
        },
        
        // Sound effect saat boss menyerang
        bossAttack: {
            src: '/public/assets/sounds/boss-attack.MP3',
            volume: 0.5,
            enabled: true
        },
        
        // Sound effect saat player kena damage (gunakan boss-attack sebagai fallback)
        playerHit: {
            src: '/public/assets/sounds/boss-attack.MP3',
            volume: 0.4,
            enabled: true
        },
        
        // Sound effect saat boss kena damage (gunakan player-attack sebagai fallback)
        bossHit: {
            src: '/public/assets/sounds/player-attack.MP3',
            volume: 0.4,
            enabled: true
        },
        
        // Sound effect saat heal
        heal: {
            src: '/public/assets/sounds/heal.MP3',
            volume: 0.5,
            enabled: true
        },
        
        // Sound effect saat jawaban benar (gunakan victory sebagai fallback)
        correct: {
            src: '/public/assets/sounds/victory.MP3',
            volume: 0.6,
            enabled: true
        },
        
        // Sound effect saat jawaban salah (gunakan defeat sebagai fallback)
        wrong: {
            src: '/public/assets/sounds/defeat.MP3',
            volume: 0.5,
            enabled: true
        },
        
        // Sound effect saat victory
        victory: {
            src: '/public/assets/sounds/victory.MP3',
            volume: 0.7,
            enabled: true
        },
        
        // Sound effect saat defeat
        defeat: {
            src: '/public/assets/sounds/defeat.MP3',
            volume: 0.6,
            enabled: true
        },
        
        // Sound effect timer warning (10 detik terakhir)
        timerWarning: {
            src: '/public/assets/sounds/timer-warning.MP3',
            volume: 0.3,
            enabled: true
        }
    },
    
    // ==========================================
    // PENGATURAN LAINNYA
    // ==========================================
    settings: {
        // Preload semua aset saat halaman dimuat
        preloadAssets: true,
        
        // Tampilkan error di console jika aset tidak ditemukan
        showErrors: true,
        
        // Gunakan placeholder saat loading
        usePlaceholder: true
    }
};

// Export untuk digunakan di file lain
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ASSETS_CONFIG;
}
