from sympy import (
    sympify, limit, Symbol, sqrt, factor, cancel, expand, latex, oo,
    sin, cos, tan, Poly, degree, numer, denom, Add, Mul, Pow, S, Rational
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

def _solve_rasionalisasi_beda_akar(f, x, point):
    """
    Fungsi KHUSUS untuk rasionalisasi beda akar (Level 9)
    Menggunakan metode "Memecah dan Merasionalisasi" untuk kejelasan.
    VERSI FINAL dengan substitusi eksplisit dan tipografi yang disempurnakan.
    """
    from sympy import expand, cancel, Add, Rational, N
    
    num, den = f.as_numer_denom()
    point_latex = latex(sympify(point))
    
    # --- Langkah 1: Verifikasi & Dekomposisi ---
    num_terms = num.as_ordered_terms()
    sqrt_terms = [t for t in num_terms if 'sqrt' in str(t)]
    const_terms = [t for t in num_terms if 'sqrt' not in str(t)]
    
    if not (len(sqrt_terms) == 2 and len(const_terms) == 1):
        return "Error: Metode ini hanya untuk soal dengan dua akar dan satu konstanta.", ""

    sqrt_A_expr = sqrt_terms[0]
    sqrt_B_expr = sqrt_terms[1]
    const_C_val = const_terms[0]
    
    const_C1_val = sqrt_A_expr.subs(x, point)
    const_C2_val = sqrt_B_expr.subs(x, point)

    if N(const_C1_val + const_C2_val) != N(-const_C_val):
        return "Error: Soal tidak dapat diselesaikan dengan metode pemecahan konstanta.", ""

    # --- Persiapan untuk Teks Penjelasan ---
    explanation_text = (
        f"Substitusi langsung menghasilkan bentuk tak tentu 0/0. "
        f"Kita gunakan metode pemecahan konstanta, di mana {latex(const_C_val)} dipecah menjadi "
        f"{latex(-const_C1_val)} dan {latex(-const_C2_val)}."
    )
    
    # --- Langkah 2: Pisahkan Limit ---
    calc_steps = []
    den_factored = factor(den)
    limit_A_num = (sqrt_A_expr - const_C1_val)
    limit_B_num = (sqrt_B_expr - const_C2_val)

    calc_steps.append(
        rf"\lim_{{x \to {point_latex}}} \left( \frac{{{latex(limit_A_num)}}}{{{latex(den)}}} + \frac{{{latex(limit_B_num)}}}{{{latex(den)}}} \right)"
    )

    # Fungsi pembantu untuk menyelesaikan satu bagian limit
    def solve_single_part(part_num_expr, part_const_val):
        steps = []
        conjugate = (part_num_expr + part_const_val * 2)
        
        steps.append(
            rf"&= \lim_{{x \to {point_latex}}} \frac{{{latex(part_num_expr)}}}{{{latex(den_factored)}}} \times \frac{{\left({latex(conjugate)}\right)}}{{\left({latex(conjugate)}\right)}}"
        )
        
        num_expanded = expand(part_num_expr * conjugate)
        den_unexpanded_display = f"\\left({latex(den_factored)}\\right)\\left({latex(conjugate)}\\right)"
        steps.append(
            rf"&= \lim_{{x \to {point_latex}}} \frac{{{latex(num_expanded)}}}{{{den_unexpanded_display}}}"
        )

        num_factored = factor(num_expanded)
        if latex(num_factored) != latex(num_expanded):
            steps.append(
                rf"&= \lim_{{x \to {point_latex}}} \frac{{{latex(num_factored)}}}{{{den_unexpanded_display}}}"
            )
            
        common_factor = (x - point)
        num_after_cancel = cancel(num_factored / common_factor)
        den_main_after_cancel = cancel(den_factored / common_factor)
        
        expr_after_cancel = num_after_cancel / (den_main_after_cancel * conjugate)
        steps.append(rf"&= \lim_{{x \to {point_latex}}} {latex(expr_after_cancel)}")
        
        # --- PERUBAHAN 1: TAMPILKAN SUBSTITUSI EKSPLISIT ---
        # Ganti simbol 'x' dengan nilainya dalam tanda kurung
        substitusi_display = latex(expr_after_cancel).replace('x', f'({point_latex})')
        steps.append(rf"&= {substitusi_display}")
        # --- AKHIR PERUBAHAN 1 ---
        
        final_num = num_after_cancel.subs(x, point)
        final_den = (den_main_after_cancel * conjugate).subs(x, point)
        
        result = Rational(final_num, final_den)
        steps.append(f"&= {latex(result)}")

        return result, steps

    # --- PERUBAHAN 2: HAPUS \textbf DARI JUDUL ---
    calc_steps.append(r"\\ \text{Menyelesaikan limit bagian pertama (L_1):}")
    result_A, steps_A = solve_single_part(limit_A_num, const_C1_val)
    calc_steps.extend(steps_A)

    calc_steps.append(r"\\ \text{Menyelesaikan limit bagian kedua (L_2):}")
    result_B, steps_B = solve_single_part(limit_B_num, const_C2_val)
    calc_steps.extend(steps_B)

    calc_steps.append(r"\\ \text{Menjumlahkan hasil akhir (L_1 + L_2):}")
    # --- AKHIR PERUBAHAN 2 ---
    
    final_answer = result_A + result_B
    calc_steps.append(rf"&= {latex(result_A)} + {latex(result_B)}")
    calc_steps.append(rf"&= {latex(final_answer)}")

    # --- PERUBAHAN 3: BUNGKUS DENGAN ARRAY 'c' UNTUK ALIGN TENGAH ---
    # Gabungkan semua langkah menjadi satu blok LaTeX yang terpusat
    calculation_latex = "\\begin{array}{c}" + "\\begin{aligned}" + " \\\\ ".join(calc_steps) + "\\end{aligned}" + "\\end{array}"
    # --- AKHIR PERUBAHAN 3 ---
    
    return explanation_text, calculation_latex

def _solve_trigonometri(f, x, point):
    """
    REVISED: Memberikan penjelasan langkah demi langkah untuk soal trigonometri,
    terutama yang memerlukan substitusi variabel (Level 10).
    """
    from sympy import pi, numer, denom, factor
    
    # --- Cek apakah soal ini cocok dengan pola substitusi ---
    # Pola: sin(ax) / (b(x-c)) atau tan(ax) / (b(x-c))
    num, den = f.as_numer_denom()
    is_substitution_pattern = (
        point != 0 and
        (num.func == sin or num.func == tan) and
        len(num.args) == 1 and
        len(den.args) == 2 # Harus perkalian, misal: 15 * (x - 2*pi)
    )

    if is_substitution_pattern:
        try:
            # --- Implementasi Template Pengerjaan Langkah-demi-Langkah ---
            a_coeff = num.args[0].as_coeff_mul()[0]
            
            # Ekstrak koefisien dan faktor dari penyebut
            den_factored = factor(den)
            b_coeff = S.One
            x_minus_c_part = S.One

            if den_factored.is_Mul:
                for arg in den_factored.args:
                    if arg.is_Number:
                        b_coeff = arg
                    else:
                        x_minus_c_part = arg
            else: # Jika penyebut tidak dalam bentuk perkalian (misal: x - pi)
                b_coeff = S.One
                x_minus_c_part = den_factored

            # Validasi akhir pola
            if x_minus_c_part != (x - point):
                 raise ValueError("Pola tidak cocok setelah faktorisasi")

            calc_steps = []
            point_latex = latex(point)
            
            # Langkah 1: Faktorkan Penyebut
            explanation_text = "Substitusi langsung menghasilkan 0/0. Kita perlu memfaktorkan penyebut dan melakukan substitusi variabel."
            calc_steps.append(rf"\lim_{{x \to {point_latex}}} \frac{{{latex(num)}}}{{{latex(factor(den))}}}")

            # Langkah 2: Substitusi Variabel
            y = Symbol('y')
            calc_steps.append(r"\\ \text{Misalkan } y = " + latex(x-point) + r", \text{ sehingga } x = y + " + point_latex)
            calc_steps.append(r"\text{Ketika } x \to " + point_latex + r", \text{ maka } y \to 0.")
            
            num_substituted = num.subs(x, y + point)
            calc_steps.append(rf"\lim_{{y \to 0}} \frac{{{latex(num_substituted)}}}{{{latex(b_coeff * y)}}}")

            # Langkah 3: Gunakan Sifat Periodisitas
            # Sederhanakan argumen sin/tan, misal sin(6y + 12*pi) -> sin(6y)
            num_simplified_arg = num.func(a_coeff * y)
            if num_substituted != num_simplified_arg:
                calc_steps.append(r"\\ \text{Gunakan sifat periodisitas: } " + latex(num_substituted) + " = " + latex(num_simplified_arg))
                calc_steps.append(rf"\lim_{{y \to 0}} \frac{{{latex(num_simplified_arg)}}}{{{latex(b_coeff * y)}}}")

            # Langkah 4 & 5: Selesaikan Limit Dasar dan Hasil Akhir
            final_answer = limit(f, x, point)
            calc_steps.append(rf"&= \frac{{{latex(a_coeff)}}}{{{latex(b_coeff)}}}")
            
            if final_answer != Rational(a_coeff, b_coeff):
                calc_steps.append(f"&= {latex(final_answer)}")

            calculation_latex = "\\begin{aligned}" + " \\\\ ".join(calc_steps) + "\\end{aligned}"
            return explanation_text, calculation_latex

        except Exception:
            # Jika terjadi error saat memproses, kembali ke metode simpel
            pass

    # --- Fallback: Metode Penjelasan Simpel (untuk soal x->0 atau pola lain) ---
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
    elif 'rasionalisasi_beda_akar' in problem_type:
        # ROUTING KHUSUS untuk level 9 (beda akar)
        return _solve_rasionalisasi_beda_akar(f, x, point)
    elif 'rasionalisasi' in problem_type:
        # Level 7 dan 8 (rasionalisasi biasa)
        return _solve_rasionalisasi(f, x, point)
    elif 'trigonometri' in problem_type:
        return _solve_trigonometri(f, x, point)
    elif 'tak_hingga' in problem_type:
        return _solve_tak_hingga(f, x)
    else:
        return f"Tipe soal '{problem_type}' tidak dikenali.", ""