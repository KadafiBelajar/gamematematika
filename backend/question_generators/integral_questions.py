import random
from sympy import Symbol, latex, integrate, sin, cos, tan, sec, exp, log, asin, atan, sqrt, Rational, simplify, expand, factor, pi, S
from sympy import symbols, Mul, Add


x = Symbol('x')


def _fmt_answer(expr):
    """Format jawaban integral, hilangkan konstanta C untuk pilihan ganda."""
    try:
        simp = simplify(expr)
        # Hapus konstanta integrasi jika ada
        if isinstance(simp, Add):
            # Cek apakah ada konstanta bebas x
            const = 0
            other_terms = []
            for term in simp.args:
                if term.is_constant(x):
                    const += term
                else:
                    other_terms.append(term)
            if other_terms:
                result = Add(*other_terms)
                return str(simplify(result))
            else:
                return str(simplify(simp))
        return str(simp)
    except Exception:
        return str(expr)


def _level1():
    """Level 1: Integral Polinomial Sederhana - Perkalian koefisien"""
    k = random.randint(2, 10)
    c = random.randint(2, 10)
    n = random.randint(3, 20)
    # Tampilkan sebagai perkalian untuk membuat terlihat rumit
    if random.random() < 0.5:
        # Bentuk: k * c * x^n
        f = k * c * x**n
        latex_str = rf"\int {k} \cdot {c} \cdot x^{{{n}}} \,dx"
    else:
        # Bentuk: (k * c * d) * x^n
        d = random.randint(2, 5)
        f = k * c * d * x**n
        latex_str = rf"\int ({k} \cdot {c} \cdot {d}) x^{{{n}}} \,dx"
    
    F = integrate(f, x)
    return {
        "latex": latex_str,
        "answer": _fmt_answer(F),
        "params": {"type": "integral_power_basic", "k": k, "c": c, "n": n}
    }


def _level2():
    """Level 2: Integral Penjumlahan & Pengurangan Polinomial"""
    num_terms = random.randint(3, 5)
    terms = []
    coeffs = []
    powers = []
    
    # Generate suku-suku dengan pangkat tidak berurutan
    available_powers = list(range(0, 21))
    random.shuffle(available_powers)
    
    for i in range(num_terms):
        coeff = random.randint(2, 50) * random.choice([1, -1])
        power = available_powers[i]
        terms.append(coeff * x**power)
        coeffs.append(coeff)
        powers.append(power)
    
    f = Add(*terms)
    F = integrate(f, x)
    
    return {
        "latex": rf"\int \left({latex(f)}\right) \,dx",
        "answer": _fmt_answer(F),
        "params": {"type": "integral_polynomial_sum", "num_terms": num_terms, "coeffs": coeffs, "powers": powers}
    }


def _level3():
    """Level 3: Kamuflase Bentuk Akar dan Pecahan"""
    choice = random.random()
    
    if choice < 0.33:
        # Bentuk: a * sqrt[m](x^n) ± b/x^p
        a = random.randint(2, 20)
        b = random.randint(2, 20)
        m = random.choice([2, 3, 4, 5])
        n = random.randint(1, m-1)
        p = random.randint(2, 9)
        sign = random.choice(['+', '-'])
        
        f = a * x**(Rational(n, m)) + (b if sign == '+' else -b) * x**(-p)
        
        if m == 2:
            root_str = rf"\sqrt{{x^{{{n}}}}}"
        else:
            root_str = rf"\sqrt[{m}]{{x^{{{n}}}}}"
        
        latex_str = rf"\int \left({a}\sqrt[{m}]{{x^{{{n}}}}} {sign} \frac{{{b}}}{{x^{{{p}}}}}\right) \,dx"
        
    elif choice < 0.66:
        # Bentuk: b/x^p ± a*sqrt[m](x^n)
        a = random.randint(2, 20)
        b = random.randint(2, 20)
        m = random.choice([2, 3, 4])
        n = random.randint(1, m-1)
        p = random.randint(2, 9)
        sign = random.choice(['+', '-'])
        
        f = (b if sign == '+' else -b) * x**(-p) + a * x**(Rational(n, m))
        latex_str = rf"\int \left(\frac{{{b}}}{{x^{{{p}}}}} {sign} {a}\sqrt[{m}]{{x^{{{n}}}}}\right) \,dx"
    else:
        # Bentuk: a*sqrt(x^n) - 1/sqrt[m](x^n)
        a = random.randint(2, 15)
        m = random.choice([3, 4])
        n = random.randint(1, m-1)
        
        f = a * sqrt(x**3) - x**(-Rational(n, m))
        latex_str = rf"\int \left({a}\sqrt{{x^3}} - \frac{{1}}{{\sqrt[{m}]{{x^{{{n}}}}}}}\right) \,dx"
    
    F = integrate(f, x)
    return {
        "latex": latex_str,
        "answer": _fmt_answer(F),
        "params": {"type": "integral_root_fraction"}
    }


