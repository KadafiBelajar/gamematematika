import random
from sympy import Symbol, limit, oo, latex, sqrt, sin, cos, tan, expand, S


# The following implementations are adapted from the previous monolithic file
# and grouped under a single dispatcher: generate_limit_question(level)


def _gen_substitusi(level):
    x = Symbol('x')
    point = random.randint(-5, 5)

    if level == 1:
        a = random.randint(1, 10) * random.choice([-1, 1])
        b = random.randint(-10, 10)
        f = a * x + b
        gen_type = 'substitusi_linear'
    elif level == 2:
        a = random.randint(1, 7) * random.choice([-1, 1])
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        f = a * x**2 + b * x + c
        gen_type = 'substitusi_kuadrat'
    else:
        while True:
            point = random.randint(-5, 5)
            den_a = random.randint(1, 7) * random.choice([-1, 1])
            den_b = random.randint(-10, 10)
            while den_a * point + den_b == 0:
                point = random.randint(-5, 5)
            num_a = random.randint(1, 10) * random.choice([-1, 1])
            num_b = random.randint(-10, 10)
            num = num_a * x + num_b
            den = den_a * x + den_b
            if not (num/den).is_constant(x):
                f = num / den
                break
        gen_type = 'substitusi_rasional'

    ans = limit(f, x, point)
    return {
        "latex": rf"\lim_{{x \to {point}}} \left({latex(f)}\right)",
        "answer": str(ans),
        "params": {"type": gen_type, "f_str": str(f), "point": point}
    }


def _gen_faktorisasi(level):
    x = Symbol('x')
    a = random.randint(2, 9) * random.choice([-1, 1])

    if level <= 4:
        num = x**2 - a**2
        den = x - a
        point = a
        gen_type = 'faktorisasi_sederhana'
    elif level == 5:
        b = random.randint(2, 9) * random.choice([-1, 1])
        while a == b or a == -b:
            b = random.randint(2, 9) * random.choice([-1, 1])
        num = expand((x - a) * (x - b))
        c = random.randint(2, 5)
        den = c*x - c*a
        point = a
        gen_type = 'faktorisasi_polinomial'
    else:
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
        d = random.randint(2, 7) * random.choice([-1, 1])
        while a == d:
            d = random.randint(2, 7) * random.choice([-1, 1])
        num = expand((x - a) * (x**2 + b*x + c))
        den = expand((x - a) * (x - d))
        point = a
        gen_type = 'faktorisasi_kubik'

    ans = limit(num / den, x, point)
    f_str_original = f"({num})/({den})"
    latex_original = f"\\frac{{{latex(num)}}}{{{latex(den)}}}"
    return {
        "latex": rf"\lim_{{x \to {point}}} \left({latex_original}\right)",
        "answer": str(ans),
        "params": {"type": gen_type, "f_str": f_str_original, "point": point}
    }


def _gen_rasionalisasi(level):
    x = Symbol('x')
    if level == 7:
        max_attempts = 30
        for _ in range(max_attempts):
            soal_type = random.choice(['sqrt_minus_const', 'const_minus_sqrt', 'sqrt_linear_den'])
            if soal_type == 'sqrt_minus_const':
                c = random.randint(2, 10)
                c_squared = c * c
                a = random.choice([1, 2, 3, 4, 5])
                point = random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
                b = c_squared - a * point
                d = random.randint(1, 5)
                den_expanded = d * (x - point)
                num = sqrt(a*x + b) - c
            elif soal_type == 'const_minus_sqrt':
                c = random.randint(2, 10)
                c_squared = c * c
                a = random.choice([1, 2, 3, 4, 5])
                point = random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
                b = c_squared - a * point
                d = random.randint(1, 5)
                den_expanded = d * (x - point)
                num = c - sqrt(a*x + b)
            else:
                c = random.randint(2, 8)
                c_squared = c * c
                a = random.choice([1, 2, 3, 4])
                point = random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])
                b = c_squared - a * point
                m = random.randint(1, 6)
                n = -m * point
                den_expanded = m*x + n
                num = sqrt(a*x + b) - c
            f = num / den_expanded
            num_at_point = num.subs(x, point)
            den_at_point = den_expanded.subs(x, point)
            if num_at_point == 0 and den_at_point == 0:
                ans = limit(f, x, point)
                if ans.is_Integer or ans.is_Rational:
                    if abs(ans) < 100:
                        gen_type = 'rasionalisasi_akar_sederhana'
                        f_str_original = f"({num})/({den_expanded})"
                        latex_original = f"\\frac{{{latex(num)}}}{{{latex(den_expanded)}}}"
                        return {
                            "latex": rf"\lim_{{x \to {point}}} \left({latex_original}\right)",
                            "answer": str(ans),
                            "params": {"type": gen_type, "f_str": f_str_original, "point": point}
                        }
        return _gen_rasionalisasi_fallback(level)
    elif level == 8:
        return _gen_rasionalisasi_level_8()
    else:
        return _gen_rasionalisasi_level_9()


