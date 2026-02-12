# Alogram PayRisk Local Emulator

[![Docker Image](https://img.shields.io/badge/docker-alogram%2Fpayrisk--emulator-blue.svg)](https://hub.docker.com/r/alogram/payrisk-emulator)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

The official local emulator for the Alogram PayRisk API. This emulator provides a fully spec-compliant API for local development and CI/CD, allowing you to test your integrations without requiring network access or production API keys.

## 🚀 Quick Start

### 1. Build and Run with Docker

Alogram provides the full source code for the local emulator to ensure maximum transparency and security. Build and launch it locally:

```bash
# 1. Clone the repository
git clone https://github.com/alogram/alogram-payrisk-emulator.git
cd alogram-payrisk-emulator

# 2. Build the image
docker build -t alogram/payrisk-emulator .

# 3. Run the container
docker run -p 8080:8080 alogram/payrisk-emulator
```

The emulator will be available at `http://localhost:8080`.

### 2. Run with Docker Compose

Add this to your `docker-compose.yml` for seamless local development:

```yaml
services:
  alogram-emulator:
    build: 
      context: ./path/to/alogram-payrisk-emulator
    ports:
      - "8080:8080"
    environment:
      - DEBUG=true
```

## 🧪 Verification

### 1. Health Check
Verify the emulator is running and healthy:
```bash
curl -i http://localhost:8080/v1/health
```

### 2. Smoke Test (Risk Check)
Test a mock purchase evaluation:
```bash
curl -X POST http://localhost:8080/v1/risk/check \
  -H "Content-Type: application/json" \
  -H "x-api-key: test_key" \
  -H "X-Idempotency-Key: idk_550e8400e29b41d4a716446655440000" \
  -d '{
    "purchase": {
      "amount": 99.99,
      "currency": "USD",
      "transaction_id": "tx_smoke_001"
    }
  }'
```

## 🛡️ SDK Integration

To use the emulator, simply override the `baseUrl` (or `BaseURL`) in your SDK client:

| SDK Language | Client Initialization |
| :--- | :--- |
| **Python** | `AlogramRiskClient(base_url="http://localhost:8080", api_key="test")` |
| **TypeScript** | `new AlogramRiskClient({ baseUrl: 'http://localhost:8080', apiKey: 'test' })` |
| **Go** | `alogram.NewAlogramRiskClient(alogram.ClientOptions{ BaseURL: "http://localhost:8080", APIKey: "test" })` |

## 🔑 Authentication

The emulator accepts **any string** as an API Key. You do not need a real key from the Alogram Dashboard for local testing.

## 🤖 For AI Agents (Integration Context)

If you are using an AI agent (like ChatGPT, Claude, or Gemini), provide this context:

> "I want to test my Alogram PayRisk integration locally. I have the Alogram Local Emulator running on `http://localhost:8080`. Configure my SDK client to point to this local endpoint and use 'test_key' as the API key."

---

## 🧪 Advanced Usage

The emulator returns spec-compliant responses (e.g., `approve`) by default. In future releases, you will be able to script specific outcomes using custom request headers.

## 🏗️ Building from Source

If you wish to build the emulator image manually:

```bash
docker build -t alogram/payrisk-emulator .
```

## ⚖️ License

Apache License 2.0. See [LICENSE](LICENSE) for details.