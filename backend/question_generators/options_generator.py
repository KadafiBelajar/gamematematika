import random
from fractions import Fraction
from sympy import sympify, sqrt, Symbol, Rational, nsimplify, diff, sin, cos, tan, sec, exp, log, asin, atan, Mul, Add, Pow, simplify, integrate, expand


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
    # LEVEL 13: Second Derivative (ekspresi kompleks yang sangat mirip)
    # ============================================================
    elif problem_type == 'second_derivative_poly' and a is not None and b is not None:
        c_val = params.get('c', 0)
        f = a*x**3 + b*x**2 + c_val*x
        
        # Jawaban benar: 6*a*x + 2*b
        fp = diff(f, x)
        fpp_correct = diff(fp, x)  # 6*a*x + 2*b
        
        # Distraktor 1: Turunan pertama (salah konsep - hanya turun sekali)
        distractors.append(fmt_expr(fp))
        
        # Distraktor 2: Salah koefisien pada suku pertama (6*a menjadi 3*a atau 12*a)
        distractors.append(fmt_expr(3*a*x + 2*b))  # lupa kali 2
        distractors.append(fmt_expr(12*a*x + 2*b))  # kali 2 kali lagi
        
        # Distraktor 3: Salah koefisien pada suku kedua (2*b menjadi b atau 4*b)
        distractors.append(fmt_expr(6*a*x + b))  # lupa kali 2
        distractors.append(fmt_expr(6*a*x + 4*b))  # kali 2 kali lagi
        
        # Distraktor 4: Salah evaluasi - pakai f'(x) yang masih punya x^2
        # Ambil suku linier dari fp sebagai distraktor (salah interpretasi)
        fp_linear_only = 2*b*x  # hanya ambil suku linier dari turunan pertama
        distractors.append(fmt_expr(fp_linear_only))
        
        # Distraktor 5: Salah urutan - turunkan dari bentuk yang sudah disederhanakan dengan salah
        # Misal: anggap f(x) = x^2*(ax+b), turunkan dengan cara salah
        if c_val == 0:  # jika c=0, bisa buat distraktor alternatif
            distractors.append(fmt_expr(3*a*x + b))  # salah bentuk
        
        # Distraktor 6: Offset kecil pada koefisien
        distractors.append(fmt_expr(6*a*x + 2*b + 1))  # tambah konstanta kecil
        distractors.append(fmt_expr(6*a*x + 2*b - 1))  # kurang konstanta kecil
        distractors.append(fmt_expr((6*a + 1)*x + 2*b))  # offset koefisien x
        distractors.append(fmt_expr(6*a*x + (2*b + 1)))  # offset konstanta
        
        # Distraktor 7: Salah tanda pada salah satu suku
        distractors.append(fmt_expr(-6*a*x + 2*b))  # salah tanda suku pertama
        distractors.append(fmt_expr(6*a*x - 2*b))  # salah tanda suku kedua
    
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
    # LEVEL 15: Stationary Points (bangun distraktor numerik yang sangat mirip)
    # ============================================================
    elif problem_type == 'stationary_points':
        # Semua opsi dalam format pasangan (x, f(x)) agar 99% mirip
        try:
            a = params.get('a'); b = params.get('b'); c = params.get('c')
            f_str = params.get('f_str')
            x = Symbol('x')
            f = sympify(f_str) if f_str else a*x**3 + b*x**2 + c

            # Turunan benar dan akarnya
            from sympy import solve, S
            roots_true = []
            try:
                roots_true = solve(3*a*x**2 + 2*b*x, x)
            except Exception:
                pass

            def fmt_pair(rx):
                try:
                    ry = simplify(f.subs(x, rx))
                except Exception:
                    ry = f.subs(x, rx)
                return f"({simplify(rx)}, {ry})"

            # Distraktor berbasis kesalahan umum pada f'(x)
            cand_x = []
            # Lupa faktor 3 → ax^2 + 2bx = 0
            try:
                cand_x += solve(a*x**2 + 2*b*x, x)
            except Exception:
                pass
            # Lupa faktor 2 pada bx → 3ax^2 + b x = 0
            try:
                cand_x += solve(3*a*x**2 + b*x, x)
            except Exception:
                pass
            # Tambahkan offset kecil terhadap akar benar jika ada
            for r in roots_true[:2]:
                for off_num, off_den in [(1,6), (-1,6), (1,12)]:
                    cand_x.append(simplify(r + S(off_num)/off_den))

            # Bangun pasangan (x, f(x)) dari kandidat
            for rx in cand_x:
                distractors.append(fmt_pair(rx))
        except Exception:
            pass
    
    # Filter distraktor yang sama dengan jawaban benar
    distractors = [d for d in distractors if d != correct_answer_str and d]
    
    return distractors[:5]  # Ambil maksimal 5 distraktor terbaik


