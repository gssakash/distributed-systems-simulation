import streamlit as st
from distributed_systems_simulator.components.cluster_node import ClusterNode
from simulation_algorithms.bft import show_bft_simulation
from simulation_algorithms.raft import show_raft_simulation
from simulation_algorithms.sync import show_sync_simulation
from simulation_algorithms.bloom_filter import show_bloom_filter_demo

def main():
    st.set_page_config(layout="wide", page_title="Distributed Systems Simulator")
    st.title("Comprehensive Distributed Systems Simulator")
    
    if 'nodes' not in st.session_state:
        st.session_state.nodes = [
            ClusterNode(1), ClusterNode(2), ClusterNode(3), ClusterNode(4)
        ]
        st.session_state.key_to_read = 1
        st.session_state.current_page = "BFT Consensus"

    page = st.sidebar.radio(
        "Select Algorithm/Concept",
        [
            "BFT Consensus", 
            "Raft Consensus", 
            "Distributed Synchronization", 
            "Bloom Filter Demo"
        ],
        key="page_selection"
    )
    
    st.sidebar.divider()
    st.sidebar.header("Fault Injection (Shared)")
    
    for node in st.session_state.nodes:
        is_active = st.sidebar.checkbox(
            f"Node {node.node_id} Status: Active", 
            value=node.is_active, 
            key=f"status_{node.node_id}"
        )
        node.is_active = is_active

        if page == "BFT Consensus":
            is_byzantine = st.sidebar.checkbox(
                f"Node {node.node_id} (😈 Byzantine)", 
                value=node.is_byzantine, 
                key=f"byzantine_{node.node_id}",
                disabled=not node.is_active
            )
            node.is_byzantine = is_byzantine
            status_icon = "🟢"
            if node.is_byzantine: status_icon = "😈"
            elif not node.is_active: status_icon = "🔴"
            st.sidebar.markdown(f"**Node {node.node_id}:** {status_icon}")
        else:
            if not node.is_active: 
                st.sidebar.markdown(f"**Node {node.node_id}:** 🔴 CRASHED")
            else:
                st.sidebar.markdown(f"**Node {node.node_id}:** 🟢 ACTIVE")
    
    # Route to simulation
    if page == "BFT Consensus":
        show_bft_simulation(st.session_state.nodes)
    elif page == "Raft Consensus":
        show_raft_simulation(st.session_state.nodes)
    elif page == "Distributed Synchronization":
        show_sync_simulation(st.session_state.nodes)
    elif page == "Bloom Filter Demo":
        show_bloom_filter_demo()

if __name__ == "__main__":
    main()
