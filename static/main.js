// Lokasi: static/main.js

// --- Event Listener untuk Toggle Developer Mode ---
document.addEventListener('DOMContentLoaded', () => {
    const devToggle = document.getElementById('dev-mode-toggle');
    if (devToggle) {
        devToggle.addEventListener('change', async function() {
            try {
                const response = await fetch('/api/dev/toggle-dev-mode', { 
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const result = await response.json();
                // Reload halaman untuk melihat perubahan
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
    
    const stageName = ui.fightContainer.dataset.stageName;
    const levelNum = ui.fightContainer.dataset.levelNum;

    // ==========================================================
    // --- FUNGSI UTAMA GAME ---
    // ==========================================================

    /**
     * Memulai level. Ini adalah satu-satunya titik masuk.
     */
    const startLevel = () => {
        // 1. ATUR HP PLAYER DAN BOSS DAHULU
        playerHP = 100;
        bossHP = 100;
        isGameOver = false;

        // 2. ATUR TAMPILAN VISUAL HP
        ui.playerHpBar.style.width = '100%';
        ui.bossHpBar.style.width = '100%';
        ui.playerHpText.textContent = `100 / 100`;
        ui.bossHpText.textContent = `100 / 100`;
        
        // 3. SEMBUNYIKAN LAYAR KEMENANGAN/KEKALAHAN
        ui.gameOverOverlay.classList.add('hidden');
        ui.victoryOverlay.classList.add('hidden');
        
        // 4. BARU MUAT SOAL SETELAH SEMUANYA SIAP
        fetchAndDisplayQuestion();
    };

    /**
     * Fungsi ini dipanggil HANYA SETELAH ada perubahan HP.
     * Ini adalah satu-satunya tempat logika menang/kalah berada.
     */
    const applyDamageAndCheckStatus = (damageTo, amount) => {
        if (damageTo === 'player') {
            playerHP -= amount;
        } else if (damageTo === 'boss') {
            bossHP -= amount;
        }

        // Update tampilan visual HP
        playerHP = Math.max(0, playerHP);
        bossHP = Math.max(0, bossHP);
        ui.playerHpBar.style.width = `${playerHP}%`;
        ui.bossHpBar.style.width = `${bossHP}%`;
        ui.playerHpText.textContent = `${playerHP} / 100`;
        ui.bossHpText.textContent = `${bossHP} / 100`;

        // LOGIKA EKSPLISIT SESUAI PERMINTAAN ANDA
        if (bossHP <= 0) {
            isGameOver = true;
            stopTimer();
            ui.victoryOverlay.classList.remove('hidden');
        } else if (playerHP <= 0) {
            isGameOver = true;
            stopTimer();
            ui.gameOverOverlay.classList.remove('hidden');
        }
    };

    // --- ALUR GAME ---

    const submitAnswerHandler = async () => {
        if (isGameOver || !selectedAnswer) return;
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
            ui.feedbackArea.textContent = 'Benar! Serangan berhasil!';
            ui.feedbackArea.style.color = 'green';
            applyDamageAndCheckStatus('boss', 10); // Serang boss
        } else {
            ui.feedbackArea.textContent = `Salah! ❌ Jawaban yang benar: ${result.canonical_answer}`;
            ui.feedbackArea.style.color = 'red';
            applyDamageAndCheckStatus('player', 20); // Serang player
        }

        if (!isGameOver) {
            ui.submitBtn.classList.add('hidden');
            ui.continueBtn.textContent = 'Soal Berikutnya';
            ui.continueBtn.onclick = fetchAndDisplayQuestion;
            ui.continueBtn.classList.remove('hidden');
        }
    };

    const handleTimeOut = () => {
        if (isGameOver) return;
        ui.feedbackArea.textContent = 'Waktu Habis! Kamu terkena serangan!';
        ui.feedbackArea.style.color = 'orange';
        
        applyDamageAndCheckStatus('player', 5); // Serang player

        if (!isGameOver) {
            ui.continueBtn.textContent = 'Beralih ke Soal Lain';
            ui.continueBtn.onclick = fetchAndDisplayQuestion;
            ui.continueBtn.classList.remove('hidden');
            ui.submitBtn.classList.add('hidden');
            document.querySelectorAll('.option-btn').forEach(btn => btn.disabled = true);
        }
    };
    
    // --- FUNGSI-FUNGSI BANTU ---
    const stopTimer = () => clearInterval(timer);
    const startTimer = () => {
        if (isGameOver) return;
        let timerValue = 60;
        ui.timerDisplay.textContent = timerValue;
        stopTimer();
        timer = setInterval(() => {
            if (isGameOver) { stopTimer(); return; }
            timerValue--;
            ui.timerDisplay.textContent = timerValue;
            if (timerValue <= 0) {
                stopTimer();
                handleTimeOut();
            }
        }, 1000);
    };

    const fetchAndDisplayQuestion = async () => {
        if (isGameOver) return;
        
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
            ui.questionArea.innerHTML = `<p style="color: red;">Gagal memuat soal.</p>`;
        }
    };

    // --- EVENT LISTENERS ---
    ui.submitBtn.addEventListener('click', submitAnswerHandler);
    ui.retryBtn.addEventListener('click', startLevel);
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
    startLevel();
});