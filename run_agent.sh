#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "================================================================="
echo "  Starting AURA: Enterprise IT & BPO Voice & Chat Agent Core     "
echo "  Matrix Solutions Pakistan — 24/7 Global Delivery & Triage     "
echo "================================================================="

export PYTHONPATH=.
export PYTHONUNBUFFERED=1
exec python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
