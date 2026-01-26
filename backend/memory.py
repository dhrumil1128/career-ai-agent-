"""
memory.py
---------
Enhanced memory system with conversation context and resume awareness.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

MEMORY_FILE = "data/memory.json"
os.makedirs("data", exist_ok=True)

# Constants
MAX_HISTORY_LENGTH = 50  # Keep last 50 messages
MAX_CONVERSATION_PAIRS = 20  # Keep last 20 conversation pairs

def load_memory(user_id: str = "default") -> Dict[str, Any]:
    """
    Load memory for a specific user.
    
    Args:
        user_id: User identifier
        
    Returns:
        Dictionary containing user memory
    """
    if not os.path.exists(MEMORY_FILE):
        return create_empty_memory()
    
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            all_memory = json.load(f)
            user_memory = all_memory.get(user_id, {})
            
            # Ensure required fields exist
            return ensure_memory_structure(user_memory)
    except (json.JSONDecodeError, IOError):
        return create_empty_memory()

def save_memory(user_id: str, memory: Dict[str, Any]) -> None:
    """
    Save memory for a specific user.
    
    Args:
        user_id: User identifier
        memory: Memory data to save
    """
    # Load existing memory
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                all_memory = json.load(f)
        except (json.JSONDecodeError, IOError):
            all_memory = {}
    else:
        all_memory = {}
    
    # Ensure memory structure is valid
    memory = ensure_memory_structure(memory)
    
    # Update memory for user
    all_memory[user_id] = memory
    
    # Save to file
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(all_memory, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving memory: {e}")

def create_empty_memory() -> Dict[str, Any]:
    """
    Create an empty memory structure.
    
    Returns:
        Empty memory dictionary with required structure
    """
    return {
        "history": [],
        "conversation_pairs": [],
        "resume_text": "",
        "resume_uploaded": False,
        "resume_file": "",
        "star_mode": False,
        "last_response": "",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "interview": {
            "index": 0,
            "answers": [],
            "started_at": None
        }
    }

def ensure_memory_structure(memory: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure memory has all required fields.
    
    Args:
        memory: Memory dictionary to validate
        
    Returns:
        Validated memory dictionary
    """
    required_fields = {
        "history": [],
        "conversation_pairs": [],
        "resume_text": "",
        "resume_uploaded": False,
        "resume_file": "",
        "star_mode": False,
        "last_response": "",
        "interview": {
            "index": 0,
            "answers": [],
            "started_at": None
        }
    }
    
    # Add missing fields
    for key, default_value in required_fields.items():
        if key not in memory:
            memory[key] = default_value
    
    # Ensure interview structure
    if "interview" not in memory:
        memory["interview"] = required_fields["interview"]
    else:
        interview_fields = required_fields["interview"]
        for key in interview_fields:
            if key not in memory["interview"]:
                memory["interview"][key] = interview_fields[key]
    
    # Update timestamp
    memory["updated_at"] = datetime.utcnow().isoformat()
    
    return memory