def _gen_rasionalisasi_fallback(level):
    x = Symbol('x')
    combinations = [
        (1, 9, 3, 0),
        (1, 16, 4, 0),
        (2, 8, 4, 0),
        (1, 25, 5, 0),
        (3, 12, 6, 0),
        (1, 4, 2, -2),
        (1, 9, 3, -5),
        (2, 18, 6, 0),
    ]
    a, b, c, point = random.choice(combinations)
    num = sqrt(a*x + b) - c
    den = x - point if point != 0 else x
    f = num / den
    ans = limit(f, x, point)
    return {
        "latex": rf"\lim_{{x \to {point}}} \left(\\frac{{{latex(num)}}}{{{latex(den)}}}\right)",
        "answer": str(ans),
        "params": {"type": "rasionalisasi_akar_sederhana", "f_str": f"({num})/({den})", "point": point}
    }


def _gen_rasionalisasi_level_8():
    x = Symbol('x')
    import math
    while True:
        d = random.randint(2, 5) * random.choice([-1, 1])
        a_val = random.randint(1, 4)
        b_val = random.randint(1, 25)
        rad_val = a_val * d + b_val
        if rad_val > 0 and math.isqrt(rad_val)**2 == rad_val:
            c_val = math.isqrt(rad_val)
            if c_val != 0:
                break
    sqrt_expr = sqrt(a_val*x + b_val)
    scenario = random.choice(['complex_den', 'sqrt_in_den'])
    if scenario == 'complex_den':
        num = sqrt_expr - c_val
        den = x**2 - d**2
        point = d
    else:
        num = x**2 - d**2
        den = sqrt_expr - c_val
        point = d
    ans = limit(num / den, x, point)
    if ans.is_Integer or ans.is_Float or ans.is_Rational:
        f_str_original = f"({num})/({den})"
        latex_original = f"\\frac{{{latex(num)}}}{{{latex(den)}}}"
        return {
            "latex": rf"\lim_{{x \to {point}}} \left({latex_original}\right)",
            "answer": str(ans),
            "params": {"type": "rasionalisasi_akar_kompleks", "f_str": f_str_original, "point": point}
        }


def _gen_rasionalisasi_level_9():
    from sympy import sqrt
    x = Symbol('x')
    max_attempts = 50
    for _ in range(max_attempts):
        soal_type = random.choice(['beda_akar_linear', 'beda_akar_kuadrat', 'jumlah_akar', 'akar_kompleks'])
        point = random.choice([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6])
        if soal_type == 'beda_akar_linear':
            a = random.randint(1, 6)
            sqrt_val_1 = random.randint(2, 8)
            b = sqrt_val_1**2 - a * point
            c = random.randint(1, 6)
            while c == a:
                c = random.randint(1, 6)
            sqrt_val_2 = random.randint(2, 8)
            while sqrt_val_2 == sqrt_val_1:
                sqrt_val_2 = random.randint(2, 8)
            d = sqrt_val_2**2 - c * point
            if b <= 0 or d <= 0:
                continue
            m = random.randint(1, 5)
            n = -m * point
            num = sqrt(a*x + b) - sqrt(c*x + d)
            den = m*x + n
        elif soal_type == 'beda_akar_kuadrat':
            a = random.randint(1, 5)
            sqrt_val_1 = random.randint(2, 7)
            b = sqrt_val_1**2 - a * point
            c = random.randint(1, 5)
            while c == a:
                c = random.randint(1, 5)
            sqrt_val_2 = random.randint(2, 7)
            while sqrt_val_2 == sqrt_val_1:
                sqrt_val_2 = random.randint(2, 7)
            d = sqrt_val_2**2 - c * point
            if b <= 0 or d <= 0:
                continue
            other_root = random.choice([r for r in range(-5, 6) if r != point])
            den = expand((x - point) * (x - other_root))
            num = sqrt(a*x + b) - sqrt(c*x + d)
        elif soal_type == 'jumlah_akar':
            a = random.randint(1, 5)
            sqrt_val_1 = random.randint(2, 6)
            b = sqrt_val_1**2 - a * point
            c = random.randint(1, 5)
            sqrt_val_2 = random.randint(2, 6)
            d = sqrt_val_2**2 - c * point
            if b <= 0 or d <= 0:
                continue
            k = sqrt_val_1 + sqrt_val_2
            m = random.randint(1, 5)
            n = -m * point
            num = sqrt(a*x + b) + sqrt(c*x + d) - k
            den = m*x + n
        else:
            k1 = random.randint(2, 4)
            k2 = random.randint(2, 4)
            a = random.randint(1, 4)
            sqrt_val_1 = random.randint(2, 6)
            b = sqrt_val_1**2 - a * point
            c = random.randint(1, 4)
            sqrt_val_2 = random.randint(2, 6)
            d = sqrt_val_2**2 - c * point
            if b <= 0 or d <= 0:
                continue
            if k1 * sqrt_val_1 == k2 * sqrt_val_2:
                k2 += 1
            m = random.randint(1, 5)
            n = -m * point
            num = k1 * sqrt(a*x + b) - k2 * sqrt(c*x + d)
            den = m*x + n
        f = num / den
        try:
            num_at_point = num.subs(x, point)
            den_at_point = den.subs(x, point)
            if num_at_point == 0 and den_at_point == 0:
                ans = limit(f, x, point)
                if ans.is_Integer or ans.is_Rational:
                    if abs(ans) < 100 and ans != 0:
                        gen_type = 'rasionalisasi_beda_akar'
                        f_str_original = f"({num})/({den})"
                        latex_original = f"\\frac{{{latex(num)}}}{{{latex(den)}}}"
                        return {
                            "latex": rf"\lim_{{x \to {point}}} \left({latex_original}\right)",
                            "answer": str(ans),
                            "params": {"type": gen_type, "f_str": f_str_original, "point": point}
                        }
        except Exception:
            continue
    return _gen_rasionalisasi_level_9_fallback()


