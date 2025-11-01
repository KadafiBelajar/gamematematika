// ==========================================
// SOUND MANAGER
// ==========================================
// Sistem untuk mengelola sound effects dan background music

class SoundManager {
    constructor(config) {
        this.config = config;
        this.sounds = {};
        this.backgroundMusic = null;
        this.isMuted = false;
        this.isBackgroundMusicPlaying = false;
    }

    /**
     * Initialize sound manager
     */
    async init() {
        console.log('🔊 Initializing Sound Manager...');
        
        // Preload sounds jika diaktifkan
        if (this.config.settings.preloadAssets) {
            await this.preloadAllSounds();
        }
        
        console.log('✅ Sound Manager initialized');
    }

    /**
     * Preload all sound effects
     */
    async preloadAllSounds() {
        console.log('⏳ Preloading sounds...');
        
        const promises = [];
        
        // Preload background music
        if (this.config.sounds.backgroundMusic.enabled) {
            promises.push(this.loadSound('backgroundMusic'));
        }
        
        // Preload sound effects
        const soundKeys = [
            'playerAttack', 'bossAttack',
            'playerHit', 'bossHit',
            'heal', 'correct', 'wrong',
            'victory', 'defeat', 'timerWarning'
        ];
        
        soundKeys.forEach(key => {
            if (this.config.sounds[key].enabled) {
                promises.push(this.loadSound(key));
            }
        });
        
        await Promise.all(promises);
        console.log('✅ All sounds preloaded');
    }

    /**
     * Load single sound
     */
    async loadSound(soundKey) {
        return new Promise((resolve) => {
            const soundConfig = this.config.sounds[soundKey];
            
            if (!soundConfig || !soundConfig.src) {
                if (this.config.settings.showErrors) {
                    console.warn(`⚠️ No sound configured for ${soundKey}`);
                }
                resolve(null);
                return;
            }

            const audio = new Audio();
            audio.preload = 'auto';
            
            audio.addEventListener('canplaythrough', () => {
                audio.volume = soundConfig.volume || 0.5;
                if (soundConfig.loop) {
                    audio.loop = true;
                }
                
                if (soundKey === 'backgroundMusic') {
                    this.backgroundMusic = audio;
                } else {
                    this.sounds[soundKey] = audio;
                }
                
                console.log(`✅ Loaded sound: ${soundKey}`);
                resolve(audio);
            }, { once: true });
            
            audio.addEventListener('error', () => {
                if (this.config.settings.showErrors) {
                    console.warn(`⚠️ Failed to load sound: ${soundConfig.src}`);
                }
                resolve(null);
            }, { once: true });
            
            audio.src = soundConfig.src;
        });
    }

    /**
     * Play sound effect
     */
    play(soundKey) {
        if (this.isMuted) return;
        
        const soundConfig = this.config.sounds[soundKey];
        if (!soundConfig || !soundConfig.enabled) return;

        let audio = this.sounds[soundKey];
        
        // Load sound on-demand if not preloaded
        if (!audio) {
            this.loadSound(soundKey).then(loadedAudio => {
                if (loadedAudio) {
                    loadedAudio.currentTime = 0;
                    loadedAudio.play().catch(e => {
                        if (this.config.settings.showErrors) {
                            console.warn(`⚠️ Failed to play sound: ${soundKey}`, e);
                        }
                    });
                }
            });
            return;
        }

        // Play sound
        try {
            audio.currentTime = 0;
            audio.play().catch(e => {
                if (this.config.settings.showErrors) {
                    console.warn(`⚠️ Failed to play sound: ${soundKey}`, e);
                }
            });
        } catch (e) {
            if (this.config.settings.showErrors) {
                console.warn(`⚠️ Error playing sound: ${soundKey}`, e);
            }
        }
    }

    /**
     * Play background music
     */
    playBackgroundMusic() {
        if (this.isMuted) return;
        if (!this.config.sounds.backgroundMusic.enabled) return;
        
        if (!this.backgroundMusic) {
            this.loadSound('backgroundMusic').then(audio => {
                if (audio && !this.isBackgroundMusicPlaying) {
                    audio.play().catch(e => {
                        if (this.config.settings.showErrors) {
                            console.warn('⚠️ Failed to play background music', e);
                        }
                    });
                    this.isBackgroundMusicPlaying = true;
                }
            });
            return;
        }

        if (!this.isBackgroundMusicPlaying) {
            this.backgroundMusic.play().catch(e => {
                if (this.config.settings.showErrors) {
                    console.warn('⚠️ Failed to play background music', e);
                }
            });
            this.isBackgroundMusicPlaying = true;
        }
    }

    /**
     * Stop background music
     */
    stopBackgroundMusic() {
        if (this.backgroundMusic) {
            this.backgroundMusic.pause();
            this.backgroundMusic.currentTime = 0;
            this.isBackgroundMusicPlaying = false;
        }
    }

    /**
     * Pause background music
     */
    pauseBackgroundMusic() {
        if (this.backgroundMusic) {
            this.backgroundMusic.pause();
            this.isBackgroundMusicPlaying = false;
        }
    }

    /**
     * Resume background music
     */
    resumeBackgroundMusic() {
        if (this.backgroundMusic && !this.isMuted) {
            this.backgroundMusic.play().catch(e => {
                if (this.config.settings.showErrors) {
                    console.warn('⚠️ Failed to resume background music', e);
                }
            });
            this.isBackgroundMusicPlaying = true;
        }
    }

    /**
     * Toggle mute
     */
    toggleMute() {
        this.isMuted = !this.isMuted;
        
        if (this.isMuted) {
            this.pauseBackgroundMusic();
        } else {
            this.resumeBackgroundMusic();
        }
        
        return this.isMuted;
    }

    /**
     * Set volume for specific sound
     */
    setVolume(soundKey, volume) {
        volume = Math.max(0, Math.min(1, volume)); // Clamp 0-1
        
        if (soundKey === 'backgroundMusic' && this.backgroundMusic) {
            this.backgroundMusic.volume = volume;
        } else if (this.sounds[soundKey]) {
            this.sounds[soundKey].volume = volume;
        }
    }

    /**
     * Set master volume
     */
    setMasterVolume(volume) {
        volume = Math.max(0, Math.min(1, volume));
        
        // Set background music volume
        if (this.backgroundMusic) {
            this.backgroundMusic.volume = this.config.sounds.backgroundMusic.volume * volume;
        }
        
        // Set all sound effects volume
        Object.keys(this.sounds).forEach(key => {
            if (this.sounds[key]) {
                this.sounds[key].volume = this.config.sounds[key].volume * volume;
            }
        });
    }
}

// Export untuk digunakan di file lain
if (typeof window !== 'undefined') {
    window.SoundManager = SoundManager;
}
