# 🏦 Insurance Policy Enquiry AI Agent

A production-grade **Voice & Chat Insurance Policy Enquiry AI Assistant** built using FastAPI.
The system provides **accurate, policy-grounded responses** while strictly following
insurance compliance, privacy, and escalation rules.

---

## 🎯 Project Objective

- Answer insurance policy queries in real-time
- Reduce call-center workload
- Ensure zero hallucination using document grounding
- Escalate safely when confidence is low or queries are out of scope

---

## 🚫 Out of Scope (Strict Rules)

- ❌ Claim initiation
- ❌ Payment processing
- ❌ Personalized advice
- ❌ Policy interpretation beyond documents

---

## 🧠 Supported Query Types

- Policy coverage
- Policy benefits
- Policy exclusions
- Policy validity
- Renewal dates
- Claim process (information only)
- Human agent request

---

## 🏗️ Project Architecture

- **FastAPI** → Backend API
- **NLU Layer** → Intent detection & confidence scoring
- **Retrieval Layer** → Policy JSON grounding
- **Escalation Layer** → Human handoff logic
- **Logging Layer** → Auditable conversation logs
- **.env** → Secure API key storage (Gemini-ready)

---

## 📁 Project Structure

