import streamlit as st
import hashlib

# Simple Bloom Filter simulation (inspired by bloom-filter library concept)
class SimpleBloomFilter:
    def __init__(self, size=30, num_hashes=3):
        self.size = size
        self.bit_array = [False] * size
        self.num_hashes = num_hashes

    def _hash(self, item, seed):
        # A simple hashing function using built-in hashlib
        s = hashlib.sha256(f"{item}-{seed}".encode()).hexdigest()
        return int(s, 16) % self.size

    def add(self, item):
        for i in range(self.num_hashes):
            index = self._hash(item, i)
            self.bit_array[index] = True

    def check(self, item):
        for i in range(self.num_hashes):
            index = self._hash(item, i)
            if not self.bit_array[index]:
                return False  # Definitely not present
        return True # Potentially present (false positive possible)

def show_bloom_filter_demo():
    st.header("Bloom Filter Demonstration")
    st.markdown("Simulates a **Bloom Filter**, a probabilistic structure used for checking set membership quickly (related to data indexing/caching).")
    
    if 'bloom_filter' not in st.session_state or 'bloom_items' not in st.session_state:
        st.session_state.bloom_filter = SimpleBloomFilter(size=30, num_hashes=3)
        st.session_state.bloom_items = set()

    bf = st.session_state.bloom_filter

    col_add, col_check = st.columns(2)

    with col_add:
        st.subheader("Add Item")
        new_item = st.text_input("Item to Add (e.g., 'user_123')", key="bf_add_item", value="")
        if st.button("Add to Filter", use_container_width=True, disabled=not new_item):
            bf.add(new_item)
            st.session_state.bloom_items.add(new_item)
            st.success(f"Added '{new_item}'.")

    with col_check:
        st.subheader("Check Item")
        check_item = st.text_input("Item to Check", key="bf_check_item", value="user_999")
        if st.button("Check Filter", use_container_width=True, disabled=not check_item):
            if bf.check(check_item):
                if check_item in st.session_state.bloom_items:
                    st.success(f"✅ Item '{check_item}' is definitely present. (True Positive)")
                else:
                    st.error(f"⚠️ **FALSE POSITIVE:** Item '{check_item}' is reported as present, but was never added! (Probabilistic nature).")
            else:
                st.info(f"❌ Item '{check_item}' is definitely NOT present. (True Negative)")

    st.divider()
    st.subheader("Bloom Filter State")
    st.markdown(f"**Filter Size:** {bf.size} bits | **Hash Functions:** {bf.num_hashes}")
    st.markdown(f"**Items Added:** {st.session_state.bloom_items}")
    
    # Visualize the bit array
    bit_str = "".join(["1" if b else "0" for b in bf.bit_array])
    st.code(bit_str)
