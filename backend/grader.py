from sympy import (
    sympify, limit, Symbol, sqrt, factor, cancel, expand, latex, oo,
    sin, cos, tan, Poly, degree, numer, denom, Add, Mul, Pow, S
)

def check_answer(user_answer, correct_answer):
    """Memeriksa apakah jawaban pengguna sama dengan jawaban yang benar."""
    return user_answer.strip() == str(correct_answer).strip()

# ==============================================================================
# FUNGSI-FUNGSI PEMBANTU
# ==============================================================================

def _solve_substitusi_rasional(f, x, point, num, den):
    """
    Fungsi KHUSUS untuk menghasilkan langkah pengerjaan
    substitusi langsung pada FUNGSI RASIONAL (PECAHAN).
    VERSI FINAL DENGAN ALGORITMA YANG LOGIS DAN STABIL.
    """
    
    # Helper function untuk menggabungkan suku-suku LaTeX
    def join_latex_terms(terms_list):
        result = ""
        for i, term_str in enumerate(terms_list):
            term_str = term_str.strip()
            is_neg = term_str.startswith('-')
            if i == 0:
                result = term_str
            else:
                result += f" - {term_str[1:]}" if is_neg else f" + {term_str}"
        return result

    calc_steps = []
    
    den_val_at_point = den.subs(x, point)
    if den_val_at_point == 0:
        return ("Substitusi langsung menghasilkan penyebut nol. Metode lain mungkin diperlukan.", "")

    explanation_text = f"Karena ini adalah fungsi rasional dan nilai penyebut tidak nol saat x mendekati {point}, kita bisa menggunakan metode substitusi langsung."
    
    # Pecah pembilang dan penyebut menjadi daftar suku-suku
    num_terms = num.as_ordered_terms()
    den_terms = den.as_ordered_terms()
    point_latex = latex(sympify(point))
    
    # --- Langkah 1: Substitusi (dengan tanda kurung dan urutan yang benar) ---
    num_sub_latex_list = [latex(term).replace('x', f"({point_latex})") for term in num_terms]
    den_sub_latex_list = [latex(term).replace('x', f"({point_latex})") for term in den_terms]
    
    num_display_sub = join_latex_terms(num_sub_latex_list)
    den_display_sub = join_latex_terms(den_sub_latex_list)
    
    step1_rhs = f"\\frac{{{num_display_sub}}}{{{den_display_sub}}}"
    calc_steps.append(rf"\lim_{{x \to {point}}} {latex(f)} &= {step1_rhs}")
    last_rhs = step1_rhs
    
    # --- Langkah 2: Evaluasi Perkalian di dalam pembilang & penyebut ---
    has_multiplication = any('*' in str(term) for term in num_terms) or any('*' in str(term) for term in den_terms)
    if has_multiplication:
        num_mul_latex_list = [latex(term.subs(x, point)) for term in num_terms]
        den_mul_latex_list = [latex(term.subs(x, point)) for term in den_terms]

        num_display_mul = join_latex_terms(num_mul_latex_list)
        den_display_mul = join_latex_terms(den_mul_latex_list)
        
        step2_rhs = f"\\frac{{{num_display_mul}}}{{{den_display_mul}}}"
        if step2_rhs != last_rhs:
            calc_steps.append(f"&= {step2_rhs}")
            last_rhs = step2_rhs
        
    # --- Langkah 3: Evaluasi Penjumlahan/Pengurangan ---
    num_evaluated = num.subs(x, point)
    den_evaluated = den.subs(x, point)
    
    step3_rhs = f"\\frac{{{latex(num_evaluated)}}}{{{latex(den_evaluated)}}}"
    if step3_rhs != last_rhs:
        calc_steps.append(f"&= {step3_rhs}")
        last_rhs = step3_rhs
        
    # --- Langkah 4: Hasil Akhir ---
    hasil_akhir = limit(f, x, point)
    if latex(hasil_akhir) != last_rhs.replace("\\", ""):
        calc_steps.append(f"&= {latex(hasil_akhir)}")
        
    # Finalisasi
    unique_steps = [calc_steps[0]]
    for step in calc_steps[1:]:
        if unique_steps[-1].split('&=')[-1].strip() != step.split('&=')[-1].strip():
            unique_steps.append(step)
    
    calculation_latex = "\\begin{aligned}" + " \\\\ ".join(unique_steps) + "\\end{aligned}"
    return explanation_text, calculation_latex

