import random
from sympy import Symbol, latex, integrate, sin, cos


x = Symbol('x')


def generate_integral_question(level: int):
    """
    Placeholder generator for Integral stage to keep app functional.
    Produces simple indefinite integral problems across 15 levels.
    """
    level = max(1, min(15, int(level)))
    t = level % 5
    if t == 1:
        a = random.randint(1, 7)
        n = random.randint(1, 5)
        f = a * x**n
    elif t == 2:
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        f = a * x**2 + b * x
    elif t == 3:
        a = random.randint(1, 5)
        f = a * sin(x)
    elif t == 4:
        a = random.randint(1, 5)
        f = a * cos(x)
    else:
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        f = a * x + b
    F = integrate(f, x)
    return {
        "latex": rf"\int {latex(f)}\,dx",
        "answer": str(F),  # Konstanta integrasi diabaikan untuk pilihan ganda
        "params": {"type": "integral_basic", "level": level}
    }


