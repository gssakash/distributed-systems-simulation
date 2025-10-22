import streamlit as st
import time
import random

def show_raft_simulation(nodes):
    st.header("Raft Consensus (Simulated Leader Election)")
    st.markdown("Simulates Raft's core: **Leader Election** and **Log Replication** (non-Byzantine). Raft requires a simple majority ($N/2 + 1$) for consensus.")
    
    # Raft-specific state
    if 'raft_leader' not in st.session_state: st.session_state.raft_leader = 1
    if 'raft_term' not in st.session_state: st.session_state.raft_term = 1
    if 'raft_log' not in st.session_state: st.session_state.raft_log = {}

    def elect_new_leader():
        st.session_state.raft_term += 1
        active_nodes = [node.node_id for node in nodes if node.is_active]
        if not active_nodes:
            st.error("Cannot elect a leader: No active nodes!")
            st.session_state.raft_leader = None
            return

        # Simple random election (simulating the randomized timeouts of Raft)
        new_leader = random.choice(active_nodes)
        st.session_state.raft_leader = new_leader
        st.success(f"🚨 Term {st.session_state.raft_term}: Node {new_leader} elected as the new LEADER!")

    def replicate_log(key, value):
        leader_id = st.session_state.raft_leader
        if leader_id is None:
            st.error("No leader is currently elected. Cannot commit log.")
            return

        # Raft requires majority consensus (N/2 + 1) for COMMIT
        majority = len(nodes) // 2 + 1 
        replication_count = 0
        
        st.info(f"Leader (Node {leader_id}) is appending log entry {key} to its log.")
        
        # 1. Append to Leader's local log
        log_entry = {'term': st.session_state.raft_term, 'command': f"SET {key} = '{value}'"}
        st.session_state.raft_log[str(key)] = log_entry
        replication_count += 1

        # 2. Send AppendEntries RPC to followers (simulated)
        for node in nodes:
            if node.is_active and node.node_id != leader_id:
                time.sleep(0.05)
                st.success(f"✅ Follower Node {node.node_id} acknowledges log entry {key}.")
                replication_count += 1
                
        if replication_count >= majority:
            st.balloons()
            st.success(f"🎉 Log Entry {key} Committed! Replicated by {replication_count}/{len(nodes)} nodes (Majority: {majority}).")
            # In a real Raft, the state machine (SQLite) would now be updated.
            # We simulate the final commit to the SQLite storage on the leader/followers
            for node in nodes:
                 if node.is_active:
                    node.process_transaction(key, value, is_byzantine_op=False)
        else:
            st.error(f"🛑 Log replication failed. Only {replication_count} responses received (Need {majority}).")


    st.subheader(f"Current State: Term {st.session_state.raft_term}, Leader: Node {st.session_state.raft_leader}")

    if st.button("Trigger New Election (Simulate Timeout)", use_container_width=True):
        elect_new_leader()

    st.subheader("Log Replication (Write Operation)")
    key = st.number_input("Log Key", min_value=1, value=10, step=1, key="raft_log_key")
    value = st.text_input("Log Command Value", "Raft Log Entry", key="raft_log_value")

    if st.button("Replicate Log Entry", use_container_width=True, disabled=(st.session_state.raft_leader is None)):
        replicate_log(key, value)
    
    st.divider()
    st.subheader("Simulated Cluster Logs")
    st.json(st.session_state.raft_log)