def _solve_substitusi(f, x, point):
    """
    Dispatcher untuk metode substitusi (polinomial atau rasional).
    """
    num, den = f.as_numer_denom()

    if den != 1:
        return _solve_substitusi_rasional(f, x, point, num, den)
    else:
        # Logika untuk Polinomial (sudah benar)
        def join_latex_terms(terms_list):
            result = ""
            for i, term_str in enumerate(terms_list):
                term_str = term_str.strip()
                is_neg = term_str.startswith('-')
                if i == 0: result = term_str
                else: result += f" - {term_str[1:]}" if is_neg else f" + {term_str}"
            return result

        explanation_text = "Karena ini adalah fungsi polinomial yang kontinu, kita bisa langsung menemukan nilainya dengan metode substitusi langsung:"
        terms = f.as_ordered_terms()
        point_latex = latex(sympify(point))
        substituted_terms_latex = [latex(term).replace('x', f"({point_latex})") for term in terms]
        display_substitution = join_latex_terms(substituted_terms_latex)
        calc_steps = [rf"\lim_{{x \to {point}}} {latex(f)} &= {display_substitution}"]
        last_display = display_substitution
        
        if any('^' in term for term in substituted_terms_latex):
            power_eval_terms_latex = []
            for term in terms:
                term_after_pow = term.subs(x, point).replace(lambda p: isinstance(p, Pow), lambda p: p.base ** p.exp)
                if isinstance(term_after_pow, Mul):
                    coeff, val = term_after_pow.as_coeff_Mul()
                    power_eval_terms_latex.append(f"{latex(coeff)}({latex(val)})")
                else:
                    power_eval_terms_latex.append(latex(term_after_pow))
            display_after_power = join_latex_terms(power_eval_terms_latex)
            if display_after_power != last_display:
                calc_steps.append(f"&= {display_after_power}")
                last_display = display_after_power
        
        multiplied_terms_latex = [latex(term.subs(x, point)) for term in terms]
        display_after_multiplication = join_latex_terms(multiplied_terms_latex)
        if display_after_multiplication != last_display:
            calc_steps.append(f"&= {display_after_multiplication}")
            last_display = display_after_multiplication
            
        hasil_akhir = limit(f, x, point)
        if latex(hasil_akhir) != last_display:
            calc_steps.append(f"&= {latex(hasil_akhir)}")

        unique_steps = [calc_steps[0]]
        for i in range(1, len(calc_steps)):
            if unique_steps[-1].split('&=')[-1].strip() != calc_steps[i].split('&=')[-1].strip():
                unique_steps.append(calc_steps[i])
        
        calculation_latex = "\\begin{aligned}" + " \\\\ ".join(unique_steps) + "\\end{aligned}"
        return explanation_text, calculation_latex

def _solve_faktorisasi(f, x, point):
    """
    Menghasilkan langkah-langkah untuk metode faktorisasi yang detail.
    """
    explanation_text = r"Substitusi langsung pada fungsi ini menghasilkan bentuk tak tentu $\frac{0}{0}$. Oleh karena itu, kita perlu menyederhanakan fungsi menggunakan metode faktorisasi:"
    num, den = f.as_numer_denom()
    num_factored, den_factored = factor(num), factor(den)
    f_canceled = cancel(f)
    hasil_akhir = limit(f, x, point)
    
    calc_steps = [
        rf"\lim_{{x \to {point}}} {latex(f)} &= \frac{{{latex(num_factored)}}}{{{latex(den_factored)}}}",
        rf"&= {latex(f_canceled)}",
        f"&= {latex(f_canceled).replace('x', f'({point})')}",
        f"&= {latex(hasil_akhir)}"
    ]
    
    unique_steps = [calc_steps[0]]
    for step in calc_steps[1:]:
        if unique_steps[-1].split('&=')[-1].strip() != step.split('&=')[-1].strip():
            unique_steps.append(step)

    calculation_latex = "\\begin{aligned}" + " \\\\ ".join(unique_steps) + "\\end{aligned}"
    return explanation_text, calculation_latex

