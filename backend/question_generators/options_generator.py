import random
from fractions import Fraction
from sympy import sympify, sqrt, Symbol, Rational, nsimplify, diff, sin, cos, tan, Mul, Add, Pow, simplify


def _generate_derivative_distractors(correct_answer_str, params):
    """
    Membuat distraktor berbasis ekspresi matematika yang mirip dengan jawaban benar.
    Untuk semua level turunan, menghasilkan opsi salah yang kompleks dan mengecoh.
    """
    x = Symbol('x')
    distractors = []
    
    try:
        # Parse jawaban benar sebagai ekspresi
        correct_expr = sympify(correct_answer_str)
    except Exception:
        return []
    
    problem_type = params.get('type', '')
    a = params.get('a')
    b = params.get('b')
    c = params.get('c')
    d = params.get('d')
    n = params.get('n')
    m = params.get('m')
    c0 = params.get('point')
    func_name = params.get('func', 'sin')
    
    # Helper: format ekspresi ke string yang konsisten
    def fmt_expr(expr):
        try:
            simp = simplify(expr)
            return str(simp)
        except Exception:
            return str(expr)
    
    # ============================================================
    # LEVEL 1: Power Rule Basic (a*x^n)
    # ============================================================
    if problem_type == 'derivative_power_basic' and a is not None and n is not None:
        # Lupa kali n
        distractors.append(fmt_expr(a * x**(n-1)))
        # Salah pangkat (pakai n+1)
        distractors.append(fmt_expr(a * (n+1) * x**n))
        # Lupa kurangi pangkat
        distractors.append(fmt_expr(a * x**n))
        # Salah koefisien (pakai a*n*2)
        distractors.append(fmt_expr(a * n * 2 * x**(n-1)))
    
    # ============================================================
    # LEVEL 2: Polynomial (a*x^n + b*x^m + c)
    # ============================================================
    elif problem_type == 'derivative_polynomial' and a is not None and b is not None and n is not None and m is not None:
        # Lupa turunkan suku kedua
        distractors.append(fmt_expr(a * n * x**(n-1)))
        # Lupa turunkan suku pertama
        distractors.append(fmt_expr(b * m * x**(m-1)))
        # Salah koefisien suku pertama
        distractors.append(fmt_expr(a * (n-1) * x**(n-1) + b * m * x**(m-1)))
        # Salah pangkat
        distractors.append(fmt_expr(a * n * x**n + b * m * x**m))
    
    # ============================================================
    # LEVEL 3: Negative Power / Sqrt
    # ============================================================
    elif 'negative_power' in problem_type and a is not None and n is not None:
        # Salah tanda
        distractors.append(fmt_expr(a * n * x**(-(n+1))))
        # Tidak kurangi pangkat
        distractors.append(fmt_expr(a * x**(-n)))
        # Salah koefisien
        distractors.append(fmt_expr(-a * (n+1) * x**(-(n+1))))
    
    elif 'sqrt' in problem_type and a is not None:
        # Lupa faktor 1/2
        distractors.append(fmt_expr(a * sqrt(x)))
        # Salah bentuk (pakai x^(-1) bukan x^(-1/2))
        distractors.append(fmt_expr(a * x**(-1)))
        # Salah koefisien
        distractors.append(fmt_expr(a * 2 / (2*sqrt(x))))
    
    # ============================================================
    # LEVEL 4-5: Product Rule
    # ============================================================
    elif problem_type in ('product_linear', 'product_quadratic') and a is not None and b is not None and c is not None and d is not None:
        # Hanya u'v (lupa u v')
        u_prime = a if problem_type == 'product_linear' else 2*a*x
        u_val = a*x + b if problem_type == 'product_linear' else a*x**2 + b
        v_val = c*x + d
        distractors.append(fmt_expr(u_prime * v_val))
        
        # Hanya u v' (lupa u'v)
        v_prime = c
        distractors.append(fmt_expr(u_val * v_prime))
        
        # Salah tanda pada salah satu suku
        distractors.append(fmt_expr(u_prime * v_val - u_val * v_prime))
    
    # ============================================================
    # LEVEL 6-7: Quotient Rule
    # ============================================================
    elif problem_type in ('quotient_linear', 'quotient_quadratic') and a is not None and b is not None and c is not None and d is not None:
        u_val = a*x + b if problem_type == 'quotient_linear' else a*x**2 + b
        v_val = c*x + d
        u_prime = a if problem_type == 'quotient_linear' else 2*a*x
        v_prime = c
        
        # Hanya u'/v (lupa -uv'/v^2)
        distractors.append(fmt_expr(u_prime / v_val))
        
        # Hanya -uv'/v^2 (lupa u'/v)
        distractors.append(fmt_expr(-u_val * v_prime / v_val**2))
        
        # Salah tanda (pakai + bukan -)
        distractors.append(fmt_expr((u_prime * v_val + u_val * v_prime) / v_val**2))
    
    # ============================================================
    # LEVEL 8: Chain Rule Power
    # ============================================================
    elif problem_type == 'chain_power' and a is not None and b is not None and n is not None:
        inner = a*x**2 + b
        # Lupa kali turunan dalam (2*a*x)
        distractors.append(fmt_expr(n * inner**(n-1)))
        # Lupa kali n
        distractors.append(fmt_expr(2*a*x * inner**(n-1)))
        # Salah pangkat (n+1)
        distractors.append(fmt_expr(n * (2*a*x) * inner**(n+1)))
    
    # ============================================================
    # LEVEL 9: Basic Trig
    # ============================================================
    elif problem_type == 'trig_basic' and a is not None and b is not None:
        # Salah tanda (misal d/dx cos = -sin, tapi pakai +sin)
        if func_name == 'cos':
            distractors.append(fmt_expr(a * b * sin(b*x)))  # seharusnya -a*b*sin
        elif func_name == 'sin':
            distractors.append(fmt_expr(-a * b * cos(b*x)))  # seharusnya a*b*cos
        # Lupa kali b (koefisien dalam)
        if func_name == 'sin':
            distractors.append(fmt_expr(a * cos(b*x)))  # lupa kali b
        elif func_name == 'cos':
            distractors.append(fmt_expr(-a * sin(b*x)))  # lupa kali b
        elif func_name == 'tan':
            distractors.append(fmt_expr(a / cos(b*x)**2))  # lupa kali b
    
    # ============================================================
    # LEVEL 10: Chain Rule with Trig
    # ============================================================
    elif problem_type == 'chain_trig' and a is not None and c is not None and d is not None:
        inner = c*x**2 + d
        # Lupa kali turunan dalam (2*c*x) - jawaban benar: a*2*c*x*cos(inner)
        distractors.append(fmt_expr(a * cos(inner)))
        # Salah fungsi trig (pakai sin bukan cos pada turunan luar)
        distractors.append(fmt_expr(a * 2*c*x * sin(inner)))
        # Lupa kali koefisien a
        distractors.append(fmt_expr(2*c*x * cos(inner)))
        # Lupa kali 2 dari turunan x^2
        distractors.append(fmt_expr(a * c*x * cos(inner)))
    
    # ============================================================
    # LEVEL 11: Product & Trig
    # ============================================================
    elif problem_type == 'product_trig' and a is not None and n is not None and b is not None:
        u_val = a * x**n
        v_val = sin(b*x)
        u_prime = a * n * x**(n-1)
        v_prime = b * cos(b*x)
        
        # Hanya u'v
        distractors.append(fmt_expr(u_prime * v_val))
        # Hanya u v'
        distractors.append(fmt_expr(u_val * v_prime))
        # Salah tanda pada v'
        distractors.append(fmt_expr(u_prime * v_val - u_val * v_prime))
    
    # ============================================================
    # LEVEL 12: Quotient & Trig
    # ============================================================
    elif problem_type == 'quotient_trig' and a is not None and c is not None and d is not None:
        u_val = sin(a*x)
        v_val = c*x + d
        u_prime = a * cos(a*x)
        v_prime = c
        
        # Hanya u'/v
        distractors.append(fmt_expr(u_prime / v_val))
        # Salah tanda
        distractors.append(fmt_expr((u_prime * v_val + u_val * v_prime) / v_val**2))
        # Lupa kali a (koefisien dalam sin)
        distractors.append(fmt_expr((cos(a*x) * v_val - u_val * v_prime) / v_val**2))
    
    # ============================================================
    # LEVEL 13: Second Derivative
    # ============================================================
    elif problem_type == 'second_derivative_poly' and a is not None and b is not None:
        c_val = params.get('c', 0)
        f = a*x**3 + b*x**2 + c_val*x
        fp = diff(f, x)
        # Kembalikan turunan pertama
        distractors.append(fmt_expr(fp))
        # Salah koefisien
        distractors.append(fmt_expr(6*a*x + 4*b))  # tanpa *x
        distractors.append(fmt_expr(3*a*x + 2*b))
    
    # ============================================================
    # LEVEL 14: Tangent Gradient (jawaban numerik)
    # ============================================================
    elif problem_type == 'tangent_gradient' and a is not None and b is not None and c0 is not None:
        f = a*x**3 + b*x**2 + x
        fp = diff(f, x)
        correct_val = fp.subs(x, c0)
        
        # Pakai f(c) bukan f'(c)
        f_at_c = f.subs(x, c0)
        try:
            distractors.append(str(simplify(f_at_c)))
        except Exception:
            distractors.append(str(f_at_c))
        
        # Pakai f'(0) bukan f'(c)
        fp_at_zero = fp.subs(x, 0)
        try:
            distractors.append(str(simplify(fp_at_zero)))
        except Exception:
            distractors.append(str(fp_at_zero))
        
        # Salah evaluasi (c+1 atau c-1)
        for offset in [1, -1, 2]:
            fp_at_wrong = fp.subs(x, c0 + offset)
            try:
                val = str(simplify(fp_at_wrong))
                if val != str(correct_val):
                    distractors.append(val)
                    break
            except Exception:
                pass
    
    # ============================================================
    # LEVEL 15: Stationary Points (tidak bisa dibuat distraktor ekspresi)
    # ============================================================
    elif problem_type == 'stationary_points':
        # Untuk stationary points, jawaban adalah nilai x, bukan ekspresi
        # Tetap kembalikan kosong, akan dihandle oleh logika umum
        pass
    
    # Filter distraktor yang sama dengan jawaban benar
    distractors = [d for d in distractors if d != correct_answer_str and d]
    
    return distractors[:5]  # Ambil maksimal 5 distraktor terbaik


