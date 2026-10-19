"""
AURA Enterprise Operations Engine:
SLA Ticketing, Real-time Escalations, and Project Scope & Cost Estimator.
"""

import time
import json
import uuid
from typing import List, Dict, Any, Optional

SLA_POLICIES = {
    "P1": {"response_mins": 15, "resolution_mins": 120, "description": "Critical Blocker / Production Outage"},
    "P2": {"response_mins": 60, "resolution_mins": 240, "description": "Major Degradation / Core Feature Broken"},
    "P3": {"response_mins": 240, "resolution_mins": 1440, "description": "Standard Technical Inquiry / Minor Bug"},
    "P4": {"response_mins": 1440, "resolution_mins": 4320, "description": "Consultation / Scoping & General Request"}
}

ESCALATION_ROSTER = {
    "L1": {"title": "L1 Triage Operations", "name": "Bilal Ahmed (Support Hub)", "email": "bilal.ahmed@aura.ai"},
    "L2": {"title": "L2 Senior DevOps Lead", "name": "Zeeshan Tariq (Senior SRE)", "email": "zeeshan.t@aura.ai"},
    "L3": {"title": "L3 VP of Engineering", "name": "Hamza Ihsan (Executive Delivery)", "email": "hamza.ihsan@aura.ai"}
}