def _solve_rasionalisasi(f, x, point):
    """
    Menghasilkan langkah pengerjaan rasionalisasi yang sistematis.
    Mengikuti pola: Limit → Kalikan Sekawan → Ekspansi → Faktorisasi → Coret → Substitusi → Hasil
    """
    from sympy import sqrt, expand, factor, cancel, simplify
    
    explanation_text = r"Hasil substitusi langsung adalah bentuk tak tentu $\frac{0}{0}$. Kita akan menggunakan metode rasionalisasi dengan mengalikan dengan bentuk sekawan."
    
    num, den = f.as_numer_denom()
    calc_steps = []
    
    # Identifikasi bagian yang mengandung akar
    target_expr, conjugate = None, None
    
    if 'sqrt' in str(num):
        target_expr = num
    elif 'sqrt' in str(den):
        target_expr = den
    else:
        return "Error: Tidak ditemukan bentuk akar.", ""
    
    # Buat bentuk sekawan
    terms = target_expr.as_ordered_terms()
    if len(terms) == 2:
        conjugate = terms[0] - terms[1]
    else:
        return "Error: Gagal memproses bentuk sekawan.", ""
    
    point_latex = latex(sympify(point))
    
    # LANGKAH 1: Limit awal
    calc_steps.append(
        rf"\lim_{{x \to {point_latex}}} {latex(f)}"
    )
    
    # LANGKAH 2: Kalikan dengan sekawan (tampilkan dalam bentuk perkalian)
    calc_steps.append(
        rf"&= \lim_{{x \to {point_latex}}} \left( {latex(f)} \right) \cdot \frac{{{latex(conjugate)}}}{{{latex(conjugate)}}}"
    )
    
    # LANGKAH 3: Hasil perkalian menggunakan (a-b)(a+b) = a²-b²
    # Hitung pembilang dan penyebut baru
    new_num = expand(num * conjugate)
    new_den = expand(den * conjugate)
    
    calc_steps.append(
        rf"&= \lim_{{x \to {point_latex}}} \frac{{{latex(new_num)}}}{{{latex(new_den)}}}"
    )
    
    # LANGKAH 4: Faktorisasi (jika memungkinkan)
    num_factored = factor(new_num)
    den_factored = factor(new_den)
    
    # Cek apakah ada perubahan setelah faktorisasi
    if latex(num_factored) != latex(new_num) or latex(den_factored) != latex(new_den):
        calc_steps.append(
            rf"&= \lim_{{x \to {point_latex}}} \frac{{{latex(num_factored)}}}{{{latex(den_factored)}}}"
        )
    
    # LANGKAH 5: Coret faktor yang sama
    f_canceled = cancel(num_factored / den_factored)
    
    # Cek apakah ada pembatalan
    if latex(f_canceled) != latex(num_factored / den_factored):
        calc_steps.append(
            rf"&= \lim_{{x \to {point_latex}}} {latex(f_canceled)}"
        )
    
    # LANGKAH 6: Substitusi nilai x (dengan tanda kurung)
    num_final, den_final = f_canceled.as_numer_denom()
    
    # Ganti x dengan nilai point dalam tanda kurung
    num_substituted = latex(num_final).replace(str(x), f'({point_latex})')
    
    if den_final != 1:
        den_substituted = latex(den_final).replace(str(x), f'({point_latex})')
        calc_steps.append(
            rf"&= \frac{{{num_substituted}}}{{{den_substituted}}}"
        )
    else:
        calc_steps.append(
            f"&= {num_substituted}"
        )
    
    # LANGKAH 7: Evaluasi perhitungan dalam akar
    num_eval = num_final.subs(x, point)
    den_eval = den_final.subs(x, point)
    
    # Cek apakah masih ada akar yang bisa dievaluasi
    if 'sqrt' in latex(num_eval) or 'sqrt' in latex(den_eval):
        if den_eval != 1:
            calc_steps.append(
                rf"&= \frac{{{latex(num_eval)}}}{{{latex(den_eval)}}}"
            )
        else:
            calc_steps.append(
                f"&= {latex(num_eval)}"
            )
    
    # LANGKAH 8: Hitung nilai akar
    num_sqrt_eval = num_eval
    den_sqrt_eval = den_eval
    
    # Evaluasi akar jika ada
    try:
        if 'sqrt' in str(num_eval):
            num_sqrt_eval = num_eval.evalf()
            num_sqrt_eval = sympify(num_sqrt_eval) if num_sqrt_eval == int(num_sqrt_eval) else num_eval
        
        if 'sqrt' in str(den_eval):
            den_sqrt_eval = den_eval.evalf()
            den_sqrt_eval = sympify(den_sqrt_eval) if den_sqrt_eval == int(den_sqrt_eval) else den_eval
        
        if den_sqrt_eval != 1 and (latex(num_sqrt_eval) != latex(num_eval) or latex(den_sqrt_eval) != latex(den_eval)):
            calc_steps.append(
                rf"&= \frac{{{latex(num_sqrt_eval)}}}{{{latex(den_sqrt_eval)}}}"
            )
        elif den_sqrt_eval == 1 and latex(num_sqrt_eval) != latex(num_eval):
            calc_steps.append(
                f"&= {latex(num_sqrt_eval)}"
            )
    except:
        pass
    
    # LANGKAH 9: Hasil akhir
    hasil_akhir = limit(f, x, point)
    last_value = calc_steps[-1].split('=')[-1].strip()
    
    if latex(hasil_akhir) not in last_value:
        calc_steps.append(
            f"&= {latex(hasil_akhir)}"
        )
    
    # Hilangkan langkah duplikat
    unique_steps = [calc_steps[0]]
    for step in calc_steps[1:]:
        current_rhs = step.split('&=')[-1].strip() if '&=' in step else step.strip()
        previous_rhs = unique_steps[-1].split('&=')[-1].strip() if '&=' in unique_steps[-1] else unique_steps[-1].strip()
        
        # Normalisasi untuk perbandingan
        current_clean = current_rhs.replace(' ', '').replace('\\left', '').replace('\\right', '')
        previous_clean = previous_rhs.replace(' ', '').replace('\\left', '').replace('\\right', '')
        
        if current_clean != previous_clean:
            unique_steps.append(step)
    
    calculation_latex = "\\begin{aligned}\n" + " \\\\ \n".join(unique_steps) + "\n\\end{aligned}"
    
    return explanation_text, calculation_latex

