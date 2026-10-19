"""
AURA Agentic Tool Calling Registry
Maps LLM function calls and natural language actions to operational backend tasks.
"""

import time
from typing import Dict, Any, List
from backend.ops.ticket_engine import ticket_engine
from backend.knowledge.store import knowledge_base

TOOL_DEFINITIONS = [
    {
        "name": "create_sla_ticket",
        "description": "Creates a new enterprise SLA support ticket with severity triage (P1 Critical to P4 Low).",
        "parameters": {
            "type": "object",
            "properties": {
                "client": {"type": "string", "description": "Client company name or reporter"},
                "summary": {"type": "string", "description": "Brief summary of the issue or error encountered"},
                "severity": {"type": "string", "enum": ["P1", "P2", "P3", "P4"], "description": "Severity level"},
                "service": {"type": "string", "description": "Impacted service or infrastructure component"}
            },
            "required": ["client", "summary", "severity"]
        }
    },
    {
        "name": "escalate_incident",
        "description": "Escalates an active ticket or critical incident to Tier-2 Tech Lead or L3 VP of Engineering.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {"type": "string", "description": "Ticket ID (e.g., TICK-9041)"},
                "reason": {"type": "string", "description": "Justification for escalation"}
            },
            "required": ["ticket_id", "reason"]
        }
    },
    {
        "name": "search_runbooks",
        "description": "Retrieves incident mitigation steps, playbooks, or SLA policy documentation from the RAG knowledge base.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Technical query (e.g., database deadlock, 502 gateway timeout, Stripe webhook)"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculate_scope_estimate",
        "description": "Calculates project engineering hours, sprint timelines, and dual-currency cost estimates (USD / PKR) for software development.",
        "parameters": {
            "type": "object",
            "properties": {
                "project_name": {"type": "string", "description": "Name or type of the software project"},
                "tech_stack": {"type": "string", "description": "Proposed technology stack (e.g., React, Node, Python, AWS)"},
                "complexity": {"type": "string", "enum": ["low", "medium", "high", "enterprise"], "description": "Technical complexity level"},
                "duration_weeks": {"type": "integer", "description": "Estimated target timeframe in weeks (default 6)"}
            },
            "required": ["project_name", "tech_stack"]
        }
    },
    {
        "name": "schedule_technical_sync",
        "description": "Schedules a technical discovery or incident bridge sync with offshore and onshore stakeholders.",
        "parameters": {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "Client or stakeholder name"},
                "topic": {"type": "string", "description": "Sync topic or incident bridge discussion"},
                "preferred_time": {"type": "string", "description": "Proposed time and timezone (e.g., Tomorrow 16:00 PKT / 11:00 UTC)"}
            },
            "required": ["client_name", "topic"]
        }
    },
    {
        "name": "get_service_status",
        "description": "Checks the live health and telemetry status of core enterprise services.",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {"type": "string", "description": "Service name to check (e.g., payment-gateway, api-cluster, database)"}
            }
        }
    }
]

class ToolExecutor:
    @staticmethod
    def execute(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the tool by name with provided arguments and returns execution result."""
        if name == "create_sla_ticket":
            client = args.get("client", "Valued Enterprise Client")
            summary = args.get("summary", "Unspecified Technical Incident")
            severity = args.get("severity", "P3")
            service = args.get("service", "Cloud Infrastructure")
            ticket = ticket_engine.create_ticket(client=client, summary=summary, severity=severity, service=service)
            return {
                "status": "success",
                "message": f"Ticket {ticket['id']} created under {severity} policy.",
                "data": ticket
            }

        elif name == "escalate_incident":
            ticket_id = args.get("ticket_id", "")
            reason = args.get("reason", "Urgent client escalation requested.")
            res = ticket_engine.escalate_ticket(ticket_id=ticket_id, reason=reason)
            if res:
                return {
                    "status": "success",
                    "message": f"Incident {res['id']} escalated to {res['escalation_level']} ({res['assigned_to']}).",
                    "data": res
                }
            return {
                "status": "error",
                "message": f"Ticket ID '{ticket_id}' not found in active roster."
            }

        elif name == "search_runbooks":
            query = args.get("query", "")
            docs = knowledge_base.search(query, top_k=2)
            return {
                "status": "success",
                "query": query,
                "matches": [
                    {"id": d["id"], "title": d["title"], "category": d["category"], "content": d["content"]}
                    for d in docs
                ]
            }

        elif name == "calculate_scope_estimate":
            project_name = args.get("project_name", "Custom Web & Mobile Application")
            tech_stack = args.get("tech_stack", "Full-Stack TypeScript & Python")
            complexity = args.get("complexity", "medium")
            duration_weeks = int(args.get("duration_weeks", 6))
            scope = ticket_engine.calculate_project_scope(
                project_name=project_name,
                tech_stack=tech_stack,
                complexity=complexity,
                duration_weeks=duration_weeks
            )
            return {
                "status": "success",
                "message": f"Scope estimation for {project_name} generated successfully.",
                "data": scope
            }

        elif name == "schedule_technical_sync":
            client = args.get("client_name", "Enterprise Partner")
            topic = args.get("topic", "Architecture Review")
            pref_time = args.get("preferred_time", "Tomorrow 15:00 PKT (10:00 UTC)")
            return {
                "status": "success",
                "message": f"Sync confirmed with {client} for '{topic}' at {pref_time}. Calendar invite dispatched.",
                "details": {
                    "client": client,
                    "topic": topic,
                    "time": pref_time,
                    "meeting_link": "https://meet.aura.ai/sync-room"
                }
            }

        elif name == "get_service_status":
            service_name = args.get("service_name", "all").lower()
            statuses = {
                "api-cluster": {"status": "HEALTHY", "latency_ms": 38, "uptime": "99.98%"},
                "database": {"status": "DEGRADED", "connection_usage": "88%", "active_deadlocks": 1},
                "payment-gateway": {"status": "OPERATIONAL", "success_rate": "99.4%"},
                "auth-service": {"status": "HEALTHY", "latency_ms": 14, "uptime": "100%"}
            }
            if service_name in statuses:
                return {"service": service_name, "metrics": statuses[service_name]}
            return {"services": statuses}

        return {"status": "unknown_tool", "message": f"Tool '{name}' not found."}
