from sympy import (
    sympify, limit, Symbol, sqrt, factor, cancel, expand, latex, oo,
    sin, cos, tan, Poly, degree, numer, denom, Add, Mul, Pow
)

def check_answer(user_answer, correct_answer):
    """Memeriksa apakah jawaban pengguna sama dengan jawaban yang benar."""
    return user_answer.strip() == str(correct_answer).strip()

# ==============================================================================
# FUNGSI-FUNGSI PEMBANTU UNTUK SETIAP TIPE SOAL
# ==============================================================================

def _solve_substitusi_rasional(f, x, point, num, den):
    """
    Fungsi KHUSUS untuk menghasilkan langkah pengerjaan
    substitusi langsung pada FUNGSI RASIONAL (PECAHAN).
    VERSI DETAIL DENGAN LANGKAH PEMDAS LENGKAP.
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
    # Cek apakah ada perkalian yang perlu dilakukan
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
    unique_steps = []
    if calc_steps:
        unique_steps.append(calc_steps[0])
        for i in range(1, len(calc_steps)):
            prev_rhs = unique_steps[-1].split('&=')[-1].strip()
            current_rhs = calc_steps[i].split('&=')[-1].strip()
            if prev_rhs != current_rhs:
                unique_steps.append(calc_steps[i])
    
    calculation_latex = "\\begin{aligned}" + " \\\\ ".join(unique_steps) + "\\end{aligned}"
    return explanation_text, calculation_latex

def _solve_substitusi(f, x, point):
    """
    Memilih metode penyelesaian substitusi yang tepat
    berdasarkan bentuk fungsi (polinomial atau rasional).
    """
    num, den = f.as_numer_denom()

    if den != 1:
        return _solve_substitusi_rasional(f, x, point, num, den)
    else:
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

        unique_steps = []
        if calc_steps:
            unique_steps.append(calc_steps[0])
            for i in range(1, len(calc_steps)):
                prev_rhs = unique_steps[-1].split('&=')[-1].strip()
                current_rhs = calc_steps[i].split('&=')[-1].strip()
                if prev_rhs != current_rhs:
                    unique_steps.append(calc_steps[i])
        
        calculation_latex = "\\begin{aligned}" + " \\\\ ".join(unique_steps) + "\\end{aligned}"
        return explanation_text, calculation_latex

def _solve_faktorisasi(f, x, point):
    """Menghasilkan langkah-langkah untuk metode faktorisasi."""
    explanation_text = r"Substitusi langsung pada fungsi ini menghasilkan bentuk tak tentu $\frac{0}{0}$. Oleh karena itu, kita perlu menyederhanakan fungsi menggunakan metode faktorisasi:"
    num, den = f.as_numer_denom()
    num_factored = factor(num)
    den_factored = factor(den)
    f_canceled = cancel(f)
    hasil_akhir = limit(f, x, point)
    
    # --- PERBAIKAN DIMULAI DI SINI ---
    
    # Membuat string LaTeX secara aman
    num_factored_latex = latex(num_factored)
    den_factored_latex = latex(den_factored)
    
    # Membuat daftar langkah pengerjaan yang baru dan lebih detail
    calc_steps = [
        # Langkah 1: Tampilkan faktorisasi (tanpa 'lim' di sisi kanan)
        rf"\lim_{{x \to {point}}} {latex(f)} &= \frac{{{num_factored_latex}}}{{{den_factored_latex}}}",
        
        # Langkah 2: Tampilkan fungsi setelah disederhanakan/dicoret (tanpa 'lim')
        rf"&= {latex(f_canceled)}",
        
        # Langkah 3: Tampilkan proses substitusi (LANGKAH BARU)
        f"&= {latex(f_canceled).replace('x', f'({point})')}",
        
        # Langkah 4: Tampilkan Hasil Akhir
        f"&= {latex(hasil_akhir)}"
    ]
    
    # Membersihkan jika ada langkah yang hasilnya identik
    unique_steps = []
    if calc_steps:
        unique_steps.append(calc_steps[0])
        for i in range(1, len(calc_steps)):
            prev_rhs = unique_steps[-1].split('&=')[-1].strip()
            current_rhs = calc_steps[i].split('&=')[-1].strip()
            if prev_rhs != current_rhs:
                unique_steps.append(calc_steps[i])

    # Menggabungkan semua langkah
    calculation_latex = "\\begin{aligned}" + " \\\\ ".join(unique_steps) + "\\end{aligned}"
    return explanation_text, calculation_latex

def _solve_rasionalisasi(f, x, point):
    """Menghasilkan langkah-langkah untuk metode rasionalisasi."""
    explanation_text = r"Hasil substitusi langsung adalah bentuk tak tentu $\frac{0}{0}$. Kita akan menggunakan metode rasionalisasi dengan mengalikan dengan bentuk sekawan."
    num, den = f.as_numer_denom()
    
    target_expr = None
    is_num_target = False
    
    if 'sqrt' in str(num):
        target_expr = num
        is_num_target = True
    elif 'sqrt' in str(den):
        target_expr = den
        is_num_target = False
    else:
        return "Error: Tidak ditemukan bentuk akar untuk dirasionalisasi.", ""

    terms = target_expr.as_ordered_terms()
    if len(terms) == 2:
        conjugate = terms[0] - terms[1]
    else:
        return "Error: Gagal memproses bentuk sekawan.", ""

    if is_num_target:
        num_rationalized = expand(num * conjugate)
        rationalized_display = rf"\frac{{{latex(num_rationalized)}}}{{\left({latex(den)}\right)\left({latex(conjugate)}\right)}}"
        f_rationalized = num_rationalized / (den * conjugate)
    else: 
        den_rationalized = expand(den * conjugate)
        rationalized_display = rf"\frac{{\left({latex(num)}\right)\left({latex(conjugate)}\right)}}{{{latex(den_rationalized)}}}"
        f_rationalized = (num * conjugate) / den_rationalized

    f_canceled = cancel(f_rationalized)
    hasil_akhir = limit(f, x, point)
    
    # --- PERBAIKAN DIMULAI DI SINI ---
    # Daftar langkah pengerjaan yang disempurnakan
    calc_steps = [
        # Langkah 1: Kalikan dengan sekawan/sekawan
        rf"\lim_{{x \to {point}}} {latex(f)} &= \lim_{{x \to {point}}} \left( {latex(f)} \right) \cdot \frac{{{latex(conjugate)}}}{{{latex(conjugate)}}}",
        
        # Langkah 2: Tampilkan hasil perkalian sekawan
        rf"&= \lim_{{x \to {point}}} {rationalized_display}",
        
        # Langkah 3: Tampilkan setelah disederhanakan/dicoret
        rf"&= \lim_{{x \to {point}}} {latex(f_canceled)}",
        
        # Langkah 4: Tampilkan proses substitusi (LANGKAH BARU)
        f"&= {latex(f_canceled).replace('x', f'({point})')}",
        
        # Langkah 5: Tampilkan Hasil Akhir
        f"&= {latex(hasil_akhir)}"
    ]
    # --- AKHIR PERBAIKAN ---
    
    # Membersihkan langkah duplikat jika ada
    unique_steps = []
    if calc_steps:
        unique_steps.append(calc_steps[0])
        for i in range(1, len(calc_steps)):
            prev_rhs = unique_steps[-1].split('&=')[-1].strip()
            current_rhs = calc_steps[i].split('&=')[-1].strip()
            if prev_rhs != current_rhs:
                unique_steps.append(calc_steps[i])

    calculation_latex = "\\begin{aligned}" + " \\\\ ".join(unique_steps) + "\\end{aligned}"
    return explanation_text, calculation_latex

def _solve_trigonometri(f, x, point):
    # (Kode ini disalin dari file Anda untuk kelengkapan)
    explanation_text = r"Untuk limit trigonometri menuju 0, kita gunakan sifat-sifat khusus."
    hasil_akhir = limit(f, x, point)
    calc_steps = [rf"\lim_{{x \to {point}}} {latex(f)}", f"&= {latex(hasil_akhir)}"]
    calculation_latex = "\\begin{aligned}" + " \\\\ ".join(calc_steps) + "\\end{aligned}"
    return explanation_text, calculation_latex


def _solve_tak_hingga(f, x):
    # (Kode ini disalin dari file Anda untuk kelengkapan)
    explanation_text = r"Untuk limit menuju tak hingga, ..."
    # ... (sisa fungsi tidak diubah)
    num, den = f.as_numer_denom()
    deg_num, deg_den = degree(Poly(num, x)), degree(Poly(den, x))
    highest_power_term = x**deg_den
    new_num, new_den = expand(num / highest_power_term), expand(den / highest_power_term)
    f_divided = new_num / new_den
    hasil_akhir = limit(f, x, oo)
    calc_steps = [
        rf"\lim_{{x \to \infty}} {latex(f)} &= \lim_{{x \to \infty}} \frac{{\frac{{{latex(num)}}}{{{latex(highest_power_term)}}}}}{{\frac{{{latex(den)}}}{{{latex(highest_power_term)}}}}}",
        rf"&= \lim_{{x \to \infty}} {latex(f_divided)}"]
    if latex(hasil_akhir) not in calc_steps[-1]: calc_steps.append(f"&= {latex(hasil_akhir)}")
    unique_steps = []
    if calc_steps:
        unique_steps.append(calc_steps[0])
        for i in range(1, len(calc_steps)):
            if unique_steps[-1].split('&=')[-1].strip() != calc_steps[i].split('&=')[-1].strip():
                unique_steps.append(calc_steps[i])
    calculation_latex = "\\begin{aligned}" + " \\\\ ".join(unique_steps) + "\\end{aligned}"
    return explanation_text, calculation_latex

# ==============================================================================
# FUNGSI UTAMA (DISPATCHER)
# ==============================================================================

def generate_limit_explanation(params):
    """
    Menghasilkan penjelasan dan blok kalkulasi LaTeX untuk soal limit.
    """
    problem_type = params.get('type')
    if not problem_type:
        return "Error: 'type' tidak ditemukan dalam parameter.", ""

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