def _solve_trigonometri(f, x, point):
    explanation_text = r"Penyelesaian untuk limit trigonometri."
    hasil_akhir = limit(f, x, point)
    calc_steps = [rf"\lim_{{x \to {point}}} {latex(f)}", f"&= {latex(hasil_akhir)}"]
    calculation_latex = "\\begin{aligned}" + " \\\\ ".join(calc_steps) + "\\end{aligned}"
    return explanation_text, calculation_latex

def _solve_tak_hingga(f, x):
    explanation_text = r"Penyelesaian untuk limit tak hingga."
    hasil_akhir = limit(f, x, oo)
    calc_steps = [rf"\lim_{{x \to \infty}} {latex(f)}", f"&= {latex(hasil_akhir)}"]
    calculation_latex = "\\begin{aligned}" + " \\\\ ".join(calc_steps) + "\\end{aligned}"
    return explanation_text, calculation_latex

# ==============================================================================
# FUNGSI UTAMA (DISPATCHER)
# ==============================================================================

def generate_limit_explanation(params):
    problem_type = params.get('type')
    if not problem_type:
        return "Error: 'type' tidak ditemukan.", ""

    x = Symbol('x')
    f = sympify(params['f_str'])
    point_str = str(params['point'])
    point = sympify(point_str) if point_str not in ['oo', '-oo'] else oo

    if 'substitusi' in problem_type:
        return _solve_substitusi(f, x, point)
    elif 'faktorisasi' in problem_type:
        return _solve_faktorisasi(f, x, point)
    elif 'rasionalisasi' in problem_type:
        return _solve_rasionalisasi(f, x, point)
    elif 'trigonometri' in problem_type:
        return _solve_trigonometri(f, x, point)
    elif 'tak_hingga' in problem_type:
        return _solve_tak_hingga(f, x)
    else:
        return f"Tipe soal '{problem_type}' tidak dikenali.", ""