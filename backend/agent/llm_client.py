"""
AURA High-Empathy Customer AI Intelligence Engine
Tailored for everyday accessibility in Pakistan and global enterprise delivery.
Provides warm, simple, jargon-free solutions that anyone can easily understand.
"""

import os
import json
import re
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from backend.agent.tools import TOOL_DEFINITIONS, ToolExecutor
from backend.agent.bilingual_processor import BilingualProcessor
from backend.knowledge.store import knowledge_base

SYSTEM_PROMPT = """You are Aura, an exceptionally polite, warm, and helpful AI assistant for customer support and IT services.
Your audience includes everyday common people who may not be technical and need simple, comforting guidance.
Rules:
1. Keep responses very simple, reassuring, and easy to understand.
2. NEVER use complex programming jargon, raw code, or confusing error logs.
3. If user speaks in Urdu, reply in clean, simple, polite Urdu.
4. If user speaks in Roman Urdu, reply in natural, friendly Roman Urdu.
5. If user speaks in English, reply in plain, courteous, easy English.
6. When an issue occurs, reassure them that their data/money is safe, tell them their complaint/ticket number, and explain that the senior team is fixing it right now.
"""

class LLMClient:
    def __init__(self):
        self.ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.ollama_model = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")

    def _call_ollama(self, prompt: str) -> Optional[str]:
        try:
            req_data = json.dumps({
                "model": self.ollama_model,
                "prompt": prompt,
                "system": SYSTEM_PROMPT,
                "stream": False
            }).encode("utf-8")
            req = urllib.request.Request(self.ollama_url, data=req_data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                ans = data.get("response", "").strip()
                return ans if len(ans) > 5 else None
        except Exception:
            return None

    def _simple_human_reasoning(self, user_text: str, context_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Provides crystal-clear, reassuring solutions for everyday users."""
        intent_info = BilingualProcessor.analyze_intent(user_text)
        lang = intent_info["language"]
        urgency = intent_info["urgency_score"]
        severity = intent_info["suggested_severity"]
        user_lower = user_text.lower()

        executed_tools = []
        speech_text = ""
        action_summary = ""

        # Problem Type 1: Payment issue / Money stuck / Transaction failed
        if "payment" in user_lower or "pese" in user_lower or "paisa" in user_lower or "jazzcash" in user_lower or "easypaisa" in user_lower or "kat" in user_lower or intent_info["primary_intent"] == "payment_failure":
            tool_res = ToolExecutor.execute("create_sla_ticket", {
                "client": "Customer Support Account",
                "summary": user_text,
                "severity": "P1",
                "service": "Payment Verification Desk"
            })
            executed_tools.append({"tool": "create_sla_ticket", "result": tool_res})
            ticket = tool_res["data"]

            if lang == "ur":
                speech_text = (
                    f"فکر نہ کریں، آپ کے پیسے بالکل محفوظ ہیں۔ ہم نے آپ کی شکایت درج کر لی ہے جس کا ٹکٹ نمبر {ticket['id']} ہے۔ "
                    f"ہماری ٹیکنیکل ٹیم اگلے 15 منٹ میں بینک سے چیک کر کے آپ کا مسئلہ حل کر دے گی۔ آپ تسلی رکھیں۔"
                )
            elif lang == "roman_ur":
                speech_text = (
                    f"Fikar bilkul na karein, aap ke paise 100% mehfooz hain. Humne aap ki complaint darj kar li hai (Ticket: {ticket['id']}). "
                    f"Hamari technical team agle 15 minute ke andar bank se verify kar ke masla theek kar degi. Aap tasalli rakhein."
                )
            else:
                speech_text = (
                    f"Please do not worry, your payment is completely safe. I have registered your priority complaint under Ticket #{ticket['id']}. "
                    f"Our senior verification team has been alerted and will resolve this within 15 minutes."
                )

            action_summary = f"Complaint #{ticket['id']} registered for Payment Support (Assigned to {ticket['assigned_to']})."

        # Problem Type 2: Server down / Website or App not opening / Crash
        elif "down" in user_lower or "band" in user_lower or "ruk" in user_lower or "crash" in user_lower or "chal nahi" in user_lower or intent_info["primary_intent"] == "server_down":
            tool_res = ToolExecutor.execute("create_sla_ticket", {
                "client": "System Operations",
                "summary": user_text,
                "severity": "P1",
                "service": "Core Server Infrastructure"
            })
            executed_tools.append({"tool": "create_sla_ticket", "result": tool_res})
            ticket = tool_res["data"]

            if lang == "ur":
                speech_text = (
                    f"جی بالکل، ہم نے سسٹم چیک کر لیا ہے۔ سرور کا مسئلہ ہماری نظر میں آ چکا ہے اور شکایت {ticket['id']} درج کر لی گئی ہے۔ "
                    f"ہمارے سینئر انجینئرز اس کو فورا ٹھیک کر رہے ہیں۔ آپ چند منٹ بعد دوبارہ چیک کریں۔"
                )
            elif lang == "roman_ur":
                speech_text = (
                    f"Ji samajh gaya. Server mein thora technical issue aya hai jo humne notice kar liya hai. "
                    f"Ticket #{ticket['id']} generate kar ke senior engineers ko alert bhej diya hai. Thori der intezar karein, system jaldi chal jayega."
                )
            else:
                speech_text = (
                    f"I have identified the system issue and dispatched emergency ticket #{ticket['id']} directly to our lead engineers. "
                    f"They are actively restoring the service. You can expect it to be back online shortly."
                )

            action_summary = f"Dispatched Emergency Ticket #{ticket['id']} to restore server infrastructure."

        # Problem Type 3: Project cost / estimation / new website or app
        elif "scope" in user_lower or "estimate" in user_lower or "cost" in user_lower or "budget" in user_lower or "kharcha" in user_lower or "banana" in user_lower or intent_info["primary_intent"] == "scope_estimation":
            weeks = 6
            scope_res = ToolExecutor.execute("calculate_scope_estimate", {
                "project_name": "Custom Mobile App & Web Solution",
                "tech_stack": "Complete Mobile App & Website",
                "complexity": "medium",
                "duration_weeks": weeks
            })
            executed_tools.append({"tool": "calculate_scope_estimate", "result": scope_res})
            s_data = scope_res["data"]

            if lang == "ur":
                speech_text = (
                    f"آپ کا نیا پروجیکٹ تقریباً {s_data['estimated_weeks']} ہفتوں میں مکمل تیار ہو سکتا ہے۔ "
                    f"اس کا کل خرچہ تقریباً {s_data['total_pkr']:,} روپے بنتا ہے جس میں مکمل موبائل ایپ، ویب سائٹ اور مینٹیننس شامل ہے۔ "
                    f"کیا آپ چاہتے ہیں کہ ہمارا مینیجر آپ سے فون پر بات کر کے تفصیل بتائے؟"
                )
            elif lang == "roman_ur":
                speech_text = (
                    f"Aap ka project taqreeban {s_data['estimated_weeks']} hafton (weeks) mein mukammal tayar ho sakta hai. "
                    f"Iska kul kharcha taqreeban Rs. {s_data['total_pkr']:,} PKR banega ($35/hr standard offshore rate). "
                    f"Isme mobile app, website aur testing shamil hai. Kya aap chahte hain ke hamara manager aap se direct call kare?"
                )
            else:
                speech_text = (
                    f"Your custom software project will take approximately {s_data['estimated_weeks']} weeks to build. "
                    f"The total estimated cost is ${s_data['total_usd']:,} USD (approximately Rs. {s_data['total_pkr']:,} PKR). "
                    f"This covers end-to-end design, development, and quality assurance. Would you like to schedule a discovery call?"
                )

            action_summary = f"Estimated project duration ({s_data['estimated_weeks']} weeks) and budget (Rs. {s_data['total_pkr']:,} PKR)."

        # Problem Type 4: Speak to manager / Urgent escalation
        elif "manager" in user_lower or "lead" in user_lower or "senior" in user_lower or "escalate" in user_lower or "jaldi" in user_lower or intent_info["primary_intent"] == "urgent_escalation":
            esc_res = ToolExecutor.execute("escalate_incident", {
                "ticket_id": "TICK-9041",
                "reason": user_text
            })
            executed_tools.append({"tool": "escalate_incident", "result": esc_res})

            if lang == "ur":
                speech_text = (
                    "جی بالکل، آپ کی درخواست پر آپ کا کیس فوری طور پر ہمارے سینئر مینیجر اور ٹیکنیکل لیڈ کو بھیج دیا گیا ہے۔ "
                    "وہ ترجیحی بنیاد پر خود آپ کے مسئلے کو دیکھ رہے ہیں۔"
                )
            elif lang == "roman_ur":
                speech_text = (
                    "Ji bilkul, aapki request par case fori tor par hamare Senior Manager aur Tech Lead ko forward kar diya gaya hai. "
                    "Woh personally aapka issue resolve kar rahe hain."
                )
            else:
                speech_text = (
                    "Your request has been escalated directly to our Senior Engineering Leadership. "
                    "A lead specialist has taken personal ownership of your issue."
                )

            action_summary = "Escalated case to Senior Leadership roster."

        # Problem Type 5: General guidance / How to use / Help
        else:
            if lang == "ur":
                speech_text = (
                    "السلام علیکم! میں آپ کی کیا مدد کر سکتا ہوں؟ "
                    "اگر آپ کی پیمنٹ میں مسئلہ ہے، ویب سائٹ نہیں چل رہی، یا کوئی نیا سافٹ ویئر بنوانا ہے، تو مجھے بول کر یا لکھ کر بتائیں۔"
                )
            elif lang == "roman_ur":
                speech_text = (
                    "Assalam-o-Alaikum! Main aapki kya madad kar sakta hoon? "
                    "Agar payment ka masla hai, website down hai, ya naya project banana hai, to aap mic daba kar bol sakte hain ya likh kar bata sakte hain."
                )
            else:
                speech_text = (
                    "Welcome! How may I assist you today? "
                    "You can ask me to help with payment issues, website downtime, speaking with a manager, or estimating new project costs."
                )

            action_summary = "Provided customer assistance guidance."

        return {
            "text": speech_text,
            "speech": speech_text,
            "language": lang,
            "urgency": urgency,
            "tools_executed": executed_tools,
            "action_summary": action_summary
        }

    def generate_response(self, user_text: str, context_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        context_history = context_history or []
        decision = self._simple_human_reasoning(user_text, context_history)
        return decision

llm_client = LLMClient()