def _level4():
    """Level 4: Distribusi dan Sederhanakan Dulu"""
    choice = random.random()
    
    if choice < 0.5:
        # Bentuk: (ax^n + b)(cx^m + d)
        a = random.randint(2, 15)
        b = random.randint(2, 15)
        c = random.randint(2, 15)
        d = random.randint(2, 15)
        n = random.randint(1, 5)
        m = random.randint(1, 5)
        
        u = a*x**n + b
        v = c*x**m + d
        f = u * v
        F = integrate(expand(f), x)
        
        latex_str = rf"\int ({latex(u)})({latex(v)}) \,dx"
        
        return {
            "latex": latex_str,
            "answer": _fmt_answer(F),
            "params": {"type": "integral_expand_first", "a": a, "b": b, "c": c, "d": d, "n": n, "m": m, "form": "product"}
        }
        
    elif choice < 0.75:
        # Bentuk: x^n(ax^m + bx + c)
        n = random.randint(1, 5)
        a = random.randint(2, 15)
        m = random.randint(1, 5)
        b = random.randint(2, 15)
        c = random.randint(2, 15)
        
        poly = a*x**m + b*x + c
        f = x**n * poly
        F = integrate(expand(f), x)
        
        latex_str = rf"\int x^{{{n}}}({latex(poly)}) \,dx"
        
        return {
            "latex": latex_str,
            "answer": _fmt_answer(F),
            "params": {"type": "integral_expand_first", "n": n, "a": a, "b": b, "c": c, "m": m, "form": "multiply"}
        }
    else:
        # Bentuk: (ax^n + bx^m)/(cx^p)
        a = random.randint(2, 15)
        b = random.randint(2, 15)
        n = random.randint(3, 7)
        m = random.randint(1, n-1)
        c = random.randint(2, 10)
        p = random.randint(1, 3)
        
        num = a*x**n + b*x**m
        den = c*x**p
        f = num / den
        F = integrate(expand(f), x)
        
        latex_str = rf"\int \frac{{{latex(num)}}}{{{latex(den)}}} \,dx"
        
        return {
            "latex": latex_str,
            "answer": _fmt_answer(F),
            "params": {"type": "integral_expand_first", "a": a, "b": b, "c": c, "n": n, "m": m, "p": p, "form": "divide"}
        }


def _level5():
    """Level 5: Integral Trigonometri Dasar"""
    a = random.randint(2, 25) * random.choice([1, -1])
    b = random.randint(2, 25) * random.choice([1, -1])
    c = random.randint(2, 25) * random.choice([1, -1])
    
    terms = []
    latex_terms = []
    
    if random.random() < 0.5:
        terms.append(a * sin(x))
        latex_terms.append(f"{a}\\sin(x)")
    else:
        terms.append(a * sin(x))
        latex_terms.append(f"{a}\\sin(x)")
    
    if random.random() < 0.7:
        sign = '+' if b > 0 else ''
        terms.append(b * cos(x))
        latex_terms.append(f"{sign}{b}\\cos(x)")
    
    if random.random() < 0.5:
        sign = '+' if c > 0 else ''
        terms.append(c * sec(x)**2)
        latex_terms.append(f"{sign}{c}\\sec^2(x)")
    
    f = Add(*terms)
    F = integrate(f, x)
    
    latex_str = rf"\int \left({' + '.join(latex_terms)}\right) \,dx"
    
    return {
        "latex": latex_str,
        "answer": _fmt_answer(F),
        "params": {"type": "integral_trig_basic", "a": a, "b": b, "c": c}
    }