def _gen_rasionalisasi_level_9_fallback():
    x = Symbol('x')
    preset_combinations = [
        (1, 1, 2, 1, 1, 0, 0),
        (2, 2, 3, 2, 1, 0, 0),
        (1, 4, 2, 4, 1, 0, 0),
        (1, 9, 3, 9, 1, 0, 0),
        (2, 8, 1, 8, 1, 0, 0),
        (1, 5, 2, 2, 1, 1, -1),
        (1, 13, 2, 8, 1, 2, -2),
        (2, 10, 1, 8, 1, -1, 1),
        (1, 8, 3, 0, 2, 4, -2),
        (3, 3, 1, 9, 1, -2, 2),
        (4, 4, 1, 16, 1, 0, 0),
        (1, 16, 4, 4, 1, 0, 0),
        (2, 18, 1, 25, 1, 3, -3),
        (3, 12, 2, 18, 2, -6, 3),
        (1, 20, 5, 0, 1, 4, -4),
    ]
    a, b, c, d, m, n, point = random.choice(preset_combinations)
    num = sqrt(a*x + b) - sqrt(c*x + d)
    den = m*x + n
    f = num / den
    ans = limit(f, x, point)
    f_str_original = f"({num})/({den})"
    latex_original = f"\\frac{{{latex(num)}}}{{{latex(den)}}}"
    return {
        "latex": rf"\lim_{{x \to {point}}} \left({latex_original}\right)",
        "answer": str(ans),
        "params": {"type": "rasionalisasi_beda_akar", "f_str": f_str_original, "point": point}
    }


