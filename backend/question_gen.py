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
    x = Symbol('x')
    
    for _ in range(20): # Coba hingga 20 kali untuk dapat soal yang valid
        if level <= 7: # Level 7: Rasionalisasi Sederhana
            a = random.choice([1, 4, 9, 16, 25, 36, 49, 64, 81, 100])
            b = int(math.sqrt(a)) * random.choice([-1, 1])
            
            if random.choice([True, False]):
                num = sqrt(x + a) - b
            else:
                num = b - sqrt(x + a)
            
            den = x
            point = 0
            if num.subs(x, point) != 0: continue
            gen_type = 'rasionalisasi_akar_sederhana'

        elif level == 8: # Level 8: Rasionalisasi Kompleks (DENGAN PERBAIKAN)
            gen_type = 'rasionalisasi_akar_kompleks'
            
            # --- PERBAIKAN: Gunakan `while True` untuk menjamin soal valid ---
            while True:
                d = random.randint(2, 5) * random.choice([-1, 1])
                a_val = random.randint(1, 4)
                b_val = random.randint(1, 25) # Perluas rentang untuk peluang lebih besar
                
                rad_val = a_val * d + b_val
                # Cek apakah rad_val adalah kuadrat sempurna yang positif
                if rad_val > 0 and math.isqrt(rad_val)**2 == rad_val:
                    c_val = math.isqrt(rad_val)
                    if c_val != 0:
                        break # Kombinasi valid ditemukan, keluar dari loop
            # --- AKHIR PERBAIKAN ---

            sqrt_expr = sqrt(a_val*x + b_val)
            
            # Pilih secara acak salah satu dari dua skenario sulit
            scenario = random.choice(['complex_den', 'sqrt_in_den'])
            
            if scenario == 'complex_den':
                # Skenario A: Penyebut lebih kompleks (kuadrat)
                num = sqrt_expr - c_val
                den = x**2 - d**2
                point = d
            else: # scenario == 'sqrt_in_den'
                # Skenario B: Akar ada di penyebut
                num = x**2 - d**2
                den = sqrt_expr - c_val
                point = d

        else: # Level 9
            a_val, b_val = random.randint(1, 5), random.randint(1, 5)
            while a_val == b_val:
                 b_val = random.randint(1, 5)
            num, den, point = sqrt(a_val*x + 1) - sqrt(b_val*x + 1), x, 0
            gen_type = 'rasionalisasi_beda_akar'

        ans = limit(num / den, x, point)
        
        if ans.is_Integer or ans.is_Float or ans.is_Rational:
            f_str_original = f"({num})/({den})"
            latex_original = f"\\frac{{{latex(num)}}}{{{latex(den)}}}"
            return {
                "latex": rf"\lim_{{x \to {point}}} {latex_original}",
                "answer": str(ans),
                "params": {"type": gen_type, "f_str": f_str_original, "point": point}
            }

    return _gen_faktorisasi(6) # Fallback jika gagal membuat soal

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