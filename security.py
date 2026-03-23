from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

def sanitize_path(path: str) -> Path:
    """
    Превращает относительный путь в безопасный абсолютный путь внутри корня проекта.
    """
    abs_path = (PROJECT_ROOT / path).resolve()
    if PROJECT_ROOT not in abs_path.parents and PROJECT_ROOT != abs_path:
        raise ValueError(f"Путь {path} выходит за пределы проекта!")
    return abs_path