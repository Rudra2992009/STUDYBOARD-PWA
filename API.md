# STUDYBOARD API Documentation

## Base URL

**Local Development**: `http://localhost:5000`
**Production**: `https://your-domain.com`

---

## Authentication

Currently no authentication required. For production, implement API keys or OAuth.

---

## Endpoints

### Health Check

**GET** `/health`

Check if the server and models are ready.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-21T18:30:00.000Z",
  "models_loaded": true
}
```

**Status Codes**:
- `200 OK`: Server is healthy
- `503 Service Unavailable`: Models not loaded

---

### Chat Endpoint

**POST** `/api/chat`

Send a message to the AI tutor and optionally generate an image.

**Request Body**:
```json
{
  "message": "Explain Newton's first law of motion",
  "exam_class": "10",
  "generate_image": true
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | User's question (max 500 chars) |
| `exam_class` | string | No | Class level: "10" or "12" (default: "10") |
| `generate_image` | boolean | No | Generate visual diagram (default: true) |

**Response**:
```json
{
  "text_response": "Newton's first law states that an object at rest stays at rest...",
  "image_url": "/api/images/study_img_abc123.png",
  "timestamp": "2025-11-21T18:30:05.000Z"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `text_response` | string | AI-generated explanation |
| `image_url` | string/null | URL to generated image (null if not requested) |
| `timestamp` | string | ISO timestamp of response |

**Status Codes**:
- `200 OK`: Success
- `400 Bad Request`: Missing or invalid parameters
- `500 Internal Server Error`: Model inference failed

**Example Request** (cURL):
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is photosynthesis?",
    "exam_class": "10",
    "generate_image": true
  }'
```

**Example Request** (JavaScript):
```javascript
fetch('http://localhost:5000/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'Explain Ohm\'s Law',
    exam_class: '12',
    generate_image: true
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### Model Status

**GET** `/api/models/status`

Get current status of loaded AI models.

**Response**:
```json
{
  "ready": true,
  "device": "cuda",
  "text_model_loaded": true,
  "image_model_loaded": true
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `ready` | boolean | All models ready for inference |
| `device` | string | Compute device: "cuda" or "cpu" |
| `text_model_loaded` | boolean | Text model (Llama) loaded |
| `image_model_loaded` | boolean | Image model (SD) loaded |

**Status Codes**:
- `200 OK`: Status retrieved

---

### Serve Generated Images

**GET** `/api/images/{filename}`

Retrieve a generated image by filename.

**Parameters**:
- `filename`: Image filename (e.g., `study_img_abc123.png`)

**Response**:
- Binary image data (PNG format)

**Status Codes**:
- `200 OK`: Image found
- `404 Not Found`: Image doesn't exist

**Example**:
```html
<img src="http://localhost:5000/api/images/study_img_abc123.png" alt="Diagram">
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

**Common Errors**:

### 400 Bad Request
```json
{
  "error": "Invalid request",
  "message": "Message is required"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "CUDA out of memory"
}
```

---

## Rate Limiting

**Current**: No rate limiting (local use)

**Recommended for Production**:
- 10 requests per minute per IP
- 100 requests per hour per IP

Implement using Flask-Limiter:
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    # ...
```

---

## WebSocket API (Future)

**Planned**: Real-time streaming responses

```javascript
const ws = new WebSocket('ws://localhost:5000/ws/chat');

ws.onopen = () => {
  ws.send(JSON.stringify({
    message: 'Explain gravity',
    exam_class: '10'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Partial response:', data.text);
};
```

---

## CORS Configuration

**Development**: All origins allowed

**Production**: Configure specific origins in `server.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://yourdomain.com",
            "https://www.yourdomain.com"
        ]
    }
})
```

---

## Best Practices

1. **Timeouts**: Set request timeout to 300s for AI operations
2. **Retry Logic**: Implement exponential backoff for failed requests
3. **Caching**: Cache responses for identical queries
4. **Input Validation**: Sanitize user input before sending
5. **Error Handling**: Always handle errors gracefully

**Example with Retry**:
```javascript
async function chatWithRetry(message, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
        timeout: 300000  // 5 minutes
      });
      return await response.json();
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i)));
    }
  }
}
```

---

## Performance Tips

1. **Batch Requests**: Send multiple questions in one call (future feature)
2. **Image Size**: Reduce to 256x256 for faster generation
3. **Model Selection**: Use TinyLlama for faster responses
4. **Caching**: Implement Redis for response caching

---

## Security Considerations

1. **Input Sanitization**: Prevent injection attacks
2. **Rate Limiting**: Prevent abuse
3. **HTTPS**: Always use in production
4. **API Keys**: Implement authentication
5. **Content Filtering**: Block inappropriate requests

---

## Support

- **GitHub Issues**: [Report bugs](https://github.com/Rudra2992009/STUDYBOARD-PWA/issues)
- **Email**: rudra160113.work@gmail.com
- **Documentation**: [README](README.md)