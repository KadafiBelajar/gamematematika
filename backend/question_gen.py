import random
import uuid
import math
from sympy import sympify, limit, oo, Symbol, latex, sqrt, sin, cos, tan, expand

# --- Helper Functions ---

def _generate_options(correct_answer):
    """
    Membuat 3 pilihan jawaban salah yang masuk akal di sekitar jawaban benar.
    """
    options = {str(correct_answer)}
    
    try:
        correct_float = float(sympify(correct_answer))
        candidates = {
            str(int(-correct_float)),
            str(int(correct_float + random.randint(1, 5))),
            str(int(correct_float - random.randint(1, 5))),
            "0", "1", "tak terdefinisi"
        }
        candidates.discard(str(correct_answer))
        for cand in candidates:
            if len(options) < 4:
                options.add(cand)
    except (ValueError, TypeError):
        pass

    while len(options) < 4:
        try:
            offset = random.randint(1, 5) * random.choice([-1, 1])
            base_num = int(sympify(correct_answer))
            options.add(str(base_num + offset))
        except (ValueError, TypeError):
            # Fallback jika jawaban bukan angka
            options.add(str(random.randint(-10, 10)))

    options.discard(str(correct_answer))
    final_options = list(options)[:3] + [str(correct_answer)]
    random.shuffle(final_options)
    return final_options

# --- Dynamic Question Generators (dengan variasi angka yang ditingkatkan) ---

def _gen_substitusi(level):
    x = Symbol('x')
    point = random.randint(-5, 5) # Rentang titik limit diperluas
    
    if level == 1: # Linear
        a = random.randint(1, 10) * random.choice([-1, 1]) # Koefisien a lebih bervariasi
        b = random.randint(-10, 10) # Konstanta b lebih bervariasi
        f = a * x + b
        gen_type = 'substitusi_linear'
    elif level == 2: # Kuadrat
        a = random.randint(1, 7) * random.choice([-1, 1]) # Koefisien a lebih bervariasi
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        f = a * x**2 + b * x + c
        gen_type = 'substitusi_kuadrat'
    else: # Level 3 - Rasional
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
        "latex": rf"\lim_{{x \to {point}}} {latex(f)}",
        "answer": str(ans),
        "params": {"type": gen_type, "f_str": str(f), "point": point}
    }

def _gen_faktorisasi(level):
    x = Symbol('x')
    a = random.randint(2, 9) * random.choice([-1, 1]) # Rentang 'a' diperluas
    
    if level <= 4:
        # Level 4: Bentuk (x^2 - a^2) / (x - a)
        num = x**2 - a**2
        den = x - a
        point = a
        gen_type = 'faktorisasi_sederhana'
    elif level == 5:
        # Level 5: Faktorisasi polinomial kuadrat
        b = random.randint(2, 9) * random.choice([-1, 1])
        while a == b or a == -b:
            b = random.randint(2, 9) * random.choice([-1, 1])
        
        num = expand((x - a) * (x - b))
        c = random.randint(2, 5) # Koefisien penyebut lebih bervariasi
        den = c*x - c*a
        point = a
        gen_type = 'faktorisasi_polinomial'
    else: # Level 6
        # Level 6: Faktorisasi Kubik / Kuadrat
        b = random.randint(-5, 5) # Rentang diperluas
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
        "latex": rf"\lim_{{x \to {point}}} {latex_original}",
        "answer": str(ans),
        "params": {"type": gen_type, "f_str": f_str_original, "point": point}
    }

