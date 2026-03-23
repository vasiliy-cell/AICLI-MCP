def get_project_summary():
    return {
        "languages": ["Python", "Rust", "JS/TS"],
        "entrypoints": {
            "python": "python/ai_service.py",
            "rust": "src-tauri/src/main.rs"
        },
        "subsystems": [
            {"name": "Python AI service", "description": "Центральный AI API Hub"},
            {"name": "Rust PTY bridge", "description": "Связь с терминалом и системные вызовы"},
            {"name": "Frontend", "description": "Интерфейс на xterm.js + Tauri"}
        ]
    }