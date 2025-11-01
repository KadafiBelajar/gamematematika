// ==========================================================
// --- GLOBAL MANAGERS ---
// ==========================================================
let characterAnimator = null;
let soundManager = null;
let globalBackgroundMusic = null; // Global audio instance

// ==========================================================
// --- GLOBAL BACKGROUND MUSIC ---
// ==========================================================
let lastSavedTime = 0; // Global variable for tracking last save time

function initializeGlobalBackgroundMusic() {
    // Create new audio instance
    globalBackgroundMusic = new Audio('/static/assets/sounds/background-music.mp3');
    globalBackgroundMusic.loop = true;
    globalBackgroundMusic.volume = 0.3;
    
    // Try to restore playback position from sessionStorage
    const savedPosition = sessionStorage.getItem('musicPosition');
    const savedStartTime = sessionStorage.getItem('musicStartTime');
    
    if (savedPosition && savedStartTime) {
        const now = Date.now();
        const elapsed = (now - parseInt(savedStartTime)) / 1000; // elapsed in seconds
        const position = parseFloat(savedPosition) + elapsed;
        
        // Limit to audio duration to avoid issues
        globalBackgroundMusic.addEventListener('loadedmetadata', () => {
            const duration = globalBackgroundMusic.duration;
            if (position < duration && position > 0) {
                globalBackgroundMusic.currentTime = position;
                console.log(`🎵 Resuming music at position: ${position.toFixed(1)}s`);
            }
        });
    }
    
    // Handle errors
    globalBackgroundMusic.addEventListener('error', (e) => {
        console.error('❌ Error loading background music:', e);
    });
    
    // Save playback position every 5 seconds
    globalBackgroundMusic.addEventListener('timeupdate', () => {
        const now = Date.now();
        if (now - lastSavedTime > 5000) { // Save every 5 seconds
            sessionStorage.setItem('musicPosition', globalBackgroundMusic.currentTime.toString());
            sessionStorage.setItem('musicStartTime', now.toString());
            lastSavedTime = now;
        }
    });
    
    console.log('🎵 Global background music created');
}

function startGlobalBackgroundMusic() {
    if (globalBackgroundMusic) {
        globalBackgroundMusic.play().catch(e => {
            console.warn('⚠️ Could not play background music:', e);
        });
    } else {
        initializeGlobalBackgroundMusic();
    }
}

