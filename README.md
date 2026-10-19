# AURA: Autonomous Voice and Chat AI Agent

A bilingual real-time voice and chat platform designed for enterprise IT triage, customer support, and software scoping. AURA supports English, Urdu, and Roman Urdu, allowing everyday users and enterprise teams to communicate naturally via speech or text.

---

## Key Capabilities

- Real-Time Voice Processing: Interactive speech recognition with animated waveform visualization and automatic text-to-speech voice playback.
- Trilingual Understanding: Native handling and code-switching across English, Urdu, and Roman Urdu.
- Customer-Centric Triage: Plain-language, reassuring problem diagnosis with automatic complaint ticket generation.
- Incident Escalation: Classifies issues from P1 (Critical) to P4 (Low) and routes them to on-call engineering leads.
- Dual-Currency Project Scoping: Computes software project durations, sprint milestones, and dual budget estimates in USD and PKR.
- Operations Knowledge Base: Instant retrieval of operational runbooks for databases, cloud clusters, and payment integrations.

---

## System Requirements

- Linux or macOS (Ubuntu/Debian/Kali tested)
- Python 3.10 or higher
- Modern web browser with microphone access (Firefox, Chrome, or Chromium)

---

## Installation and Setup

1. Clone the repository:
```bash
git clone git@github.com:hamzaihsan9/aura-ai-agent.git
cd aura-ai-agent
```

2. Verify dependencies:
Ensure Python packages are installed:
```bash
pip install fastapi uvicorn websockets pydantic
```

---

## How to Run

1. Start the server using the provided launch script:
```bash
./run_agent.sh
```

Alternatively, run via Uvicorn directly:
```bash
export PYTHONPATH=.
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

2. Open the web interface:
Navigate to `http://localhost:8000` in your web browser.

---

## How to Use

1. Voice Mode:
- Click the Speak button (microphone icon).
- Speak your inquiry or issue in English, Urdu, or Roman Urdu.
- Click again to stop speaking, or pause for automatic detection.
- AURA will process the audio, display the transcript, and respond both in text and spoken voice.

2. Text Mode:
- Type your message into the text field at the bottom.
- Press Enter or click the Send button.

3. Quick Problem Actions:
- Use the 1-click action cards to immediately test common workflows:
  - Payment Stuck: Initiates payment verification and registers a support ticket.
  - System Down: Diagnoses server outages and alerts on-call engineering.
  - Talk to Manager: Triggers immediate escalation to senior leadership.
  - Check Cost: Computes engineering hours, duration, and budget.

4. Operations Radar:
- View active tickets and complaints in the live radar section at the bottom.
- Click the Escalate button on any active ticket to elevate its severity level.

---

## Running Automated Tests

Run the comprehensive unit test suite:
```bash
PYTHONPATH=. python3 tests/test_aura_engine.py
```

All 8 test suites verify:
- Bilingual language detection across dialects
- Intent analysis and urgency scoring
- Autonomous SLA ticket creation and escalation
- Dual-currency scoping calculations
- Runbook knowledge base search
- Multi-turn conversation handling

---

## Repository Structure

```
aura-ai-agent/
├── backend/
│   ├── main.py                  # FastAPI application and WebSocket endpoints
│   ├── agent/
│   │   ├── bilingual_processor.py # Dialect analysis and intent scoring
│   │   ├── llm_client.py        # Customer response reasoning engine
│   │   ├── orchestrator.py      # Conversation turn and state manager
│   │   └── tools.py             # Tool execution registry
│   ├── knowledge/
│   │   └── store.py             # Runbook retrieval store
│   └── ops/
│       └── ticket_engine.py     # SLA ticket management and cost estimator
├── frontend/
│   └── templates/
│       └── index.html           # Web interface template
├── tests/
│   └── test_aura_engine.py      # Automated test harness
├── run_agent.sh                 # Startup executable script
└── README.md                    # Project documentation
```

---

## API Summary

- GET `/`: Web console interface
- GET `/api/status`: Service health check and supported dialects
- GET `/api/tickets`: Returns active complaint and incident tickets
- POST `/api/tickets`: Creates a new ticket
- POST `/api/tickets/escalate`: Escalates an existing ticket to senior engineering
- POST `/api/scope/calculate`: Computes software duration, hours, and budget
- GET `/api/knowledge/search`: Searches operational runbooks
- POST `/api/chat`: Processes text input and returns agent reasoning
- WebSocket `/ws/voice-agent`: Bidirectional audio and text streaming
