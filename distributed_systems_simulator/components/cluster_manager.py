import json
import streamlit as st
import time

class ClusterManager:
    def __init__(self, nodes):
        self.nodes = nodes
        self.consensus_quorum = 3 
        self.total_nodes = len(nodes)

    def read_key(self, key):
        responses = {}
        successful_reads = 0
        for node in self.nodes:
            try:
                state = node.get_state()
                state_str = json.dumps(state, sort_keys=True)
                if state_str not in responses: responses[state_str] = []
                responses[state_str].append(node.node_id)
                successful_reads += 1
            except ConnectionError:
                pass
        
        if successful_reads < self.consensus_quorum:
            st.warning(f"❌ Read failed: Need {self.consensus_quorum} for QC.")
            return None, responses
            
        if len(responses) > 1:
            st.error("🚨 MAJOR CONSISTENCY FAILURE DETECTED! (Different states received)")
            return None, responses

        state_str = list(responses.keys())[0]
        state = json.loads(state_str)
        key_str = str(key) 
        if key_str in state:
            return state[key_str], responses
        else:
            return f"Key '{key}' not found.", responses
            
    def write_key(self, key, value):
        success_count = 0
        st.info(f"🔑 PROPOSE: Leader sends transaction (SET {key} = '{value}')")
        time.sleep(0.1)

        for node in self.nodes:
            if node.is_active:
                try:
                    status = node.process_transaction(key, value, is_byzantine_op=True)
                    if status == "COMMITTED":
                        st.success(f"✅ Node {node.node_id} Committed.")
                        success_count += 1
                    elif status == "CORRUPTED":
                        st.error(f"😈 Node {node.node_id} is BYZANTINE! Committed corrupted data.")
                        success_count += 1 
                except ConnectionError:
                    st.error(f"❌ Node {node.node_id} crashed.")
                except Exception as e:
                    st.error(f"❌ Node {node.node_id} error: {e}")
            else:
                st.warning(f"⚠️ Node {node.node_id} inactive.")

        if success_count >= self.consensus_quorum:
            st.balloons()
            st.markdown(f"## 🎉 DECIDE SUCCESSFUL! QC Achieved ({success_count}/{self.total_nodes})")
            return True
        else:
            st.error(f"## 🛑 DECIDE FAILED! Quorum ({self.consensus_quorum}) not met.")
            return False