// ==========================================================
// --- PARTICLES ANIMATION ---
// ==========================================================
function initParticles() {
    const particlesContainer = document.getElementById('particles-container');
    if (!particlesContainer) return;
    
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 3}s`;
        particle.style.animationDuration = `${3 + Math.random() * 2}s`;
        particlesContainer.appendChild(particle);
    }
}

// ==========================================================
// --- ATTACK EFFECTS ---
// ==========================================================
function createSlashEffect(target = 'boss') {
    const effectsContainer = document.getElementById('attack-effects');
    if (!effectsContainer) return;
    
    const slash = document.createElement('div');
    slash.className = 'slash-effect';
    slash.style.top = `${Math.random() * 50 + 25}%`;
    
    if (target === 'boss') {
        slash.style.left = '50%';
    } else {
        slash.style.left = '10%';
        slash.style.transform = 'rotate(45deg)';
    }
    
    effectsContainer.appendChild(slash);
    
    setTimeout(() => slash.remove(), 500);
}

function animateAttack(attacker, playSound = true) {
    const element = document.getElementById(`${attacker}-avatar`);
    if (element) {
        element.classList.add('attacking');
        setTimeout(() => element.classList.remove('attacking'), 500);
    }
    
    // Play attack animation menggunakan CharacterAnimator
    if (characterAnimator) {
        characterAnimator.playAttackAnimation(attacker);
    }
    
    // Play attack sound (disabled by default to avoid duplicate sounds)
    if (playSound && soundManager) {
        const soundKey = attacker === 'player' ? 'playerAttack' : 'bossAttack';
        soundManager.play(soundKey);
    }
}

function animateDamage(target, playSound = true) {
    const element = document.getElementById(`${target}-avatar`);
    const hpBar = document.getElementById(`${target}-hp-bar`);
    
    if (element) {
        element.classList.add('damaged');
        setTimeout(() => element.classList.remove('damaged'), 500);
    }
    
    if (hpBar) {
        hpBar.classList.add('damaged');
        setTimeout(() => hpBar.classList.remove('damaged'), 300);
    }
    
    // Play hit animation menggunakan CharacterAnimator
    if (characterAnimator) {
        characterAnimator.playHitAnimation(target);
    }
    
    // Play hit sound (disabled by default to avoid duplicate sounds)
    if (playSound && soundManager) {
        const soundKey = target === 'player' ? 'playerHit' : 'bossHit';
        soundManager.play(soundKey);
    }
}

// ==========================================================
// --- HEAL ANIMATION ---
// ==========================================================
function animateHeal() {
    const playerAvatar = document.getElementById('player-avatar');
    if (!playerAvatar) return;
    
    // Create healing particles
    for (let i = 0; i < 10; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.style.width = '6px';
        particle.style.height = '6px';
        particle.style.background = '#3b82f6';
        particle.style.borderRadius = '50%';
        particle.style.boxShadow = '0 0 10px #3b82f6';
        particle.style.left = '50%';
        particle.style.top = '50%';
        particle.style.transform = 'translate(-50%, -50%)';
        particle.style.animation = `heal-particle ${0.8 + Math.random() * 0.4}s ease-out forwards`;
        particle.style.animationDelay = `${i * 0.05}s`;
        
        playerAvatar.appendChild(particle);
        
        setTimeout(() => particle.remove(), 1500);
    }
    
    // Play heal sound
    if (soundManager) {
        soundManager.play('heal');
    }
}

// Add heal particle animation to CSS dynamically
if (!document.querySelector('#heal-particle-style')) {
    const style = document.createElement('style');
    style.id = 'heal-particle-style';
    style.textContent = `
        @keyframes heal-particle {
            0% {
                transform: translate(-50%, -50%) scale(0);
                opacity: 1;
            }
            100% {
                transform: translate(${Math.random() * 200 - 100}px, ${-100 - Math.random() * 100}px) scale(1);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// ==========================================================
// --- INITIALIZE MANAGERS ---
// ==========================================================
async function initializeManagers() {
    console.log('🚀 Initializing managers...');
    
    // Initialize Character Animator
    if (typeof ASSETS_CONFIG !== 'undefined' && typeof CharacterAnimator !== 'undefined') {
        characterAnimator = new CharacterAnimator(ASSETS_CONFIG);
        await characterAnimator.init();
    } else {
        console.warn('⚠️ CharacterAnimator or ASSETS_CONFIG not available');
    }
    
    // Initialize Sound Manager
    if (typeof ASSETS_CONFIG !== 'undefined' && typeof SoundManager !== 'undefined') {
        soundManager = new SoundManager(ASSETS_CONFIG);
        await soundManager.init();
        
        // Auto-play background music (user interaction required)
        // Will be played on first user interaction
    } else {
        console.warn('⚠️ SoundManager or ASSETS_CONFIG not available');
    }
    
    console.log('✅ Managers initialized');
}

// ==========================================================
// --- Event Listener untuk Toggle Developer Mode ---
// ==========================================================
document.addEventListener('DOMContentLoaded', async () => {
    // Initialize particles
    initParticles();
    
    // Initialize managers (Character Animator & Sound Manager)
    await initializeManagers();
    
    // Note: Global background music is NOT started here for non-battle pages
    // Background music will only play in battle mode (handled in battle-specific code below)
    
    const devToggle = document.getElementById('dev-mode-toggle');
    if (devToggle) {
        devToggle.addEventListener('change', async function() {
            try {
                const response = await fetch('/api/dev/toggle-dev-mode', { 
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const result = await response.json();
                location.reload();
            } catch (error) {
                console.error('Error toggling dev mode:', error);
                alert('Gagal mengubah Developer Mode');
            }
        });
    }
});

// --- Game Logic (hanya untuk halaman main.html) ---
document.addEventListener('DOMContentLoaded', () => {
    // --- State & UI Elements ---
    let playerHP;
    let bossHP;
    let isGameOver;
    let isPaused = false;
    let timer;
    let currentQuestionId;
    let selectedAnswer;
    let musicVolume = 50;
    let sfxVolume = 50;

    const ui = {
        playerHpBar: document.getElementById('player-hp-bar'),
        playerHpText: document.getElementById('player-hp-text'),
        bossHpBar: document.getElementById('boss-hp-bar'),
        bossHpText: document.getElementById('boss-hp-text'),
        timerDisplay: document.getElementById('timer-display'),
        questionArea: document.getElementById('question-area'),
        optionsContainer: document.getElementById('options-container'),
        feedbackArea: document.getElementById('feedback-area'),
        continueBtn: document.getElementById('continue-btn'),
        submitBtn: document.getElementById('submit-btn'),
        gameOverOverlay: document.getElementById('game-over-overlay'),
        victoryOverlay: document.getElementById('victory-overlay'),
        pauseOverlay: document.getElementById('pause-overlay'),
        settingsOverlay: document.getElementById('settings-overlay'),
        retryBtn: document.getElementById('retry-btn'),
        fightContainer: document.querySelector('.fight-container'),
        pauseBtn: document.getElementById('pause-btn'),
        resumeBtn: document.getElementById('resume-btn'),
        restartBtn: document.getElementById('restart-btn'),
        settingsBtn: document.getElementById('settings-btn'),
        settingsBackBtn: document.getElementById('settings-back-btn'),
        musicVolumeSlider: document.getElementById('music-volume'),
        sfxVolumeSlider: document.getElementById('sfx-volume'),
        musicVolumeValue: document.getElementById('music-volume-value'),
        sfxVolumeValue: document.getElementById('sfx-volume-value'),
        nextLevelBtn: document.getElementById('next-level-btn'),
    };
    
    const fightContainer = document.querySelector('.fight-container');
    if (!fightContainer) return; // Keluar jika tidak di halaman pertarungan

    const stageName = ui.fightContainer.dataset.stageName;
    const levelNum = ui.fightContainer.dataset.levelNum;

    // ==========================================================
    // HELPER FUNCTIONS - SHOW/HIDE OVERLAY
    // ==========================================================
    
    function hideAllOverlays() {
        ui.gameOverOverlay.classList.add('hidden');
        ui.gameOverOverlay.style.display = 'none';
        ui.gameOverOverlay.style.visibility = 'hidden';
        
        ui.victoryOverlay.classList.add('hidden');
        ui.victoryOverlay.style.display = 'none';
        ui.victoryOverlay.style.visibility = 'hidden';
        
        ui.pauseOverlay.classList.add('hidden');
        ui.pauseOverlay.style.display = 'none';
        ui.pauseOverlay.style.visibility = 'hidden';
        
        ui.settingsOverlay.classList.add('hidden');
        ui.settingsOverlay.style.display = 'none';
        ui.settingsOverlay.style.visibility = 'hidden';
    }
    
    function showGameOverOverlay() {
        hideAllOverlays();
        ui.gameOverOverlay.classList.remove('hidden');
        ui.gameOverOverlay.style.display = 'flex';
        ui.gameOverOverlay.style.visibility = 'visible';
    }
    
    function showVictoryOverlay() {
        hideAllOverlays();
        ui.victoryOverlay.classList.remove('hidden');
        ui.victoryOverlay.style.display = 'flex';
        ui.victoryOverlay.style.visibility = 'visible';
    }
    
    function showPauseOverlay() {
        isPaused = true;
        stopTimer();
        ui.pauseOverlay.classList.remove('hidden');
        ui.pauseOverlay.style.display = 'flex';
        ui.pauseOverlay.style.visibility = 'visible';
        // Pause global background music
        if (globalBackgroundMusic) {
            globalBackgroundMusic.pause();
        }
    }
    
    function hidePauseOverlay() {
        isPaused = false;
        ui.pauseOverlay.classList.add('hidden');
        ui.pauseOverlay.style.display = 'none';
        ui.pauseOverlay.style.visibility = 'hidden';
        // Resume global background music
        if (globalBackgroundMusic) {
            globalBackgroundMusic.play();
        }
    }
    
    function showSettingsOverlay() {
        ui.pauseOverlay.classList.add('hidden');
        ui.settingsOverlay.classList.remove('hidden');
        ui.settingsOverlay.style.display = 'flex';
        ui.settingsOverlay.style.visibility = 'visible';
    }
    
    function hideSettingsOverlay() {
        ui.settingsOverlay.classList.add('hidden');
        ui.settingsOverlay.style.display = 'none';
        ui.settingsOverlay.style.visibility = 'hidden';
        showPauseOverlay();
    }

    // ==========================================================
    // --- FUNGSI UTAMA GAME ---
    // ==========================================================

    const startLevel = () => {
        console.log('=== START LEVEL ===');
        
        isGameOver = false;
        selectedAnswer = null;
        
        playerHP = 100;
        bossHP = 100;
        
        console.log('Player HP:', playerHP, 'Boss HP:', bossHP);

        ui.playerHpBar.style.width = '100%';
        ui.bossHpBar.style.width = '100%';
        ui.playerHpText.textContent = '100%';
        ui.bossHpText.textContent = '100%';
        
        hideAllOverlays();
        
        console.log('Overlays hidden');
        
        ui.feedbackArea.innerHTML = '';
        ui.continueBtn.classList.add('hidden');
        
        fetchAndDisplayQuestion();
    };

    /**
     * FUNGSI BARU: Unlock level berikutnya saat boss dikalahkan
     */
    const unlockNextLevel = async () => {
        console.log('>>> Attempting to unlock next level...');
        
        try {
            const response = await fetch('/api/level-complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    stage_name: stageName, 
                    level_num: levelNum 
                })
            });
            
            const result = await response.json();
            console.log('Unlock result:', result);
            
            if (result.next_level) {
                console.log(`✅ Level ${result.next_level} UNLOCKED!`);
            } else {
                console.log('ℹ️ No new level to unlock (max level or already unlocked)');
            }
        } catch (error) {
            console.error('Error unlocking level:', error);
        }
    };

    const applyDamageAndCheckStatus = (damageTo, amount) => {
        console.log(`=== APPLY DAMAGE: ${amount} to ${damageTo} ===`);
        
        if (damageTo === 'player') {
            playerHP -= amount;
        } else if (damageTo === 'boss') {
            bossHP -= amount;
        }

        console.log('After damage - Player HP:', playerHP, 'Boss HP:', bossHP);

        ui.playerHpBar.style.width = `${playerHP}%`;
        ui.bossHpBar.style.width = `${bossHP}%`;
        ui.playerHpText.textContent = `${playerHP}%`;
        ui.bossHpText.textContent = `${bossHP}%`;

        // CEK KONDISI MENANG/KALAH
        if (bossHP <= 0 && !isGameOver) {
            console.log('>>> BOSS DEFEATED - YOU WIN! <<<');
            isGameOver = true;
            stopTimer();
            
            // Unlock next level
            unlockNextLevel();
            
            // Play victory sound
            if (soundManager) {
                soundManager.play('victory');
            }
            // Note: Background music continues playing
            
            setTimeout(() => {
                showVictoryOverlay();
            }, 500);
        } else if (playerHP <= 0 && !isGameOver) {
            console.log('>>> PLAYER DEFEATED - GAME OVER <<<');
            isGameOver = true;
            stopTimer();
            
            // Play defeat sound
            if (soundManager) {
                soundManager.play('defeat');
            }
            // Note: Background music continues playing
            
            setTimeout(() => {
                showGameOverOverlay();
            }, 500);
        } else {
            // Only play damage animation if game is not over
            animateDamage(damageTo);
        }
    };

    // --- ALUR GAME ---

    const submitAnswerHandler = async () => {
        if (isGameOver || !selectedAnswer) return;
        
        console.log('Submitting answer:', selectedAnswer);
        
        stopTimer();
        document.querySelectorAll('.option-btn').forEach(btn => btn.disabled = true);
        ui.submitBtn.disabled = true;

        const response = await fetch(`/api/answer`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question_id: currentQuestionId, answer: selectedAnswer, stage_name: stageName, level_num: levelNum })
        });
        const result = await response.json();
        
        if (result.correct) {
            ui.feedbackArea.textContent = '✓ Benar! Serangan berhasil!';
            ui.feedbackArea.style.color = '#10b981';
            
            // Play player attack sound
            if (soundManager) soundManager.play('playerAttack');
            
            // Animate player attack (no sound, already played above)
            animateAttack('player', false);
            createSlashEffect('boss');
            
            setTimeout(() => {
                applyDamageAndCheckStatus('boss', 10); // Serang boss (plays bossHit)
            }, 300);
        } else {
            ui.feedbackArea.textContent = `✗ Salah! Jawaban yang benar: ${result.canonical_answer}`;
            ui.feedbackArea.style.color = '#ff4b4b';
            
            // Play boss attack sound
            if (soundManager) soundManager.play('bossAttack');
            
            // Animate boss attack (no sound, already played above)
            animateAttack('boss', false);
            createSlashEffect('player');
            
            setTimeout(() => {
                applyDamageAndCheckStatus('player', 20); // Serang player (plays playerHit)
            }, 300);
        }

        if (!isGameOver) {
            ui.submitBtn.classList.add('hidden');
            ui.continueBtn.classList.remove('hidden');
        }
    };

    const handleTimeOut = () => {
        if (isGameOver || isPaused) return;
        ui.feedbackArea.textContent = '⏱ Waktu Habis! Kamu terkena serangan!';
        ui.feedbackArea.style.color = '#f59e0b';
        
        animateAttack('boss');
        createSlashEffect('player');
        
        setTimeout(() => {
            applyDamageAndCheckStatus('player', 5); // Serang player
        }, 300);

        if (!isGameOver) {
            ui.continueBtn.classList.remove('hidden');
            ui.submitBtn.classList.add('hidden');
            document.querySelectorAll('.option-btn').forEach(btn => btn.disabled = true);
        }
    };
    
    // --- FUNGSI-FUNGSI BANTU ---
    const stopTimer = () => {
        if (timer) {
            clearInterval(timer);
            timer = null;
        }
    };
    
    const startTimer = () => {
        if (isGameOver || isPaused) return;
        let timerValue = 90;
        let warningPlayed = false;
        ui.timerDisplay.textContent = timerValue;
        ui.timerDisplay.classList.remove('warning', 'critical');
        stopTimer();
        
        timer = setInterval(() => {
            if (isGameOver || isPaused) {
                stopTimer();
                return;
            }
            
            timerValue--;
            ui.timerDisplay.textContent = timerValue;
            
            // Visual warnings
            if (timerValue <= 10) {
                ui.timerDisplay.classList.add('critical');
                
                // Play warning sound once
                if (!warningPlayed && soundManager) {
                    soundManager.play('timerWarning');
                    warningPlayed = true;
                }
            } else if (timerValue <= 30) {
                ui.timerDisplay.classList.add('warning');
            }
            
            if (timerValue <= 0) {
                stopTimer();
                handleTimeOut();
            }
        }, 1000);
    };

    const fetchAndDisplayQuestion = async () => {
        if (isGameOver) {
            console.log('Game is over, not fetching new question');
            return;
        }
        
        console.log('Fetching new question...');
        
        ui.continueBtn.classList.add('hidden');
        ui.questionArea.innerHTML = '<p>Memuat soal...</p>';
        ui.optionsContainer.innerHTML = '';
        ui.feedbackArea.innerHTML = '';
        selectedAnswer = null;
        ui.submitBtn.disabled = true;
        ui.submitBtn.classList.remove('hidden');
        
        try {
            const response = await fetch(`/api/question?stage=${encodeURIComponent(stageName)}&level=${levelNum}`);
            const question = await response.json();
            
            console.log('Question loaded:', question.id);
            
            currentQuestionId = question.id;
            ui.questionArea.innerHTML = `<div>$$${question.latex}$$</div>`;
            const displayList = question.options_display && question.options_display.length === question.options.length
                ? question.options_display
                : question.options;

            question.options.forEach((option, index) => {
                const button = document.createElement('button');
                button.className = 'option-btn';
                // Tampilkan LaTeX, tetapi simpan nilai asli untuk dikirim saat submit
                button.dataset.value = option;
                button.innerHTML = `$$${displayList[index]}$$`;
                button.style.animationDelay = `${index * 0.1}s`;
                button.onclick = () => {
                    if (isGameOver) return;
                    document.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('selected'));
                    button.classList.add('selected');
                    selectedAnswer = button.dataset.value;
                    ui.submitBtn.disabled = false;
                };
                ui.optionsContainer.appendChild(button);
            });
            
            MathJax.typesetPromise([ui.questionArea, ui.optionsContainer]);
            startTimer();
        } catch (error) {
            ui.questionArea.innerHTML = `<p style="color: #ff4b4b;">Gagal memuat soal.</p>`;
        }
    };

    // --- HEAL BUTTON LOGIC ---
    const healBtn = document.getElementById('heal-btn');
    let healCount = 3; // Player can heal 3 times per level
    
    const handleHeal = () => {
        if (healCount <= 0 || isGameOver || playerHP >= 100) return;
        
        healCount--;
        const healAmount = 25;
        playerHP = Math.min(100, playerHP + healAmount);
        
        // Update UI
        ui.playerHpBar.style.width = `${playerHP}%`;
        ui.playerHpText.textContent = `${playerHP}%`;
        
        // Show feedback
        ui.feedbackArea.textContent = `💙 +${healAmount} HP! (${healCount} heal tersisa)`;
        ui.feedbackArea.style.color = '#3b82f6';
        
        // Animate
        animateHeal();
        
        // Disable button if no heals left
        if (healCount <= 0) {
            healBtn.disabled = true;
            healBtn.style.opacity = '0.3';
        }
        
        // Update button text
        healBtn.querySelector('span').textContent = `HEAL (${healCount})`;
        
        setTimeout(() => {
            ui.feedbackArea.textContent = '';
        }, 2000);
    };
    
    if (healBtn) {
        healBtn.addEventListener('click', handleHeal);
        healBtn.querySelector('span').textContent = `HEAL (${healCount})`;
    }

    // ==========================================================
    // VOLUME CONTROL
    // ==========================================================
    const updateMusicVolume = (value) => {
        musicVolume = value;
        ui.musicVolumeValue.textContent = `${value}%`;
        if (soundManager && soundManager.backgroundMusic) {
            soundManager.backgroundMusic.volume = value / 100;
        }
    };
    
    const updateSfxVolume = (value) => {
        sfxVolume = value;
        ui.sfxVolumeValue.textContent = `${value}%`;
        if (soundManager) {
            // Update all sound effects volume
            Object.keys(soundManager.sounds).forEach(key => {
                if (soundManager.sounds[key]) {
                    const baseVolume = soundManager.config.sounds[key].volume || 0.5;
                    soundManager.sounds[key].volume = baseVolume * (value / 100);
                }
            });
        }
    };
    
    // ==========================================================
    // NEXT LEVEL HANDLER
    // ==========================================================
    const handleNextLevel = async () => {
        try {
            const nextLevel = parseInt(levelNum) + 1;
            window.location.href = `/main/${stageName}/${nextLevel}`;
        } catch (error) {
            console.error('Error navigating to next level:', error);
            // Fallback ke level select
            window.location.href = `/levels/${stageName}`;
        }
    };
    
    // ==========================================================
    // EVENT LISTENERS
    // ==========================================================
    
    // Submit & Continue
    ui.submitBtn.addEventListener('click', submitAnswerHandler);
    
    if (ui.continueBtn) {
        ui.continueBtn.addEventListener('click', fetchAndDisplayQuestion);
    }
    
    // Retry Button
    ui.retryBtn.addEventListener('click', () => {
        healCount = 3;
        if (healBtn) {
            healBtn.disabled = false;
            healBtn.style.opacity = '1';
            healBtn.querySelector('span').textContent = `HEAL (${healCount})`;
        }
        startLevel();
    });
    
    // Pause Menu Buttons
    if (ui.pauseBtn) {
        ui.pauseBtn.addEventListener('click', () => {
            if (!isGameOver) {
                showPauseOverlay();
            }
        });
    }
    
    if (ui.resumeBtn) {
        ui.resumeBtn.addEventListener('click', () => {
            hidePauseOverlay();
            if (!isGameOver && !isPaused) {
                startTimer();
            }
        });
    }
    
    if (ui.restartBtn) {
        ui.restartBtn.addEventListener('click', () => {
            hidePauseOverlay();
            healCount = 3;
            if (healBtn) {
                healBtn.disabled = false;
                healBtn.style.opacity = '1';
                healBtn.querySelector('span').textContent = `HEAL (${healCount})`;
            }
            startLevel();
        });
    }
    
    if (ui.settingsBtn) {
        ui.settingsBtn.addEventListener('click', () => {
            showSettingsOverlay();
        });
    }
    
    if (ui.settingsBackBtn) {
        ui.settingsBackBtn.addEventListener('click', () => {
            hideSettingsOverlay();
        });
    }
    
    // Next Level Button
    if (ui.nextLevelBtn) {
        ui.nextLevelBtn.addEventListener('click', handleNextLevel);
    }
    
    // Volume Sliders
    if (ui.musicVolumeSlider) {
        ui.musicVolumeSlider.addEventListener('input', (e) => {
            updateMusicVolume(parseInt(e.target.value));
        });
    }
    
    if (ui.sfxVolumeSlider) {
        ui.sfxVolumeSlider.addEventListener('input', (e) => {
            updateSfxVolume(parseInt(e.target.value));
        });
    }
    
    // Keyboard Events
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            if (!isPaused && !ui.submitBtn.disabled && !ui.submitBtn.classList.contains('hidden')) {
                submitAnswerHandler();
            } else if (!isPaused && !ui.continueBtn.classList.contains('hidden') && !isGameOver) {
                fetchAndDisplayQuestion();
            }
        }
        
        // ESC to pause/unpause
        if (event.key === 'Escape') {
            event.preventDefault();
            if (!isGameOver) {
                if (isPaused) {
                    if (!ui.settingsOverlay.classList.contains('hidden')) {
                        hideSettingsOverlay();
                    } else {
                        hidePauseOverlay();
                        startTimer();
                    }
                } else {
                    showPauseOverlay();
                }
            }
        }
    });
    
    // Click outside pause menu to resume
    if (ui.pauseOverlay) {
        ui.pauseOverlay.addEventListener('click', (event) => {
            // Check if click is directly on the overlay (not on its children)
            if (event.target === ui.pauseOverlay) {
                hidePauseOverlay();
                if (!isGameOver && !isPaused) {
                    startTimer();
                }
            }
        });
    }
    
    // Click outside settings menu to go back to pause menu
    if (ui.settingsOverlay) {
        ui.settingsOverlay.addEventListener('click', (event) => {
            // Check if click is directly on the overlay (not on its children)
            if (event.target === ui.settingsOverlay) {
                hideSettingsOverlay();
            }
        });
    }

    // ==========================================================
    // INITIALIZE VOLUME
    // ==========================================================
    const initializeVolume = () => {
        // Set initial volume values
        if (ui.musicVolumeSlider) {
            ui.musicVolumeSlider.value = musicVolume;
            ui.musicVolumeValue.textContent = `${musicVolume}%`;
        }
        
        if (ui.sfxVolumeSlider) {
            ui.sfxVolumeSlider.value = sfxVolume;
            ui.sfxVolumeValue.textContent = `${sfxVolume}%`;
        }
        
        // Apply initial volume to global background music
        if (globalBackgroundMusic) {
            globalBackgroundMusic.volume = musicVolume / 100;
        }
        
        // Apply volume to sound effects
        if (soundManager) {
            Object.keys(soundManager.sounds).forEach(key => {
                if (soundManager.sounds[key]) {
                    const baseVolume = soundManager.config.sounds[key].volume || 0.5;
                    soundManager.sounds[key].volume = baseVolume * (sfxVolume / 100);
                }
            });
        }
    };
    
    // --- MULAI PERMAINAN ---
    console.log('Initializing game...');
    
    // Initialize global background music for battle mode
    initializeGlobalBackgroundMusic();
    
    // Initialize volume controls
    initializeVolume();
    
    // Start global background music on first user interaction
    const startBackgroundMusic = () => {
        if (globalBackgroundMusic) {
            globalBackgroundMusic.play();
            // Apply music volume after starting
            globalBackgroundMusic.volume = musicVolume / 100;
        }
        // Remove listeners after first interaction
        document.removeEventListener('click', startBackgroundMusic);
        document.removeEventListener('keydown', startBackgroundMusic);
    };
    
    document.addEventListener('click', startBackgroundMusic, { once: true });
    document.addEventListener('keydown', startBackgroundMusic, { once: true });
    
    startLevel();
});