def generate_options(correct_answer, params=None):
    """
    Membuat 3 pilihan jawaban salah yang berasal dari kesalahan umum dalam perhitungan.
    Semua jawaban dalam bentuk pecahan/bilangan bulat, tidak ada desimal.
    Digunakan bersama oleh semua generator soal.
    """
    options = set()

    try:
        correct_sympy = sympify(correct_answer)
        if '.' in str(correct_answer):
            correct_fraction = nsimplify(correct_sympy, rational=True)
            correct_answer = str(correct_fraction)
            correct_sympy = correct_fraction
        options.add(str(correct_answer))
        correct_value = float(correct_sympy)
    except Exception:
        options.add(str(correct_answer))
        correct_value = 0

    problem_type = params.get('type', '') if params else ''
    x = Symbol('x')

    def make_fraction(numerator, denominator):
        if denominator == 1:
            return str(int(numerator))
        if denominator == 0:
            return "tak terdefinisi"
        from math import gcd
        g = gcd(int(abs(numerator)), int(abs(denominator))) or 1
        num = int(numerator / g)
        den = int(denominator / g)
        if den < 0:
            num = -num
            den = -den
        if den == 1:
            return str(num)
        return f"{num}/{den}"

    def extract_fraction(value_str):
        try:
            if '/' in value_str:
                parts = value_str.split('/')
                return int(parts[0]), int(parts[1])
            val = float(sympify(value_str))
            frac = Fraction(val).limit_denominator(100)
            return frac.numerator, frac.denominator
        except Exception:
            return 1, 1

    correct_num, correct_den = extract_fraction(str(correct_answer))

    # Cek apakah ini soal turunan (di luar try agar tetap terdefinisi)
    is_derivative = problem_type.startswith('derivative') or 'product_' in problem_type or 'quotient_' in problem_type or 'trig_' in problem_type or problem_type in {
        'chain_power', 'chain_trig', 'product_trig', 'quotient_trig', 'second_derivative_poly', 'tangent_gradient', 'stationary_points'
    }

    try:
        if any(tag in problem_type for tag in ['substitusi', 'faktorisasi', 'rasionalisasi', 'trigonometri', 'tak_hingga', 'derivative', 'integral']):
            # Kesalahan umum: terbalik, salah tanda, 0/1/tak terdefinisi
            options.update(["0", "1", "tak terdefinisi"])  # aman, akan difilter nanti
            if correct_den != 0:
                options.add(make_fraction(correct_den, correct_num))
            options.add(make_fraction(-correct_num, correct_den))

        # Tambahan pengecoh berbasis nilai benar
        if len(options) < 8:
            options.add(make_fraction(correct_num * 2, correct_den))
            options.add(make_fraction(correct_num, correct_den * 2 if correct_den != 0 else 1))
            options.add(make_fraction(correct_num + correct_den, correct_den if correct_den != 0 else 1))
            options.add(make_fraction(correct_num - correct_den, correct_den if correct_den != 0 else 1))

        # ============================================================
        # Distraktor KHUSUS untuk TURUNAN (derivative_*)
        # ============================================================
        if is_derivative:
            # PRIORITAS: Gunakan distraktor berbasis ekspresi matematika kompleks
            derivative_distractors = _generate_derivative_distractors(str(correct_answer), params)
            for distractor in derivative_distractors:
                options.add(distractor)

        # ============================================================
        # Distraktor KHUSUS untuk INTEGRAL (integral_basic)
        # ============================================================
        if 'integral' in problem_type:
            # Power rule kebalik (n-1), lupa bagi dengan pangkat baru, salah tanda trig
            options.add('power_rule_terbalik')
            options.add('lupa_bagi_pangkat_baru')
            options.add('salah_tanda_trig_integral')

    except Exception:
        pass

    options.add(str(correct_answer))

    options = {opt for opt in options if opt and opt != str(correct_answer)
               and 'zoo' not in opt.lower() and 'oo' not in opt.lower()}

    # Untuk turunan dan integral, hindari bilangan sederhana
    # KECUALI untuk stationary_points dan tangent_gradient yang jawabannya adalah nilai numerik
    if (is_derivative or 'integral' in problem_type) and problem_type not in ('stationary_points', 'tangent_gradient'):
        # Prioritas distraktor ekspresi kompleks
        complex_options = []
        simple_options = []
        
        for opt in options:
            try:
                # Coba parse sebagai ekspresi
                expr = sympify(opt)
                # Jika berisi variabel x atau ekspresi kompleks, masukkan ke complex
                if 'x' in str(expr) or str(expr).count('*') > 0 or str(expr).count('+') > 0 or str(expr).count('(') > 0:
                    complex_options.append(opt)
                else:
                    simple_options.append(opt)
            except Exception:
                # Jika tidak bisa parse, anggap sebagai opsi sederhana
                simple_options.append(opt)
        
        # Prioritaskan distraktor kompleks
        if len(complex_options) >= 3:
            wrong_options = complex_options
        elif len(complex_options) > 0:
            # Tambahkan simple hanya jika perlu
            wrong_options = complex_options + simple_options[:3-len(complex_options)]
        else:
            wrong_options = simple_options
        
        selected_wrong = wrong_options[:3]
        
    else:
        # Untuk limit dan lainnya, gunakan logika lama
        simple_fractions = [
            "1/2", "1/3", "1/4", "1/5", "1/6", "1/8",
            "2/3", "3/4", "2/5", "3/5",
            "-1/2", "-1/3", "-1/4",
            "1", "2", "3", "0"
        ]

        while len(options) < 10:
            frac = random.choice(simple_fractions)
            if frac != str(correct_answer):
                options.add(frac)

        try:
            correct_value = float(sympify(correct_answer))
        except Exception:
            correct_value = 0

        def option_score(opt):
            try:
                val = float(sympify(opt))
                distance = abs(val - correct_value)
                return distance if '/' not in opt else distance + 0.5
            except Exception:
                return 1000

        wrong_options = list(options)
        wrong_options.sort(key=option_score)
        selected_wrong = wrong_options[:3]

    final_options = selected_wrong + [str(correct_answer)]
    random.shuffle(final_options)
    return final_options


