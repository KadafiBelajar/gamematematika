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

def _solve_substitusi(f, x, point):
    """
    Menghasilkan langkah-langkah untuk metode substitusi langsung.
    Versi ini memecah ekspresi menjadi suku-suku untuk kontrol penuh atas PEMDAS.
    """

    # Helper function untuk menggabungkan suku-suku LaTeX dengan benar
    def join_latex_terms(terms_list):
        result = ""
        for i, term_str in enumerate(terms_list):
            term_str = term_str.strip()
            # Tentukan apakah suku bernilai negatif
            is_neg = term_str.startswith('-')
            
            if i == 0:
                result = term_str
            else:
                if is_neg:
                    # Tambahkan sebagai operasi pengurangan
                    result += f" - {term_str[1:]}"
                else:
                    # Tambahkan sebagai operasi penjumlahan
                    result += f" + {term_str}"
        return result

    num, den = f.as_numer_denom()
    calc_steps = []
    explanation_text = ""

    # Kasus untuk fungsi rasional tidak berubah
    if den != 1:
        # ... (Logika untuk fungsi rasional tetap sama persis seperti sebelumnya)
        den_val_at_point = den.subs(x, point)
        if den_val_at_point == 0: return ("Error:...", "")
        explanation_text = f"Ini adalah fungsi rasional..."
        num_sub_display = sympify(str(num).replace('x', f"({point})"))
        den_sub_display = sympify(str(den).replace('x', f"({point})"))
        calc_steps.append(rf"\lim_{{x \to {point}}} {latex(f)} &= \frac{{{latex(num_sub_display)}}}{{\latex(den_sub_display)}}")
        num_evaluated = num.subs(x, point)
        den_evaluated = den.subs(x, point)
        if num_evaluated != num_sub_display or den_evaluated != den_sub_display:
            calc_steps.append(rf"&= \frac{{{latex(num_evaluated)}}}{{\latex(den_evaluated)}}")
        hasil_akhir = limit(f, x, point)
        if (num_evaluated / den_evaluated) != hasil_akhir:
            calc_steps.append(f"&= {latex(hasil_akhir)}")
        
    # --- PENDEKATAN BARU UNTUK FUNGSI POLINOMIAL ---
    else:
        explanation_text = "Karena ini adalah fungsi polinomial yang kontinu, kita bisa langsung menemukan nilainya dengan metode substitusi langsung:"
        
        # Pecah ekspresi f menjadi daftar suku-suku [4x^2, -4x, -5]
        terms = f.as_ordered_terms()
        
        # --- Langkah 1: Substitusi ---
        point_latex = latex(sympify(point))
        substituted_terms_latex = []
        for term in terms:
            # Ganti 'x' di representasi LaTeX dari setiap suku
            term_latex = latex(term).replace('x', f"({point_latex})")
            substituted_terms_latex.append(term_latex)
        
        display_substitution = join_latex_terms(substituted_terms_latex)
        calc_steps.append(rf"\lim_{{x \to {point}}} {latex(f)} &= {display_substitution}")
        last_display = display_substitution
        
        # --- Langkah 2: Evaluasi Pangkat (Exponents) ---
        has_power = any('^' in term for term in substituted_terms_latex)
        if has_power:
            power_eval_terms_latex = []
            for term in terms:
                # Lakukan substitusi dan evaluasi pangkat pada setiap suku
                term_after_pow = term.subs(x, point).replace(
                    lambda p: isinstance(p, Pow) and p.base.is_number, 
                    lambda p: p.base ** p.exp
                )
                # Format khusus untuk tampilan, misal: 4(9)
                if isinstance(term_after_pow, Mul):
                    coeff, val = term_after_pow.as_coeff_Mul()
                    power_eval_terms_latex.append(f"{latex(coeff)}({latex(val)})")
                else:
                    power_eval_terms_latex.append(latex(term_after_pow))

            display_after_power = join_latex_terms(power_eval_terms_latex)
            if display_after_power != last_display:
                calc_steps.append(f"&= {display_after_power}")
                last_display = display_after_power
        
        # --- Langkah 3: Evaluasi Perkalian (Multiplication) ---
        multiplied_terms_latex = [latex(term.subs(x, point)) for term in terms]
        display_after_multiplication = join_latex_terms(multiplied_terms_latex)
        if display_after_multiplication != last_display:
            calc_steps.append(f"&= {display_after_multiplication}")
            last_display = display_after_multiplication
            
        # --- Langkah 4: Hasil Akhir (Addition/Subtraction) ---
        hasil_akhir = limit(f, x, point)
        if latex(hasil_akhir) != last_display:
            calc_steps.append(f"&= {latex(hasil_akhir)}")

    # Membersihkan langkah duplikat
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
    explanation_text = r"Substitusi langsung pada fungsi ini menghasilkan bentuk tak tentu $rac{{0}}{{0}}$. Oleh karena itu, kita perlu menyederhanakan fungsi menggunakan metode faktorisasi:"
    num, den = f.as_numer_denom()
    num_factored = factor(num)
    den_factored = factor(den)
    f_canceled = cancel(f)
    hasil_akhir = limit(f, x, point)
    
    calc_steps = [
        rf"\lim_{{x \to {point}}} {latex(f)} &= \lim_{{x \to {point}}} \frac{{{latex(num_factored)}}}{{\latex(den_factored)}}\)",
        rf"&= \lim_{{x \to {point}}} {latex(f_canceled)}",
        f"&= {latex(f_canceled.subs(x, point))}",
        f"&= {latex(hasil_akhir)}"
    ]
    
    unique_steps = []
    for step in calc_steps:
        if not unique_steps or unique_steps[-1].split('=')[-1].strip() != step.split('=')[-1].strip():
            unique_steps.append(step)

    calculation_latex = "\\begin{aligned}" + " \\ ".join(unique_steps) + "\\end{aligned}"
    return explanation_text, calculation_latex

