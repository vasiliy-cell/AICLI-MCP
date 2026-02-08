from pathlib import Path
from typing import List, Dict, Union

def get_tree_structure(root_path: Union[str, Path], max_depth: int, current_depth: 0) -> List[Dict]:
    """
    Возвращает структуру директорий в виде списка словарей для LLM.
    """
    tree_data = []
    root_path = Path(root_path)

    if current_depth > max_depth:
        return []

    try:
            
        # Сортировка: сначала папки, потом файлы
        entries = sorted(root_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return []

    for entry in entries:
        # Пропускаем скрытые файлы/папки (стандарт для MCP)
        if entry.name.startswith('.'):
            continue

        node = {
            "name": entry.name,
            "type": "directory" if entry.is_dir() else "file"
        }

        # Если это папка, рекурсивно собираем её содержимое в ключ 'children'
        if entry.is_dir():
            children = get_tree_structure(entry, max_depth, current_depth + 1)
            if children:
                node["children"] = children
        
        tree_data.append(node)

    return tree_data

# Пример вызова (как это сделал бы сервер MCP)
if __name__ == "__main__":
    # Теперь мы можем передать ЛЮБОЙ путь
    target_dir = "."  # Текущая папка
    result = {
        "root": Path(target_dir).resolve().name,
        "tree": get_tree_structure(target_dir, max_depth=1, current_depth=0)
    }
    
    # В реальности MCP сервер отправит этот JSON модели
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
