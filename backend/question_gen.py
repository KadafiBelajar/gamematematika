import random
import uuid
import math
from sympy import sympify, limit, oo, Symbol, latex, sqrt, sin, cos, tan

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
            str(int(correct_float + random.randint(1, 3))),
            str(int(correct_float - random.randint(1, 3))),
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
            options.add(str(random.randint(0, 10)))

    options.discard(str(correct_answer))
    final_options = list(options)[:3] + [str(correct_answer)]
    random.shuffle(final_options)
    return final_options

# --- Dynamic Question Generators (Refactored to use latex()) ---

def _gen_substitusi(level):
    x = Symbol('x')
    
    if level == 1: # Linear
        point = random.randint(-3, 3)
        a, b = random.randint(1, 5), random.randint(-5, 5)
        f = a * x + b
        gen_type = 'substitusi_linear'
    elif level == 2: # Kuadrat
        point = random.randint(-3, 3)
        a, b, c = random.randint(1, 4), random.randint(-5, 5), random.randint(-5, 5)
        f = a * x**2 + b * x + c
        gen_type = 'substitusi_kuadrat'
    else: # Level 3 - Rasional (DENGAN PERBAIKAN)
        while True: # Loop untuk memastikan fungsi tidak konstan
            point = random.randint(-3, 3)
            den_a, den_b = random.randint(1, 3), random.randint(1, 5)
            
            # Pastikan penyebut tidak nol pada titik limit
            while den_a * point + den_b == 0:
                point = random.randint(-3, 3) # Cari titik baru jika penyebut nol
                
            num_a, num_b = random.randint(1, 5), random.randint(-5, 5)
            
            # Buat objek Sympy untuk pembilang dan penyebut
            num = num_a * x + num_b
            den = den_a * x + den_b
            
            # Cek apakah fungsi menyederhanakan menjadi konstanta.
            # Jika tidak, baru keluar dari loop.
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
    a = random.randint(2, 6) * random.choice([-1, 1])
    
    if level <= 4: # (x^2 - a^2) / (x - a)
        num, den, point = x**2 - a**2, x - a, a
        gen_type = 'faktorisasi_sederhana'
    else:
        b = random.randint(2, 6) * random.choice([-1, 1])
        while a == b:
            b = random.randint(2, 6) * random.choice([-1, 1])
        
        if level == 5: # (x-a)(x-b) / (x-a)
            num, den, point = (x - a) * (x - b), x - a, a
            gen_type = 'faktorisasi_polinomial'
        else: # Level 6 - (x^3 - a^3) / (x-a)
            num, den, point = x**3 - a**3, x - a, a
            gen_type = 'faktorisasi_kubik'
            
    f = num / den
    ans = limit(f, x, point)
    return {
        "latex": rf"\lim_{{x \to {point}}} {latex(f)}",
        "answer": str(ans),
        "params": {"type": gen_type, "f_str": str(f), "point": point}
    }

def _gen_rasionalisasi(level):
    x = Symbol('x')
    
    for _ in range(10):
        if level <= 7: # sqrt(x+a) - b / x
            a = random.choice([1, 4, 9, 16, 25])
            b = int(math.sqrt(a))
            num, den, point = sqrt(x + a) - b, x, 0
            gen_type = 'rasionalisasi_akar_sederhana'
        elif level == 8: # sqrt(ax+b) - c / (x-d)
            d = random.randint(1, 5)
            a_val = random.randint(1, 4)
            b_val = random.randint(1, 10)
            c_val = (a_val * d + b_val)**(1/2)
            while c_val != int(c_val):
                b_val += 1
                c_val = (a_val * d + b_val)**(1/2)
            c_val = int(c_val)
            num, den, point = sqrt(a_val*x + b_val) - c_val, x - d, d
            gen_type = 'rasionalisasi_akar_kompleks'
        else: # Level 9 - Beda akar
            a_val, b_val = random.randint(1, 4), random.randint(1, 4)
            num, den, point = sqrt(a_val*x + 1) - sqrt(b_val*x + 1), x, 0
            gen_type = 'rasionalisasi_beda_akar'

        f = num / den
        ans = limit(f, x, point)
        
        if ans.is_Integer or ans.is_Float or ans.is_Rational:
            return {
                "latex": rf"\lim_{{x \to {point}}} {latex(f)}",
                "answer": str(ans),
                "params": {"type": gen_type, "f_str": str(f), "point": point}
            }

    return _gen_faktorisasi(6) # Fallback

def _gen_trigonometri(level):
    x = Symbol('x')
    a = random.randint(2, 6)
    b = random.randint(2, 6)
    
    if level <= 10: # sin(ax)/bx atau tan(ax)/bx
        func = random.choice([sin, tan])
        f = func(a*x) / (b*x)
        gen_type = 'trigonometri_sederhana'
    elif level == 11: # sin(ax)/tan(bx)
        f = sin(a*x) / tan(b*x)
        gen_type = 'trigonometri_tan'
    else: # Level 12 - (1-cos(ax))/x^2
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
        
    num_coeffs = [random.randint(1, 8) for _ in range(deg + 1)]
    den_coeffs = [random.randint(1, 8) for _ in range(deg + 1)]
    
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
            if level > min(level_range):
                if name == 'faktorisasi': possible_generators.append(GENERATOR_MAP['substitusi'][0])
                if name == 'rasionalisasi': possible_generators.append(GENERATOR_MAP['faktorisasi'][0])
                if name == 'trigonometri': possible_generators.append(GENERATOR_MAP['rasionalisasi'][0])
                if name == 'tak_hingga': possible_generators.append(GENERATOR_MAP['trigonometri'][0])

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
