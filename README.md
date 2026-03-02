# LLM Agent Tool Server

Minimal LLM-powered agent tool server built to demonstrate fast API integration,
tool calling, and agent-style decision logic.

## What this does
- Exposes an HTTP API to run an agent
- Agent decides whether to call a tool or respond directly
- Demonstrates structured inputs and outputs
- Designed to be simple, fast, and extendable

## Endpoint

POST `/agent/run`

### Request
```json
{
  "message": "2 + 2"
}
