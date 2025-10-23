// Lokasi: static/main.js - WITH LEVEL UNLOCK SYSTEM

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
        ui.playerHpText.textContent = `100 / 100`;
        ui.bossHpText.textContent = `100 / 100`;
        
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
            playerHP = Math.max(0, playerHP - amount);
        } else if (damageTo === 'boss') {
            bossHP = Math.max(0, bossHP - amount);
        }

        console.log('After damage - Player HP:', playerHP, 'Boss HP:', bossHP);

        ui.playerHpBar.style.width = `${playerHP}%`;
        ui.bossHpBar.style.width = `${bossHP}%`;
        ui.playerHpText.textContent = `${playerHP} / 100`;
        ui.bossHpText.textContent = `${bossHP} / 100`;

        // CEK KONDISI MENANG/KALAH
        if (bossHP <= 0 && !isGameOver) {
            console.log('>>> BOSS DEFEATED - YOU WIN! <<<');
            isGameOver = true;
            stopTimer();
            
            // UNLOCK LEVEL BERIKUTNYA
            unlockNextLevel();
            
            setTimeout(() => showVictoryOverlay(), 500);
        } else if (playerHP <= 0 && !isGameOver) {
            console.log('>>> PLAYER DEFEATED - GAME OVER <<<');
            isGameOver = true;
            stopTimer();
            setTimeout(() => showGameOverOverlay(), 500);
        }
    };

    // --- ALUR GAME ---

    const submitAnswerHandler = async () => {
        if (isGameOver || !selectedAnswer) return;
        
        console.log('Submitting answer:', selectedAnswer);
        
        stopTimer();
        document.querySelectorAll('.option-btn').forEach(btn => btn.disabled = true);
        ui.submitBtn.disabled = true;

        try {
            const response = await fetch(`/api/answer`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    question_id: currentQuestionId, 
                    answer: selectedAnswer, 
                    stage_name: stageName, 
                    level_num: levelNum 
                })
            });
            const result = await response.json();
            
            console.log('Answer result:', result);
            
            if (result.correct) {
                ui.feedbackArea.textContent = 'Benar! Serangan berhasil!';
                ui.feedbackArea.style.color = 'green';
                applyDamageAndCheckStatus('boss', 10);
            } else {
                ui.feedbackArea.textContent = `Salah! ❌ Jawaban yang benar: ${result.canonical_answer}`;
                ui.feedbackArea.style.color = 'red';
                applyDamageAndCheckStatus('player', 20);
            }

            if (!isGameOver) {
                ui.submitBtn.classList.add('hidden');
                ui.continueBtn.textContent = 'Soal Berikutnya';
                ui.continueBtn.onclick = fetchAndDisplayQuestion;
                ui.continueBtn.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Error submitting answer:', error);
            ui.feedbackArea.textContent = 'Error: Gagal mengirim jawaban';
            ui.feedbackArea.style.color = 'red';
        }
    };

    const handleTimeOut = () => {
        if (isGameOver) return;
        
        console.log('Time out!');
        
        ui.feedbackArea.textContent = 'Waktu Habis! Kamu terkena serangan!';
        ui.feedbackArea.style.color = 'orange';
        
        applyDamageAndCheckStatus('player', 5);

        if (!isGameOver) {
            ui.continueBtn.textContent = 'Soal Berikutnya';
            ui.continueBtn.onclick = fetchAndDisplayQuestion;
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
        
        let timerValue = 60;
        ui.timerDisplay.textContent = timerValue;
        stopTimer();
        
        timer = setInterval(() => {
            if (isGameOver) {
                stopTimer();
                return;
            }
            
            timerValue--;
            ui.timerDisplay.textContent = timerValue;
            
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
            ui.questionArea.innerHTML = `<p>Soal:</p><div>$$${question.latex}$$</div>`;
            
            question.options.forEach(option => {
                const button = document.createElement('button');
                button.className = 'option-btn';
                button.textContent = option;
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
            console.error('Error fetching question:', error);
            ui.questionArea.innerHTML = `<p style="color: red;">Gagal memuat soal: ${error.message}</p>`;
        }
    };

    // --- EVENT LISTENERS ---
    ui.submitBtn.addEventListener('click', submitAnswerHandler);
    ui.retryBtn.addEventListener('click', () => {
        console.log('Retry button clicked');
        startLevel();
    });
    
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            if (!ui.submitBtn.disabled && !ui.submitBtn.classList.contains('hidden')) {
                submitAnswerHandler();
            } else if (!ui.continueBtn.classList.contains('hidden') && !isGameOver) {
                ui.continueBtn.click();
            }
        }
    });

    // --- MULAI PERMAINAN ---
    console.log('Initializing game...');
    startLevel();
});