def _level6():
    """Level 6: Integral Tentu Polinomial Sederhana"""
    k = random.randint(2, 10)
    n = random.randint(1, 3)
    
    # Pilih batas yang "menarik"
    if random.random() < 0.3:
        a = 0
        b = random.randint(1, 3)
    elif random.random() < 0.5:
        a = random.randint(-3, -1)
        b = random.randint(1, 3)
    else:
        a = random.randint(-2, 0)
        b = 0
    
    f = k * x**n
    F_definite = integrate(f, (x, a, b))
    
    latex_str = rf"\int_{{{a}}}^{{{b}}} {latex(f)} \,dx"
    
    return {
        "latex": latex_str,
        "answer": _fmt_answer(F_definite),
        "params": {"type": "integral_definite_basic", "k": k, "n": n, "a": a, "b": b}
    }


def _level7():
    """Level 7: Integral Substitusi Paling Dasar (u = ax + b)"""
    k = random.randint(2, 9)
    a = random.randint(2, 9)
    b = random.randint(2, 9) * random.choice([1, -1])
    n = random.randint(3, 15)
    
    if random.random() < 0.7:
        # Bentuk: k(ax+b)^n
        inner = a*x + b
        f = k * inner**n
        latex_str = rf"\int {k}({latex(inner)})^{{{n}}} \,dx"
    else:
        # Bentuk: k/(ax+b)^n
        inner = a*x + b
        f = k * inner**(-n)
        latex_str = rf"\int \frac{{{k}}}{{({latex(inner)})^{{{n}}}}} \,dx"
    
    F = integrate(f, x)
    
    return {
        "latex": latex_str,
        "answer": _fmt_answer(F),
        "params": {"type": "integral_substitution_basic", "k": k, "a": a, "b": b, "n": n}
    }


def _level8():
    """Level 8: Integral Substitusi Lanjutan (u = ax^n + b)"""
    choice = random.random()
    
    if choice < 0.4:
        # Bentuk: kx^(n-1)(ax^n+b)^m
        a = random.randint(2, 9)
        b = random.randint(2, 9) * random.choice([1, -1])
        n = random.randint(2, 5)
        m = random.randint(2, 10)
        k = a * n  # Pastikan k adalah kelipatan a*n
        
        inner = a*x**n + b
        f = k * x**(n-1) * inner**m
        F = integrate(f, x)
        latex_str = rf"\int {k}x^{{{n-1}}} ({latex(inner)})^{{{m}}} \,dx"
        
    elif choice < 0.7:
        # Bentuk: kx^2/sqrt(ax^3+b)
        a = random.randint(2, 9)
        b = random.randint(1, 9)
        k = a * 3  # k = a*3 untuk memudahkan
        
        inner = a*x**3 + b
        f = k * x**2 / sqrt(inner)
        F = integrate(f, x)
        latex_str = rf"\int \frac{{{k}x^2}}{{\sqrt{{{latex(inner)}}}}} \,dx"
    else:
        # Bentuk: kx*sin(ax^2+b)
        a = random.randint(2, 9)
        b = random.randint(1, 9)
        k = a * 2
        
        inner = a*x**2 + b
        f = k * x * sin(inner)
        F = integrate(f, x)
        latex_str = rf"\int {k}x \sin({latex(inner)}) \,dx"
    
    return {
        "latex": latex_str,
        "answer": _fmt_answer(F),
        "params": {"type": "integral_substitution_advanced"}
    }


def _level9():
    """Level 9: Integral Parsial Sederhana (LIATE)"""
    a = random.randint(2, 10)
    b = random.randint(2, 10)
    
    func_choice = random.choice(['sin', 'cos', 'exp'])
    
    if func_choice == 'sin':
        f = a * x * sin(b * x)
        latex_str = rf"\int {a}x \sin({b}x) \,dx"
    elif func_choice == 'cos':
        f = a * x * cos(b * x)
        latex_str = rf"\int {a}x \cos({b}x) \,dx"
    else:
        f = a * x * exp(b * x)
        latex_str = rf"\int {a}x e^{{{b}x}} \,dx"
    
    F = integrate(f, x)
    
    return {
        "latex": latex_str,
        "answer": _fmt_answer(F),
        "params": {"type": "integral_by_parts", "a": a, "b": b, "func": func_choice}
    }


