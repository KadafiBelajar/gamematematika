import random
from sympy import symbols, Symbol, latex, diff, simplify, sin, cos, tan, sqrt, Rational


x = Symbol('x')


def _fmt_answer(expr):
    try:
        simp = simplify(expr)
        return str(simp)
    except Exception:
        return str(expr)


def _level1():
    # f(x) = a x^n
    a = random.randint(1, 9) * random.choice([1, -1])
    n = random.randint(1, 6)
    f = a * x**n
    fp = diff(f, x)
    return {
        "latex": rf"\text{{Turunkan }} f(x) = {latex(f)}",
        "answer": _fmt_answer(fp),
        "params": {"type": "derivative_power_basic", "a": a, "n": n}
    }


def _level2():
    # f(x) = a x^n + b x^m + c
    a = random.randint(1, 7) * random.choice([1, -1])
    b = random.randint(1, 7) * random.choice([1, -1])
    c = random.randint(-9, 9)
    n = random.randint(2, 6)
    m = random.randint(1, n-1)
    f = a*x**n + b*x**m + c
    return {
        "latex": rf"\text{{Turunkan }} f(x) = {latex(f)}",
        "answer": _fmt_answer(diff(f, x)),
        "params": {"type": "derivative_polynomial", "a": a, "b": b, "c": c, "n": n, "m": m}
    }


def _level3():
    # f(x) = a x^-n atau a sqrt(x)
    if random.random() < 0.5:
        a = random.randint(1, 7) * random.choice([1, -1])
        n = random.randint(1, 5)
        f = a * x**(-n)
        t = "negative_power"
    else:
        a = random.randint(1, 7) * random.choice([1, -1])
        f = a * sqrt(x)
        t = "sqrt"
    return {
        "latex": rf"\text{{Turunkan }} f(x) = {latex(f)}",
        "answer": _fmt_answer(diff(f, x)),
        "params": {"type": f"derivative_{t}", "a": a}
    }


def _level4():
    # Product rule linear: (ax+b)(cx+d)
    a = random.randint(1, 7) * random.choice([1, -1])
    b = random.randint(-9, 9)
    c = random.randint(1, 7) * random.choice([1, -1])
    d = random.randint(-9, 9)
    f = (a*x + b) * (c*x + d)
    return {
        "latex": rf"\text{{Turunkan }} f(x) = ({latex(a*x+b)})({latex(c*x+d)})",
        "answer": _fmt_answer(diff(f, x)),
        "params": {"type": "product_linear", "a": a, "b": b, "c": c, "d": d}
    }


def _level5():
    # Product rule quadratic: (ax^2+b)(cx+d)
    a = random.randint(1, 5) * random.choice([1, -1])
    b = random.randint(-9, 9)
    c = random.randint(1, 7) * random.choice([1, -1])
    d = random.randint(-9, 9)
    f = (a*x**2 + b) * (c*x + d)
    return {
        "latex": rf"\text{{Turunkan }} f(x) = ({latex(a*x**2+b)})({latex(c*x+d)})",
        "answer": _fmt_answer(diff(f, x)),
        "params": {"type": "product_quadratic", "a": a, "b": b, "c": c, "d": d}
    }


def _level6():
    # Quotient rule linear: (ax+b)/(cx+d)
    a = random.randint(1, 7) * random.choice([1, -1])
    b = random.randint(-9, 9)
    c = random.randint(1, 7) * random.choice([1, -1])
    d = random.randint(-9, 9)
    f = (a*x + b) / (c*x + d)
    return {
        "latex": rf"\text{{Turunkan }} f(x) = {latex(f)}",
        "answer": _fmt_answer(diff(f, x)),
        "params": {"type": "quotient_linear", "a": a, "b": b, "c": c, "d": d}
    }


def _level7():
    # Quotient rule quadratic: (ax^2+b)/(cx+d)
    a = random.randint(1, 5) * random.choice([1, -1])
    b = random.randint(-9, 9)
    c = random.randint(1, 7) * random.choice([1, -1])
    d = random.randint(-9, 9)
    f = (a*x**2 + b) / (c*x + d)
    return {
        "latex": rf"\text{{Turunkan }} f(x) = {latex(f)}",
        "answer": _fmt_answer(diff(f, x)),
        "params": {"type": "quotient_quadratic", "a": a, "b": b, "c": c, "d": d}
    }


