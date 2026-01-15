# Architecture & Component Flow

## Component Hierarchy

```
App (Main Component - src/App.jsx)
│
├─ State Management:
│  ├─ tree: Node[]
│  ├─ selectedNodeId: number | null
│  ├─ message: string
│  └─ loading: boolean
│
├─ API Handlers:
│  ├─ fetchTree()
│  ├─ handleSendMessage()
│  ├─ handleClearBranch()
│  └─ handleClearTree()
│
└─ Child Components:
   │
   ├─ <aside> Sidebar
   │  ├─ Title "Conversation Tree"
   │  ├─ <TreeDisplay>
   │  │  └─ <TreeNode> (recursive)
   │  │     ├─ Expand/collapse button
   │  │     ├─ Node button (clickable)
   │  │     ├─ Node ID
   │  │     └─ <TreeNode> (children) [recursive]
   │  │
   │  └─ Refresh Button
   │
   └─ <main> Main Content
      ├─ Title "AI Memory Tree Chat"
      └─ {selectedNode ? (
         │  <NodePanel>
         │  ├─ Node header (ID + depth)
         │  ├─ Prompt section
         │  ├─ Response section
         │  ├─ Message input area
         │  ├─ Send button
         │  └─ Action buttons
         │
         ) : (
            <div> "Select a node..."
         )}
```

## State Flow

```
User clicks node
    ↓
setSelectedNodeId(nodeId)
    ↓
findNodeById(tree, nodeId)
    ↓
Render <NodePanel> with node data
```

## API Call Flow

### 1. Fetch Tree
```
App mounts
    ↓
useEffect(() => fetchTree(), [])
    ↓
GET /tree
    ↓
setTree(data)
    ↓
Render TreeDisplay with tree
```

### 2. Send Message
```
User clicks "Send Message"
    ↓
handleSendMessage()
    ↓
POST /chat {message, parent_id}
    ↓
Backend creates new node
    ↓
Response: {node_id, ...}
    ↓
setSelectedNodeId(node_id)
    ↓
fetchTree() ← update tree
    ↓
TreeDisplay re-renders with new node
```

### 3. Clear Branch
```
User clicks "Clear Current Branch"
    ↓
Confirmation dialog
    ↓
handleClearBranch()
    ↓
DELETE /clear/{node_id}
    ↓
setSelectedNodeId(null)
    ↓
fetchTree() ← refresh tree
    ↓
TreeDisplay re-renders (branch removed)
```

### 4. Clear Tree
```
User clicks "Clear Entire Tree"
    ↓
Confirmation dialog
    ↓
handleClearTree()
    ↓
DELETE /clear
    ↓
setTree([])
    ↓
setSelectedNodeId(null)
    ↓
fetchTree() ← refresh tree
    ↓
Show "No nodes yet"
```

## Data Structure

### Tree Node Format (from backend)
```javascript
{
  id: 1,
  prompt: "User's message",
  response: "LLM response",
  depth: 0,
  parent_id: null,
  children: [
    {
      id: 2,
      prompt: "Next message",
      response: "LLM response",
      depth: 1,
      parent_id: 1,
      children: []
    }
  ]
}
```

## Styling Organization

### Global Styles (src/styles.css)
- Colors and dark theme
- Layout (app-container, sidebar, main)
- Typography and fonts
- Scrollbar styling
- Responsive design

### Component Styles
- `src/styles/TreeNode.css` - Tree sidebar styling
- `src/styles/NodePanel.css` - Main panel styling

## Hook Usage

```javascript
// App.jsx
useState()
  ├─ tree
  ├─ selectedNodeId
  ├─ loading
  └─ message

useEffect()
  └─ fetchTree() on mount
```

## Error Handling

```
API Call
    ↓
try {
  const response = await fetch(...)
  if (!response.ok) throw error
  const data = response.json()
  // Update state
} catch (error) {
  console.error(error)
  alert("User-friendly message")
}
```

## Performance Considerations

1. **Tree Fetching**: Entire tree fetched on mount and after mutations
2. **Node Selection**: Local state, no re-fetch needed
3. **Re-renders**: Only affected components re-render due to React's diffing
4. **Virtual DOM**: Efficient updates with reconciliation
5. **CSS**: No runtime style calculations, pure CSS

## Browser APIs Used

- `fetch()` - HTTP requests
- `JSON.parse()` - Response parsing
- `window.confirm()` - User confirmation
- `alert()` - User notifications
- `console.error()` - Error logging

## Component Props

### TreeNode
```javascript
{
  node: {id, prompt, response, children...},
  isSelected: boolean,
  onSelect: (nodeId) => void
}
```

### TreeDisplay
```javascript
{
  tree: Node[],
  selectedId: number,
  onSelect: (nodeId) => void
}
```

### NodePanel
```javascript
{
  node: Node,
  message: string,
  onMessageChange: (msg) => void,
  onSendMessage: () => void,
  onClearBranch: () => void,
  onClearTree: () => void
}
```

---

**Last Updated**: January 15, 2026