def _generate_integral_distractors(correct_answer_str, params):
    """
    Membuat distraktor berbasis ekspresi matematika yang mirip dengan jawaban benar.
    Untuk semua level integral, menghasilkan opsi salah yang kompleks dan mengecoh.
    """
    x = Symbol('x')
    distractors = []
    
    try:
        # Parse jawaban benar sebagai ekspresi
        correct_expr = sympify(correct_answer_str)
    except Exception:
        return []
    
    problem_type = params.get('type', '')
    
    # Helper: format ekspresi ke string yang konsisten
    def fmt_expr(expr):
        try:
            simp = simplify(expr)
            # Hapus konstanta jika ada
            if isinstance(simp, Add):
                const = 0
                other_terms = []
                for term in simp.args:
                    if term.is_constant(x):
                        const += term
                    else:
                        other_terms.append(term)
                if other_terms:
                    result = Add(*other_terms)
                    # Coba convert ke bentuk pecahan yang rapi
                    try:
                        # Gunakan nsimplify untuk mendapatkan pecahan
                        result = nsimplify(result, rational=True)
                        # Format ulang dengan pecahan
                        return str(simplify(result))
                    except:
                        return str(simplify(result))
            # Coba convert ke pecahan
            try:
                simp = nsimplify(simp, rational=True)
                return str(simplify(simp))
            except:
                return str(simp)
        except Exception:
            return str(expr)
    
    # ============================================================
    # LEVEL 1: Power Rule Basic
    # ============================================================
    if problem_type == 'integral_power_basic':
        k = params.get('k', 1)
        c = params.get('c', 1)
        n = params.get('n', 1)
        
        # Jawaban benar: (k*c)/(n+1) * x^(n+1)
        # Distraktor 1: Lupa kalikan k dan c (hanya pakai k)
        distractors.append(fmt_expr((k / (n+1)) * x**(n+1)))
        # Distraktor 2: Lupa bagi (n+1) - langsung kali n
        distractors.append(fmt_expr(k * c * n * x**(n+1)))
        # Distraktor 3: Salah pangkat (n bukan n+1)
        distractors.append(fmt_expr((k*c / (n+1)) * x**n))
        # Distraktor 4: Bagi dengan n bukan n+1
        distractors.append(fmt_expr((k*c / n) * x**(n+1)))
    
    # ============================================================
    # LEVEL 2: Polynomial Sum
    # ============================================================
    elif problem_type == 'integral_polynomial_sum':
        coeffs = params.get('coeffs', [])
        powers = params.get('powers', [])
        
        if coeffs and powers:
            # Distraktor: lupa naikkan pangkat salah satu suku
            distractor_terms = []
            for i, (coeff, power) in enumerate(zip(coeffs, powers)):
                if i == 0 and power > 0:
                    # Lupa naikkan pangkat suku pertama
                    distractor_terms.append((coeff / (power + 1)) * x**power)  # salah
                else:
                    distractor_terms.append((coeff / (power + 1)) * x**(power + 1))
            distractors.append(fmt_expr(Add(*distractor_terms)))
            
            # Distraktor: salah koefisien pada salah satu suku
            distractor_terms2 = []
            for i, (coeff, power) in enumerate(zip(coeffs, powers)):
                if i == 0:
                    distractor_terms2.append((coeff / power) * x**(power + 1))  # bagi dengan power bukan power+1
                else:
                    distractor_terms2.append((coeff / (power + 1)) * x**(power + 1))
            distractors.append(fmt_expr(Add(*distractor_terms2)))
    
    # ============================================================
    # LEVEL 3: Root & Fraction (ekspresi kompleks yang sangat mirip)
    # ============================================================
    elif problem_type == 'integral_root_fraction':
        # Distraktor: salah koefisien setelah konversi atau salah pangkat
        try:
            # Ambil struktur dari jawaban benar
            if isinstance(correct_expr, Add):
                terms = correct_expr.args
                
                # Ambil suku pertama dan kedua jika ada
                if len(terms) >= 2:
                    term1 = terms[0]
                    term2 = terms[1]
                    
                    # Distraktor 1: Salah koefisien pada suku pertama (kali 2 atau bagi 2)
                    if isinstance(term1, Mul):
                        coeff1 = term1.args[0] if term1.args else 1
                        rest1 = Mul(*term1.args[1:]) if len(term1.args) > 1 else term1
                        distractors.append(fmt_expr(2 * coeff1 * rest1 + term2))  # kali 2
                        distractors.append(fmt_expr(coeff1 / 2 * rest1 + term2))  # bagi 2
                    
                    # Distraktor 2: Salah pangkat pada suku pertama
                    # Coba ganti pangkat dengan yang salah (misal +1 atau -1)
                    try:
                        # Ambil pangkat dari suku pertama
                        if isinstance(term1, Mul):
                            for arg in term1.args:
                                if isinstance(arg, Pow):
                                    old_pow = arg.args[1]
                                    wrong_pow1 = old_pow + Rational(1, 2) if hasattr(old_pow, '__add__') else old_pow + 1
                                    wrong_pow2 = old_pow - Rational(1, 2) if hasattr(old_pow, '__sub__') else old_pow - 1
                                    # Buat variasi dengan pangkat salah
                                    new_arg1 = Pow(arg.args[0], wrong_pow1)
                                    new_arg2 = Pow(arg.args[0], wrong_pow2)
                                    new_term1 = Mul(coeff1, new_arg1) if isinstance(term1, Mul) and term1.args else term1
                                    distractors.append(fmt_expr(new_term1 + term2))
                                    break
                    except:
                        pass
                elif len(terms) == 1:
                    # Hanya satu suku
                    term = terms[0]
                    if isinstance(term, Mul):
                        coeff = term.args[0] if term.args else 1
                        rest = Mul(*term.args[1:]) if len(term.args) > 1 else term
                        distractors.append(fmt_expr(2 * coeff * rest))  # kali 2
                        distractors.append(fmt_expr(coeff / 2 * rest))  # bagi 2
        except Exception:
            pass
    
    # ============================================================
    # LEVEL 4: Expand First (ekspresi kompleks yang sangat mirip)
    # ============================================================
    elif problem_type == 'integral_expand_first':
        try:
            form = params.get('form', 'product')
            
            if form == 'product':
                # Bentuk: (ax^n + b)(cx^m + d)
                a = params.get('a', 1)
                b = params.get('b', 1)
                c = params.get('c', 1)
                d = params.get('d', 1)
                n = params.get('n', 1)
                m = params.get('m', 1)
                
                # Ekspansi benar: ac*x^(n+m) + ad*x^n + bc*x^m + bd
                # Integral benar: ac/(n+m+1)*x^(n+m+1) + ad/(n+1)*x^(n+1) + bc/(m+1)*x^(m+1) + bd*x
                
                # Distraktor 1: Salah koefisien pada suku pertama (ac menjadi a atau ac*2)
                distractors.append(fmt_expr((a / (n+m+1)) * x**(n+m+1) + (a*d / (n+1)) * x**(n+1) + (b*c / (m+1)) * x**(m+1) + b*d * x))
                distractors.append(fmt_expr((2*a*c / (n+m+1)) * x**(n+m+1) + (a*d / (n+1)) * x**(n+1) + (b*c / (m+1)) * x**(m+1) + b*d * x))
                
                # Distraktor 2: Salah pangkat pada salah satu suku
                distractors.append(fmt_expr((a*c / (n+m+1)) * x**(n+m) + (a*d / (n+1)) * x**(n+1) + (b*c / (m+1)) * x**(m+1) + b*d * x))  # pangkat n+m bukan n+m+1
                distractors.append(fmt_expr((a*c / (n+m+1)) * x**(n+m+1) + (a*d / (n+1)) * x**n + (b*c / (m+1)) * x**(m+1) + b*d * x))  # pangkat n bukan n+1
                
                # Distraktor 3: Bagi dengan salah satu koefisien (lupa bagi dengan pangkat+1 pada salah satu suku)
                distractors.append(fmt_expr((a*c / (n+m)) * x**(n+m+1) + (a*d / (n+1)) * x**(n+1) + (b*c / (m+1)) * x**(m+1) + b*d * x))  # bagi n+m bukan n+m+1
                
            elif form == 'multiply':
                # Bentuk: x^n(ax^m + bx + c)
                n = params.get('n', 1)
                a = params.get('a', 1)
                b = params.get('b', 1)
                c = params.get('c', 1)
                m = params.get('m', 1)
                
                # Integral benar: a/(n+m+1)*x^(n+m+1) + b/(n+2)*x^(n+2) + c/(n+1)*x^(n+1)
                
                # Distraktor: salah koefisien atau pangkat
                distractors.append(fmt_expr((a / (n+m)) * x**(n+m+1) + (b / (n+2)) * x**(n+2) + (c / (n+1)) * x**(n+1)))  # bagi n+m bukan n+m+1
                distractors.append(fmt_expr((2*a / (n+m+1)) * x**(n+m+1) + (b / (n+2)) * x**(n+2) + (c / (n+1)) * x**(n+1)))  # kali 2
                distractors.append(fmt_expr((a / (n+m+1)) * x**(n+m) + (b / (n+2)) * x**(n+2) + (c / (n+1)) * x**(n+1)))  # pangkat n+m bukan n+m+1
                
            elif form == 'divide':
                # Bentuk: (ax^n + bx^m)/(cx^p)
                a = params.get('a', 1)
                b = params.get('b', 1)
                c = params.get('c', 1)
                n = params.get('n', 1)
                m = params.get('m', 1)
                p = params.get('p', 1)
                
                # Setelah dibagi: (a/c)*x^(n-p) + (b/c)*x^(m-p)
                # Integral benar: (a/c)/(n-p+1)*x^(n-p+1) + (b/c)/(m-p+1)*x^(m-p+1)
                
                # Distraktor: salah koefisien atau pangkat
                distractors.append(fmt_expr((a/c) / (n-p) * x**(n-p+1) + (b/c) / (m-p+1) * x**(m-p+1)))  # bagi n-p bukan n-p+1
                distractors.append(fmt_expr((2*a/c) / (n-p+1) * x**(n-p+1) + (b/c) / (m-p+1) * x**(m-p+1)))  # kali 2
                distractors.append(fmt_expr((a/c) / (n-p+1) * x**(n-p) + (b/c) / (m-p+1) * x**(m-p+1)))  # pangkat n-p bukan n-p+1
                
        except Exception as e:
            pass
    
    # ============================================================
    # LEVEL 5: Trig Basic
    # ============================================================
    elif problem_type == 'integral_trig_basic':
        a = params.get('a', 1)
        b = params.get('b', 1)
        c = params.get('c', 0)
        
        # Distraktor: salah tanda pada sin/cos
        # ∫ sin(x) = -cos(x), tapi pemain mungkin pakai +cos(x)
        distractors.append(fmt_expr(a * cos(x)))  # seharusnya -a*cos untuk sin
        distractors.append(fmt_expr(-b * sin(x)))  # seharusnya b*sin untuk cos
        
        # Distraktor: lupa koefisien
        if c != 0:
            distractors.append(fmt_expr(-a * cos(x) + b * sin(x)))  # lupa sec^2
    
    # ============================================================
    # LEVEL 6: Definite Basic
    # ============================================================
    elif problem_type == 'integral_definite_basic':
        k = params.get('k', 1)
        n = params.get('n', 1)
        a = params.get('a', 0)
        b = params.get('b', 1)
        
        # Distraktor: salah evaluasi batas
        # Pakai a^2 bukan (b^n - a^n)
        wrong1 = k * b**n  # hanya evaluasi di b
        distractors.append(fmt_expr(wrong1))
        wrong2 = k * a**n  # hanya evaluasi di a
        distractors.append(fmt_expr(wrong2))
        # Lupa kurangi
        wrong3 = k / (n+1) * b**(n+1)  # hanya F(b)
        distractors.append(fmt_expr(wrong3))
    
    # ============================================================
    # LEVEL 7: Substitution Basic
    # ============================================================
    elif problem_type == 'integral_substitution_basic':
        k = params.get('k', 1)
        a = params.get('a', 1)
        b = params.get('b', 0)
        n = params.get('n', 1)
        
        # Distraktor: lupa bagi dengan a (faktor dari du)
        inner = a*x + b
        distractors.append(fmt_expr((k / (n+1)) * inner**(n+1)))  # lupa /a
        
        # Distraktor: salah pangkat
        distractors.append(fmt_expr((k / (a*(n+1))) * inner**n))  # pangkat n bukan n+1
    
    # ============================================================
    # LEVEL 9: Trig Identity
    # ============================================================
    elif problem_type == 'integral_trig_identity':
        a = params.get('a', 1)
        func_choice = params.get('func', 'sin2')
        
        # Jawaban benar sudah menggunakan identitas, misal: x/2 - sin(2x)/4
        # Distraktor: salah tanda atau lupa bagi 2
        try:
            if isinstance(correct_expr, Add):
                terms = correct_expr.args
                if len(terms) >= 2:
                    # Ganti tanda suku kedua
                    distractors.append(fmt_expr(terms[0] + terms[1]))
                if len(terms) >= 2 and isinstance(terms[0], Mul):
                    # Lupa bagi 2 pada suku pertama
                    coeff = terms[0].args[0] if len(terms[0].args) > 0 else 1
                    rest = Mul(*terms[0].args[1:]) if len(terms[0].args) > 1 else 1
                    distractors.append(fmt_expr(2*coeff*rest + terms[1]))
        except Exception:
            pass
    
    # ============================================================
    # LEVEL 8-15: Advanced Techniques
    # ============================================================
    elif problem_type in ('integral_substitution_advanced', 'integral_by_parts', 
                          'integral_trig_substitution',
                          'integral_partial_fractions', 'integral_trick_substitution_vs_parts',
                          'integral_definite_trick', 'integral_seemingly_impossible'):
        # Untuk teknik lanjutan, buat distraktor dengan kesalahan umum:
        # 1. Salah teknik (pakai teknik yang salah)
        # 2. Lupa faktor konstan
        # 3. Salah tanda
        
        try:
            # Coba parse jawaban dan buat variasi
            if 'x' in str(correct_expr):
                # Tambahkan/mengurangi konstanta kecil
                if isinstance(correct_expr, Add):
                    # Tambah konstanta ke salah satu suku
                    first_term = correct_expr.args[0] if correct_expr.args else correct_expr
                    distractors.append(fmt_expr(first_term + 1))
                    distractors.append(fmt_expr(first_term - 1))
                # Ganti tanda pada salah satu bagian
                if '*' in str(correct_expr) or '/' in str(correct_expr):
                    # Ganti salah satu koefisien
                    try:
                        wrong = correct_expr.subs(x, 2*x)  # Ganti x dengan 2x (salah)
                        distractors.append(fmt_expr(wrong))
                    except:
                        pass
        except:
            pass
    
    # Filter distraktor yang sama dengan jawaban benar
    distractors = [d for d in distractors if d != correct_answer_str and d and 'lupa' not in str(d) and 'salah' not in str(d)]
    
    return distractors[:5]


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

    # Cek apakah ini soal turunan atau integral (di luar try agar tetap terdefinisi)
    is_derivative = problem_type.startswith('derivative') or 'product_' in problem_type or 'quotient_' in problem_type or 'trig_' in problem_type or problem_type in {
        'chain_power', 'chain_trig', 'product_trig', 'quotient_trig', 'second_derivative_poly', 'tangent_gradient', 'stationary_points'
    }
    is_integral = problem_type.startswith('integral') or 'integral' in problem_type

    try:
        if any(tag in problem_type for tag in ['substitusi', 'faktorisasi', 'rasionalisasi', 'trigonometri', 'tak_hingga', 'derivative', 'integral']):
            # Kesalahan umum: terbalik, salah tanda, 0/1/tak terdefinisi
            # SKIP untuk second_derivative_poly dan semua integral karena harus pakai ekspresi kompleks
            if problem_type != 'second_derivative_poly' and not is_integral:
                options.update(["0", "1", "tak terdefinisi"])  # aman, akan difilter nanti
            # Untuk integral, jangan tambahkan pecahan sederhana
            if not is_integral and correct_den != 0:
                options.add(make_fraction(correct_den, correct_num))
            if not is_integral:
                options.add(make_fraction(-correct_num, correct_den))

        # Tambahan pengecoh berbasis nilai benar (skip untuk stationary_points, second_derivative_poly, dan semua integral)
        if problem_type not in ('stationary_points', 'second_derivative_poly') and not is_integral and len(options) < 8:
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
        # Distraktor KHUSUS untuk INTEGRAL
        # ============================================================
        if 'integral' in problem_type:
            # Panggil fungsi khusus untuk integral
            integral_distractors = _generate_integral_distractors(str(correct_answer), params)
            for distractor in integral_distractors:
                options.add(distractor)

    except Exception:
        pass

    options.add(str(correct_answer))

    # Filter opsi: hapus kosong, identik dengan jawaban benar, zoo/oo, dan untuk integral/turunan hapus bilangan sederhana
    filtered_options = []
    simple_numbers = {'0', '1', '-1', '2', '-2', '1/2', '-1/2', '1/3', '-1/3', 'tak terdefinisi'}
    
    for opt in options:
        if not opt or opt == str(correct_answer):
            continue
        if 'zoo' in opt.lower() or 'oo' in opt.lower():
            continue
        
        # Untuk integral dan turunan (kecuali stationary_points, tangent_gradient), filter bilangan sederhana
        if (is_integral or is_derivative) and problem_type not in ('stationary_points', 'tangent_gradient'):
            if opt.strip() in simple_numbers or opt.strip() in {'0', '1', '-1', '2', '-2'}:
                continue  # Skip bilangan sederhana untuk integral/turunan
        
        filtered_options.append(opt)
    
    options = set(filtered_options)

    # Khusus level 15: paksa semua opsi menjadi pasangan (x, f(x))
    if problem_type == 'stationary_points':
        f_str = params.get('f_str')
        x = Symbol('x')
        try:
            f_expr = sympify(f_str)
        except Exception:
            f_expr = None

        def is_pair(s):
            return isinstance(s, str) and s.strip().startswith('(') and ',' in s and s.strip().endswith(')')

        pair_options = [opt for opt in options if is_pair(opt)]

        # Jika kurang dari 3, sintetis pasangan dari jawaban benar dengan offset kecil
        if len(pair_options) < 3 and f_expr is not None:
            try:
                # Ambil x dari jawaban benar
                raw = str(correct_answer).strip()[1:-1]
                x_part = raw.split(',')[0]
                x_true = sympify(x_part)
                for num, den in [(1, 12), (-1, 12), (1, 6), (-1, 6), (1, 8)]:
                    x_alt = x_true + Rational(num, den)
                    y_alt = f_expr.subs(x, x_alt)
                    pair_options.append(f"({simplify(x_alt)}, {simplify(y_alt)})")
                    if len(pair_options) >= 4:
                        break
            except Exception:
                pass

        # Ambil maksimal 3 distraktor pasangan
        selected_wrong = pair_options[:3]
        final_options = selected_wrong + [str(correct_answer)]
        random.shuffle(final_options)
        return final_options

    # Untuk turunan dan integral, hindari bilangan sederhana
    # KECUALI untuk stationary_points dan tangent_gradient yang jawabannya adalah nilai numerik
    # Level 13 (second_derivative_poly) harus selalu pakai ekspresi kompleks
    # SEMUA level integral harus pakai ekspresi kompleks
    if (is_derivative or is_integral) and problem_type not in ('stationary_points', 'tangent_gradient'):
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
    
    # Fallback: Jika selected_wrong kosong atau kurang dari 3, buat distraktor sederhana
    if len(selected_wrong) < 3:
        x = Symbol('x')
        simple_fallbacks = [
            "1/2", "1/3", "1/4", "1/5", "1/6", "1/8",
            "2/3", "3/4", "2/5", "3/5",
            "-1/2", "-1/3", "-1/4",
            "1", "2", "3", "0"
        ]
        
        for fallback in simple_fallbacks:
            if fallback != str(correct_answer) and fallback not in selected_wrong:
                selected_wrong.append(fallback)
            if len(selected_wrong) >= 3:
                break
    
    # Jika masih kurang, buat dari ekspresi x
    if len(selected_wrong) < 3 and 'x' in str(correct_answer):
        x_variations = [f"{x}", f"2*{x}", f"x^2", f"x/2", f"x+1", f"x-1"]
        for var in x_variations:
            if var != str(correct_answer) and var not in selected_wrong:
                selected_wrong.append(var)
            if len(selected_wrong) >= 3:
                break

    final_options = selected_wrong + [str(correct_answer)]
    random.shuffle(final_options)
    return final_options


