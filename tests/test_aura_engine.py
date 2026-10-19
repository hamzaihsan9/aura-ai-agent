"""
AURA Enterprise Voice & Chat Agent Test Suite
Verifies bilingual intent analysis, SLA escalation, project scoping, and RAG knowledge search.
"""

import asyncio
import unittest
from backend.agent.bilingual_processor import BilingualProcessor
from backend.ops.ticket_engine import ticket_engine
from backend.knowledge.store import knowledge_base
from backend.agent.tools import ToolExecutor
from backend.agent.orchestrator import orchestrator

class TestAuraEngine(unittest.TestCase):

    def test_bilingual_language_detection(self):
        """Verifies detection across English, Urdu (Nastaliq), and Roman Urdu."""
        en_text = "The payment webhook has timed out on production cluster."
        ur_text = "ہمارا پروڈکشن سرور ڈاؤن ہو گیا ہے برائے مہربانی چیک کریں۔"
        roman_ur_text = "Humara payment gateway fail ho raha hai transaction ruk gayi hai."

        self.assertEqual(BilingualProcessor.detect_language(en_text), "en")
        self.assertEqual(BilingualProcessor.detect_language(ur_text), "ur")
        self.assertEqual(BilingualProcessor.detect_language(roman_ur_text), "roman_ur")

    def test_intent_and_urgency_scoring(self):
        """Tests that critical outages trigger P1 severity and high urgency score."""
        critical_input = "CRITICAL: Production server down and database connection pool exhausted!"
        analysis = BilingualProcessor.analyze_intent(critical_input)
        
        self.assertEqual(analysis["urgency_score"], 4)
        self.assertEqual(analysis["suggested_severity"], "P1")
        self.assertIn("server_down", analysis["detected_intents"])

    def test_ticket_creation_and_escalation(self):
        """Tests autonomous SLA ticket creation and subsequent L2 escalation."""
        ticket = ticket_engine.create_ticket(
            client="Global FinTech Ltd",
            summary="Payment gateway signature verification failure",
            severity="P2",
            service="Payment Switch"
        )
        self.assertTrue(ticket["id"].startswith("TICK-"))
        self.assertEqual(ticket["severity"], "P2")

        # Escalate (since P2 starts at L2, it escalates to L3 VP of Engineering)
        escalated = ticket_engine.escalate_ticket(ticket["id"], reason="SLA breach imminent")
        self.assertIsNotNone(escalated)
        self.assertEqual(escalated["status"], "ESCALATED")
        self.assertEqual(escalated["escalation_level"], "L3")

    def test_project_scope_dual_currency(self):
        """Tests scoping hours and conversion to USD and PKR at benchmark rates."""
        scope = ticket_engine.calculate_project_scope(
            project_name="Custom FinTech Banking API",
            tech_stack="Node, React, PostgreSQL",
            complexity="medium",
            duration_weeks=6
        )
        self.assertEqual(scope["estimated_weeks"], 6)
        self.assertEqual(scope["rate_usd_hour"], 35.0)
        self.assertGreater(scope["total_usd"], 0)
        self.assertGreater(scope["total_pkr"], scope["total_usd"])
        self.assertEqual(len(scope["recommended_team"]), 4)

    def test_rag_runbook_retrieval(self):
        """Tests TF-IDF / keyword retrieval for technical incident runbooks."""
        results = knowledge_base.search("postgres database deadlock connection pool", top_k=1)
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]["id"], "RUNBOOK-01")
        self.assertIn("deadlock", results[0]["title"].lower())

    def test_tool_executor(self):
        """Tests dynamic tool execution registry."""
        res = ToolExecutor.execute("get_service_status", {"service_name": "database"})
        self.assertEqual(res["service"], "database")
        self.assertEqual(res["metrics"]["status"], "DEGRADED")


class TestOrchestratorAsync(unittest.IsolatedAsyncioTestCase):

    async def test_orchestrator_turn_roman_urdu(self):
        """Tests full agentic turn with Roman Urdu input."""
        resp = await orchestrator.handle_user_input(
            session_id="test_sess_01",
            text="Server down ho gya hai jaldi ticket banao"
        )
        self.assertEqual(resp["type"], "agent_response")
        self.assertIn(resp["language"], ["roman_ur", "ur"])
        self.assertTrue(len(resp["tools_executed"]) > 0)
        self.assertIn("ticket", resp["action_summary"].lower())

    async def test_orchestrator_scoping_request(self):
        """Tests full agentic turn for cross-border software scoping."""
        resp = await orchestrator.handle_user_input(
            session_id="test_sess_02",
            text="We need a project estimate and budget for an 8-week SaaS platform."
        )
        self.assertEqual(resp["type"], "agent_response")
        self.assertEqual(resp["language"], "en")
        self.assertTrue(len(resp["tools_executed"]) > 0)
        self.assertIn("scope", resp["action_summary"].lower())


if __name__ == "__main__":
    unittest.main()
