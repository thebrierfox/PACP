import json
import hashlib
import time
from datetime import datetime
from collections import deque

class PACP:
    def __init__(self):
        self.project_state = {}
        self.version_history = deque(maxlen=100)  # Stores past versions for rollback
        self.timestamp = lambda: datetime.utcnow().isoformat()

    def update_state(self, key, value):
        """Updates project state with contradiction resolution and versioning."""
        if key in self.project_state and self.project_state[key] != value:
            print(f"🔄 Resolving contradiction for {key}: '{self.project_state[key]}' -> '{value}'")
        self._save_version()  # Save previous state before modifying
        self.project_state[key] = value
        self.project_state["_last_updated"] = self.timestamp()
        self._generate_hash()

    def _save_version(self):
        """Stores a snapshot of the current project state before any updates."""
        snapshot = json.dumps(self.project_state, sort_keys=True)
        version_hash = hashlib.sha256(snapshot.encode()).hexdigest()
        self.version_history.append((version_hash, self.project_state.copy()))

    def rollback(self, steps=1):
        """Rolls back the project state by a given number of steps."""
        if steps > len(self.version_history):
            print("⚠️ Not enough history to roll back that far.")
            return
        _, previous_state = self.version_history[-steps]
        self.project_state = previous_state.copy()
        print(f"⏪ Rolled back {steps} step(s).")

    def _generate_hash(self):
        """Generates a cryptographic hash of the current project state."""
        state_snapshot = json.dumps(self.project_state, sort_keys=True)
        state_hash = hashlib.sha256(state_snapshot.encode()).hexdigest()
        self.project_state["_state_hash"] = state_hash

    def get_state(self):
        """Returns the current project state."""
        return self.project_state

# Example usage
if __name__ == "__main__":
    pacp = PACP()
    pacp.update_state("LeaseAgreement", "Pending")
    pacp.update_state("StorageLocation", "Undecided")
    pacp.update_state("StorageLocation", "Confirmed: Central Warehouse")  # This triggers contradiction resolution

    print("\n📞 Current Project State:", pacp.get_state())
    pacp.rollback(1)
    print("\n🔄 After Rollback:", pacp.get_state())