def _gen_rasionalisasi(level):
    """
    Generator soal rasionalisasi yang lebih variatif dengan banyak kemungkinan kombinasi.
    """
    x = Symbol('x')
    
    # Level 7: Rasionalisasi Sederhana dengan variasi tinggi
    if level == 7:
        max_attempts = 30
        for attempt in range(max_attempts):
            # Pilih tipe soal secara acak
            soal_type = random.choice([
                'sqrt_minus_const',  # √(ax+b) - c
                'const_minus_sqrt',  # c - √(ax+b)
                'sqrt_linear_den',   # bentuk dengan penyebut linear
            ])
            
            if soal_type == 'sqrt_minus_const':
                # Bentuk: (√(ax+b) - c) / (dx + e)
                # Dimana: ax+b = c² saat x = point
                
                # Pilih konstanta c (hasil akar)
                c = random.randint(2, 10)
                c_squared = c * c
                
                # Pilih koefisien untuk di dalam akar
                a = random.choice([1, 2, 3, 4, 5])
                
                # Pilih point (tidak selalu 0!)
                point = random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
                
                # Hitung b agar √(ax+b) = c saat x = point
                b = c_squared - a * point
                
                # Buat penyebut yang menghasilkan 0 di point
                # Bentuk: d(x - point)
                d = random.randint(1, 5)
                den = d * (x - point)
                den_expanded = expand(den)
                
                num = sqrt(a*x + b) - c
                
            elif soal_type == 'const_minus_sqrt':
                # Bentuk: (c - √(ax+b)) / (dx + e)
                c = random.randint(2, 10)
                c_squared = c * c
                a = random.choice([1, 2, 3, 4, 5])
                point = random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
                b = c_squared - a * point
                d = random.randint(1, 5)
                den = d * (x - point)
                den_expanded = expand(den)
                
                num = c - sqrt(a*x + b)
                
            else:  # sqrt_linear_den
                # Bentuk: (√(ax+b) - c) / (mx + n)
                c = random.randint(2, 8)
                c_squared = c * c
                a = random.choice([1, 2, 3, 4])
                point = random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])
                b = c_squared - a * point
                
                # Penyebut: mx + n dimana mx + n = 0 saat x = point
                m = random.randint(1, 6)
                n = -m * point
                den_expanded = m*x + n
                
                num = sqrt(a*x + b) - c
            
            # Validasi soal
            f = num / den_expanded
            
            # Cek apakah substitusi langsung = 0/0
            num_at_point = num.subs(x, point)
            den_at_point = den_expanded.subs(x, point)
            
            if num_at_point == 0 and den_at_point == 0:
                # Hitung limit
                ans = limit(f, x, point)
                
                # Pastikan jawaban adalah bilangan rasional yang sederhana
                if ans.is_Integer or ans.is_Rational:
                    if abs(ans) < 100:  # Jawaban tidak terlalu besar
                        gen_type = 'rasionalisasi_akar_sederhana'
                        
                        f_str_original = f"({num})/({den_expanded})"
                        latex_original = f"\\frac{{{latex(num)}}}{{{latex(den_expanded)}}}"
                        
                        return {
                            "latex": rf"\lim_{{x \to {point}}} {latex_original}",
                            "answer": str(ans),
                            "params": {"type": gen_type, "f_str": f_str_original, "point": point}
                        }
        
        # Fallback jika gagal generate setelah max_attempts
        return _gen_rasionalisasi_fallback(level)
    
    # Level 8 dan 9 (tetap seperti sebelumnya)
    elif level == 8:
        return _gen_rasionalisasi_level_8()
    else:  # level 9
        return _gen_rasionalisasi_level_9()


