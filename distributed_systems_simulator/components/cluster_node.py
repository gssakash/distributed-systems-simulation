import sqlite3
import time

class ClusterNode:
    """
    Simulates a single node in the distributed cluster, using SQLite for storage.
    """
    def __init__(self, node_id, is_active=True, is_byzantine=False):
        self.node_id = node_id
        self.db_name = f"node_{node_id}_db.sqlite"
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        self.is_active = is_active
        self.is_byzantine = is_byzantine
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS key_value (
                key INTEGER PRIMARY KEY,
                value TEXT
            );
        """)
        
        self.cursor.execute("SELECT value FROM key_value WHERE key = 1")
        if self.cursor.fetchone() is None:
            initial_value = f"Initial SQL Value for Node {node_id}"
            self.cursor.execute("INSERT INTO key_value (key, value) VALUES (?, ?)", (1, initial_value))
            self.conn.commit()

    def get_state(self):
        """Returns the current state of the database as a dictionary."""
        if not self.is_active:
            raise ConnectionError(f"Node {self.node_id} is crashed/inactive.")
        
        self.cursor.execute("SELECT key, value FROM key_value")
        rows = self.cursor.fetchall()
        return {str(k): v for k, v in rows}

    def process_transaction(self, key, value, is_byzantine_op=False):
        """Processes a write, applying corruption if set to Byzantine."""
        if not self.is_active:
            raise ConnectionError(f"Node {self.node_id} is crashed/inactive. Transaction rejected.")
        
        import time
        if is_byzantine_op and self.is_byzantine:
            corrupt_value = f"CORRUPTED BY NODE {self.node_id} @ {time.time()}" 
            self.cursor.execute("INSERT OR REPLACE INTO key_value (key, value) VALUES (?, ?)", (key, corrupt_value))
            self.conn.commit()
            return "CORRUPTED"
        
        self.cursor.execute("INSERT OR REPLACE INTO key_value (key, value) VALUES (?, ?)", (key, value))
        self.conn.commit()
        return "COMMITTED"
