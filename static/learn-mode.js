// ==========================================================
// TRAINING MODE CONTENT LOADER
// ==========================================================

// Content data untuk semua level
const LEARNING_CONTENT = {
    limit: {
        1: {
            title: "Level 1: Substitusi Linear",
            description: "Pelajari cara menghitung limit fungsi linear dengan metode substitusi langsung.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Limit fungsi linear dapat dihitung dengan substitusi langsung. Jika f(x) adalah fungsi yang kontinu di titik x = a, maka:</p>
                <div class="formula-box">
                    $\\lim_{x \\to a} f(x) = f(a)$
                </div>
                <p>Contoh:</p>
                <div class="example-box">
                    <strong>Contoh 1:</strong> Hitung $\\lim_{x \\to 3} (2x + 5)$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Substitusi x = 3 ke dalam fungsi:</p>
                        $\\lim_{x \\to 3} (2x + 5) = 2(3) + 5 = 11$
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to 2} (5x - 3)$",
                answer: "7",
                solution: "Substitusi x = 2: $5(2) - 3 = 10 - 3 = 7$"
            }
        },
        2: {
            title: "Level 2: Substitusi Kuadrat",
            description: "Kuasi limit fungsi kuadrat dengan substitusi.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Prinsip yang sama berlaku untuk fungsi kuadrat. Substitusi langsung nilai x ke dalam fungsi.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\lim_{x \\to 4} (x^2 + 3x - 2)$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        $\\lim_{x \\to 4} (x^2 + 3x - 2) = 4^2 + 3(4) - 2 = 16 + 12 - 2 = 26$
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to -1} (2x^2 - 3x + 1)$",
                answer: "6",
                solution: "$2(-1)^2 - 3(-1) + 1 = 2 + 3 + 1 = 6$"
            }
        },
        3: {
            title: "Level 3: Substitusi Rasional",
            description: "Hitung limit fungsi rasional dengan substitusi.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Fungsi rasional juga dapat menggunakan substitusi langsung jika penyebut tidak menjadi nol.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\lim_{x \\to 3} \\frac{x+2}{x-1}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        $\\lim_{x \\to 3} \\frac{x+2}{x-1} = \\frac{3+2}{3-1} = \\frac{5}{2}$
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to 2} \\frac{3x-1}{x+1}$",
                answer: "5/3",
                solution: "$\\frac{3(2)-1}{2+1} = \\frac{5}{3}$"
            }
        },
        4: {
            title: "Level 4: Faktorisasi Linear",
            description: "Gunakan faktorisasi untuk menyelesaikan bentuk 0/0.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Jika substitusi menghasilkan bentuk tak tentu $\\frac{0}{0}$, kita perlu faktorisasi untuk menghilangkan faktor yang menyebabkan bentuk ini.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\lim_{x \\to 2} \\frac{x^2-4}{x-2}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Substitusi langsung: $\\frac{0}{0}$ (bentuk tak tentu)</p>
                        <p>Faktorisasi pembilang:</p>
                        $\\frac{x^2-4}{x-2} = \\frac{(x-2)(x+2)}{x-2} = x+2$
                        <p>Jadi:</p>
                        $\\lim_{x \\to 2} \\frac{x^2-4}{x-2} = \\lim_{x \\to 2} (x+2) = 4$
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to 3} \\frac{x^2-9}{x-3}$",
                answer: "6",
                solution: "Faktorisasi: $\\frac{(x-3)(x+3)}{x-3} = x+3$. Substitusi: $3+3 = 6$"
            }
        },
        5: {
            title: "Level 5: Faktorisasi Kuadrat",
            description: "Faktorisasi bentuk kuadrat yang lebih kompleks.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Prinsip yang sama untuk bentuk kuadrat yang dapat difaktorkan.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\lim_{x \\to -2} \\frac{x^2+5x+6}{x+2}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Faktorkan: $x^2+5x+6 = (x+2)(x+3)$</p>
                        $\\lim_{x \\to -2} \\frac{(x+2)(x+3)}{x+2} = \\lim_{x \\to -2} (x+3) = 1$
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to 1} \\frac{x^2-x-2}{x-1}$",
                answer: "3",
                solution: "$\\frac{(x-1)(x+2)}{x-1} = x+2$, substitusi: $1+2=3$"
            }
        },
        6: {
            title: "Level 6: Faktorisasi Polinomial",
            description: "Faktorisasi polinomial derajat lebih tinggi.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Metode yang sama untuk polinomial derajat tiga atau lebih.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\lim_{x \\to 1} \\frac{x^3-1}{x-1}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Gunakan identitas: $x^3-1 = (x-1)(x^2+x+1)$</p>
                        $\\lim_{x \\to 1} \\frac{(x-1)(x^2+x+1)}{x-1} = \\lim_{x \\to 1} (x^2+x+1) = 3$
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to 2} \\frac{x^3-8}{x-2}$",
                answer: "12",
                solution: "$x^3-8 = (x-2)(x^2+2x+4)$, substitusi: $4+4+4=12$"
            }
        },
        7: {
            title: "Level 7: Rasionalisasi Root",
            description: "Rasionalisasi untuk menghilangkan akar di penyebut.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Jika ada akar di penyebut, kalikan dengan sekawan untuk menghilangkan akar.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\lim_{x \\to 0} \\frac{\\sqrt{x+4}-2}{x}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Kalikan dengan sekawan:</p>
                        $\\frac{\\sqrt{x+4}-2}{x} \\cdot \\frac{\\sqrt{x+4}+2}{\\sqrt{x+4}+2} = \\frac{x}{x(\\sqrt{x+4}+2)} = \\frac{1}{\\sqrt{x+4}+2}$
                        <p>Jadi:</p>
                        $\\lim_{x \\to 0} = \\frac{1}{\\sqrt{4}+2} = \\frac{1}{4}$
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to 0} \\frac{\\sqrt{x+9}-3}{x}$",
                answer: "1/6",
                solution: "Rasionalisasi: $\\frac{1}{\\sqrt{x+9}+3}$, substitusi: $\\frac{1}{3+3} = \\frac{1}{6}$"
            }
        },
        8: {
            title: "Level 8: Rasionalisasi Ganda",
            description: "Rasionalisasi untuk bentuk yang lebih kompleks.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Untuk bentuk yang lebih kompleks, mungkin perlu lebih dari satu langkah rasionalisasi.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\lim_{x \\to 1} \\frac{\\sqrt{x}-1}{x-1}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        $\\frac{\\sqrt{x}-1}{x-1} \\cdot \\frac{\\sqrt{x}+1}{\\sqrt{x}+1} = \\frac{x-1}{(x-1)(\\sqrt{x}+1)} = \\frac{1}{\\sqrt{x}+1}$
                        <p>Substitusi: $\\frac{1}{\\sqrt{1}+1} = \\frac{1}{2}$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to 4} \\frac{\\sqrt{x}-2}{x-4}$",
                answer: "1/4",
                solution: "Rasionalisasi dan substitusi menghasilkan $\\frac{1}{\\sqrt{4}+2} = \\frac{1}{4}$"
            }
        },
        9: {
            title: "Level 9: Rasionalisasi Beda Akar",
            description: "Rasionalisasi untuk ekspresi yang mengandung beberapa akar.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Ketika ada beberapa akar dalam satu ekspresi, pastikan untuk menghilangkan semua akar.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\lim_{x \\to 0} \\frac{\\sqrt{x+1}-\\sqrt{1-x}}{x}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Kalikan dengan sekawan: $\\frac{(\\sqrt{x+1}+\\sqrt{1-x})}{(\\sqrt{x+1}+\\sqrt{1-x})}$</p>
                        <p>Setelah disederhanakan, substitusi x = 0.</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to 0} \\frac{\\sqrt{x+4}-\\sqrt{4-x}}{x}$",
                answer: "1/2",
                solution: "Rasionalisasi dan substitusi menghasilkan $\\frac{1}{\\sqrt{4}+\\sqrt{4}} = \\frac{1}{4}$"
            }
        },
        10: {
            title: "Level 10: Limit Trigonometri Dasar",
            description: "Limit fungsi trigonometri fundamental.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Limit trigonometri fundamental yang penting:</p>
                <div class="formula-box">
                    <p>$\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1$</p>
                    <p>$\\lim_{x \\to 0} \\frac{\\tan x}{x} = 1$</p>
                    <p>$\\lim_{x \\to 0} \\frac{1-\\cos x}{x} = 0$</p>
                </div>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\lim_{x \\to 0} \\frac{\\sin(3x)}{x}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        $\\lim_{x \\to 0} \\frac{\\sin(3x)}{x} = 3 \\cdot \\lim_{x \\to 0} \\frac{\\sin(3x)}{3x} = 3(1) = 3$
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to 0} \\frac{\\sin(5x)}{x}$",
                answer: "5",
                solution: "$5 \\cdot \\lim_{x \\to 0} \\frac{\\sin(5x)}{5x} = 5$"
            }
        },
        11: {
            title: "Level 11: Limit Trigonometri Lanjutan",
            description: "Bentuk limit trigonometri yang lebih kompleks.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Gunakan identitas trigonometri untuk menyederhanakan.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\lim_{x \\to 0} \\frac{1-\\cos(x)}{x^2}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Gunakan identitas: $1-\\cos x = 2\\sin^2(\\frac{x}{2})$</p>
                        $\\lim_{x \\to 0} \\frac{2\\sin^2(\\frac{x}{2})}{x^2} = \\lim_{x \\to 0} \\frac{1}{2} \\left(\\frac{\\sin(\\frac{x}{2})}{\\frac{x}{2}}\\right)^2 = \\frac{1}{2}$
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to 0} \\frac{\\tan(2x)}{x}$",
                answer: "2",
                solution: "Gunakan limit fundamental: $\\lim_{x \\to 0} \\frac{\\tan(2x)}{x} = 2$"
            }
        },
        12: {
            title: "Level 12: Limit Trigonometri dengan Identitas",
            description: "Gunakan identitas trigonometri untuk menyelesaikan limit.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Identitas trigonometri yang sering digunakan:</p>
                <div class="formula-box">
                    <p>$\\sin^2 x + \\cos^2 x = 1$</p>
                    <p>$\\tan x = \\frac{\\sin x}{\\cos x}$</p>
                    <p>$1 + \\tan^2 x = \\sec^2 x$</p>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to 0} \\frac{\\sin(x)\\cos(x)}{x}$",
                answer: "1",
                solution: "Gunakan identitas dan limit fundamental trigonometri"
            }
        },
        13: {
            title: "Level 13: Limit Tak Hingga Fungsi Rasional",
            description: "Hitung limit ketika x menuju tak hingga untuk fungsi rasional.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Untuk $\\lim_{x \\to \\infty} \\frac{P(x)}{Q(x)}$ dengan P dan Q polinomial:</p>
                <ul>
                    <li>Jika derajat P = derajat Q, limit = rasio koefisien tertinggi</li>
                    <li>Jika derajat P < derajat Q, limit = 0</li>
                    <li>Jika derajat P > derajat Q, limit = ∞ atau -∞ tergantung tanda</li>
                </ul>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\lim_{x \\to \\infty} \\frac{3x^2+2x-1}{5x^2-3x+2}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Derajat P = Derajat Q, ambil rasio koefisien tertinggi:</p>
                        $\\lim_{x \\to \\infty} \\frac{3x^2+2x-1}{5x^2-3x+2} = \\frac{3}{5}$
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to \\infty} \\frac{2x^3-1}{x^2+5}$",
                answer: "∞",
                solution: "Derajat P > derajat Q, limit = ∞"
            }
        },
        14: {
            title: "Level 14: Limit Tak Hingga dengan Akar",
            description: "Limit tak hingga untuk fungsi yang mengandung akar.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Untuk limit tak hingga dengan akar, kalikan dengan konjugat atau faktorkan pangkat tertinggi.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\lim_{x \\to \\infty} (\\sqrt{x+1} - \\sqrt{x})$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Kalikan dengan konjugat: $\\frac{(\\sqrt{x+1} - \\sqrt{x})(\\sqrt{x+1} + \\sqrt{x})}{\\sqrt{x+1} + \\sqrt{x}}$</p>
                        <p>Sederhanakan: $\\frac{1}{\\sqrt{x+1} + \\sqrt{x}}$</p>
                        <p>Limit: $\\lim_{x \\to \\infty} \\frac{1}{\\sqrt{x+1} + \\sqrt{x}} = 0$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to \\infty} (\\sqrt{x^2+1} - x)$",
                answer: "0",
                solution: "Kalikan dengan konjugat dan sederhanakan"
            }
        },
        15: {
            title: "Level 15: Limit Tak Hingga Lanjutan",
            description: "Kombinasi berbagai teknik untuk limit tak hingga.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Gunakan kombinasi faktorisasi, rasionalisasi, dan pemfaktoran pangkat tertinggi.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\lim_{x \\to \\infty} \\frac{\\sqrt{x^2+3x}-x}{x}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Faktorkan x dari akar dan sederhanakan.</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\lim_{x \\to \\infty} \\frac{x^3}{x^4+1}$",
                answer: "0",
                solution: "Derajat P < derajat Q, limit = 0"
            }
        }
    },
    turunan: {
        1: {
            title: "Level 1: Power Rule Dasar",
            description: "Pelajari aturan pangkat untuk turunan.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Power Rule adalah aturan dasar untuk turunan:</p>
                <div class="formula-box">
                    $\\frac{d}{dx}[x^n] = nx^{n-1}$
                </div>
                <div class="example-box">
                    <strong>Contoh:</strong> Turunkan $f(x) = x^5$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        $f'(x) = 5x^{5-1} = 5x^4$
                    </div>
                </div>
            `,
            practice: {
                question: "Turunkan $f(x) = x^8$",
                answer: "8x^7",
                solution: "$f'(x) = 8x^{8-1} = 8x^7$"
            }
        }
    },
    integral: {
        1: {
            title: "Level 1: Power Rule untuk Integral",
            description: "Pelajari aturan pangkat untuk integral.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Power Rule untuk integral:</p>
                <div class="formula-box">
                    $\\int x^n \\, dx = \\frac{x^{n+1}}{n+1} + C$ (untuk n ≠ -1)
                </div>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int x^4 \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        $\\int x^4 \\, dx = \\frac{x^{4+1}}{4+1} + C = \\frac{x^5}{5} + C$
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int x^3 \\, dx$",
                answer: "x^4/4 + C",
                solution: "$\\int x^3 \\, dx = \\frac{x^4}{4} + C$"
            }
        }
    }
};

// ==========================================
// RENDER LEARNING CONTENT
// ==========================================
function renderLearningContent(content) {
    let html = `
        <h1>${content.title}</h1>
        <p class="intro">${content.description}</p>
        
        <div class="content-section">
            ${content.theory || ''}
        </div>
    `;
    
    if (content.practice) {
        html += `
            <div class="practice-section">
                <h2>🎯 Latihan</h2>
                <div class="practice-box">
                    <p class="practice-question"><strong>Soal:</strong> ${content.practice.question}</p>
                    <button class="show-solution-btn" onclick="toggleSolution(this)">Tampilkan Jawaban</button>
                    <div class="solution-box" style="display:none;">
                        <p><strong>Jawaban:</strong> ${content.practice.answer}</p>
                        <p>${content.practice.solution}</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    return html;
}

function toggleSolution(btn) {
    const solutionBox = btn.nextElementSibling;
    const isShown = solutionBox.style.display !== 'none';
    
    solutionBox.style.display = isShown ? 'none' : 'block';
    btn.textContent = isShown ? 'Tampilkan Jawaban' : 'Sembunyikan Jawaban';
    
    if (!isShown) {
        MathJax.typesetPromise([solutionBox]);
    }
}

// ==========================================
// LOAD CONTENT BY TOPIC AND LEVEL
// ==========================================
function loadLearningContent(topic, level) {
    const content = LEARNING_CONTENT[topic]?.[level];
    
    if (!content) {
        document.getElementById('learnContent').innerHTML = `
            <h1>Konten Belum Tersedia</h1>
            <p class="intro">Materi untuk ${topic} level ${level} sedang dalam pengembangan.</p>
            <a href="/learn" class="back-btn">← Kembali ke Menu Training</a>
        `;
        MathJax.typesetPromise([document.getElementById('learnContent')]);
        return;
    }
    
    let html = renderLearningContent(content);
    
    // Add navigation
    const levelNum = parseInt(level);
    html += `
        <div class="content-navigation">
            ${levelNum > 1 ? `<a href="/learn?topic=${topic}&level=${levelNum-1}" class="nav-btn prev-btn">← Sebelumnya</a>` : ''}
            <a href="/learn" class="nav-btn menu-btn">Menu Training</a>
            ${levelNum < 15 ? `<a href="/learn?topic=${topic}&level=${levelNum+1}" class="nav-btn next-btn">Selanjutnya →</a>` : ''}
        </div>
    `;
    
    document.getElementById('learnContent').innerHTML = html;
    
    // Re-render MathJax for the new content
    MathJax.typesetPromise([document.getElementById('learnContent')]).then(() => {
        console.log('✅ Math content rendered');
    });
}

// ==========================================
// INITIALIZE ON PAGE LOAD
// ==========================================
window.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const topic = urlParams.get('topic');
    const level = urlParams.get('level');
    
    if (topic && level) {
        loadLearningContent(topic, level);
        
        // Highlight active nav item
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            if (item.href.includes(`topic=${topic}&level=${level}`)) {
                item.style.background = 'rgba(168, 85, 247, 0.3)';
                item.style.borderLeftColor = 'var(--color-accent)';
                item.style.color = 'var(--color-player)';
            }
        });
    }
    
    // Initialize MathJax if not already loaded
    if (typeof MathJax !== 'undefined') {
        MathJax.typesetPromise([document.body]).catch(err => {
            console.error('MathJax error:', err);
        });
    }
});