from pathlib import Path
import re
from typing import List, Dict
from security import sanitize_path

def search(query: str, path: str = ".", regex: bool = False) -> List[Dict]:
    """
    Поиск по файлам в директории path.
    
    Args:
        query: строка или регулярное выражение для поиска
        path: директория или файл, в котором ищем
        regex: если True, query воспринимается как регулярное выражение
    
    Returns:
        Список словарей с результатами:
        [
            {"file": "path/to/file", "line": 3, "text": "строка с совпадением"},
            ...
        ]
    """
    path = sanitize_path(path)  # безопасный путь внутри проекта
    results = []

    # Если это один файл
    if path.is_file():
        _search_file(path, query, regex, results)
    else:
        # Рекурсивно проходим по всем файлам в директории
        for p in path.rglob("*"):
            if p.is_file() and not p.name.startswith("."):  # пропускаем скрытые
                _search_file(p, query, regex, results)
    
    return results

def _search_file(file_path: Path, query: str, regex: bool, results: List[Dict]):
    """
    Внутренний поиск по одному файлу
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                if regex:
                    if re.search(query, line):
                        results.append({"file": str(file_path), "line": lineno, "text": line.rstrip()})
                else:
                    if query in line:
                        results.append({"file": str(file_path), "line": lineno, "text": line.rstrip()})
    except (UnicodeDecodeError, PermissionError):
        # Файл не читаем — пропускаем
        pass