def _level10():
    """Level 10: Integral Trigonometri dengan Identitas"""
    a = random.randint(2, 12)
    
    func_choice = random.choice(['sin2', 'cos2', 'tan2'])
    
    if func_choice == 'sin2':
        f = sin(a*x)**2
        latex_str = rf"\int \sin^2({a}x) \,dx"
    elif func_choice == 'cos2':
        f = cos(a*x)**2
        latex_str = rf"\int \cos^2({a}x) \,dx"
    else:
        f = tan(a*x)**2
        latex_str = rf"\int \tan^2({a}x) \,dx"
    
    F = integrate(f, x)
    
    return {
        "latex": latex_str,
        "answer": _fmt_answer(F),
        "params": {"type": "integral_trig_identity", "a": a, "func": func_choice}
    }


def _level11():
    """Level 11: Integral Substitusi Trigonometri (Bentuk Sederhana)"""
    a = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    a_squared = a**2
    
    choice = random.random()
    
    if choice < 0.5:
        # Bentuk: k/sqrt(a^2-x^2) -> arcsin
        k = random.randint(1, 10) * random.choice([1, -1])
        f = k / sqrt(a_squared - x**2)
        F = integrate(f, x)
        latex_str = rf"\int \frac{{{k}}}{{\sqrt{{{a_squared}-x^2}}}} \,dx"
    else:
        # Bentuk: k/(a^2+x^2) -> arctan
        k = random.randint(1, 10)
        f = k / (a_squared + x**2)
        F = integrate(f, x)
        latex_str = rf"\int \frac{{{k}}}{{{a_squared}+x^2}} \,dx"
    
    return {
        "latex": latex_str,
        "answer": _fmt_answer(F),
        "params": {"type": "integral_trig_substitution", "a": a}
    }


def _level12():
    """Level 12: Integral Pecahan Parsial (Kasus Faktor Linear Berbeda)"""
    # Pilih parameter kecil untuk hasil A dan B yang bagus
    a, b, c, d = random.randint(1, 5), random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)
    k = random.randint(1, 5)
    
    # Pastikan penyebut bisa difaktorkan
    den1 = a*x + b
    den2 = c*x + d
    
    if random.random() < 0.5:
        # Bentuk: k/(ax+b)(cx+d)
        f = k / (den1 * den2)
        latex_str = rf"\int \frac{{{k}}}{{({latex(den1)})({latex(den2)})}} \,dx"
    else:
        # Bentuk: (kx+m)/(x^2+px+q) yang bisa difaktorkan
        # Buat polinomial kuadrat yang bisa difaktorkan
        r1 = random.randint(-5, 5)
        r2 = random.randint(-5, 5)
        if r1 == r2:
            r2 += 1
        
        den_expanded = expand((x - r1)*(x - r2))
        num = random.randint(1, 5) * x + random.randint(-5, 5)
        f = num / den_expanded
        latex_str = rf"\int \frac{{{latex(num)}}}{{{latex(den_expanded)}}} \,dx"
    
    F = integrate(f, x)
    
    return {
        "latex": latex_str,
        "answer": _fmt_answer(F),
        "params": {"type": "integral_partial_fractions"}
    }


def _level13():
    """Level 13: Integral 'Jebakan' Substitusi vs Parsial"""
    choice = random.random()
    
    if choice < 0.5:
        # Bentuk substitusi: x * f(x^2)
        k = random.randint(2, 10)
        b = random.randint(2, 10)
        
        if random.random() < 0.5:
            # x * sin(x^2)
            f = k * x * sin(b * x**2)
            latex_str = rf"\int {k}x \sin({b}x^2) \,dx"
        else:
            # x * e^(x^2)
            f = k * x * exp(b * x**2)
            latex_str = rf"\int {k}x e^{{{b}x^2}} \,dx"
    else:
        # Bentuk parsial: x * f(x)
        k = random.randint(2, 10)
        b = random.randint(2, 10)
        
        if random.random() < 0.5:
            # x * sin(x)
            f = k * x * sin(b * x)
            latex_str = rf"\int {k}x \sin({b}x) \,dx"
        else:
            # x * e^x
            f = k * x * exp(b * x)
            latex_str = rf"\int {k}x e^{{{b}x}} \,dx"
    
    F = integrate(f, x)
    
    return {
        "latex": latex_str,
        "answer": _fmt_answer(F),
        "params": {"type": "integral_trick_substitution_vs_parts"}
    }


