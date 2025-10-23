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

function animateAttack(attacker) {
    const element = document.getElementById(`${attacker}-avatar`);
    if (element) {
        element.classList.add('attacking');
        setTimeout(() => element.classList.remove('attacking'), 500);
    }
}

function animateDamage(target) {
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
// --- Event Listener untuk Toggle Developer Mode ---
// ==========================================================
document.addEventListener('DOMContentLoaded', () => {
    // Initialize particles
    initParticles();
    
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
    let timer;
    let currentQuestionId;
    let selectedAnswer;

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
        retryBtn: document.getElementById('retry-btn'),
        fightContainer: document.querySelector('.fight-container'),
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
            animateDamage('player');
        } else if (damageTo === 'boss') {
            bossHP -= amount;
            animateDamage('boss');
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
            setTimeout(() => {
                ui.victoryOverlay.classList.remove('hidden');
            }, 500);
        } else if (playerHP <= 0) {
            isGameOver = true;
            stopTimer();
            setTimeout(() => {
                ui.gameOverOverlay.classList.remove('hidden');
            }, 500);
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
            
            // Animate player attack
            animateAttack('player');
            createSlashEffect('boss');
            
            setTimeout(() => {
                applyDamageAndCheckStatus('boss', 10); // Serang boss
            }, 300);
        } else {
            ui.feedbackArea.textContent = `✗ Salah! Jawaban yang benar: ${result.canonical_answer}`;
            ui.feedbackArea.style.color = '#ff4b4b';
            
            // Animate boss attack
            animateAttack('boss');
            createSlashEffect('player');
            
            setTimeout(() => {
                applyDamageAndCheckStatus('player', 20); // Serang player
            }, 300);
        }

        if (!isGameOver) {
            ui.submitBtn.classList.add('hidden');
            ui.continueBtn.classList.remove('hidden');
        }
    };

    const handleTimeOut = () => {
        if (isGameOver) return;
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
        if (isGameOver) return;
        let timerValue = 90;
        ui.timerDisplay.textContent = timerValue;
        ui.timerDisplay.classList.remove('warning', 'critical');
        stopTimer();
        
        timer = setInterval(() => {
            if (isGameOver) {
                stopTimer();
                return;
            }
            
            timerValue--;
            ui.timerDisplay.textContent = timerValue;
            
            // Visual warnings
            if (timerValue <= 10) {
                ui.timerDisplay.classList.add('critical');
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
            const response = await fetch(`/api/question?level=${levelNum}`);
            const question = await response.json();
            
            console.log('Question loaded:', question.id);
            
            currentQuestionId = question.id;
            ui.questionArea.innerHTML = `<div>$$${question.latex}$$</div>`;
            question.options.forEach((option, index) => {
                const button = document.createElement('button');
                button.className = 'option-btn';
                button.textContent = option;
                button.style.animationDelay = `${index * 0.1}s`;
                button.onclick = () => {
                    if (isGameOver) return;
                    document.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('selected'));
                    button.classList.add('selected');
                    selectedAnswer = option;
                    ui.submitBtn.disabled = false;
                };
                ui.optionsContainer.appendChild(button);
            });
            
            MathJax.typesetPromise([ui.questionArea]);
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

    // --- EVENT LISTENERS ---
    ui.submitBtn.addEventListener('click', submitAnswerHandler);
    ui.retryBtn.addEventListener('click', () => {
        healCount = 3;
        if (healBtn) {
            healBtn.disabled = false;
            healBtn.style.opacity = '1';
            healBtn.querySelector('span').textContent = `HEAL (${healCount})`;
        }
        startLevel();
    });
    
    if (ui.continueBtn) {
        ui.continueBtn.addEventListener('click', fetchAndDisplayQuestion);
    }
    
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            if (!ui.submitBtn.disabled && !ui.submitBtn.classList.contains('hidden')) {
                submitAnswerHandler();
            } else if (!ui.continueBtn.classList.contains('hidden') && !isGameOver) {
                fetchAndDisplayQuestion();
            }
        }
    });

    // --- MULAI PERMAINAN ---
    console.log('Initializing game...');
    startLevel();
});