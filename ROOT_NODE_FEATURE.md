# Root Node Feature

## Overview

The application now has a **fixed root node** that serves as the starting point of the conversation tree.

## Root Node Details

- **Prompt**: "Hi"
- **ID**: Always ID #1 (first node created)
- **Parent**: None (parent_id = null)
- **Depth**: 0
- **Fixed**: Cannot be deleted

## Behavior

### On App Start
When the backend starts:
1. If the database is empty, a default root node with "Hi" message is automatically created
2. The LLM generates a response for the "Hi" message
3. The root node becomes the foundation of the conversation tree

### When Clearing Entire Tree
When you click "Clear Entire Tree":
1. All nodes are deleted from the database
2. A new default root node is automatically recreated
3. The tree starts fresh with the root node

### Protection Against Deletion
The root node is protected:
- ✅ The "Clear Current Branch" button is disabled when viewing the root node
- ✅ A message appears: "This is the root node. It cannot be deleted."
- ✅ Even if you try to delete it via API, the backend prevents it
- ✅ Only "Clear Entire Tree" (which recreates the root) works

## User Experience

### Viewing Root Node
1. Open the app
2. The tree displays with the root node (ID #1, "Hi")
3. Click on the root node in the sidebar
4. Main panel shows:
   - Node #1, Depth 0
   - Prompt: "Hi"
   - Response: (LLM's response to "Hi")
   - Message input to create branches
   - Info: "This is the root node. It cannot be deleted."
   - Only "Clear Entire Tree" button available

### Creating Branches
1. Click the root node
2. Type a message in "Create Branch" section
3. Click "Send Message"
4. New child node is created with parent_id = 1
5. Tree updates to show the new branch
6. You can now create sub-branches from the new node

### Tree Structure
```
Root Node (ID: 1)
├─ Child 1 (ID: 2)
│  ├─ Grandchild 1 (ID: 3)
│  └─ Grandchild 2 (ID: 4)
└─ Child 2 (ID: 5)
   └─ Grandchild 3 (ID: 6)
```

## Implementation Details

### Backend (Python/FastAPI)

**Startup Event** (`src/main.py`):
```python
@app.on_event("startup")
def startup():
    init_db()
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
```

**Clear All Endpoint** (`DELETE /clear`):
```python
@app.delete("/clear")
def clear_all(db: Session = Depends(get_db)):
    db.query(NewMemoryNode).delete()
    db.commit()
    
    # Create a new default root node
    default_prompt = "Hi"
    default_response = generate_response(default_prompt)
    root_node = NewMemoryNode(...)
    db.add(root_node)
    db.commit()
    
    return {"deleted": True, "new_root_created": True}
```

### Frontend (React)

**App.jsx** - Root node protection:
```javascript
const handleClearBranch = async () => {
  // Prevent deletion of root node
  if (selectedNode.parent_id === null && selectedNode.prompt === "Hi") {
    alert("Cannot delete the root node. It's the starting point...");
    return;
  }
  // ... rest of deletion logic
}
```

**NodePanel.jsx** - Conditional UI:
```javascript
{node.parent_id === null && node.prompt === "Hi" ? (
  <div className="root-node-info">
    <p>This is the root node. It cannot be deleted.</p>
  </div>
) : (
  <button className="danger-btn" onClick={onClearBranch}>
    🗑 Clear Current Branch
  </button>
)}
```

## Features

✅ **Root node always exists** - Never an empty tree
✅ **Fixed starting point** - Consistent conversation entry
✅ **Protected from deletion** - Can only be reset via "Clear Entire Tree"
✅ **Auto-generated response** - LLM responds to "Hi" on startup
✅ **Clear visual indication** - UI shows root node status
✅ **Automatic recreation** - After clearing tree, root is recreated

## Example Workflow

1. **Start App**
   - Root node created with "Hi" message
   - Backend: "Hi there! How can I help you today?"

2. **Branch from Root**
   - User: "What is AI?"
   - System creates child node (ID: 2)
   - Backend: "AI is artificial intelligence..."

3. **Branch from Child**
   - User: "Tell me more about machine learning"
   - System creates child of child (ID: 3)
   - Backend provides response with context

4. **Clear and Start Over**
   - User clicks "Clear Entire Tree"
   - All nodes deleted
   - Root node recreated with "Hi"
   - Tree is fresh, ready for new conversation

## Benefits

- **Consistency**: Every session starts the same way
- **Simplicity**: No need to create first node manually
- **Safety**: Can't accidentally delete starting point
- **Clarity**: Clear structure and hierarchy
- **UX**: Better user guidance and understanding

---

**Last Updated**: January 15, 2026
