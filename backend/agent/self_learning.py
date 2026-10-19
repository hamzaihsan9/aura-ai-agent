"""
AURA Autonomous Self-Learning & Memory Engine
Enables the AI to continually learn, retain, and reinforce new operational knowledge
from user conversations and manual training prompts.
Persists memory to backend/data/learned_memory.json.
"""

import os
import json
import time
import re
from typing import List, Dict, Any, Optional

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "learned_memory.json")

class SelfLearningEngine:
    def __init__(self):
        self.memory_path = MEMORY_FILE
        self.learned_items: List[Dict[str, Any]] = []
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.learned_items = data.get("learned_items", [])
            except Exception:
                self.learned_items = []
        else:
            self._seed_default_learned_knowledge()
            self._save_memory()

    def _seed_default_learned_knowledge(self):
        """Initial learned operational knowledge base."""
        self.learned_items = [
            {
                "id": "LEARN-001",
                "topic": "Office Timings and Physical Inquiries",
                "keywords": ["timing", "waqt", "office kab khulta hai", "working hours"],
                "content_en": "Our engineering and customer support centers operate Monday through Saturday from 9:00 AM to 9:00 PM PKT.",
                "content_ur": "ہمارے دفاتر پیر سے ہفتہ صبح 9 بجے سے رات 9 بجے تک کھلے رہتے ہیں۔",
                "content_roman": "Office timings: Peer se Hafta (Monday to Saturday) subah 9 baje se raat 9 baje tak hain.",
                "created_at": time.time(),
                "learned_from": "system_bootstrap",
                "confidence_score": 0.98
            },
            {
                "id": "LEARN-002",
                "topic": "Official Support Helpline Number",
                "keywords": ["helpline", "phone number", "call number", "rabta number", "support call"],
                "content_en": "You can call our dedicated support hotline at 0800-AURA-AI (+92 42 111 000 111) for toll-free assistance.",
                "content_ur": "آپ ہماری ٹول فری ہیلپ لائن 0800-2872 پر کسی بھی وقت رابطہ کر سکتے ہیں۔",
                "content_roman": "Aap hamari helpline 0800-2872 par call kar ke fori assistance le sakte hain.",
                "created_at": time.time(),
                "learned_from": "system_bootstrap",
                "confidence_score": 0.95
            }
        ]

    def _save_memory(self):
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        try:
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump({
                    "version": "1.0",
                    "updated_at": time.time(),
                    "total_learned_items": len(self.learned_items),
                    "learned_items": self.learned_items
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving learned memory: {e}")

    def learn_new_fact(self, topic: str, content: str, keywords: List[str] = None, source: str = "user_conversation") -> Dict[str, Any]:
        """Adds a new fact or operational command learned dynamically from conversation."""
        item_id = f"LEARN-{len(self.learned_items) + 1:03d}"
        if not keywords:
            keywords = re.findall(r"\w{3,}", (topic + " " + content).lower())[:8]

        new_item = {
            "id": item_id,
            "topic": topic,
            "keywords": keywords,
            "content_en": content,
            "content_ur": content,
            "content_roman": content,
            "created_at": time.time(),
            "learned_from": source,
            "confidence_score": 0.92
        }
        self.learned_items.insert(0, new_item)
        self._save_memory()
        return new_item

    def detect_teaching_prompt(self, user_text: str) -> Optional[Dict[str, Any]]:
        """Detects if user is teaching the AI a new rule or operational fact."""
        text_lower = user_text.lower()
        patterns = [
            r"yaad rakho\s*[:,]?\s*(.+)",
            r"remember that\s*[:,]?\s*(.+)",
            r"learn that\s*[:,]?\s*(.+)",
            r"yeh baat seekho\s*[:,]?\s*(.+)",
            r"hamara naya\s+(.+)\s+(hai|hoga)",
            r"our new\s+(.+)\s+is\s+(.+)"
        ]
        for pat in patterns:
            match = re.search(pat, text_lower)
            if match:
                fact = match.group(0)
                learned = self.learn_new_fact(
                    topic=f"Learned: {fact[:30]}...",
                    content=user_text,
                    source="interactive_teaching"
                )
                return learned
        return None

    def query_memory(self, query: str) -> Optional[Dict[str, Any]]:
        """Retrieves matching learned knowledge for the query."""
        q_words = set(re.findall(r"\w+", query.lower()))
        best_item = None
        max_score = 0

        for item in self.learned_items:
            score = 0
            for kw in item.get("keywords", []):
                if kw.lower() in query.lower():
                    score += 3
            item_words = set(re.findall(r"\w+", (item.get("topic", "") + " " + item.get("content_en", "")).lower()))
            overlap = len(q_words.intersection(item_words))
            score += overlap

            if score > max_score:
                max_score = score
                best_item = item

        return best_item if max_score >= 3 else None

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_learned_facts": len(self.learned_items),
            "memory_file": self.memory_path,
            "recent_learned": self.learned_items[:5]
        }

learning_engine = SelfLearningEngine()
