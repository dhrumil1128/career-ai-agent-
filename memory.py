"""
memory.py
---------
Stores user memory on disk.
Used for resume awareness and conversation history.
"""

import json
import os

MEMORY_FILE = "data/memory.json"
os.makedirs("data", exist_ok=True)

def load_memory(user_id="default"):
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f).get(user_id, {})

def save_memory(user_id, memory):
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            all_memory = json.load(f)
    else:
        all_memory = {}

    all_memory[user_id] = memory

    with open(MEMORY_FILE, "w") as f:
        json.dump(all_memory, f, indent=2)
