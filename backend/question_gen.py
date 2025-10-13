import random
import uuid
import math
from sympy import sympify, limit, oo, Symbol, latex, sqrt, sin, cos, tan, expand

# --- Helper Functions ---

def _generate_options(correct_answer, params=None):
    """
    Membuat 3 pilihan jawaban salah yang berasal dari kesalahan umum dalam perhitungan.
    Semua jawaban dalam bentuk PECAHAN atau BILANGAN BULAT, TIDAK ADA DESIMAL.
    Menambahkan bilangan bulat pengecoh yang strategis.
    """
    from sympy import sympify, sqrt, limit, Symbol, simplify, Rational, nsimplify, fraction
    from fractions import Fraction
    import random
    
    options = set()
    
    # Konversi jawaban benar ke bentuk pecahan jika belum
    try:
        correct_sympy = sympify(correct_answer)
        
        # Jika desimal, konversi ke pecahan
        if '.' in str(correct_answer):
            correct_fraction = nsimplify(correct_sympy, rational=True)
            correct_answer = str(correct_fraction)
            correct_sympy = correct_fraction
        
        options.add(str(correct_answer))
        correct_value = float(correct_sympy)
    except:
        options.add(str(correct_answer))
        correct_value = 0
    
    problem_type = params.get('type', '') if params else ''
    x = Symbol('x')
    
    # Fungsi helper untuk membuat pecahan yang cantik
    def make_fraction(numerator, denominator):
        """Membuat pecahan dalam bentuk string yang sederhana."""
        if denominator == 1:
            return str(int(numerator))
        if denominator == 0:
            return "tak terdefinisi"
        
        # Sederhanakan pecahan
        from math import gcd
        g = gcd(int(abs(numerator)), int(abs(denominator)))
        num = int(numerator / g)
        den = int(denominator / g)
        
        # Pastikan tanda negatif di pembilang
        if den < 0:
            num = -num
            den = -den
        
        if den == 1:
            return str(num)
        return f"{num}/{den}"
    
    # Fungsi untuk ekstrak pembilang dan penyebut dari jawaban benar
    def extract_fraction(value_str):
        """Ekstrak pembilang dan penyebut dari string pecahan atau desimal."""
        try:
            if '/' in value_str:
                parts = value_str.split('/')
                return int(parts[0]), int(parts[1])
            else:
                val = float(sympify(value_str))
                frac = Fraction(val).limit_denominator(100)
                return frac.numerator, frac.denominator
        except:
            return 1, 1
    
    correct_num, correct_den = extract_fraction(str(correct_answer))
    
    try:
        # ========== KESALAHAN UNTUK SUBSTITUSI ==========
        if 'substitusi' in problem_type:
            f_str = params.get('f_str', '')
            point = params.get('point', 0)
            
            try:
                f = sympify(f_str)
                num, den = f.as_numer_denom()
                
                # Kesalahan 1: Lupa tanda kurung (untuk bilangan negatif)
                if point < 0 and den != 1:
                    num_val = num.subs(x, point)
                    den_val = den.subs(x, point)
                    
                    # Salah: anggap point tanpa kurung
                    num_wrong = num.subs(x, -abs(point))  # Salah tanda
                    wrong_result = simplify(num_wrong / den_val)
                    wrong_frac = nsimplify(wrong_result, rational=True)
                    if wrong_frac != correct_sympy:
                        options.add(str(wrong_frac))
                
                # Kesalahan 2: Pembilang/penyebut terbalik
                if den != 1:
                    inverted = make_fraction(correct_den, correct_num)
                    if inverted != str(correct_answer):
                        options.add(inverted)
                
                # Kesalahan 3: Salah tanda
                negated = make_fraction(-correct_num, correct_den)
                options.add(negated)
                
                # Pengecoh: Bilangan bulat yang muncul dalam soal
                # Ambil koefisien atau konstanta dari soal
                coeffs = [abs(int(c)) for c in [num.as_coefficients_dict().get(1, 0), 
                                                  den.as_coefficients_dict().get(1, 0)] if c != 0]
                if coeffs:
                    options.add(str(random.choice(coeffs)))
                
            except:
                pass
        
        # ========== KESALAHAN UNTUK FAKTORISASI ==========
        elif 'faktorisasi' in problem_type:
            f_str = params.get('f_str', '')
            point = params.get('point', 0)
            
            try:
                f = sympify(f_str)
                num, den = f.as_numer_denom()
                
                # Kesalahan 1: Tidak membatalkan faktor (0/0)
                options.add("0")
                options.add("tak terdefinisi")
                
                # Kesalahan 2: Salah coret faktor
                # Misal: (x²-9)/(x-3) dicoret jadi x-3 (salah, harusnya x+3)
                from sympy import factor, cancel
                num_factored = factor(num)
                den_factored = factor(den)
                
                # Coba ambil faktor lain dari pembilang
                if hasattr(num_factored, 'args') and len(num_factored.args) > 1:
                    for arg in num_factored.args:
                        if arg != den_factored:
                            wrong_result = arg.subs(x, point)
                            wrong_frac = nsimplify(wrong_result, rational=True)
                            if abs(float(wrong_frac)) < 100:
                                options.add(str(wrong_frac))
                                break
                
                # Kesalahan 3: Salah tanda
                negated = make_fraction(-correct_num, correct_den)
                options.add(negated)
                
                # Pengecoh: Point itu sendiri atau 2*point
                if abs(point) < 20:
                    options.add(str(abs(point)))
                    if abs(2*point) < 20:
                        options.add(str(2*abs(point)))
                
            except:
                pass
        
        # ========== KESALAHAN UNTUK RASIONALISASI ==========
        elif 'rasionalisasi' in problem_type:
            f_str = params.get('f_str', '')
            point = params.get('point', 0)
            
            try:
                f = sympify(f_str)
                num, den = f.as_numer_denom()
                
                # Kesalahan 1: Lupa rasionalisasi
                options.add("0")
                options.add("tak terdefinisi")
                
                # Kesalahan 2: Salah rumus sekawan (a²+b² bukan a²-b²)
                # Ini biasanya menghasilkan jawaban 2x atau 3x lipat
                double_wrong = make_fraction(2*correct_num, correct_den)
                options.add(double_wrong)
                
                # Kesalahan 3: Salah tanda akar (±)
                negated = make_fraction(-correct_num, correct_den)
                options.add(negated)
                
                # Kesalahan 4: Lupa sederhanakan
                # Kalikan pembilang dan penyebut dengan 2, 3, atau 4
                multiplier = random.choice([2, 3, 4])
                unsimplified = make_fraction(correct_num * multiplier, correct_den * multiplier)
                if unsimplified != str(correct_answer):
                    options.add(unsimplified)
                
                # Kesalahan 5: Terbalik
                inverted = make_fraction(correct_den, correct_num)
                if inverted != str(correct_answer):
                    options.add(inverted)
                
                # Pengecoh: Nilai konstanta dari dalam akar
                # Misal: √(x+9)-3 → pengecoh: 3, 9
                if 'sqrt' in str(num):
                    terms = num.as_ordered_terms()
                    for term in terms:
                        if 'sqrt' not in str(term):
                            const_val = abs(int(term))
                            if 1 < const_val < 20:
                                options.add(str(const_val))
                                break
                
            except:
                pass
        
        # ========== KESALAHAN UNTUK TRIGONOMETRI ==========
        elif 'trigonometri' in problem_type:
            # Kesalahan umum
            options.add("0")
            options.add("1")
            options.add("tak terdefinisi")
            
            # Terbalik
            if correct_den != 0:
                inverted = make_fraction(correct_den, correct_num)
                options.add(inverted)
            
            # Salah tanda
            negated = make_fraction(-correct_num, correct_den)
            options.add(negated)
            
            # Pengecoh: koefisien dari soal
            # sin(ax)/bx → pengecoh: a, b
            f_str = params.get('f_str', '')
            # Ekstrak koefisien (misal dari sin(3x)/4x)
            import re
            coeffs = re.findall(r'\d+', f_str)
            for c in coeffs[:2]:  # Ambil 2 koefisien pertama
                if 1 < int(c) < 20:
                    options.add(c)
        
        # ========== KESALAHAN UNTUK TAK HINGGA ==========
        elif 'tak_hingga' in problem_type:
            options.add("0")
            options.add("1")
            options.add("tak terdefinisi")
            
            # Terbalik
            if correct_den != 0:
                inverted = make_fraction(correct_den, correct_num)
                options.add(inverted)
            
            # Salah tanda
            negated = make_fraction(-correct_num, correct_den)
            options.add(negated)
            
            # Pengecoh: koefisien utama dari pembilang atau penyebut
            f_str = params.get('f_str', '')
            try:
                f = sympify(f_str)
                num, den = f.as_numer_denom()
                
                # Ambil koefisien pangkat tertinggi
                from sympy import degree, LC
                if degree(num) > 0:
                    leading_coeff_num = abs(int(LC(num, x)))
                    if 1 < leading_coeff_num < 20:
                        options.add(str(leading_coeff_num))
                
                if degree(den) > 0:
                    leading_coeff_den = abs(int(LC(den, x)))
                    if 1 < leading_coeff_den < 20:
                        options.add(str(leading_coeff_den))
            except:
                pass
        
        # ========== TAMBAHAN KESALAHAN UMUM ==========
        # Pastikan ada setidaknya 1-2 bilangan bulat sebagai pengecoh
        integers_in_options = [opt for opt in options if '/' not in opt and opt.lstrip('-').isdigit()]
        
        if len(integers_in_options) < 2:
            # Tambahkan bilangan bulat strategis
            strategic_integers = []
            
            # 1. Nilai absolut dari pembilang atau penyebut
            if correct_den != 1:
                strategic_integers.append(abs(correct_num))
                strategic_integers.append(abs(correct_den))
            
            # 2. Pembilang + penyebut atau pembilang - penyebut
            if correct_den != 1:
                strategic_integers.append(abs(correct_num + correct_den))
                strategic_integers.append(abs(correct_num - correct_den))
            
            # 3. Bilangan bulat terdekat
            if abs(correct_value) < 1:
                strategic_integers.extend([1, 2])
            else:
                nearby = int(round(correct_value))
                strategic_integers.extend([nearby, nearby + 1, nearby - 1])
            
            # Tambahkan 1-2 bilangan bulat
            for num in strategic_integers:
                if 0 < abs(num) < 20 and len(integers_in_options) < 2:
                    options.add(str(int(num)))
                    integers_in_options.append(str(int(num)))
        
        # Tambahkan beberapa variasi pecahan jika belum cukup
        if len(options) < 8:  # Buffer untuk memilih 3 terbaik nanti
            # Variasi 1: Tukar pembilang-penyebut
            if correct_den != 1 and correct_num != 0:
                options.add(make_fraction(correct_den, correct_num))
            
            # Variasi 2: Ganti tanda
            options.add(make_fraction(-correct_num, correct_den))
            
            # Variasi 3: Kalikan/bagi dengan 2
            options.add(make_fraction(correct_num * 2, correct_den))
            options.add(make_fraction(correct_num, correct_den * 2))
            
            # Variasi 4: Tambah/kurang 1 dari pembilang
            options.add(make_fraction(correct_num + correct_den, correct_den))
            options.add(make_fraction(correct_num - correct_den, correct_den))
    
    except Exception as e:
        print(f"Error in smart options: {e}")
        pass
    
    # Pastikan jawaban benar ada
    options.add(str(correct_answer))
    
    # Hapus jawaban yang tidak valid
    options = {opt for opt in options if opt and opt != str(correct_answer) 
               and 'zoo' not in opt.lower() and 'oo' not in opt.lower()}
    
    # Jika masih kurang, tambahkan pecahan sederhana
    simple_fractions = ["1/2", "1/3", "1/4", "1/5", "1/6", "1/8", 
                       "2/3", "3/4", "2/5", "3/5", 
                       "-1/2", "-1/3", "-1/4",
                       "1", "2", "3", "0"]
    
    while len(options) < 10:  # Buffer
        frac = random.choice(simple_fractions)
        if frac != str(correct_answer):
            options.add(frac)
    
    # Pilih 3 jawaban salah terbaik (yang paling mirip/masuk akal)
    options.discard(str(correct_answer))
    wrong_options = list(options)
    
    # Prioritaskan pilihan yang lebih masuk akal (nilai absolut tidak terlalu besar)
    def option_score(opt):
        """Score untuk menentukan seberapa masuk akal pilihan ini."""
        try:
            val = float(sympify(opt))
            # Prioritaskan nilai yang dekat dengan jawaban benar
            distance = abs(val - correct_value)
            # Prioritaskan bilangan bulat dan pecahan sederhana
            if '/' not in opt:
                return distance  # Bilangan bulat lebih diprioritaskan
            else:
                return distance + 0.5  # Pecahan sedikit lebih rendah prioritasnya
        except:
            return 1000  # Pilihan tidak valid
    
    wrong_options.sort(key=option_score)
    selected_wrong = wrong_options[:3]
    
    final_options = selected_wrong + [str(correct_answer)]
    
    # Shuffle agar jawaban benar tidak selalu di posisi yang sama
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
    """
    Generator untuk level 9 - Rasionalisasi dengan beda akar.
    Sangat variatif dengan kemampuan generate 1000+ soal unik.
    Point limit bisa variatif, tidak hanya x→0.
    """
    x = Symbol('x')
    
    max_attempts = 50
    
    for attempt in range(max_attempts):
        # Pilih tipe soal secara acak
        soal_type = random.choice([
            'beda_akar_linear',      # √(ax+b) - √(cx+d)
            'beda_akar_kuadrat',     # akar di pembilang, kuadrat di penyebut
            'jumlah_akar',           # √(ax+b) + √(cx+d) (bisa negatif total)
            'akar_kompleks',         # kombinasi akar dengan konstanta
        ])
        
        # Pilih point yang bervariasi (tidak selalu 0!)
        point = random.choice([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6])
        
        if soal_type == 'beda_akar_linear':
            # Bentuk: (√(ax+b) - √(cx+d)) / (mx+n)
            # Di mana penyebut = 0 saat x = point
            
            # Pilih koefisien untuk akar pertama
            a = random.randint(1, 6)
            # Hitung b agar √(ax+b) bernilai kuadrat sempurna di point
            sqrt_val_1 = random.randint(2, 8)
            b = sqrt_val_1**2 - a * point
            
            # Pilih koefisien untuk akar kedua (berbeda dari pertama)
            c = random.randint(1, 6)
            while c == a:
                c = random.randint(1, 6)
            
            # Hitung d agar √(cx+d) juga bernilai kuadrat sempurna di point
            sqrt_val_2 = random.randint(2, 8)
            while sqrt_val_2 == sqrt_val_1:  # Harus berbeda
                sqrt_val_2 = random.randint(2, 8)
            d = sqrt_val_2**2 - c * point
            
            # Pastikan nilai dalam akar positif untuk rentang x di sekitar point
            if b <= 0 or d <= 0:
                continue
            
            # Buat penyebut yang = 0 di point
            m = random.randint(1, 5)
            n = -m * point
            
            num = sqrt(a*x + b) - sqrt(c*x + d)
            den = m*x + n
            
        elif soal_type == 'beda_akar_kuadrat':
            # Bentuk: (√(ax+b) - √(cx+d)) / (x²+px+q)
            # Penyebut punya faktor (x-point)
            
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
            
            # Penyebut: (x-point)(x-other_root)
            other_root = random.choice([r for r in range(-5, 6) if r != point])
            den = expand((x - point) * (x - other_root))
            
            num = sqrt(a*x + b) - sqrt(c*x + d)
            
        elif soal_type == 'jumlah_akar':
            # Bentuk: (√(ax+b) + √(cx+d) - k) / (mx+n)
            # Di mana √(ax+b) + √(cx+d) = k saat x = point
            
            a = random.randint(1, 5)
            sqrt_val_1 = random.randint(2, 6)
            b = sqrt_val_1**2 - a * point
            
            c = random.randint(1, 5)
            sqrt_val_2 = random.randint(2, 6)
            d = sqrt_val_2**2 - c * point
            
            if b <= 0 or d <= 0:
                continue
            
            # k adalah jumlah kedua akar di point
            k = sqrt_val_1 + sqrt_val_2
            
            m = random.randint(1, 5)
            n = -m * point
            
            num = sqrt(a*x + b) + sqrt(c*x + d) - k
            den = m*x + n
            
        else:  # akar_kompleks
            # Bentuk: (k₁√(ax+b) - k₂√(cx+d)) / (mx+n)
            # Dengan koefisien k₁ dan k₂
            
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
            
            # Pastikan k₁√val₁ ≠ k₂√val₂ (agar pembilang = 0)
            if k1 * sqrt_val_1 == k2 * sqrt_val_2:
                k2 += 1
            
            m = random.randint(1, 5)
            n = -m * point
            
            num = k1 * sqrt(a*x + b) - k2 * sqrt(c*x + d)
            den = m*x + n
        
        # Validasi soal
        f = num / den
        
        # Cek apakah substitusi langsung = 0/0
        try:
            num_at_point = num.subs(x, point)
            den_at_point = den.subs(x, point)
            
            if num_at_point == 0 and den_at_point == 0:
                # Hitung limit
                ans = limit(f, x, point)
                
                # Pastikan jawaban adalah bilangan rasional yang sederhana
                if ans.is_Integer or ans.is_Rational:
                    if abs(ans) < 100 and ans != 0:  # Jawaban masuk akal
                        gen_type = 'rasionalisasi_beda_akar'
                        
                        f_str_original = f"({num})/({den})"
                        latex_original = f"\\frac{{{latex(num)}}}{{{latex(den)}}}"
                        
                        return {
                            "latex": rf"\lim_{{x \to {point}}} {latex_original}",
                            "answer": str(ans),
                            "params": {"type": gen_type, "f_str": f_str_original, "point": point}
                        }
        except:
            continue
    
    # Fallback jika gagal setelah max_attempts
    return _gen_rasionalisasi_level_9_fallback()