class TicketEngine:
    def __init__(self):
        self.tickets: List[Dict[str, Any]] = []
        self.scopes: List[Dict[str, Any]] = []
        self._seed_initial_data()

    def _seed_initial_data(self):
        now = time.time()
        self.tickets = [
            {
                "id": "TICK-9041",
                "client": "Apex Logistics (UK / UAE)",
                "summary": "Real-time Fleet Tracking Webhook Timeout on Production AWS Cluster",
                "severity": "P1",
                "status": "ESCALATED",
                "escalation_level": "L2",
                "assigned_to": ESCALATION_ROSTER["L2"]["name"],
                "service": "Fleet Tracking API",
                "created_at": now - 3600,
                "sla_target_secs": now + 3600,
                "logs": [
                    "15:30 PKT - Alert ingested via Prometheus webhook",
                    "15:32 PKT - Triage initiated by AURA Voice Agent",
                    "15:45 PKT - Auto-escalated to L2 Tech Lead due to 504 Gateway Timeouts"
                ]
            },
            {
                "id": "TICK-9042",
                "client": "FinPay Global (Karachi / Riyadh)",
                "summary": "Easypaisa / 1Link Settlement Reconciliation Job Failed with DB Lock",
                "severity": "P2",
                "status": "IN_TRIAGE",
                "escalation_level": "L1",
                "assigned_to": ESCALATION_ROSTER["L1"]["name"],
                "service": "Banking Settlement Gateway",
                "created_at": now - 1800,
                "sla_target_secs": now + 7200,
                "logs": [
                    "16:00 PKT - Support desk inquiry logged via Roman Urdu voice input",
                    "16:05 PKT - Deadlock identified on settlements_ledger table"
                ]
            },
            {
                "id": "TICK-9043",
                "client": "CloudRetail Corp (US East)",
                "summary": "Inquiry regarding PCI-DSS compliant Stripe Elements tokenization update",
                "severity": "P3",
                "status": "NEW",
                "escalation_level": "L1",
                "assigned_to": ESCALATION_ROSTER["L1"]["name"],
                "service": "Payment Frontend SDK",
                "created_at": now - 600,
                "sla_target_secs": now + 14400,
                "logs": [
                    "16:20 PKT - Client documentation request logged"
                ]
            }
        ]

    def create_ticket(self, client: str, summary: str, severity: str = "P3", service: str = "General IT Services") -> Dict[str, Any]:
        severity = severity.upper()
        if severity not in SLA_POLICIES:
            severity = "P3"
            
        now = time.time()
        sla_info = SLA_POLICIES[severity]
        target_time = now + (sla_info["response_mins"] * 60)
        
        ticket_id = f"TICK-{str(uuid.uuid4().int)[:4]}"
        level = "L2" if severity in ["P1", "P2"] else "L1"
        assignee = ESCALATION_ROSTER[level]["name"]
        
        ticket = {
            "id": ticket_id,
            "client": client or "Enterprise Client",
            "summary": summary,
            "severity": severity,
            "status": "NEW" if severity != "P1" else "ESCALATED",
            "escalation_level": level,
            "assigned_to": assignee,
            "service": service,
            "created_at": now,
            "sla_target_secs": target_time,
            "logs": [
                f"{time.strftime('%H:%M PKT')} - Ticket created autonomously by AURA Agent",
                f"{time.strftime('%H:%M PKT')} - SLA Policy [{severity}]: Response required within {sla_info['response_mins']}m"
            ]
        }
        self.tickets.insert(0, ticket)
        return ticket

    def escalate_ticket(self, ticket_id: str, reason: str = "Client requested urgent supervisor intervention") -> Optional[Dict[str, Any]]:
        for ticket in self.tickets:
            if ticket["id"].lower() == ticket_id.lower() or ticket_id in ticket["id"]:
                current_level = ticket.get("escalation_level", "L1")
                new_level = "L2" if current_level == "L1" else "L3"
                ticket["escalation_level"] = new_level
                ticket["assigned_to"] = ESCALATION_ROSTER[new_level]["name"]
                ticket["status"] = "ESCALATED"
                ticket["severity"] = "P1"
                ticket["logs"].append(
                    f"{time.strftime('%H:%M PKT')} - ESCALATED to {new_level} ({ticket['assigned_to']}): {reason}"
                )
                return ticket
        return None

    def get_all_tickets(self) -> List[Dict[str, Any]]:
        return self.tickets

    def calculate_project_scope(self, project_name: str, tech_stack: str, complexity: str, duration_weeks: int) -> Dict[str, Any]:
        """
        Calculates project estimates, resource requirements, sprint breakdown, and dual currency rates (USD / PKR).
        Used by BPO & Software Export agencies in Pakistan delivering to international markets.
        """
        complexity_mult = {"low": 1.0, "medium": 1.4, "high": 2.0, "enterprise": 2.8}.get(complexity.lower(), 1.4)
        weeks = max(2, duration_weeks)
        
        # Benchmarked Offshore BPO/Software rates in Pakistan (USD $25 - $45/hr)
        hourly_rate_usd = 35.0
        pkr_exchange_rate = 280.0
        
        dev_hours_per_week = 40
        total_dev_hours = int(weeks * dev_hours_per_week * complexity_mult)
        
        usd_total = round(total_dev_hours * hourly_rate_usd, 2)
        pkr_total = round(usd_total * pkr_exchange_rate, 2)
        
        sprints = max(1, weeks // 2)
        
        scope_result = {
            "project_name": project_name,
            "tech_stack": tech_stack,
            "complexity": complexity,
            "estimated_weeks": weeks,
            "sprint_cycles": sprints,
            "total_engineering_hours": total_dev_hours,
            "rate_usd_hour": hourly_rate_usd,
            "total_usd": usd_total,
            "total_pkr": pkr_total,
            "recommended_team": [
                {"role": "Lead Architect / DevOps", "allocation": "50%"},
                {"role": "Full-Stack Senior Engineers (2x)", "allocation": "100%"},
                {"role": "QA & Automation Specialist", "allocation": "50%"},
                {"role": "Agile Scrum Master / PM", "allocation": "25%"}
            ],
            "milestone_breakdown": [
                {"milestone": "Sprint 1-2: Architecture, CI/CD, DB Schema & Foundation", "percentage": "25%"},
                {"milestone": "Sprint 3-4: Core Business Logic & Third-Party Integrations", "percentage": "40%"},
                {"milestone": "Sprint 5: End-to-End QA, Security Hardening & UAT", "percentage": "20%"},
                {"milestone": "Sprint 6: Production Deployment & Hypercare Warranty", "percentage": "15%"}
            ]
        }
        self.scopes.insert(0, scope_result)
        return scope_result

ticket_engine = TicketEngine()