def _gen_trigonometri(level):
    x = Symbol('x')
    from sympy import pi, tan, sin, cos, sec, csc, cot
    try:
        if level == 12:
            pattern = random.choice(['one_minus_sec', 'csc_minus_cot', 'simple_camouflage', 'tan_plus_sin_over_sin3'])
            a = random.randint(2, 12); b = random.randint(2, 12); c = random.randint(2, 12)
            f = None
            use_zero_limit = random.random() < 0.2
            point = S.Zero if use_zero_limit else random.choice([S(1), S(-1), S(2), S(-2), S(3), S(-3), S(4), S(-4), pi, -pi, pi/2, -pi/2, pi/3, -pi/3, pi/4, -pi/4, S(2)*pi, S(-2)*pi])
            var = (x - point)
            if pattern == 'one_minus_sec':
                f = (1 - sec(a*var)) / (b*var**2)
            elif pattern == 'csc_minus_cot':
                f = (csc(a*var) - cot(a*var)) / (b*var)
            elif pattern == 'simple_camouflage':
                camouflage_func = random.choice([sec, cos])
                f = random.choice([sin, tan])(a*var) / (b*var * camouflage_func(c*var))
            elif pattern == 'tan_plus_sin_over_sin3':
                f = (tan(a*var) - sin(a*var)) / (b*sin(c*var)**3)
            if f is None: return _gen_trigonometri(level)
            ans = limit(f, x, point)
            if not ans.is_finite or not ans.is_Rational or ans == 0:
                return _gen_trigonometri(level)
            return {
                "latex": rf"\lim_{{x \to {latex(point)}}} \left({latex(f)}\right)",
                "answer": f"{ans.p}/{ans.q}" if ans.q != 1 else str(ans.p),
                "params": {"type": "trigonometri_expert", "f_str": str(f), "point": str(point)}
            }
        elif level == 11:
            pattern = random.choice(['one_minus_cos', 'cos_minus_cos'])
            a = random.randint(2, 12); b = random.randint(2, 12); c = random.randint(2, 12)
            while a == b: b = random.randint(2, 12)
            f = None
            use_zero_limit = random.random() < 0.3
            point = S.Zero if use_zero_limit else random.choice([S(1), S(-1), S(2), -pi, pi/2, -pi/2, pi/3])
            var = (x - point)
            if pattern == 'one_minus_cos':
                den_type = random.choice(['x_squared', 'sin_squared', 'tan_squared'])
                if den_type == 'x_squared': f = (1 - cos(a*var)) / (b*var**2)
                elif den_type == 'sin_squared': f = (1 - cos(a*var)) / (b*sin(c*var)**2)
                else: f = (1 - cos(a*var)) / (b*tan(c*var)**2)
            elif pattern == 'cos_minus_cos':
                f = (cos(a*var) - cos(b*var)) / (c*var**2)
            if f is None: return _gen_trigonometri(level)
            ans = limit(f, x, point)
            if not ans.is_finite or not ans.is_Rational: return _gen_trigonometri(level)
            return {
                "latex": rf"\lim_{{x \to {latex(point)}}} \left({latex(f)}\right)",
                "answer": f"{ans.p}/{ans.q}" if ans.q != 1 else str(ans.p),
                "params": {"type": "trigonometri_lanjutan", "f_str": str(f), "point": str(point)}
            }
        else:
            a = random.randint(1, 15)
            b = random.randint(1, 15)
            while a == b:
                b = random.randint(1, 15)
            f = None
            use_zero_limit = random.random() < 0.2
            from sympy import pi
            point = S.Zero if use_zero_limit else random.choice([S(1), S(-1), S(2), S(-2), S(3), S(-3), S(4), S(-4), S(5), S(-5), S(10), pi, -pi, pi/2, -pi/2, pi/3, -pi/3, S(2)*pi])
            var = (x - point)
            pattern = random.choice(['func_over_x', 'x_over_func', 'func_over_func'])
            func1 = random.choice([sin, tan])
            func2 = random.choice([sin, tan])
            if pattern == 'func_over_x':
                f = func1(a * var) / (b * var)
            elif pattern == 'x_over_func':
                f = (a * var) / func1(b * var)
            else:
                f = func1(a * var) / func2(b * var)
            params = {'a': a, 'b': b, "type": "trigonometri", "f_str": str(f), "point": str(point)}
            if f is None: return _gen_trigonometri(level)
            ans = limit(f, x, point)
            if not ans.is_finite or not ans.is_Rational:
                return _gen_trigonometri(level)
            return {
                "latex": rf"\lim_{{x \to {latex(point)}}} \left({latex(f)}\right)",
                "answer": f"{ans.p}/{ans.q}" if ans.q != 1 else str(ans.p),
                "params": params
            }
    except Exception:
        return _gen_trigonometri(level)


def _gen_tak_hingga(level):
    x = Symbol('x')
    deg = 1 if level <= 13 else (2 if level == 14 else 3)
    num_coeffs = [random.randint(1, 10) for _ in range(deg + 1)]
    den_coeffs = [random.randint(1, 10) for _ in range(deg + 1)]
    num = sum(c * x**i for i, c in enumerate(reversed(num_coeffs)))
    den = sum(c * x**i for i, c in enumerate(reversed(den_coeffs)))
    f = num / den
    ans = limit(f, x, oo)
    return {
        "latex": rf"\lim_{{x \to \infty}} \left({latex(f)}\right)",
        "answer": str(ans),
        "params": {"type": "tak_hingga", "f_str": str(f), "point": 'oo'}
    }


GENERATOR_MAP = {
    'substitusi': (_gen_substitusi, range(1, 4)),
    'faktorisasi': (_gen_faktorisasi, range(4, 7)),
    'rasionalisasi': (_gen_rasionalisasi, range(7, 10)),
    'trigonometri': (_gen_trigonometri, range(10, 13)),
    'tak_hingga': (_gen_tak_hingga, range(13, 16)),
}


def generate_limit_question(level):
    possible_generators = [gen for name, (gen, rng) in GENERATOR_MAP.items() if level in rng]
    generator = random.choice(possible_generators) if possible_generators else _gen_tak_hingga
    return generator(level)