def _solve_rasionalisasi(f, x, point):
    """Menghasilkan langkah-langkah untuk metode rasionalisasi."""
    explanation_text = r"Hasil substitusi langsung adalah bentuk tak tentu $rac{{0}}{{0}}$. Kita akan menggunakan metode rasionalisasi dengan mengalikan akar sekawan:"
    num, den = f.as_numer_denom()
    
    target_expr = None
    if any(isinstance(arg, Pow) and arg.exp == 1/2 for arg in Add.make_args(num)):
        target_expr = num
        is_num_target = True
    elif any(isinstance(arg, Pow) and arg.exp == 1/2 for arg in Add.make_args(den)):
        target_expr = den
        is_num_target = False
    else:
        return "Error: Tidak ditemukan bentuk akar untuk dirasionalisasi.", ""

    term_with_sqrt = None
    other_term = None
    for arg in target_expr.as_ordered_terms():
        if 'sqrt' in str(arg) or (isinstance(arg, Pow) and arg.exp == 1/2):
            term_with_sqrt = arg
        else:
            other_term = arg
    
    if term_with_sqrt is None or other_term is None:
        return "Error: Gagal memisahkan bagian akar dan non-akar.", ""

    conjugate = term_with_sqrt - other_term

    if is_num_target:
        num_rationalized = expand(num * conjugate)
        f_rationalized_display = rf"\frac{{{latex(num_rationalized)}}}{{\left({latex(den)}\right)\left({latex(conjugate)}\right)}}"
        f_rationalized = num_rationalized / (den * conjugate)
    else:
        den_rationalized = expand(den * conjugate)
        f_rationalized_display = rf"\frac{{\left({latex(num)}\right)\left({latex(conjugate)}\right)}}{{\left({latex(den_rationalized)}\right)}}"
        f_rationalized = (num * conjugate) / den_rationalized

    f_canceled = cancel(f_rationalized)
    hasil_akhir = limit(f, x, point)

    calc_steps = [
        rf"\lim_{{x \to {point}}} {latex(f)} &= \lim_{{x \to {point}}} \left( {latex(f)} \right) \cdot \frac{{{latex(conjugate)}}}{{{latex(conjugate)}}}",
        rf"&= \lim_{{x \to {point}}} {f_rationalized_display}",
        rf"&= \lim_{{x \to {point}}} {latex(f_canceled)}",
        f"&= {latex(f_canceled.subs(x, point))}",
        f"&= {latex(hasil_akhir)}"
    ]
    
    unique_steps = []
    for step in calc_steps:
        if not unique_steps or unique_steps[-1].split('=')[-1].strip() != step.split('=')[-1].strip():
            unique_steps.append(step)

    calculation_latex = "\\begin{aligned}" + " \\ ".join(unique_steps) + "\\end{aligned}"
    return explanation_text, calculation_latex

