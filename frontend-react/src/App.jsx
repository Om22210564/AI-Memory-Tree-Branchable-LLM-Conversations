import { useState, useEffect } from "react";
import TreeDisplay from "./components/TreeDisplay";
import NodePanel from "./components/NodePanel";
import "./styles.css";

const BACKEND_URL = "http://localhost:8000";

export default function App() {
  const [tree, setTree] = useState([]);
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const fetchTree = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/tree`);
      if (response.ok) {
        const data = await response.json();
        setTree(data);
      } else {
        console.error("Failed to fetch tree");
      }
    } catch (error) {
      console.error("Error fetching tree:", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchTree();
  }, []);

  const findNodeById = (nodes, id) => {
    for (const node of nodes) {
      if (node.id === id) return node;
      const found = findNodeById(node.children || [], id);
      if (found) return found;
    }
    return null;
  };

  const selectedNode = selectedNodeId ? findNodeById(tree, selectedNodeId) : null;

  const handleSendMessage = async () => {
    if (!message.trim()) {
      alert("Message cannot be empty");
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: message,
          parent_id: selectedNode.id,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessage("");
        setSelectedNodeId(data.node_id);
        await fetchTree();
      } else {
        alert("Failed to send message");
      }
    } catch (error) {
      console.error("Error sending message:", error);
      alert("Error sending message");
    }
  };

  const handleClearBranch = async () => {
    // Prevent deletion of root node with "Hi" message
    if (selectedNode.parent_id === null && selectedNode.prompt === "Hi") {
      alert("Cannot delete the root node. It's the starting point of the conversation tree.");
      return;
    }

    if (!window.confirm("Delete this branch and all its children?")) return;

    try {
      const response = await fetch(`${BACKEND_URL}/clear/${selectedNode.id}`, {
        method: "DELETE",
      });

      if (response.ok) {
        setSelectedNodeId(null);
        await fetchTree();
        alert("Branch deleted");
      } else {
        alert("Failed to delete branch");
      }
    } catch (error) {
      console.error("Error deleting branch:", error);
      alert("Error deleting branch");
    }
  };

  const handleClearTree = async () => {
    if (!window.confirm("Delete entire tree? This cannot be undone.")) return;

    try {
      const response = await fetch(`${BACKEND_URL}/clear`, {
        method: "DELETE",
      });

      if (response.ok) {
        setTree([]);
        setSelectedNodeId(null);
        await fetchTree();
        alert("Tree cleared");
      } else {
        alert("Failed to clear tree");
      }
    } catch (error) {
      console.error("Error clearing tree:", error);
      alert("Error clearing tree");
    }
  };

  return (
    <div className="app-container">
      <aside className="sidebar">
        <h2>Conversation Tree</h2>
        {loading && <p className="loading">Loading...</p>}
        {!loading && tree.length === 0 && (
          <p className="empty-tree">No nodes yet</p>
        )}
        {!loading && tree.length > 0 && (
          <TreeDisplay tree={tree} selectedId={selectedNodeId} onSelect={setSelectedNodeId} />
        )}
        <button className="refresh-btn" onClick={fetchTree}>
          ↻ Refresh Tree
        </button>
      </aside>

      <main className="main-content">
        <h1>AI Memory Tree Chat — Prototype</h1>

        {!selectedNode ? (
          <div className="no-selection">
            <p>Select a node from the tree to view its response or branch from it.</p>
          </div>
        ) : (
          <NodePanel
            node={selectedNode}
            message={message}
            onMessageChange={setMessage}
            onSendMessage={handleSendMessage}
            onClearBranch={handleClearBranch}
            onClearTree={handleClearTree}
          />
        )}
      </main>
    </div>
  );
}
