"""
AURA Enterprise Knowledge & Runbook Store
Indexed playbooks, SLA policies, and technical incident runbooks for immediate voice/chat RAG.
"""

import math
import re
from typing import List, Dict, Any

KNOWLEDGE_DOCUMENTS = [
    {
        "id": "RUNBOOK-01",
        "title": "PostgreSQL / MySQL Connection Pool Exhaustion & Deadlock Recovery",
        "category": "Database Operations",
        "keywords": ["database", "deadlock", "postgres", "mysql", "connection pool", "timeout", "slow query"],
        "content": (
            "1. Triage: Check pg_stat_activity or SHOW PROCESSLIST for blocked transactions. "
            "2. Identify long-running queries > 30s. "
            "3. Immediate Mitigation: Execute pg_terminate_backend(pid) on blocking queries. "
            "4. Verify PgBouncer or connection pooler max_connections limit. "
            "5. If deadlocks persist in financial reconciliation tables, enable row-level locking with SELECT FOR UPDATE SKIP LOCKED."
        )
    },
    {
        "id": "RUNBOOK-02",
        "title": "Kubernetes Ingress 502 / 504 Gateway Timeout & Pod CrashLoopBackOff",
        "category": "Infrastructure & Cloud",
        "keywords": ["kubernetes", "k8s", "crashloopbackoff", "ingress", "502", "504", "server down", "pod"],
        "content": (
            "1. Triage: Run `kubectl get pods -n production -o wide` to locate crashing pods. "
            "2. Check logs: `kubectl logs <pod-name> --previous` for OOMKilled (Exit Code 137) or uncaught exceptions. "
            "3. Mitigation: If OOMKilled, scale pod memory request/limit in deployment spec. "
            "4. Ingress: Check NGINX Ingress controller proxy-read-timeout and proxy-connect-timeout (default 60s). "
            "5. Temporary Relief: Trigger rolling restart: `kubectl rollout restart deployment/<app-name> -n production`."
        )
    },
    {
        "id": "RUNBOOK-03",
        "title": "Payment Gateway Webhook Timeout (Stripe, JazzCash, Easypaisa, 1Link)",
        "category": "Fintech & Payments",
        "keywords": ["payment", "stripe", "jazzcash", "easypaisa", "1link", "webhook", "transaction", "settlement"],
        "content": (
            "1. Triage: Check payment provider dashboard for failed webhook deliveries (HTTP 500 / 408). "
            "2. Validation: Verify HMAC SHA-256 signature against webhook signing secret. "
            "3. Asynchronous Ingestion: Webhook endpoints must immediately return HTTP 200/202 and push the event payload into Redis/RabbitMQ queue. "
            "4. Idempotency: Always store idempotency_key to prevent double-charging or duplicate wallet balances. "
            "5. Reconciliation: Run the end-of-day ledger script to balance unsettled transactions with 1Link/bank switch."
        )
    },
    {
        "id": "RUNBOOK-04",
        "title": "Enterprise SLA Tier Support & Response Time Matrix",
        "category": "SLA & Contracts",
        "keywords": ["sla", "contract", "support tier", "response time", "gold", "platinum", "escalation"],
        "content": (
            "1. Platinum Tier (Mission Critical): P1 response within 15 mins, 24/7 dedicated Slack/Teams bridge, hourly executive briefing. "
            "2. Gold Tier (Enterprise Core): P1 response within 30 mins, P2 within 2 hours, 24/5 coverage. "
            "3. Standard Tier: P1 response within 2 hours, business hours coverage (09:00 - 18:00 PKT / 04:00 - 13:00 UTC). "
            "4. Escalation Trigger: If P1 remains unacknowledged within 50% of SLA window, auto-page Tier-2 Tech Lead."
        )
    },
    {
        "id": "RUNBOOK-05",
        "title": "Cross-Border Project Scoping & Delivery Protocol (Offshore BPO/IT)",
        "category": "Project Scoping",
        "keywords": ["scope", "estimate", "rate", "cost", "timeline", "sprint", "bpo", "pakistan", "offshore"],
        "content": (
            "1. Scoping Phases: Discovery Call (45m) -> Architecture & Tech Stack Matrix -> Sprint Estimation (Story Points) -> SOW Signoff. "
            "2. Standard Rate Benchmarks: Full-Stack Engineers $30-$45/hr USD, QA & Automation $25-$35/hr USD. "
            "3. Local Corporate Pricing: 7,500 - 12,000 PKR/hour depending on seniority and compliance requirements. "
            "4. Timezone Overlap: Guarantee minimum 4 hours daily overlap with US EST or UK BST working hours."
        )
    }
]

class KnowledgeBase:
    """Lightweight vector/TF-IDF hybrid RAG search for low-latency voice agent answers."""

    def __init__(self):
        self.docs = KNOWLEDGE_DOCUMENTS
        self._build_vocab()

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w{3,}\b", text.lower())

    def _build_vocab(self):
        self.doc_vectors = []
        df: Dict[str, int] = {}
        total_docs = len(self.docs)

        for doc in self.docs:
            combined = f"{doc['title']} {' '.join(doc['keywords'])} {doc['content']}"
            tokens = self._tokenize(combined)
            term_freq: Dict[str, int] = {}
            for t in tokens:
                term_freq[t] = term_freq.get(t, 0) + 1
            for t in term_freq:
                df[t] = df.get(t, 0) + 1
            self.doc_vectors.append((doc, term_freq))

        self.idf = {t: math.log((total_docs + 1) / (count + 1)) + 1 for t, count in df.items()}

    def search(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        tokens = self._tokenize(query)
        if not tokens:
            return self.docs[:top_k]

        query_freq: Dict[str, int] = {}
        for t in tokens:
            query_freq[t] = query_freq.get(t, 0) + 1

        scored_docs = []
        for doc, term_freq in self.doc_vectors:
            score = 0.0
            # Keyword exact boost
            for kw in doc.get("keywords", []):
                if kw in query.lower():
                    score += 5.0

            # Cosine-like TF-IDF score
            for t, qf in query_freq.items():
                if t in term_freq:
                    tf = term_freq[t]
                    idf = self.idf.get(t, 1.0)
                    score += (tf * idf) * (qf * idf)

            if score > 0.0:
                scored_docs.append((score, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        results = [doc for _, doc in scored_docs[:top_k]]
        return results if results else self.docs[:1]

knowledge_base = KnowledgeBase()