def _gen_rasionalisasi_fallback(level):
    """Fallback generator untuk level 7 jika generator utama gagal."""
    x = Symbol('x')
    
    # Gunakan kombinasi sederhana yang pasti berhasil
    combinations = [
        (1, 9, 3, 0),    # √(x+9)-3 / x, x→0
        (1, 16, 4, 0),   # √(x+16)-4 / x, x→0
        (2, 8, 4, 0),    # √(2x+8)-4 / x, x→0
        (1, 25, 5, 0),   # √(x+25)-5 / x, x→0
        (3, 12, 6, 0),   # √(3x+12)-6 / x, x→0
        (1, 4, 2, -2),   # √(x+4)-2 / (x+2), x→-2
        (1, 9, 3, -5),   # √(x+9)-3 / (x+5), x→-5
        (2, 18, 6, 0),   # √(2x+18)-6 / x, x→0
    ]
    
    a, b, c, point = random.choice(combinations)
    num = sqrt(a*x + b) - c
    den = x - point if point != 0 else x
    
    f = num / den
    ans = limit(f, x, point)
    
    return {
        "latex": rf"\lim_{{x \to {point}}} \frac{{{latex(num)}}}{{{latex(den)}}}",
        "answer": str(ans),
        "params": {"type": "rasionalisasi_akar_sederhana", "f_str": f"({num})/({den})", "point": point}
    }


def _gen_rasionalisasi_level_8():
    """Generator untuk level 8 (kompleks)."""
    # Implementasi level 8 tetap seperti kode asli
    x = Symbol('x')
    
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
            "latex": rf"\lim_{{x \to {point}}} {latex_original}",
            "answer": str(ans),
            "params": {"type": "rasionalisasi_akar_kompleks", "f_str": f_str_original, "point": point}
        }


def _gen_rasionalisasi_level_9():
    """Generator untuk level 9 (beda akar)."""
    x = Symbol('x')
    a_val, b_val = random.randint(1, 5), random.randint(1, 5)
    while a_val == b_val:
        b_val = random.randint(1, 5)
    
    num = sqrt(a_val*x + 1) - sqrt(b_val*x + 1)
    den = x
    point = 0
    
    ans = limit(num / den, x, point)
    
    f_str_original = f"({num})/({den})"
    latex_original = f"\\frac{{{latex(num)}}}{{{latex(den)}}}"
    
    return {
        "latex": rf"\lim_{{x \to {point}}} {latex_original}",
        "answer": str(ans),
        "params": {"type": "rasionalisasi_beda_akar", "f_str": f_str_original, "point": point}
    }

# ... (sisa file tidak perlu diubah) ...
def _gen_trigonometri(level):
    x = Symbol('x')
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    
    if level <= 10:
        func = random.choice([sin, tan])
        f = func(a*x) / (b*x)
        gen_type = 'trigonometri_sederhana'
    elif level == 11:
        f = sin(a*x) / tan(b*x)
        gen_type = 'trigonometri_tan'
    else:
        f = (1 - cos(a*x)) / x**2
        gen_type = 'trigonometri_cos'
        
    ans = limit(f, x, 0)
    
    return {
        "latex": rf"\lim_{{x \to 0}} {latex(f)}",
        "answer": str(ans),
        "params": {"type": gen_type, "f_str": str(f), "point": 0}
    }

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
        "latex": rf"\lim_{{x \to \infty}} {latex(f)}",
        "answer": str(ans),
        "params": {"type": "tak_hingga", "f_str": str(f), "point": 'oo'}
    }

# --- Dispatcher Utama ---
GENERATOR_MAP = {
    'substitusi': (_gen_substitusi, range(1, 4)),
    'faktorisasi': (_gen_faktorisasi, range(4, 7)),
    'rasionalisasi': (_gen_rasionalisasi, range(7, 10)),
    'trigonometri': (_gen_trigonometri, range(10, 13)),
    'tak_hingga': (_gen_tak_hingga, range(13, 16)),
}

def generate_question_by_level(level):
    """
    Memilih generator soal yang sesuai berdasarkan level.
    """
    possible_generators = []
    for name, (gen_func, level_range) in GENERATOR_MAP.items():
        if level in level_range:
            possible_generators.append(gen_func)

    generator = random.choice(possible_generators) if possible_generators else _gen_tak_hingga

    question_data = generator(level)
    options = _generate_options(question_data['answer'])

    return {
        "id": str(uuid.uuid4()),
        "latex": question_data['latex'],
        "answer": question_data['answer'],
        "params": question_data['params'],
        "options": options,
        "level": level
    }