def add_to_history(user_id: str, user_input: str, response: Optional[str] = None) -> None:
    """
    Add a conversation turn to history.
    
    Args:
        user_id: User identifier
        user_input: User's message
        response: Assistant's response (optional)
    """
    memory = load_memory(user_id)
    
    # Add user input to history
    memory["history"].append({
        "time": datetime.utcnow().isoformat(),
        "user": user_input,
        "type": "user_input"
    })
    
    # Add response to history if provided
    if response:
        memory["history"].append({
            "time": datetime.utcnow().isoformat(),
            "assistant": response[:500],  # Store truncated response
            "type": "assistant_response"
        })
    
    # Also add to conversation pairs for context
    if response:
        memory.setdefault("conversation_pairs", []).append({
            "user": user_input,
            "assistant": response[:1000],  # Store longer version
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Keep conversation pairs within limit
        if len(memory["conversation_pairs"]) > MAX_CONVERSATION_PAIRS:
            memory["conversation_pairs"] = memory["conversation_pairs"][-MAX_CONVERSATION_PAIRS:]
    
    # Keep history within limit
    if len(memory["history"]) > MAX_HISTORY_LENGTH:
        memory["history"] = memory["history"][-MAX_HISTORY_LENGTH:]
    
    # Update last response
    if response:
        memory["last_response"] = response
    
    memory["updated_at"] = datetime.utcnow().isoformat()
    
    save_memory(user_id, memory)

def get_conversation_context(user_id: str = "default", last_n: int = 5) -> str:
    """
    Get recent conversation context.
    
    Args:
        user_id: User identifier
        last_n: Number of recent messages to include
        
    Returns:
        Formatted conversation context
    """
    memory = load_memory(user_id)
    
    # Get recent conversation pairs
    pairs = memory.get("conversation_pairs", [])
    if not pairs:
        return ""
    
    recent_pairs = pairs[-last_n:] if len(pairs) > last_n else pairs
    
    # Format context
    context_lines = []
    for pair in recent_pairs:
        context_lines.append(f"User: {pair.get('user', '')}")
        context_lines.append(f"Assistant: {pair.get('assistant', '')[:200]}")  # Truncate
    
    return "\n".join(context_lines)

def get_resume_context(user_id: str = "default") -> str:
    """
    Get resume context if available.
    
    Args:
        user_id: User identifier
        
    Returns:
        Resume text or empty string
    """
    memory = load_memory(user_id)
    
    if memory.get("resume_uploaded") and memory.get("resume_text"):
        # Return first 1500 characters of resume for context
        return memory["resume_text"][:1500]
    
    return ""

def set_resume(user_id: str, resume_text: str, file_path: str = "") -> None:
    """
    Set resume data in memory.
    
    Args:
        user_id: User identifier
        resume_text: Extracted resume text
        file_path: Path to resume file
    """
    memory = load_memory(user_id)
    
    memory["resume_text"] = resume_text
    memory["resume_uploaded"] = True
    memory["resume_file"] = file_path
    memory["updated_at"] = datetime.utcnow().isoformat()
    
    save_memory(user_id, memory)

def clear_resume(user_id: str = "default") -> None:
    """
    Clear resume data from memory.
    
    Args:
        user_id: User identifier
    """
    memory = load_memory(user_id)
    
    memory["resume_text"] = ""
    memory["resume_uploaded"] = False
    memory["resume_file"] = ""
    memory["updated_at"] = datetime.utcnow().isoformat()
    
    save_memory(user_id, memory)

def is_resume_uploaded(user_id: str = "default") -> bool:
    """
    Check if resume is uploaded.
    
    Args:
        user_id: User identifier
        
    Returns:
        True if resume is uploaded, False otherwise
    """
    memory = load_memory(user_id)
    return memory.get("resume_uploaded", False)

def get_resume_text(user_id: str = "default") -> str:
    """
    Get resume text if available.
    
    Args:
        user_id: User identifier
        
    Returns:
        Resume text or empty string
    """
    memory = load_memory(user_id)
    return memory.get("resume_text", "")

def set_star_mode(user_id: str, enabled: bool) -> None:
    """
    Set STAR mode status.
    
    Args:
        user_id: User identifier
        enabled: Whether STAR mode is enabled
    """
    memory = load_memory(user_id)
    
    memory["star_mode"] = enabled
    memory["updated_at"] = datetime.utcnow().isoformat()
    
    save_memory(user_id, memory)

def is_star_mode(user_id: str = "default") -> bool:
    """
    Check if STAR mode is enabled.
    
    Args:
        user_id: User identifier
        
    Returns:
        True if STAR mode is enabled, False otherwise
    """
    memory = load_memory(user_id)
    return memory.get("star_mode", False)

def update_interview_progress(user_id: str, answer: str = None) -> None:
    """
    Update interview progress.
    
    Args:
        user_id: User identifier
        answer: Current answer (optional)
    """
    memory = load_memory(user_id)
    
    interview = memory.get("interview", {
        "index": 0,
        "answers": [],
        "started_at": None
    })
    
    if answer is not None:
        interview["answers"].append(answer)
    
    interview["index"] = len(interview["answers"])
    
    if interview["started_at"] is None:
        interview["started_at"] = datetime.utcnow().isoformat()
    
    memory["interview"] = interview
    memory["updated_at"] = datetime.utcnow().isoformat()
    
    save_memory(user_id, memory)

def clear_memory(user_id: str = "default") -> None:
    """
    Clear all memory for a user.
    
    Args:
        user_id: User identifier
    """
    # Keep only basic structure
    empty_memory = create_empty_memory()
    save_memory(user_id, empty_memory)

def get_memory_summary(user_id: str = "default") -> Dict[str, Any]:
    """
    Get a summary of memory state.
    
    Args:
        user_id: User identifier
        
    Returns:
        Memory summary dictionary
    """
    memory = load_memory(user_id)
    
    return {
        "has_resume": memory.get("resume_uploaded", False),
        "resume_length": len(memory.get("resume_text", "")),
        "history_count": len(memory.get("history", [])),
        "conversation_pairs": len(memory.get("conversation_pairs", [])),
        "star_mode": memory.get("star_mode", False),
        "interview_progress": memory.get("interview", {}).get("index", 0),
        "created_at": memory.get("created_at", ""),
        "updated_at": memory.get("updated_at", "")
    }