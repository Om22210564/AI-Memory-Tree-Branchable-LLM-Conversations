import { useState } from "react";
import "../styles/TreeNode.css";

export default function TreeNode({ node, isSelected, onSelect }) {
  const [expanded, setExpanded] = useState(true);

  const hasChildren = node.children && node.children.length > 0;
  const preview = node.prompt ? node.prompt.substring(0, 40) + (node.prompt.length > 40 ? "..." : "") : "(no prompt)";

  return (
    <div className={`tree-item ${isSelected ? "selected" : ""}`}>
      <div className="tree-item-header">
        {hasChildren && (
          <button
            className="expand-btn"
            onClick={() => setExpanded(!expanded)}
          >
            {expanded ? "▼" : "▶"}
          </button>
        )}
        {!hasChildren && <span className="no-expand"></span>}
        <button className="node-button" onClick={() => onSelect(node.id)}>
          {preview}
        </button>
        <span className="node-id">#{node.id}</span>
      </div>

      {hasChildren && expanded && (
        <div className="tree-children">
          {node.children.map((child) => (
            <TreeNode
              key={child.id}
              node={child}
              isSelected={isSelected}
              onSelect={onSelect}
            />
          ))}
        </div>
      )}
    </div>
  );
}
