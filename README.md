# 🌐 Distributed Systems Simulator (Streamlit Edition)

This project is a single-file, interactive web application built with **Streamlit** and **Python**. It is designed to simulate the core logic and fault-tolerance principles of several foundational distributed systems algorithms.

The goal is to provide a safe, runnable environment to test scenarios like **Byzantine faults**, **Raft leader election**, and **atomic transactions** without the need for complex network setup.

---

## 1. Current Status: Interactive Simulation

The entire application runs as a single Python process, simulating inter-node communication via **function calls** and using isolated **SQLite files** for local node persistence.

---

## 🧩 Prerequisites

You only need Streamlit installed:

```
pip install streamlit
```

---

## ⚙️ Execution

Save the provided code as **bft_simulation.py** and run the application from your terminal:

```
streamlit run bft_simulation.py
```
