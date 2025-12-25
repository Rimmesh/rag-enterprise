import os
import json
from datetime import datetime
from typing import Dict, List

CHAT_PATH = "data/chats.json"

def load_chats() -> Dict[str, List[dict]]:
    if not os.path.exists(CHAT_PATH):
        return {}
    with open(CHAT_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_chats(chats: Dict[str, List[dict]]):
    os.makedirs(os.path.dirname(CHAT_PATH), exist_ok=True)
    with open(CHAT_PATH, "w", encoding="utf-8") as f:
        json.dump(chats, f, indent=2, ensure_ascii=False)

def add_message(user_email: str, role: str, content: str):
    chats = load_chats()
    chats.setdefault(user_email, []).append({
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow().isoformat()
    })
    save_chats(chats)

def get_history(user_email: str) -> List[dict]:
    chats = load_chats()
    return chats.get(user_email, [])
