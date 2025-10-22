import streamlit as st
import time
import random

def show_sync_simulation(nodes):
    st.header("Distributed Synchronization (2-Phase Commit)")
    st.markdown("Simulates a **Two-Phase Commit (2PC)** protocol across clusters to ensure **atomicity**. Atomicity means a transaction either commits everywhere or aborts everywhere.")

    def run_2pc(key, value):
        active_nodes = [node for node in nodes if node.is_active]
        if not active_nodes:
            st.error("No active nodes for 2PC.")
            return

        # Phase 1: VOTE Request
        st.subheader("Phase 1: VOTE Request (PREPARE)")
        can_commit = True
        
        for node in active_nodes:
            time.sleep(0.05)
            # Simulate a random failure during the vote phase (15% chance of ABORT)
            if random.random() < 0.15:
                st.error(f"❌ Coordinator: Node {node.node_id} ABORTED (Simulated network/local failure).")
                can_commit = False
                break
            st.success(f"✅ Node {node.node_id}: Voted YES (Prepared to commit).")

        # Phase 2: Global Decision
        st.subheader("Phase 2: Global Decision (COMMIT/ABORT)")

        if can_commit:
            st.balloons()
            st.success("🎉 GLOBAL COMMIT: All nodes voted YES. Sending COMMIT message.")
            for node in active_nodes:
                node.process_transaction(key, value, is_byzantine_op=False) # Commit the change
                st.info(f"✅ Node {node.node_id}: COMMIT successful (State updated in SQLite).")
        else:
            st.error("🛑 GLOBAL ABORT: At least one node voted NO or failed. Sending ABORT message.")
            for node in active_nodes:
                # In a real 2PC, nodes would rollback here. We just log the abort.
                st.warning(f"⚠️ Node {node.node_id}: ABORTED and rolled back.")

    st.subheader("2PC Transaction")
    key = st.number_input("Transaction Key", min_value=1, value=20, step=1, key="sync_key")
    value = st.text_input("Transaction Value", "2PC Atomic Transaction", key="sync_value")
    
    if st.button("Run 2-Phase Commit", use_container_width=True, type="primary"):
        run_2pc(key, value)