def _level8():
    # Chain rule power: (ax^2+b)^n
    a = random.randint(1, 5) * random.choice([1, -1])
    b = random.randint(-6, 6)
    n = random.randint(2, 5)
    f = (a*x**2 + b)**n
    return {
        "latex": rf"\text{{Turunkan }} f(x) = {latex(f)}",
        "answer": _fmt_answer(diff(f, x)),
        "params": {"type": "chain_power", "a": a, "b": b, "n": n}
    }


def _level9():
    # Basic trig derivatives: a*sin(bx), a*cos(bx), a*tan(bx)
    a = random.randint(1, 7) * random.choice([1, -1])
    b = random.randint(1, 6)
    func = random.choice([sin, cos, tan])
    f = a * func(b*x)
    return {
        "latex": rf"\text{{Turunkan }} f(x) = {latex(f)}",
        "answer": _fmt_answer(diff(f, x)),
        "params": {"type": "trig_basic", "a": a, "b": b, "func": func.__name__}
    }


def _level10():
    # Chain rule with trig: a*sin(c x^2 + d)
    a = random.randint(1, 5) * random.choice([1, -1])
    c = random.randint(1, 5)
    d = random.randint(-6, 6)
    inner = c*x**2 + d
    f = a * sin(inner)
    return {
        "latex": rf"\text{{Turunkan }} f(x) = {latex(f)}",
        "answer": _fmt_answer(diff(f, x)),
        "params": {"type": "chain_trig", "a": a, "c": c, "d": d}
    }


def _level11():
    # Combination product & trig: a x^n * sin(bx)
    a = random.randint(1, 5) * random.choice([1, -1])
    n = random.randint(1, 5)
    b = random.randint(1, 6)
    f = a * x**n * sin(b*x)
    return {
        "latex": rf"\text{{Turunkan }} f(x) = {latex(f)}",
        "answer": _fmt_answer(diff(f, x)),
        "params": {"type": "product_trig", "a": a, "n": n, "b": b}
    }


def _level12():
    # Combination quotient & trig: sin(ax)/(cx+d)
    a = random.randint(1, 6)
    c = random.randint(1, 6) * random.choice([1, -1])
    d = random.randint(-6, 6)
    f = sin(a*x) / (c*x + d)
    return {
        "latex": rf"\text{{Turunkan }} f(x) = {latex(f)}",
        "answer": _fmt_answer(diff(f, x)),
        "params": {"type": "quotient_trig", "a": a, "c": c, "d": d}
    }


def _level13():
    # Second derivative of polynomial
    a = random.randint(1, 5) * random.choice([1, -1])
    b = random.randint(1, 5) * random.choice([1, -1])
    c = random.randint(-6, 6)
    f = a*x**3 + b*x**2 + c*x
    fpp = diff(f, x, 2)
    return {
        "latex": rf"\text{{Cari }} f''(x) \text{ dari } f(x) = {latex(f)}",
        "answer": _fmt_answer(fpp),
        "params": {"type": "second_derivative_poly"}
    }


def _level14():
    # Gradient of tangent line at x=c
    a = random.randint(1, 5) * random.choice([1, -1])
    b = random.randint(1, 5) * random.choice([1, -1])
    c0 = random.randint(-4, 4)
    f = a*x**3 + b*x**2 + x
    fp = diff(f, x)
    ans = fp.subs(x, c0)
    return {
        "latex": rf"\text{{Gradien garis singgung }} f(x)={latex(f)} \text{ di } x={c0} \text{ adalah }?",
        "answer": _fmt_answer(ans),
        "params": {"type": "tangent_gradient", "point": c0}
    }


def _level15():
    # Stationary points of f(x)=ax^3+bx^2+c
    a = random.randint(1, 5) * random.choice([1, -1])
    b = random.randint(1, 5) * random.choice([1, -1])
    c = random.randint(-6, 6)
    f = a*x**3 + b*x**2 + c
    fp = diff(f, x)
    critical_points = sorted(set([sol for sol in fp.as_poly(x).all_roots()]))
    # Return x-coordinate(s) of stationary points; if multiple, join with commas
    if not critical_points:
        ans = "Tidak ada"
    else:
        ans = ", ".join(str(simplify(pt)) for pt in critical_points)
    return {
        "latex": rf"\text{{Titik stasioner dari }} f(x)={latex(f)} \text{ (nilai } x)\text{ adalah?}",
        "answer": ans,
        "params": {"type": "stationary_points"}
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


def generate_derivative_question(level: int):
    level = max(1, min(15, int(level)))
    return LEVEL_MAP[level]()