def _level14():
    """Level 14: Integral Tentu dengan Trik"""
    choice = random.random()
    
    if choice < 0.4:
        # Integral fungsi ganjil dengan batas simetris -> hasilnya 0
        a_bound = random.randint(2, 5)
        b_bound = -a_bound
        
        # Fungsi ganjil: x^(odd), sin, tan
        func_type = random.choice(['x_odd', 'sin', 'tan'])
        
        if func_type == 'x_odd':
            n = random.choice([3, 5, 7, 9])
            f = x**n
        elif func_type == 'sin':
            f = sin(x)
        else:
            f = tan(x)
        
        F = integrate(f, (x, b_bound, a_bound))
        latex_str = rf"\int_{{{b_bound}}}^{{{a_bound}}} {latex(f)} \,dx"
        
    elif choice < 0.7:
        # Integral dengan batas e atau pi yang menyederhanakan
        k = random.randint(2, 10)
        
        if random.random() < 0.5:
            # ∫ k/x dx dari 1 ke e -> k*ln(e) - k*ln(1) = k
            f = k / x
            F = integrate(f, (x, 1, exp(1)))
            latex_str = rf"\int_{{1}}^{{e}} \frac{{{k}}}{{x}} \,dx"
        else:
            # ∫ k*cos(x) dx dari 0 ke pi/2 -> k*sin(pi/2) - k*sin(0) = k
            f = k * cos(x)
            F = integrate(f, (x, 0, pi/2))
            latex_str = rf"\int_{{0}}^{{\pi/2}} {k}\cos(x) \,dx"
    else:
        # Integral yang hasilnya bisa disederhanakan
        a = random.randint(2, 10)
        b = random.randint(1, 5)
        
        # ∫ e^x dx dari 0 ke 1
        f = a * exp(x)
        F = integrate(f, (x, 0, 1))
        latex_str = rf"\int_{{0}}^{{1}} {a}e^x \,dx"
    
    return {
        "latex": latex_str,
        "answer": _fmt_answer(F),
        "params": {"type": "integral_definite_trick"}
    }


def _level15():
    """Level 15: Integral 'Mustahil' yang Ternyata Mudah"""
    choice = random.random()
    
    if choice < 0.25:
        # ∫ x^5/(x^2+1) dx -> Bagi polinomial atau substitusi
        n = random.randint(3, 7)
        f = x**n / (x**2 + 1)
        F = integrate(f, x)
        latex_str = rf"\int \frac{{x^{{{n}}}}}{{x^2+1}} \,dx"
        
    elif choice < 0.5:
        # ∫ sin(x)cos(x) dx -> Bisa dengan substitusi atau identitas
        f = sin(x) * cos(x)
        F = integrate(f, x)
        latex_str = rf"\int \sin(x)\cos(x) \,dx"
        
    elif choice < 0.75:
        # ∫ (e^x + 1)^2 dx -> Jabarkan dulu
        k = random.randint(1, 5)
        f = (k * exp(x) + 1)**2
        F = integrate(expand(f), x)
        latex_str = rf"\int ({k}e^x + 1)^2 \,dx"
    else:
        # ∫ arctan(x)/(1+x^2) dx -> Substitusi sederhana
        f = atan(x) / (1 + x**2)
        F = integrate(f, x)
        latex_str = rf"\int \frac{{\arctan(x)}}{{1+x^2}} \,dx"
    
    return {
        "latex": latex_str,
        "answer": _fmt_answer(F),
        "params": {"type": "integral_seemingly_impossible"}
    }


LEVEL_MAP = {
    1: _level1,
    2: _level2,
    3: _level3,
    4: _level4,
    5: _level5,
    6: _level6,
    7: _level7,
    8: _level8,
    9: _level9,
    10: _level10,
    11: _level11,
    12: _level12,
    13: _level13,
    14: _level14,
    15: _level15,
}


def generate_integral_question(level: int):
    """Generator soal integral untuk 15 level."""
    level = max(1, min(15, int(level)))
    return LEVEL_MAP[level]()