def _gen_rasionalisasi_level_9_fallback():
    """
    Fallback generator untuk level 9 dengan kombinasi preset yang pasti berhasil.
    """
    x = Symbol('x')
    
    # Bank soal preset yang pasti valid dan bervariasi
    preset_combinations = [
        # (a, b, c, d, m, n, point) untuk (√(ax+b) - √(cx+d)) / (mx+n) di x=point
        (1, 1, 2, 1, 1, 0, 0),      # √(x+1) - √(2x+1) / x, x→0
        (2, 2, 3, 2, 1, 0, 0),      # √(2x+2) - √(3x+2) / x, x→0
        (1, 4, 2, 4, 1, 0, 0),      # √(x+4) - √(2x+4) / x, x→0
        (1, 9, 3, 9, 1, 0, 0),      # √(x+9) - √(3x+9) / x, x→0
        (2, 8, 1, 8, 1, 0, 0),      # √(2x+8) - √(x+8) / x, x→0
        
        # Dengan point ≠ 0
        (1, 5, 2, 2, 1, 1, -1),     # √(x+5) - √(2x+2) / (x+1), x→-1
        (1, 13, 2, 8, 1, 2, -2),    # √(x+13) - √(2x+8) / (x+2), x→-2
        (2, 10, 1, 8, 1, -1, 1),    # √(2x+10) - √(x+8) / (x-1), x→1
        (1, 8, 3, 0, 2, 4, -2),     # √(x+8) - √(3x) / (2x+4), x→-2
        (3, 3, 1, 9, 1, -2, 2),     # √(3x+3) - √(x+9) / (x-2), x→2
        
        # Variasi dengan koefisien lebih besar
        (4, 4, 1, 16, 1, 0, 0),     # √(4x+4) - √(x+16) / x, x→0
        (1, 16, 4, 4, 1, 0, 0),     # √(x+16) - √(4x+4) / x, x→0
        (2, 18, 1, 25, 1, 3, -3),   # √(2x+18) - √(x+25) / (x+3), x→-3
        (3, 12, 2, 18, 2, -6, 3),   # √(3x+12) - √(2x+18) / (2x-6), x→3
        (1, 20, 5, 0, 1, 4, -4),    # √(x+20) - √(5x) / (x+4), x→-4
    ]
    
    # Pilih kombinasi secara acak
    a, b, c, d, m, n, point = random.choice(preset_combinations)
    
    num = sqrt(a*x + b) - sqrt(c*x + d)
    den = m*x + n
    
    f = num / den
    ans = limit(f, x, point)
    
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