def _solve_trigonometri(f, x, point):
    """Menghasilkan langkah-langkah untuk limit trigonometri."""
    explanation_text = r"Untuk limit trigonometri menuju 0, kita gunakan sifat-sifat khusus seperti $\lim_{{x \to 0}} \frac{{\sin(ax)}}{{bx}} = \frac{{a}}{{b}}$ dan $\lim_{{x \to 0}} \frac{{\tan(ax)}}{{bx}} = \frac{{a}}{{b}}$."
    
    hasil_akhir = limit(f, x, point)
    num, den = f.as_numer_denom()

    # Logika sederhana untuk mencocokkan pola umum
    num_str = str(num)
    den_str = str(den)
    
    calc_steps = [rf"\lim_{{x \to {point}}} {latex(f)}"]

    if 'sin' in num_str and 'x' in den_str and den.is_polynomial(x):
        a = num.args[0].coeff(x)
        b = Poly(den, x).all_coeffs()[0]
        calc_steps.append(rf"&= \frac{{{a}}}{{{b}}}")
    elif 'tan' in num_str and 'x' in den_str and den.is_polynomial(x):
        a = num.args[0].coeff(x)
        b = Poly(den, x).all_coeffs()[0]
        calc_steps.append(rf"&= \frac{{{a}}}{{{b}}}")
    elif 'sin' in num_str and 'tan' in den_str:
        a = num.args[0].coeff(x)
        b = den.args[0].coeff(x)
        calc_steps.append(rf"&= \frac{{{a}}}{{{b}}}")
    elif 'cos' in num_str:
        explanation_text = r"Untuk bentuk yang mengandung $1 - \cos(ax)$, kita bisa ubah menjadi $2\sin^2(\frac{{a}}{{2}}x)$ atau kalikan dengan sekawan $1 + \cos(ax)$."
        conjugate = 1 + cos(num.args[1] if isinstance(num, Add) else num)
        f_rationalized = expand(f * conjugate/conjugate)
        calc_steps.append(rf"&= \lim_{{x \to {point}}} {latex(f_rationalized)}")

    if str(hasil_akhir) not in calc_steps[-1]:
         calc_steps.append(f"&= {latex(hasil_akhir)}")

    unique_steps = []
    for step in calc_steps:
        if not unique_steps or unique_steps[-1].split('=')[-1].strip() != step.split('=')[-1].strip():
            unique_steps.append(step)

    calculation_latex = "\\begin{aligned}" + " \\ ".join(unique_steps) + "\\end{aligned}"
    return explanation_text, calculation_latex

def _solve_tak_hingga(f, x):
    """Menghasilkan langkah-langkah untuk limit di tak hingga."""
    num, den = f.as_numer_denom()
    deg_num = degree(Poly(num, x))
    deg_den = degree(Poly(den, x))
    
    explanation_text = f"Untuk limit menuju tak hingga, kita bagi pembilang dan penyebut dengan pangkat tertinggi dari penyebut, yaitu $x^{{{deg_den}}}$."
    
    highest_power_term = x**deg_den
    
    new_num = expand(num / highest_power_term)
    new_den = expand(den / highest_power_term)
    
    f_divided = new_num / new_den
    
    hasil_akhir = limit(f, x, oo)

    calc_steps = [
        rf"\lim_{{x \to \infty}} {latex(f)} &= \lim_{{x \to \infty}} \frac{{\frac{{{latex(num)}}}{{{latex(highest_power_term)}}}}}{{\frac{{{latex(den)}}}{{{latex(highest_power_term)}}}}}",
        rf"&= \lim_{{x \to \infty}} {latex(f_divided)}"
    ]

    # Menunjukkan substitusi oo, di mana c/x^n -> 0
    num_coeffs = Poly(num, x).all_coeffs()
    den_coeffs = Poly(den, x).all_coeffs()
    
    if deg_num == deg_den:
        explanation_text += " Karena pangkat tertinggi pembilang dan penyebut sama, hasilnya adalah rasio koefisien pangkat tertinggi."
        calc_steps.append(rf"&= \frac{{{num_coeffs[0]}}}{{{den_coeffs[0]}}}")
    elif deg_num < deg_den:
        explanation_text += " Karena pangkat tertinggi pembilang lebih kecil dari penyebut, hasilnya adalah 0."
        calc_steps.append("&= 0")
    else: # deg_num > deg_den
        explanation_text += " Karena pangkat tertinggi pembilang lebih besar dari penyebut, hasilnya adalah tak hingga (atau negatif tak hingga)."
        calc_steps.append(f"&= {latex(hasil_akhir)}")

    if str(hasil_akhir) not in calc_steps[-1]:
        calc_steps.append(f"&= {latex(hasil_akhir)}")

    unique_steps = []
    for step in calc_steps:
        if not unique_steps or unique_steps[-1].split('=')[-1].strip() != step.split('=')[-1].strip():
            unique_steps.append(step)

    calculation_latex = "\\begin{aligned}" + " \\ ".join(unique_steps) + "\\end{aligned}"
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