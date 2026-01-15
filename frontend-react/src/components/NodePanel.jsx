import "../styles/NodePanel.css";

export default function NodePanel({
  node,
  message,
  onMessageChange,
  onSendMessage,
  onClearBranch,
  onClearTree,
}) {
  return (
    <div className="node-panel">
      <div className="node-header">
        <h2>Node #{node.id}</h2>
        <span className="node-depth">Depth: {node.depth || 0}</span>
      </div>

      <div className="node-section">
        <h3>Prompt</h3>
        <div className="node-content">{node.prompt}</div>
      </div>

      <div className="node-section">
        <h3>Response</h3>
        <div className="node-content">{node.response}</div>
      </div>

      <hr />

      <div className="node-section">
        <h3>Create Branch</h3>
        <p>Send a new message from this node:</p>
        <textarea
          className="message-input"
          value={message}
          onChange={(e) => onMessageChange(e.target.value)}
          placeholder="Type your message here..."
          rows="5"
        />
        <button className="send-btn" onClick={onSendMessage}>
          Send Message
        </button>
      </div>

      <hr />

      <div className="node-section">
        <h3>Actions</h3>
        <div className="action-buttons">
          {node.parent_id === null && node.prompt === "Hi" ? (
            <div className="root-node-info">
              <p>This is the root node. It cannot be deleted.</p>
            </div>
          ) : (
            <button className="danger-btn" onClick={onClearBranch}>
              🗑 Clear Current Branch
            </button>
          )}
          <button className="danger-btn critical" onClick={onClearTree}>
            🗑 Clear Entire Tree
          </button>
        </div>
      </div>
    </div>
  );
}
