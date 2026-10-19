"""
AURA Enterprise IT & BPO Voice & Chat Agent
Main FastAPI Application Server
"""

import os
import json
import logging
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agent.orchestrator import orchestrator
from backend.ops.ticket_engine import ticket_engine
from backend.knowledge.store import knowledge_base
from backend.agent.bilingual_processor import BilingualProcessor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("aura-server")

app = FastAPI(
    title="AURA Enterprise Voice & Chat Agent",
    description="Autonomous Bilingual BPO & IT Service Delivery Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static directory if exists
static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Pydantic Request Models
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

class TicketCreateRequest(BaseModel):
    client: str
    summary: str
    severity: str = "P3"
    service: str = "General Services"

class TicketEscalateRequest(BaseModel):
    ticket_id: str
    reason: str = "Client requested urgent supervisor escalation"

class ScopeRequest(BaseModel):
    project_name: str
    tech_stack: str = "Next.js, FastAPI, PostgreSQL & Cloud"
    complexity: str = "medium"
    duration_weeks: int = 6


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = os.path.join(os.path.dirname(__file__), "..", "frontend", "templates", "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return HTMLResponse("<h1>AURA Voice Agent is Initializing...</h1>")


@app.get("/api/status")
async def get_system_status():
    return {
        "status": "ONLINE",
        "service": "AURA Enterprise Operations Core",
        "bilingual_support": ["English (Global)", "Urdu (اردو)", "Roman Urdu"],
        "active_tickets_count": len(ticket_engine.get_all_tickets()),
        "knowledge_documents_count": len(knowledge_base.docs),
        "host_location": "Aura Global Cloud Relay"
    }


@app.get("/api/tickets")
async def list_tickets():
    return {"tickets": ticket_engine.get_all_tickets()}


@app.post("/api/tickets")
async def create_ticket(req: TicketCreateRequest):
    ticket = ticket_engine.create_ticket(
        client=req.client,
        summary=req.summary,
        severity=req.severity,
        service=req.service
    )
    return {"status": "success", "ticket": ticket}


@app.post("/api/tickets/escalate")
async def escalate_ticket(req: TicketEscalateRequest):
    updated = ticket_engine.escalate_ticket(ticket_id=req.ticket_id, reason=req.reason)
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"status": "success", "ticket": updated}


@app.post("/api/scope/calculate")
async def calculate_scope(req: ScopeRequest):
    scope = ticket_engine.calculate_project_scope(
        project_name=req.project_name,
        tech_stack=req.tech_stack,
        complexity=req.complexity,
        duration_weeks=req.duration_weeks
    )
    return {"status": "success", "scope": scope}


@app.get("/api/knowledge/search")
async def search_knowledge(q: str = Query(..., description="Query terms")):
    results = knowledge_base.search(q, top_k=3)
    return {"query": q, "results": results}


@app.post("/api/chat")
async def process_chat(req: ChatRequest):
    resp = await orchestrator.handle_user_input(session_id=req.session_id, text=req.message)
    return resp


@app.websocket("/ws/voice-agent")
async def websocket_voice_agent(websocket: WebSocket):
    await websocket.accept()
    session_id = f"ws_session_{id(websocket)}"
    logger.info(f"WebSocket client connected: {session_id}")

    # Send initial greeting and system state
    await websocket.send_json({
        "type": "connection_established",
        "session_id": session_id,
        "greeting": BilingualProcessor.get_localized_confirmation("greetings", "en"),
        "greeting_roman": BilingualProcessor.get_localized_confirmation("greetings", "roman_ur"),
        "tickets": ticket_engine.get_all_tickets()
    })

    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)
            msg_type = data.get("type", "chat_message")

            if msg_type in ["chat_message", "voice_transcript"]:
                text = data.get("text", "").strip()
                if not text:
                    continue

                logger.info(f"[{session_id}] User speech/chat: {text}")
                response = await orchestrator.handle_user_input(session_id=session_id, text=text)
                await websocket.send_json(response)

            elif msg_type == "escalate_action":
                ticket_id = data.get("ticket_id", "")
                reason = data.get("reason", "Manual operator escalation via UI")
                updated = ticket_engine.escalate_ticket(ticket_id=ticket_id, reason=reason)
                await websocket.send_json({
                    "type": "tickets_update",
                    "action": "escalate",
                    "tickets": ticket_engine.get_all_tickets()
                })

            elif msg_type == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except Exception:
            pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
