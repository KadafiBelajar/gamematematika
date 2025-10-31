import random
from fractions import Fraction
from sympy import sympify, sqrt, Symbol, Rational, nsimplify


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

    except Exception:
        pass

    options.add(str(correct_answer))

    options = {opt for opt in options if opt and opt != str(correct_answer)
               and 'zoo' not in opt.lower() and 'oo' not in opt.lower()}

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


