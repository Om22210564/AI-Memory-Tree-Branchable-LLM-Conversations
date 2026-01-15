import streamlit as st
import httpx
from typing import List, Dict

# BACKEND_URL = st.secrets.get("backend_url", "http://localhost:8000")
BACKEND_URL = "http://localhost:8000"


def short_preview(text: str, length: int = 40) -> str:
    return (text[:length] + "...") if len(text) > length else text


def fetch_tree():
    try:
        r = httpx.get(f"{BACKEND_URL}/tree", timeout=10.0)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Failed to fetch tree: {e}")
        return []


def render_node(node: Dict, indent: int = 0):
    indent_str = " " * (indent * 4)
    label = short_preview(node.get("prompt", "(no prompt)"))
    key = f"node-{node['id']}"
    cols = st.columns([1, 8, 1])
    with cols[1]:
        if st.button(label, key=key):
            st.session_state.selected_node = node['id']
    with cols[2]:
        st.write(f"`#{node['id']}`")

    # show children indented
    for child in node.get("children", []):
        render_node(child, indent + 1)


def find_node_by_id(tree: List[Dict], node_id: int):
    stack = list(tree)
    while stack:
        n = stack.pop()
        if n['id'] == node_id:
            return n
        stack.extend(n.get('children', []))
    return None


def main():
    st.title("AI Memory Tree Chat — Prototype")

    if 'selected_node' not in st.session_state:
        st.session_state.selected_node = None

    tree = fetch_tree()

    st.sidebar.header("Conversation Tree")
    if not tree:
        st.sidebar.write("No nodes yet")
    else:
        for root in tree:
            render_node(root)

    st.sidebar.button("Refresh Tree", on_click=lambda: st.rerun())

    # Main area
    st.header("Selected Node")
    if st.session_state.selected_node is None:
        st.info("Select a node from the tree to view its response or branch from it.")
    else:
        node = find_node_by_id(tree, st.session_state.selected_node)
        if node is None:
            st.error("Selected node not found (it may have been deleted). Refresh tree.")
        else:
            st.subheader(f"Node #{node['id']} — depth {node.get('depth', 0)}")
            st.markdown("**Prompt:**")
            st.write(node.get('prompt'))
            st.markdown("**Response:**")
            st.write(node.get('response'))

            # Input for new message branching from this node
            st.markdown("---")
            st.markdown("**Send a new message from this node (create branch):**")
            message = st.text_area("Message", key="message_input")
            if st.button("Send Message"):
                if not message.strip():
                    st.warning("Message cannot be empty")
                else:
                    try:
                        payload = {"message": message, "parent_id": node['id']}
                        r = httpx.post(f"{BACKEND_URL}/chat", json=payload, timeout=30.0)
                        r.raise_for_status()
                        data = r.json()
                        st.success("Message sent — new node created")
                        # update selection to new node
                        st.session_state.selected_node = data.get('node_id')
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to send message: {e}")

            st.markdown("---")
            # Branch deletion
            if st.button("Clear Current Branch"):
                try:
                    r = httpx.delete(f"{BACKEND_URL}/clear/{node['id']}", timeout=20.0)
                    r.raise_for_status()
                    st.success("Branch deleted")
                    st.session_state.selected_node = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to delete branch: {e}")

    # Global clear
    st.markdown("---")
    if st.button("Clear Entire Tree"):
        try:
            r = httpx.delete(f"{BACKEND_URL}/clear", timeout=20.0)
            r.raise_for_status()
            st.success("All nodes deleted")
            st.session_state.selected_node = None
            st.rerun()
        except Exception as e:
            st.error(f"Failed to clear tree: {e}")


if __name__ == "__main__":
    main()
