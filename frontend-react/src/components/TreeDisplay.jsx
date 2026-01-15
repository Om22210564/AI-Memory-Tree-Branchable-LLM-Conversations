import TreeNode from "./TreeNode";

export default function TreeDisplay({ tree, selectedId, onSelect }) {
  return (
    <div className="tree-container">
      {tree.map((root) => (
        <TreeNode
          key={root.id}
          node={root}
          isSelected={selectedId === root.id}
          onSelect={onSelect}
        />
      ))}
    </div>
  );
}
