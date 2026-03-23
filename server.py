from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

from tools import files, tree, project
from security import sanitize_path

app = FastAPI()

class MCPRequest(BaseModel):
    tool: str
    args: dict

@app.post("/mcp")
def handle_request(req: MCPRequest):
    try:
        if req.tool == "read_file":
            path = sanitize_path(req.args["path"])
            return {"status": "ok", "result": files.read_file(path)}
        elif req.tool == "list_dir":
            path = sanitize_path(req.args.get("path", "."))
            return {"status": "ok", "result": files.list_dir(path)}
        elif req.tool == "get_tree":
            path = sanitize_path(req.args.get("path", "."))
            depth = req.args.get("depth", 3)
            return {"status": "ok", "result": tree.get_tree_structure(path, depth)}
        elif req.tool == "get_project_summary":
            return {"status": "ok", "result": project.get_project_summary()}
        else:
            raise HTTPException(status_code=400, detail="Unknown tool")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))