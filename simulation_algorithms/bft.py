import streamlit as st
import json
import time
from distributed_systems_simulator.components.cluster_manager import ClusterManager

def show_bft_simulation(nodes):
    st.header("BFT Consensus (HoneyBadger Principle)")
    st.markdown("Simulates an **$N=4$ cluster** tolerating $f=1$ Byzantine fault. Requires **3 votes** ($2f+1$) for a Quorum Certificate (QC).")

    manager = ClusterManager(nodes)
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Write (SET) Operation")
        key = st.number_input("Enter Key", min_value=1, value=4, step=1, key="bft_write_key")
        value = st.text_input("Enter New Value", "HBBFT NEW SQL VALUE", key="bft_write_value")

        if st.button("Commit Transaction (Write)", use_container_width=True, type="primary"):
            st.info("BFT Atomic Broadcast Log:")
            with st.spinner("PROPOSE and Awaiting Quorum Certificate..."):
                manager.write_key(key, value)

    with col2:
        st.subheader("2. Read (GET) Operation")
        if 'key_to_read' not in st.session_state:
             st.session_state.key_to_read = 1
             
        read_key = st.number_input("Enter Key to Read", min_value=1, value=st.session_state.key_to_read, step=1, key="bft_read_key_input")
        
        if st.button("Execute Read Consensus", use_container_width=True):
            st.session_state.key_to_read = read_key
            st.info("Read Log:")
            
            with st.spinner("Querying Quorum..."):
                result, responses = manager.read_key(read_key)
                
            if result is not None:
                st.success(f"✅ FINALIZED Read Result for Key `{read_key}`: `{result}`")
            
            st.subheader("Node Responses:")
            for state_str, responding_nodes in responses.items():
                state = json.loads(state_str)
                st.json(state)
                st.markdown(f"Reported by Nodes: **{', '.join(map(str, responding_nodes))}**")

    st.divider()
    st.subheader("Cluster State Snapshot")
    col_nodes = st.columns(4) 

    for i, node in enumerate(nodes):
        with col_nodes[i]:
            if node.is_byzantine:
                st.markdown(f"### Node {node.node_id} (😈)")
            elif node.is_active:
                st.markdown(f"### Node {node.node_id} (🟢)")
            else:
                st.markdown(f"### Node {node.node_id} (🔴)")
                
            try:
                if node.is_active:
                    if node.node_id == 1:
                        st.markdown("**LEADER**")
                    st.json(node.get_state())
            except ConnectionError:
                st.warning("Node is inactive.")
