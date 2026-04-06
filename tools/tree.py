from pathlib import Path
from typing import List, Dict, Union

def get_tree_structure(
    root_path: Union[str, Path],
    max_depth: int,
    current_depth: int = 0,
    exclude_dirs: List[str] = None
) -> List[Dict]:
    """
    Возвращает структуру директорий проекта в виде списка словарей для LLM,
    пропуская ненужные папки.
    """
    if exclude_dirs is None:
        exclude_dirs = ["node_modules", "target", "__pycache__"]

    tree_data = []
    root_path = Path(root_path)

    if current_depth > max_depth:
        return []

    try:
        entries = sorted(root_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return []

    for entry in entries:
        # Пропускаем скрытые и исключённые папки
        if entry.name.startswith('.') or entry.name in exclude_dirs:
            continue

        node = {
            "name": entry.name,
            "type": "directory" if entry.is_dir() else "file"
        }

        if entry.is_dir():
            children = get_tree_structure(entry, max_depth, current_depth + 1, exclude_dirs)
            if children:
                node["children"] = children

        tree_data.append(node)

    return tree_data

# Пример вызова
if __name__ == "__main__":
    import json

    target_dir = "../AICLI"  # путь к проекту
    result = {
        "root": Path(target_dir).resolve().name,
        "tree": get_tree_structure(target_dir, max_depth=2)
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))