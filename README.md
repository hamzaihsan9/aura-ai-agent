# AURA: Autonomous Universal Relay & Assistant
### Enterprise Bilingual Voice & Chat AI Agent

---

## 🚀 Overview
**AURA** is a high-empathy, real-time voice and chat AI platform designed for cross-border enterprise IT triage, project scoping, and high-accessibility customer service.

### 🌟 Key Capabilities
1. **Real-Time Voice Streaming**: Interactive voice input via Web Speech API with live animated waveform and dual-engine text-to-speech auto-playback.
2. **Trilingual Code-Switching**: Speaks and understands **English (Global)**, **Urdu (اردو)**, and **Roman Urdu** natively.
3. **High-Accessibility for Everyday Customers**: Reassuring, jargon-free explanations, plain language problem diagnosis, and prominent 1-click support cards for payment issues, server outages, manager escalations, and cost estimates.
4. **Autonomous SLA Operations**: Automatically triages incidents (`P1 Critical` to `P4 Low`), creates complaint tickets, and auto-pages on-call engineering leads.
5. **Cross-Border Scoping**: Instant engineering sprint estimation with dual-currency budgets in **USD** ($35/hr benchmark) and **PKR**.
6. **RAG Knowledge Base**: Instant retrieval of mitigation runbooks for PostgreSQL deadlocks, Kubernetes crash loops, and payment webhook failures.

---

## 🏗 Architecture
```
[Browser / Microphone] <====(Web Speech & WebSocket Audio)====> [FastAPI Server :8000]
                                                                        │
        ┌───────────────────────────────┬───────────────────────────────┴──────────────────────────────┐
        ▼                               ▼                                                              ▼
 [Bilingual Processor]        [Agentic Tool Engine]                                          [RAG Runbook Store]
 (EN • اردو • Roman)         • create_sla_ticket (P1–P4)                                    • Postgres Deadlocks
                             • escalate_incident (L1->L2->L3)                               • Kubernetes 502/CrashLoop
                             • calculate_scope_estimate (USD/PKR)                           • Payment Webhooks
                             • schedule_technical_sync                                      • SLA Contracts
```

---

## ⚡ Quick Start

### 1. Launch Server
```bash
./run_agent.sh
```
Access the web console at: **`http://localhost:8000`**

### 2. Run Automated Tests
```bash
PYTHONPATH=. python3 tests/test_aura_engine.py
```
*Result: 8/8 test suites passing.*

---

## 📂 Project Structure
```
aura-ai-chat/
├── backend/
│   ├── main.py                  # FastAPI server, REST & WebSocket routes
│   ├── agent/
│   │   ├── bilingual_processor.py # Dialect & intent detection
│   │   ├── llm_client.py        # High-empathy customer response reasoner
│   │   ├── orchestrator.py      # Session and dialogue manager
│   │   └── tools.py             # Agentic tool registry
│   ├── knowledge/
│   │   └── store.py             # RAG incident playbooks & SLA matrices
│   └── ops/
│       └── ticket_engine.py     # SLA ticket tracker & dual scoping engine
├── frontend/
│   └── templates/
│       └── index.html           # Dark red Apple-style accessible UI
├── tests/
│   └── test_aura_engine.py      # Automated test harness
├── run_agent.sh                 # Production startup script
└── README.md
```
