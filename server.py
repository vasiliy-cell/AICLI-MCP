from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from tools import files, tree, project

API_KEY = os.getenv("DEEPSEEK_KEY")
print("DEEPSEEK_KEY =", API_KEY)  
API_URL = "https://api.deepseek.com/v1/chat/completions"  # проверь, что у тебя именно так

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.get("/get_tree")
def get_tree(depth: int = 2):
    target_dir = "../AICLI"
    return {"tree": tree.get_tree_structure(target_dir, max_depth=depth)}

@app.get("/read_file")
def read_file(path: str):
    target_dir = "../AICLI"
    full_path = os.path.join(target_dir, path)
    return {"content": files.read_file(full_path)}

@app.post("/ask")
def ask_model(req: PromptRequest):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": req.prompt}
        ]
    }

    resp = requests.post(API_URL, headers=headers, json=data)
    resp.raise_for_status()
    print(resp.json())  # смотри, что реально возвращает DeepSeek

    try:
        resp = requests.post(API_URL, headers=headers, json=data)
        resp.raise_for_status()
        resp_json = resp.json()  # вот здесь получаем JSON от API

        if "choices" not in resp_json:
            return {"error": "API returned unexpected response", "response": resp_json}

        return {"answer": resp_json["choices"][0]["message"]["content"]}

    except requests.exceptions.RequestException as e:
        return {"error": str(e), "status_code": getattr(e.response, "status_code", None)}