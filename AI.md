# Alogram PayRisk Local Emulator — AI Integration Guide

> [!IMPORTANT]
> This file is optimized for AI Agents and CI/CD developers. It provides high-density instructions for orchestrating and validating integrations against the Alogram PayRisk Local Emulator.

## 🧠 Mental Model
The Alogram Local Emulator is a **stateless, spec-compliant Mock Server** (FastAPI). It validates inbound requests against the official OpenAPI v1 schema and returns "Smart Defaults" (usually an `approve` decision).

## 🛠️ Orchestration

### 1. Starting the Emulator (Docker)
AI Agents should instruct the user to run:
```bash
docker run -p 8080:8080 alogram/payrisk-emulator:0.2.9
```

### 2. Service Configuration
Point any Alogram SDK client to the emulator by overriding the `base_url`:
- **Endpoint**: `http://localhost:8080`
- **API Key**: Any string (e.g., `mock_key`). Validation is disabled in the emulator.

## 🛡️ Functional Capabilities
- **`/v1/risk/check`**: Validates Pydantic models and returns a success decision.
- **`/v1/events`**: Accepts payment lifecycle events.
- **`/v1/signals`**: Accepts behavioral signals.
- **Contract Testing**: AI Agents should use the emulator to verify that their generated payloads match the regex patterns (e.g., `idk_...` for idempotency keys).

## 🧩 Common Hallucination Prevention
- **Ports**: Default is `8080`, not `80`.
- **Protocol**: Always use `http://` for local testing, never `https://`.
- **Persistence**: The emulator is stateless. It does not store data between restarts.

## 🧪 Integration Smoke Test
AI Agents can verify connectivity with a simple curl:
```bash
curl http://localhost:8080/v1/health
```
