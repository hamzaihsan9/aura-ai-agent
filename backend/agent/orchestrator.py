"""
AURA Agent Orchestrator:
Manages multi-turn conversation sessions, voice/audio interactions, and action dispatching.
"""

import time
import json
from typing import Dict, Any, List
from backend.agent.llm_client import llm_client
from backend.ops.ticket_engine import ticket_engine
from backend.agent.bilingual_processor import BilingualProcessor

class ConversationSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history: List[Dict[str, str]] = []
        self.created_at = time.time()
        self.detected_language = "en"

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content, "timestamp": time.time()})

class AgentOrchestrator:
    def __init__(self):
        self.sessions: Dict[str, ConversationSession] = {}

    def get_or_create_session(self, session_id: str) -> ConversationSession:
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationSession(session_id)
        return self.sessions[session_id]

    async def handle_user_input(self, session_id: str, text: str) -> Dict[str, Any]:
        session = self.get_or_create_session(session_id)
        session.add_message("user", text)

        # Detect dialect & process
        lang = BilingualProcessor.detect_language(text)
        session.detected_language = lang

        # Generate intelligent reasoning & execute relevant tools
        response = llm_client.generate_response(user_text=text, context_history=session.history)
        session.add_message("agent", response["text"])

        # Fetch current system state for real-time dashboard sync
        tickets = ticket_engine.get_all_tickets()

        return {
            "type": "agent_response",
            "session_id": session_id,
            "text": response["text"],
            "speech": response["speech"],
            "language": response["language"],
            "urgency": response["urgency"],
            "tools_executed": response["tools_executed"],
            "action_summary": response["action_summary"],
            "tickets": tickets,
            "timestamp": time.time()
        }

orchestrator = AgentOrchestrator()
