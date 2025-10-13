// Variabel global untuk menyimpan state permainan
let currentQuestionId = null;
let selectedAnswer = null;
let stageName = null;
let levelNum = null;

// Menjalankan logika utama setelah seluruh DOM siap
document.addEventListener('DOMContentLoaded', () => {
    const gameContainer = document.querySelector('.game-container');
    if (gameContainer) {
        initializeGame(gameContainer);
    }
});

function initializeGame(container) {
    const questionArea = document.getElementById('question-area');
    const optionsContainer = document.getElementById('options-container');
    const feedbackArea = document.getElementById('feedback-area');
    const postAnswerBtn = document.getElementById('next-question-btn');
    const submitBtn = document.getElementById('submit-btn');
    const explanationArea = document.getElementById('explanation-area');
    const explanationContent = document.getElementById('explanation-content');

    stageName = container.dataset.stageName;
    levelNum = container.dataset.levelNum;

    // Fungsi aman untuk merender MathJax, menunggu promise-nya selesai.
    function renderMath(element) {
        // Cek jika MathJax sudah ada di window
        if (window.MathJax && window.MathJax.startup) {
            MathJax.startup.promise
                .then(() => {
                    return MathJax.typesetPromise([element]);
                })
                .catch((err) => console.error("MathJax typesetting error:", err));
        }
    }

    async function fetchAndDisplayQuestion() {
        questionArea.innerHTML = '<p>Memuat soal...</p>';
        optionsContainer.innerHTML = '';
        feedbackArea.innerHTML = '';
        explanationArea.style.display = 'none';
        explanationContent.innerHTML = '';
        selectedAnswer = null;
        
        submitBtn.classList.remove('hidden');
        submitBtn.disabled = true;
        postAnswerBtn.classList.add('hidden');

        try {
            const response = await fetch(`/api/question?level=${levelNum}`);
            if (!response.ok) throw new Error('Gagal mengambil soal.');
            
            const question = await response.json();
            currentQuestionId = question.id;

            questionArea.innerHTML = `<p>Soal:</p><div>$$${question.latex}$$</div>`;
            
            question.options.forEach(option => {
                const button = document.createElement('button');
                button.className = 'option-btn';
                button.textContent = option;
                button.onclick = () => selectOption(button, option);
                optionsContainer.appendChild(button);
            });

            renderMath(questionArea);

        } catch (error) {
            questionArea.innerHTML = `<p style="color: red;">${error.message}</p>`;
        }
    }

    function selectOption(selectedButton, optionValue) {
        document.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('selected'));
        selectedButton.classList.add('selected');
        selectedAnswer = optionValue;
        submitBtn.disabled = false;
    }

    function displayExplanation(explanationData) {
        explanationContent.innerHTML = '';
        if (!explanationData || explanationData.length === 0) return;

        explanationData.forEach(item => {
            if (item.type === 'text' && item.content) {
                const p = document.createElement('p');
                p.textContent = item.content;
                explanationContent.appendChild(p);
            } else if (item.type === 'latex' && item.content) {
                const div = document.createElement('div');
                div.innerHTML = `$$${item.content}$$`;
                explanationContent.appendChild(div);
            }
        });

        explanationArea.style.display = 'block';
        
        renderMath(explanationContent);
    }

    async function submitAnswerHandler() {
        if (!selectedAnswer || submitBtn.disabled) return;

        document.querySelectorAll('.option-btn').forEach(btn => btn.disabled = true);
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    question_id: currentQuestionId,
                    answer: selectedAnswer,
                    stage_name: stageName,
                    level_num: parseInt(levelNum)
                })
            });

            if (!response.ok) {
                const err = await response.json().catch(()=>null);
                throw new Error(err?.error || 'Gagal mengirim jawaban.');
            }

            const result = await response.json();
            
            submitBtn.classList.add('hidden');
            postAnswerBtn.classList.remove('hidden');

            if (result.correct) {
                feedbackArea.textContent = 'Benar! ✅ Level Selesai!';
                feedbackArea.style.color = 'green';
                postAnswerBtn.textContent = 'Lanjut ke Peta Level';
                postAnswerBtn.onclick = () => {
                    window.location.href = `/levels/${stageName}`;
                };
            } else {
                feedbackArea.textContent = `Salah! ❌ Jawaban yang benar: ${result.canonical_answer}`;
                feedbackArea.style.color = 'red';
                postAnswerBtn.textContent = 'Coba Lagi';
                postAnswerBtn.onclick = () => {
                    window.location.reload();
                };
            }

            if (result.explanation) {
                displayExplanation(result.explanation);
            }

        } catch (error) {
            feedbackArea.innerHTML = `<p style="color: red;">${error.message}</p>`;
            document.querySelectorAll('.option-btn').forEach(btn => btn.disabled = false);
            submitBtn.disabled = false;
        }
    }

    submitBtn.addEventListener('click', submitAnswerHandler);

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            if (!submitBtn.disabled && !submitBtn.classList.contains('hidden')) {
                submitAnswerHandler();
            } 
            else if (!postAnswerBtn.classList.contains('hidden')) {
                postAnswerBtn.click();
            }
        }
    });

    fetchAndDisplayQuestion();
}

// Fungsi ini perlu tetap di scope global untuk onclick di stage_select.html
async function unlockAllLevels() {
    if (!confirm('Apakah Anda yakin ingin membuka semua level dan stage? Aksi ini untuk testing.')) {
        return;
    }
    try {
        const response = await fetch('/api/dev/unlock-all', { method: 'POST' });
        if (!response.ok) throw new Error('Gagal menghubungi server.');
        const result = await response.json();
        alert(result.message);
        window.location.reload();
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}
