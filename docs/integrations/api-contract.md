# API Contract — Customer Support AI

> **Purpose:** Defines the exact request/response shapes between the React frontend, FastAPI backend, and AI pipeline. Both the AI Engineer and Software Engineer must agree on this contract BEFORE writing code.
>
> **Status:** Draft (to be finalized in Spec M1)

---

## Chat Endpoint

### `POST /api/v1/chat`

Send a user message and receive an AI response.

**Request:**
```json
{
  "message": "I was charged twice for my subscription",
  "conversation_id": "conv_abc123"
}
```

**Response:**
```json
{
  "reply": "I'm sorry to hear about the double charge. Let me help you with that. Could you please provide your account email or order number so I can look into this?",
  "agent_used": "billing",
  "confidence": 0.92,
  "sources": [
    {
      "title": "Refund Policy FAQ",
      "chunk": "If you were charged twice, please contact support with your order number. Refunds are processed within 5-7 business days.",
      "relevance_score": 0.87
    },
    {
      "title": "Billing Issues Guide",
      "chunk": "Double charges can occur due to payment processing delays. Most duplicate charges are automatically reversed within 48 hours.",
      "relevance_score": 0.82
    }
  ],
  "conversation_id": "conv_abc123",
  "message_id": "msg_def456",
  "timestamp": "2026-08-18T10:30:00Z"
}
```

**Status codes:**
- `200` — Success
- `429` — Rate limited (all LLM providers exhausted)
- `500` — Internal error

---

## Conversation Endpoints

### `POST /api/v1/conversations`

Create a new conversation.

**Response:**
```json
{
  "id": "conv_abc123",
  "created_at": "2026-08-18T10:30:00Z",
  "title": "New Conversation"
}
```

### `GET /api/v1/conversations`

List all conversations.

**Response:**
```json
{
  "conversations": [
    {
      "id": "conv_abc123",
      "title": "Billing Issue",
      "last_message_at": "2026-08-18T10:30:00Z",
      "message_count": 5
    }
  ]
}
```

### `GET /api/v1/conversations/:id`

Get full conversation history.

**Response:**
```json
{
  "id": "conv_abc123",
  "messages": [
    {
      "id": "msg_001",
      "role": "user",
      "content": "I was charged twice",
      "timestamp": "2026-08-18T10:30:00Z"
    },
    {
      "id": "msg_002",
      "role": "assistant",
      "content": "I'm sorry to hear...",
      "agent_used": "billing",
      "sources": [...],
      "timestamp": "2026-08-18T10:30:02Z"
    }
  ]
}
```

### `DELETE /api/v1/conversations/:id`

Delete a conversation. Returns `204 No Content`.

---

## Health Check

### `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "llm_provider": "gemini",
  "knowledge_base_chunks": 2500,
  "version": "0.1.0"
}
```
