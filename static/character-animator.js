// ==========================================
// CHARACTER ANIMATOR
// ==========================================
// Sistem untuk mengelola animasi karakter (idle, attack, hit)
// Support: GIF, WebP, PNG dengan transparent background

class CharacterAnimator {
    constructor(config) {
        this.config = config;
        this.loadedImages = {
            player: {},
            boss: {}
        };
        this.currentState = {
            player: 'idle',
            boss: 'idle'
        };
        this.animationTimeouts = {
            player: null,
            boss: null
        };
    }

    /**
     * Initialize character animator
     */
    async init() {
        console.log('🎨 Initializing Character Animator...');
        
        // Preload images jika diaktifkan
        if (this.config.settings.preloadAssets) {
            await this.preloadAllImages();
        }
        
        // Setup initial character states
        this.setupCharacter('player');
        this.setupCharacter('boss');
        
        console.log('✅ Character Animator initialized');
    }

    /**
     * Preload semua gambar karakter
     */
    async preloadAllImages() {
        console.log('⏳ Preloading character images...');
        
        const promises = [];
        
        // Preload player images
        ['idle', 'attack', 'hit'].forEach(state => {
            if (this.config.player[state].image) {
                promises.push(this.loadImage('player', state));
            }
        });
        
        // Preload boss images
        ['idle', 'attack', 'hit'].forEach(state => {
            if (this.config.boss[state].image) {
                promises.push(this.loadImage('boss', state));
            }
        });
        
        await Promise.all(promises);
        console.log('✅ All images preloaded');
    }

    /**
     * Load single image
     */
    async loadImage(character, state) {
        return new Promise((resolve, reject) => {
            const imageConfig = this.config[character][state];
            
            if (!imageConfig || !imageConfig.image) {
                if (this.config.settings.showErrors) {
                    console.warn(`⚠️ No image configured for ${character} ${state}`);
                }
                resolve(null);
                return;
            }

            const img = new Image();
            
            img.onload = () => {
                this.loadedImages[character][state] = img;
                console.log(`✅ Loaded: ${character} ${state}`);
                resolve(img);
            };
            
            img.onerror = () => {
                if (this.config.settings.showErrors) {
                    console.warn(`⚠️ Failed to load image: ${imageConfig.image}`);
                }
                // Use fallback (SVG default)
                this.loadedImages[character][state] = null;
                resolve(null);
            };
            
            img.src = imageConfig.image;
        });
    }

    /**
     * Setup karakter dengan state awal (idle)
     */
    setupCharacter(character) {
        const avatarElement = document.getElementById(`${character}-avatar`);
        if (!avatarElement) {
            console.error(`Element not found: ${character}-avatar`);
            return;
        }

        const frameElement = avatarElement.querySelector('.avatar-frame');
        if (!frameElement) return;

        // Set idle animation sebagai default
        this.setState(character, 'idle');
    }

    /**
     * Set character state (idle, attack, hit)
     */
    setState(character, state) {
        const avatarElement = document.getElementById(`${character}-avatar`);
        if (!avatarElement) return;

        const frameElement = avatarElement.querySelector('.avatar-frame');
        if (!frameElement) return;

        // Clear previous timeout
        if (this.animationTimeouts[character]) {
            clearTimeout(this.animationTimeouts[character]);
            this.animationTimeouts[character] = null;
        }

        // Remove existing image if any
        const existingImage = frameElement.querySelector('.avatar-image');
        if (existingImage) {
            existingImage.remove();
        }

        // Check if we have custom image
        const img = this.loadedImages[character][state];
        
        if (img) {
            // Use custom image
            const imageElement = document.createElement('img');
            imageElement.src = img.src;
            imageElement.className = 'avatar-image';
            imageElement.alt = `${character} ${state}`;
            
            // Set size from config
            const config = this.config[character][state];
            if (config.width) imageElement.style.width = config.width + 'px';
            if (config.height) imageElement.style.height = config.height + 'px';
            
            frameElement.appendChild(imageElement);
            frameElement.classList.add('has-image');
            
            // Hide SVG fallback
            const svgIcon = frameElement.querySelector('.avatar-icon');
            if (svgIcon) svgIcon.style.display = 'none';
        } else {
            // Use SVG fallback
            frameElement.classList.remove('has-image');
            const svgIcon = frameElement.querySelector('.avatar-icon');
            if (svgIcon) svgIcon.style.display = 'block';
        }

        this.currentState[character] = state;
    }

    /**
     * Play attack animation
     */
    playAttackAnimation(character) {
        console.log(`⚔️ ${character} attacks!`);
        
        this.setState(character, 'attack');
        
        // Get duration from config
        const duration = this.config[character].attack.duration || 500;
        
        // Return to idle after animation
        this.animationTimeouts[character] = setTimeout(() => {
            this.setState(character, 'idle');
        }, duration);
    }

    /**
     * Play hit animation
     */
    playHitAnimation(character) {
        console.log(`💥 ${character} got hit!`);
        
        this.setState(character, 'hit');
        
        // Get duration from config
        const duration = this.config[character].hit.duration || 500;
        
        // Return to idle after animation
        this.animationTimeouts[character] = setTimeout(() => {
            this.setState(character, 'idle');
        }, duration);
    }

    /**
     * Force set to idle state
     */
    setIdle(character) {
        if (this.animationTimeouts[character]) {
            clearTimeout(this.animationTimeouts[character]);
            this.animationTimeouts[character] = null;
        }
        this.setState(character, 'idle');
    }

    /**
     * Get current state
     */
    getCurrentState(character) {
        return this.currentState[character];
    }
}

// Export untuk digunakan di file lain
if (typeof window !== 'undefined') {
    window.CharacterAnimator = CharacterAnimator;
}
