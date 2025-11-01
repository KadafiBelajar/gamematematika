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
                <p>Aturan ini berlaku untuk semua bilangan real n, termasuk pecahan dan negatif.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Turunkan $f(x) = 3x^5$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        $f'(x) = 3 \\cdot 5x^{5-1} = 15x^4$
                    </div>
                </div>
            `,
            practice: {
                question: "Turunkan $f(x) = 4x^8$",
                answer: "32x^7",
                solution: "$f'(x) = 4 \\cdot 8x^{8-1} = 32x^7$"
            }
        },
        2: {
            title: "Level 2: Turunan Polinomial",
            description: "Turunkan fungsi polinomial dengan beberapa suku.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Turunan dari penjumlahan sama dengan penjumlahan turunan:</p>
                <div class="formula-box">
                    $\\frac{d}{dx}[f(x) + g(x)] = f'(x) + g'(x)$
                </div>
                <div class="example-box">
                    <strong>Contoh:</strong> Turunkan $f(x) = 2x^3 + 5x^2 - 3x + 1$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        $f'(x) = 2 \\cdot 3x^{3-1} + 5 \\cdot 2x^{2-1} - 3 \\cdot 1 = 6x^2 + 10x - 3$
                    </div>
                </div>
            `,
            practice: {
                question: "Turunkan $f(x) = x^4 - 3x^3 + 2x^2 - x$",
                answer: "4x^3 - 9x^2 + 4x - 1",
                solution: "$f'(x) = 4x^3 - 9x^2 + 4x - 1$"
            }
        },
        3: {
            title: "Level 3: Pangkat Negatif & Akar",
            description: "Turunkan fungsi dengan pangkat negatif dan bentuk akar.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Untuk pangkat negatif: $\\frac{d}{dx}[x^{-n}] = -nx^{-n-1}$</p>
                <p>Untuk akar: $\\frac{d}{dx}[\\sqrt{x}] = \\frac{1}{2\\sqrt{x}}$</p>
                <div class="formula-box">
                    $\\frac{d}{dx}[\\sqrt{x}] = \\frac{1}{2}x^{-\\frac{1}{2}}$
                </div>
                <div class="example-box">
                    <strong>Contoh 1:</strong> Turunkan $f(x) = \\frac{1}{x^2}$
                    <div class="solution">
                        <p>$f(x) = x^{-2}$</p>
                        <p>$f'(x) = -2x^{-3} = -\\frac{2}{x^3}$</p>
                    </div>
                </div>
                <div class="example-box">
                    <strong>Contoh 2:</strong> Turunkan $f(x) = 3\\sqrt{x}$
                    <div class="solution">
                        <p>$f'(x) = 3 \\cdot \\frac{1}{2}x^{-\\frac{1}{2}} = \\frac{3}{2\\sqrt{x}}$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Turunkan $f(x) = \\frac{5}{x^3}$",
                answer: "-15/x^4",
                solution: "$f(x) = 5x^{-3}$, maka $f'(x) = -15x^{-4} = -\\frac{15}{x^4}$"
            }
        },
        4: {
            title: "Level 4: Product Rule - Fungsi Linear",
            description: "Turunkan perkalian dua fungsi linear.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Product Rule untuk $f(x) = u(x) \\cdot v(x)$:</p>
                <div class="formula-box">
                    $f'(x) = u'(x) \\cdot v(x) + u(x) \\cdot v'(x)$
                </div>
                <div class="example-box">
                    <strong>Contoh:</strong> Turunkan $f(x) = (2x + 3)(x - 1)$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Misalkan $u(x) = 2x + 3$ dan $v(x) = x - 1$</p>
                        <p>$u'(x) = 2$, $v'(x) = 1$</p>
                        <p>$f'(x) = 2(x - 1) + (2x + 3)(1) = 2x - 2 + 2x + 3 = 4x + 1$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Turunkan $f(x) = (3x - 2)(x + 5)$",
                answer: "6x + 13",
                solution: "$f'(x) = 3(x + 5) + (3x - 2)(1) = 3x + 15 + 3x - 2 = 6x + 13$"
            }
        },
        5: {
            title: "Level 5: Product Rule - Fungsi Kuadrat",
            description: "Turunkan perkalian fungsi yang lebih kompleks.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Prinsip Product Rule sama untuk semua fungsi. Awas! Perhatikan dengan teliti.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Turunkan $f(x) = (x^2 + 1)(3x - 2)$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$u(x) = x^2 + 1$, $v(x) = 3x - 2$</p>
                        <p>$u'(x) = 2x$, $v'(x) = 3$</p>
                        <p>$f'(x) = 2x(3x - 2) + (x^2 + 1)(3) = 6x^2 - 4x + 3x^2 + 3 = 9x^2 - 4x + 3$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Turunkan $f(x) = (2x^2 - 1)(x + 3)$",
                answer: "6x^2 + 12x - 1",
                solution: "$f'(x) = 4x(x + 3) + (2x^2 - 1)(1) = 4x^2 + 12x + 2x^2 - 1 = 6x^2 + 12x - 1$"
            }
        },
        6: {
            title: "Level 6: Quotient Rule - Fungsi Linear",
            description: "Turunkan pembagian dua fungsi.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Quotient Rule untuk $f(x) = \\frac{u(x)}{v(x)}$:</p>
                <div class="formula-box">
                    $f'(x) = \\frac{u'(x) \\cdot v(x) - u(x) \\cdot v'(x)}{[v(x)]^2}$
                </div>
                <div class="example-box">
                    <strong>Contoh:</strong> Turunkan $f(x) = \\frac{x + 2}{x - 1}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$u(x) = x + 2$, $v(x) = x - 1$</p>
                        <p>$u'(x) = 1$, $v'(x) = 1$</p>
                        <p>$f'(x) = \\frac{1(x - 1) - (x + 2)(1)}{(x - 1)^2} = \\frac{x - 1 - x - 2}{(x - 1)^2} = \\frac{-3}{(x - 1)^2}$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Turunkan $f(x) = \\frac{2x - 1}{x + 3}$",
                answer: "7/(x+3)^2",
                solution: "$f'(x) = \\frac{2(x + 3) - (2x - 1)(1)}{(x + 3)^2} = \\frac{7}{(x + 3)^2}$"
            }
        },
        7: {
            title: "Level 7: Quotient Rule - Fungsi Kuadrat",
            description: "Quotient Rule untuk pembilang atau penyebut kuadrat.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Prinsip yang sama, tapi lebih kompleks untuk dihitung.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Turunkan $f(x) = \\frac{x^2 + 1}{x - 2}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$u'(x) = 2x$, $v'(x) = 1$</p>
                        <p>$f'(x) = \\frac{2x(x - 2) - (x^2 + 1)(1)}{(x - 2)^2} = \\frac{2x^2 - 4x - x^2 - 1}{(x - 2)^2} = \\frac{x^2 - 4x - 1}{(x - 2)^2}$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Turunkan $f(x) = \\frac{x^2 - 4}{x + 1}$",
                answer: "(x^2 + 2x + 4)/(x+1)^2",
                solution: "$f'(x) = \\frac{2x(x + 1) - (x^2 - 4)(1)}{(x + 1)^2}$"
            }
        },
        8: {
            title: "Level 8: Chain Rule - Power",
            description: "Turunkan fungsi komposisi berbentuk $(ax^2 + b)^n$.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Chain Rule untuk $f(x) = [g(x)]^n$:</p>
                <div class="formula-box">
                    $f'(x) = n[g(x)]^{n-1} \\cdot g'(x)$
                </div>
                <div class="example-box">
                    <strong>Contoh:</strong> Turunkan $f(x) = (x^2 + 3)^4$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$f'(x) = 4(x^2 + 3)^{4-1} \\cdot (2x) = 4(x^2 + 3)^3 \\cdot 2x = 8x(x^2 + 3)^3$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Turunkan $f(x) = (2x^2 - 5)^3$",
                answer: "12x(2x^2 - 5)^2",
                solution: "$f'(x) = 3(2x^2 - 5)^2 \\cdot 4x = 12x(2x^2 - 5)^2$"
            }
        },
        9: {
            title: "Level 9: Turunan Trigonometri Dasar",
            description: "Turunkan fungsi trigonometri dasar.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Turunan fungsi trigonometri:</p>
                <div class="formula-box">
                    <p>$\\frac{d}{dx}[\\sin x] = \\cos x$</p>
                    <p>$\\frac{d}{dx}[\\cos x] = -\\sin x$</p>
                    <p>$\\frac{d}{dx}[\\tan x] = \\sec^2 x$</p>
                </div>
                <div class="example-box">
                    <strong>Contoh:</strong> Turunkan $f(x) = 5\\sin(3x)$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Gunakan Chain Rule: $f'(x) = 5 \\cos(3x) \\cdot 3 = 15\\cos(3x)$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Turunkan $f(x) = 4\\cos(2x)$",
                answer: "-8sin(2x)",
                solution: "$f'(x) = 4 \\cdot (-\\sin(2x)) \\cdot 2 = -8\\sin(2x)$"
            }
        },
        10: {
            title: "Level 10: Chain Rule dengan Trigonometri",
            description: "Turunkan fungsi trigonometri komposisi.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Kombinasikan Chain Rule dengan turunan trigonometri.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Turunkan $f(x) = \\sin(x^2 + 5)$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$f'(x) = \\cos(x^2 + 5) \\cdot (2x) = 2x\\cos(x^2 + 5)$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Turunkan $f(x) = \\cos(3x^2 - 2)$",
                answer: "-6xsin(3x^2 - 2)",
                solution: "$f'(x) = -\\sin(3x^2 - 2) \\cdot 6x = -6x\\sin(3x^2 - 2)$"
            }
        },
        11: {
            title: "Level 11: Kombinasi Product & Trigonometri",
            description: "Turunkan perkalian fungsi trigonometri dan polinomial.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Gunakan Product Rule dengan fungsi trigonometri.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Turunkan $f(x) = x^3 \\sin(x)$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$u(x) = x^3$, $v(x) = \\sin(x)$</p>
                        <p>$u'(x) = 3x^2$, $v'(x) = \\cos(x)$</p>
                        <p>$f'(x) = 3x^2\\sin(x) + x^3\\cos(x) = x^2(3\\sin(x) + x\\cos(x))$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Turunkan $f(x) = x^2\\cos(2x)$",
                answer: "2xcos(2x) - 2x^2sin(2x)",
                solution: "$f'(x) = 2x\\cos(2x) + x^2(-\\sin(2x))(2)$"
            }
        },
        12: {
            title: "Level 12: Kombinasi Quotient & Trigonometri",
            description: "Turunkan pembagian fungsi trigonometri.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Gunakan Quotient Rule dengan fungsi trigonometri.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Turunkan $f(x) = \\frac{\\sin(2x)}{x}$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$u'(x) = 2\\cos(2x)$, $v'(x) = 1$</p>
                        <p>$f'(x) = \\frac{2\\cos(2x) \\cdot x - \\sin(2x) \\cdot 1}{x^2} = \\frac{2x\\cos(2x) - \\sin(2x)}{x^2}$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Turunkan $f(x) = \\frac{\\cos(x)}{x^2}$",
                answer: "-(xsin(x) + 2cos(x))/x^3",
                solution: "Gunakan Quotient Rule dengan $u(x) = \\cos(x)$ dan $v(x) = x^2$"
            }
        },
        13: {
            title: "Level 13: Turunan Kedua",
            description: "Hitung turunan kedua dari fungsi.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Turunan kedua adalah turunan dari turunan pertama. Notasi: $f''(x)$ atau $\\frac{d^2y}{dx^2}$</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Tentukan $f''(x)$ untuk $f(x) = x^3 + 2x^2$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$f'(x) = 3x^2 + 4x$</p>
                        <p>$f''(x) = 6x + 4$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Tentukan $f''(x)$ untuk $f(x) = 2x^3 - 5x^2 + x$",
                answer: "12x - 10",
                solution: "$f'(x) = 6x^2 - 10x + 1$, maka $f''(x) = 12x - 10$"
            }
        },
        14: {
            title: "Level 14: Gradien Garis Singgung",
            description: "Tentukan gradien garis singgung kurva di titik tertentu.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Gradien garis singgung di $x = a$ adalah nilai turunan di titik tersebut: $f'(a)$</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Tentukan gradien garis singgung kurva $f(x) = x^3 + 2x$ di $x = 2$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$f'(x) = 3x^2 + 2$</p>
                        <p>Gradien di $x = 2$: $f'(2) = 3(4) + 2 = 14$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Tentukan gradien garis singgung $f(x) = 2x^3$ di $x = 1$",
                answer: "6",
                solution: "$f'(x) = 6x^2$, maka $f'(1) = 6$"
            }
        },
        15: {
            title: "Level 15: Titik Stasioner",
            description: "Tentukan koordinat titik stasioner dari fungsi.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Titik stasioner adalah titik dimana $f'(x) = 0$. Koordinatnya: $(x, f(x))$</p>
                <p><strong>Langkah:</strong></p>
                <ol>
                    <li>Cari $f'(x)$</li>
                    <li>Atur $f'(x) = 0$ dan selesaikan untuk x</li>
                    <li>Substitusi x ke $f(x)$ untuk mendapatkan y</li>
                </ol>
                <div class="example-box">
                    <strong>Contoh:</strong> Tentukan titik stasioner dari $f(x) = x^3 + 3x^2 - 9x + 2$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$f'(x) = 3x^2 + 6x - 9$</p>
                        <p>$3x^2 + 6x - 9 = 0$</p>
                        <p>$x^2 + 2x - 3 = 0$</p>
                        <p>$(x + 3)(x - 1) = 0$</p>
                        <p>$x = -3$ atau $x = 1$</p>
                        <p>Titik stasioner: $(-3, 29)$ dan $(1, -3)$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Tentukan titik stasioner dari $f(x) = x^3 - 12x$",
                answer: "(2, -16) dan (-2, 16)",
                solution: "$f'(x) = 3x^2 - 12 = 0$, maka $x^2 = 4$, sehingga $x = 2$ atau $x = -2$"
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
                <p>Aturan ini adalah kebalikan dari turunan. Perhatikan bahwa pangkat bertambah 1.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int 3 \\cdot 5 \\cdot x^4 \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$\\int 15x^4 \\, dx = 15 \\cdot \\frac{x^{5}}{5} + C = 3x^5 + C$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int 8x^3 \\, dx$",
                answer: "2x^4 + C",
                solution: "$\\int 8x^3 \\, dx = 8 \\cdot \\frac{x^4}{4} + C = 2x^4 + C$"
            }
        },
        2: {
            title: "Level 2: Integral Penjumlahan Polinomial",
            description: "Integral dari penjumlahan atau pengurangan beberapa suku.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Integral dari penjumlahan sama dengan penjumlahan integral:</p>
                <div class="formula-box">
                    $\\int [f(x) + g(x)] \\, dx = \\int f(x) \\, dx + \\int g(x) \\, dx$
                </div>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int (3x^5 - 4x^3 + 2x^2 + 10) \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$\\int (3x^5 - 4x^3 + 2x^2 + 10) \\, dx = \\frac{3x^6}{6} - \\frac{4x^4}{4} + \\frac{2x^3}{3} + 10x + C$</p>
                        <p>$= \\frac{x^6}{2} - x^4 + \\frac{2x^3}{3} + 10x + C$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int (2x^4 - 5x^2 + x - 3) \\, dx$",
                answer: "2x^5/5 - 5x^3/3 + x^2/2 - 3x + C",
                solution: "Integralkan setiap suku secara terpisah"
            }
        },
        3: {
            title: "Level 3: Bentuk Akar & Pecahan",
            description: "Integral fungsi berbentuk akar dan pecahan.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Ubah bentuk akar menjadi pangkat pecahan:</p>
                <p>$\\sqrt[n]{x^m} = x^{\\frac{m}{n}}$</p>
                <p>Ubah pecahan menjadi pangkat negatif: $\\frac{a}{x^n} = ax^{-n}$</p>
                <div class="example-box">
                    <strong>Contoh 1:</strong> Hitung $\\int 5\\sqrt{x^3} + \\frac{2}{x^4} \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$= \\int 5x^{3/2} + 2x^{-4} \\, dx$</p>
                        <p>$= 5 \\cdot \\frac{x^{5/2}}{5/2} + 2 \\cdot \\frac{x^{-3}}{-3} + C$</p>
                        <p>$= 2x^{5/2} - \\frac{2}{3x^3} + C$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int 3\\sqrt[3]{x^2} - \\frac{4}{x^5} \\, dx$",
                answer: "9x^(5/3)/5 + 1/x^4 + C",
                solution: "$= \\int 3x^{2/3} - 4x^{-5} \\, dx$"
            }
        },
        4: {
            title: "Level 4: Distribusi & Sederhanakan",
            description: "Jabarkan dulu perkalian atau pembagian sebelum mengintegralkan.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Bentuk perkalian harus diurai dulu dengan aljabar sebelum mengintegralkan.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int (2x^3 + 1)(x - 2) \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Jabarkan: $(2x^3 + 1)(x - 2) = 2x^4 - 4x^3 + x - 2$</p>
                        <p>$\\int 2x^4 - 4x^3 + x - 2 \\, dx = \\frac{2x^5}{5} - x^4 + \\frac{x^2}{2} - 2x + C$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int x^2(x^3 + 2x + 5) \\, dx$",
                answer: "x^6/6 + 2x^4/4 + 5x^3/3 + C",
                solution: "Jabarkan $x^2(x^3 + 2x + 5)$ dulu menjadi $x^5 + 2x^3 + 5x^2$"
            }
        },
        5: {
            title: "Level 5: Integral Trigonometri Dasar",
            description: "Integral fungsi trigonometri dasar.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Rumus dasar integral trigonometri:</p>
                <div class="formula-box">
                    <p>$\\int \\sin(x) \\, dx = -\\cos(x) + C$</p>
                    <p>$\\int \\cos(x) \\, dx = \\sin(x) + C$</p>
                    <p>$\\int \\sec^2(x) \\, dx = \\tan(x) + C$</p>
                </div>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int (3\\sin(x) + 5\\cos(x) + 2\\sec^2(x)) \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$= -3\\cos(x) + 5\\sin(x) + 2\\tan(x) + C$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int (4\\sin(x) - 3\\cos(x)) \\, dx$",
                answer: "-4cos(x) - 3sin(x) + C",
                solution: "Integralkan setiap suku trigonometri secara terpisah"
            }
        },
        6: {
            title: "Level 6: Integral Tentu Polinomial",
            description: "Hitung integral dengan batas tertentu (definite integral).",
            theory: `
                <h2>📖 Teori</h2>
                <p>Integral tentu $\\int_a^b f(x) \\, dx$ dihitung dengan Teorema Dasar Kalkulus:</p>
                <div class="formula-box">
                    $\\int_a^b f(x) \\, dx = F(b) - F(a)$
                </div>
                <p>dimana $F(x)$ adalah anti-turunan dari $f(x)$.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int_0^2 3x^2 \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$F(x) = x^3$</p>
                        <p>$= F(2) - F(0) = 2^3 - 0^3 = 8$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int_{-1}^1 2x^3 \\, dx$",
                answer: "0",
                solution: "Ini fungsi ganjil dengan batas simetris, hasilnya 0"
            }
        },
        7: {
            title: "Level 7: Substitusi Paling Dasar",
            description: "Metode substitusi untuk integral bentuk $(ax+b)^n$.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Substitusi dilakukan jika muncul fungsi komposisi. Misalkan $u = g(x)$.</p>
                <div class="formula-box">
                    $\\int f(g(x)) \\cdot g'(x) \\, dx = \\int f(u) \\, du$
                </div>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int (2x + 3)^5 \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Misal $u = 2x + 3$, maka $du = 2dx$, sehingga $dx = \\frac{du}{2}$</p>
                        <p>$\\int u^5 \\cdot \\frac{du}{2} = \\frac{1}{2} \\cdot \\frac{u^6}{6} + C = \\frac{u^6}{12} + C$</p>
                        <p>$= \\frac{(2x+3)^6}{12} + C$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int (3x - 2)^4 \\, dx$",
                answer: "(3x-2)^5/15 + C",
                solution: "Misal $u = 3x - 2$, maka $du = 3dx$"
            }
        },
        8: {
            title: "Level 8: Substitusi Lanjutan",
            description: "Substitusi untuk bentuk $x^{n-1}(ax^n + b)^m$.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Ketika turunan dari fungsi dalam kurung kelipatan dari $x^{n-1}$ di luar.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int 6x^2(2x^3 + 5)^3 \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Misal $u = 2x^3 + 5$, maka $du = 6x^2 dx$</p>
                        <p>$\\int u^3 \\, du = \\frac{u^4}{4} + C = \\frac{(2x^3 + 5)^4}{4} + C$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int 2x\\sqrt{x^2 + 3} \\, dx$",
                answer: "2(x^2+3)^(3/2)/3 + C",
                solution: "Misal $u = x^2 + 3$, maka $du = 2x dx$"
            }
        },
        9: {
            title: "Level 9: Integral Parsial (LIATE)",
            description: "Metode integral parsial untuk perkalian fungsi.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Rumus integral parsial:</p>
                <div class="formula-box">
                    $\\int u \\, dv = uv - \\int v \\, du$
                </div>
                <p><strong>LIATE</strong> membantu memilih $u$: <strong>L</strong>ogaritma, <strong>I</strong>nvers trig, <strong>A</strong>ljabar, <strong>T</strong>rigonometri, <strong>E</strong>xponensial</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int x\\sin(x) \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$u = x \\Rightarrow du = dx$</p>
                        <p>$dv = \\sin(x) dx \\Rightarrow v = -\\cos(x)$</p>
                        <p>$= -x\\cos(x) + \\int \\cos(x) dx = -x\\cos(x) + \\sin(x) + C$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int xe^x \\, dx$",
                answer: "xe^x - e^x + C",
                solution: "Pilih $u = x$ dan $dv = e^x dx$"
            }
        },
        10: {
            title: "Level 10: Integral Trigonometri Identitas",
            description: "Gunakan identitas trigonometri untuk menyederhanakan integral.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Identitas penting:</p>
                <div class="formula-box">
                    <p>$\\sin^2(x) = \\frac{1-\\cos(2x)}{2}$</p>
                    <p>$\\cos^2(x) = \\frac{1+\\cos(2x)}{2}$</p>
                </div>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int \\sin^2(3x) \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$= \\int \\frac{1-\\cos(6x)}{2} dx = \\frac{1}{2} \\int (1 - \\cos(6x)) dx$</p>
                        <p>$= \\frac{1}{2}(x - \\frac{\\sin(6x)}{6}) + C$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int \\cos^2(2x) \\, dx$",
                answer: "x/2 + sin(4x)/8 + C",
                solution: "Gunakan identitas $\\cos^2(2x) = \\frac{1+\\cos(4x)}{2}$"
            }
        },
        11: {
            title: "Level 11: Substitusi Trigonometri",
            description: "Integral bentuk $\\frac{1}{\\sqrt{a^2-x^2}}$ atau $\\frac{1}{a^2+x^2}$.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Substitusi trigonometri menggunakan:</p>
                <div class="formula-box">
                    <p>$\\frac{1}{\\sqrt{a^2-x^2}}$ gunakan $x = a\\sin(\\theta)$</p>
                    <p>$\\frac{1}{a^2+x^2}$ gunakan $x = a\\tan(\\theta)$</p>
                </div>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int \\frac{1}{25+x^2} \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$= \\int \\frac{1}{25+x^2} dx = \\frac{1}{5}\\arctan(\\frac{x}{5}) + C$</p>
                        <p>(rumus umum: $\\int \\frac{1}{a^2+x^2} dx = \\frac{1}{a}\\arctan(\\frac{x}{a}) + C$)</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int \\frac{4}{9+x^2} \\, dx$",
                answer: "4arctan(x/3)/3 + C",
                solution: "$a = 3$, gunakan rumus $\\frac{1}{a}\\arctan(\\frac{x}{a})$"
            }
        },
        12: {
            title: "Level 12: Pecahan Parsial",
            description: "Integral fungsi rasional yang bisa dipecah menjadi pecahan parsial.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Jika penyebut bisa difaktorkan, uraikan menjadi pecahan parsial.</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int \\frac{5}{(x-1)(x+2)} \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Urai: $\\frac{5}{(x-1)(x+2)} = \\frac{A}{x-1} + \\frac{B}{x+2}$</p>
                        <p>Setelah penyamaan koefisien, diperoleh $A = \\frac{5}{3}$, $B = -\\frac{5}{3}$</p>
                        <p>$= \\frac{5}{3}\\ln|x-1| - \\frac{5}{3}\\ln|x+2| + C$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int \\frac{7}{(x+1)(x-3)} \\, dx$",
                answer: "7(ln|x+1| - ln|x-3|)/4 + C",
                solution: "Decompose menjadi pecahan parsial terlebih dahulu"
            }
        },
        13: {
            title: "Level 13: Jebakan Substitusi vs Parsial",
            description: "Kenali kapan pakai substitusi dan kapan parsial.",
            theory: `
                <h2>📖 Teori</h2>
                <p><strong>Substitusi:</strong> Jika ada $x \\cdot f(x^2)$, misal $x\\sin(x^2)$</p>
                <p><strong>Parsial:</strong> Jika ada $x \\cdot f(x)$, misal $x\\sin(x)$</p>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int 2x\\sin(x^2) \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Misal $u = x^2$, maka $du = 2x dx$</p>
                        <p>$= \\int \\sin(u) du = -\\cos(u) + C = -\\cos(x^2) + C$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int xe^{x^2} \\, dx$",
                answer: "e^(x^2)/2 + C",
                solution: "Gunakan substitusi $u = x^2$, bukan parsial"
            }
        },
        14: {
            title: "Level 14: Integral Tentu dengan Trik",
            description: "Gunakan sifat fungsi ganjil/genap dan nilai khusus pada batas.",
            theory: `
                <h2>📖 Teori</h2>
                <p><strong>Fungsi ganjil:</strong> $f(-x) = -f(x)$</p>
                <p>$\\int_{-a}^a f(x) dx = 0$ untuk fungsi ganjil</p>
                <p><strong>Nilai khusus:</strong> $\\int_1^e \\frac{1}{x} dx = 1$</p>
                <div class="example-box">
                    <strong>Contoh 1:</strong> Hitung $\\int_{-3}^3 x^5 \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>Fungsi ganjil dengan batas simetris: hasil = 0</p>
                    </div>
                </div>
                <div class="example-box">
                    <strong>Contoh 2:</strong> Hitung $\\int_0^{\\pi/2} \\cos(x) \\, dx$
                    <div class="solution">
                        <p><strong>Solusi:</strong></p>
                        <p>$= \\sin(\\pi/2) - \\sin(0) = 1 - 0 = 1$</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int_{-2}^2 x^3 \\, dx$",
                answer: "0",
                solution: "Fungsi ganjil dengan batas simetris"
            }
        },
        15: {
            title: "Level 15: Integral 'Mustahil' yang Mudah",
            description: "Soal yang terlihat rumit tapi memiliki trik sederhana.",
            theory: `
                <h2>📖 Teori</h2>
                <p>Perhatikan kemungkinan untuk:</p>
                <ul>
                    <li>Bagi polinomial dulu</li>
                    <li>Jabarkan bentuk kuadrat</li>
                    <li>Identitas trigonometri</li>
                    <li>Substitusi yang tersembunyi</li>
                </ul>
                <div class="example-box">
                    <strong>Contoh:</strong> Hitung $\\int \\sin(x)\\cos(x) \\, dx$
                    <div class="solution">
                        <p><strong>Solusi 1:</strong> Misal $u = \\sin(x)$, maka $du = \\cos(x) dx$</p>
                        <p>$= \\int u du = \\frac{u^2}{2} + C = \\frac{\\sin^2(x)}{2} + C$</p>
                        <p><strong>Solusi 2:</strong> Gunakan identitas $\\sin(x)\\cos(x) = \\frac{\\sin(2x)}{2}$</p>
                        <p>$= \\int \\frac{\\sin(2x)}{2} dx = -\\frac{\\cos(2x)}{4} + C$</p>
                        <p>(Kedua jawaban setara setelah disederhanakan)</p>
                    </div>
                </div>
            `,
            practice: {
                question: "Hitung $\\int (e^x + 1)^2 \\, dx$",
                answer: "e^(2x)/2 + 2e^x + x + C",
                solution: "Jabarkan menjadi $(e^x)^2 + 2e^x + 1 = e^{2x} + 2e^x + 1$"
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