from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from .db import SessionLocal, init_db
from .models import NewMemoryNode
from .groq_client import generate_response, summarize_node
from sqlalchemy.orm import Session
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    parent_id: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    node_id: int
    parent_id: Optional[int]
    depth: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def build_tree(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Build nested tree from flat node list."""
    by_id = {n['id']: dict(n, children=[]) for n in nodes}
    roots = []
    for n in by_id.values():
        pid = n.get('parent_id')
        if pid is None:
            roots.append(n)
        else:
            parent = by_id.get(pid)
            if parent:
                parent['children'].append(n)
            else:
                roots.append(n)
    return roots


@app.on_event("startup")
def startup():
    # initialize DB, recreating tables if schema changed
    init_db()
    
    # Create default root node if tree is empty
    db = SessionLocal()
    try:
        node_count = db.query(NewMemoryNode).count()
        if node_count == 0:
            default_prompt = "Hi"
            default_response = generate_response(default_prompt)
            root_node = NewMemoryNode(
                prompt=default_prompt,
                response=default_response,
                parent_id=None,
                depth=0,
                timestamp=datetime.datetime.utcnow(),
            )
            db.add(root_node)
            db.commit()
    finally:
        db.close()


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    # Determine depth and fetch parent context
    parent = None
    if req.parent_id is not None:
        parent = db.query(NewMemoryNode).filter(NewMemoryNode.id == req.parent_id).first()
        if parent is None:
            raise HTTPException(status_code=404, detail="parent_id not found")
        depth = parent.depth + 1
    else:
        depth = 0

    # Build prompt with parent context
    prompt = req.message
    if parent:
        # Check if parent context is too long (> 250 chars)
        parent_context = f"Q: {parent.prompt}\nA: {parent.response}"
        if len(parent_context) > 250:
            # Use summary if available, otherwise create one
            if parent.summary is None or parent.summary.strip() == "":
                # Generate summary and store it
                parent.summary = summarize_node(parent.prompt, parent.response)
                db.add(parent)
                db.commit()
            context_to_use = parent.summary
        else:
            context_to_use = parent_context
        
        context = f"Previous context:\n{context_to_use}\n\nNow, answer this:\n{prompt}"
    else:
        context = prompt

    # Call LLM with context-aware prompt
    llm_response = generate_response(context)

    node = NewMemoryNode(
        prompt=prompt,
        response=llm_response,
        parent_id=req.parent_id,
        depth=depth,
        timestamp=datetime.datetime.utcnow(),
    )
    db.add(node)
    db.commit()
    db.refresh(node)

    return ChatResponse(response=node.response, node_id=node.id, parent_id=node.parent_id, depth=node.depth)


@app.get("/nodes")
def get_nodes(db: Session = Depends(get_db)):
    nodes = db.query(NewMemoryNode).order_by(NewMemoryNode.id).all()
    return [n.to_dict() for n in nodes]


@app.get("/tree")
def get_tree(db: Session = Depends(get_db)):
    nodes = db.query(NewMemoryNode).order_by(NewMemoryNode.id).all()
    flat = [n.to_dict() for n in nodes]
    return build_tree(flat)


def _gather_descendants(flat_nodes: List[Dict[str, Any]], target_id: int) -> List[int]:
    children_map = {}
    for n in flat_nodes:
        pid = n.get('parent_id')
        children_map.setdefault(pid, []).append(n['id'])

    to_delete = []
    stack = [target_id]
    while stack:
        cur = stack.pop()
        to_delete.append(cur)
        for c in children_map.get(cur, []):
            stack.append(c)
    return to_delete


@app.delete("/clear")
def clear_all(db: Session = Depends(get_db)):
    # delete all nodes
    db.query(NewMemoryNode).delete()
    db.commit()
    
    # Create a new default root node
    default_prompt = "Hi"
    default_response = generate_response(default_prompt)
    root_node = NewMemoryNode(
        prompt=default_prompt,
        response=default_response,
        parent_id=None,
        depth=0,
        timestamp=datetime.datetime.utcnow(),
    )
    db.add(root_node)
    db.commit()
    
    return {"deleted": True, "new_root_created": True}


@app.delete("/clear/{node_id}")
def clear_subtree(node_id: int, db: Session = Depends(get_db)):
    nodes = db.query(NewMemoryNode).all()
    flat = [n.to_dict() for n in nodes]
    ids = _gather_descendants(flat, node_id)
    if not ids:
        raise HTTPException(status_code=404, detail="node not found")
    db.query(NewMemoryNode).filter(NewMemoryNode.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return {"deleted_ids": ids}
