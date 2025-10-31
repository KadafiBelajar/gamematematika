import uuid
from typing import Dict

from question_generators import (
    generate_limit_question,
    generate_derivative_question,
    generate_integral_question,
    generate_options,
)


def generate_question(stage_name: str, level_num: int) -> Dict:
    """Dispatcher utama yang memanggil generator sesuai stage."""
    stage = stage_name.lower()
    if stage == 'limit':
        q = generate_limit_question(level_num)
    elif stage == 'turunan':
        q = generate_derivative_question(level_num)
    elif stage == 'integral':
        q = generate_integral_question(level_num)
    else:
        q = generate_limit_question(level_num)

    opts = generate_options(q['answer'], q.get('params'))
    return {
        "id": str(uuid.uuid4()),
        "latex": q["latex"],
        "answer": q["answer"],
        "params": q.get("params", {}),
        "options": opts,
        "level": int(level_num),
        "stage": stage,
    }


