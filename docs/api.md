# 🚀 HopeShot API Documentation

---

## 🌐 **Base URL**
- **Development**: `http://localhost:8000`
- **Production**: *TBD*

---

## 📋 **Available Endpoints**

### 🏠 **GET /** 
**Purpose**: Root endpoint providing basic API information

**Response Example**:
```json
{
  "message": "Hello from HopeShot backend! 🌟",
  "status": "running",
  "version": "0.1.0"
}
```

**Status Codes**:
- ✅ `200 OK`: Successful r# HopeShot API Documentation

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: TBD

## Endpoints

### GET /
**Description**: Root endpoint providing basic API information

**Response**:
```json
{
  "message": "Hello from HopeShot backend! 🌟",
  "status": "running",
  "version": "0.1.0"
}
```

**Status Codes**:
- `200 OK`: Successful response

---

### GET /api/test
**Description**: Connection test endpoint with sample data

**Response**:
```json
{
  "message": "Backend connection successful!",
  "data": {
    "timestamp": "2024-01-01",
    "backend_status": "healthy"
  }
}
```

**Status Codes**:
- `200 OK`: Successful response

## Error Handling

### Standard Error Response
```json
{
  "detail": "Error description"
}
```

### Common Status Codes
- `200 OK`: Request successful
- `404 Not Found`: Endpoint not found
- `500 Internal Server Error`: Server error

## CORS Configuration
- **Allowed Origins**: `http://localhost:3000` (Next.js frontend)
- **Allowed Methods**: All (`*`)
- **Allowed Headers**: All (`*`)
- **Credentials**: Enabled

## Testing
- **Manual Testing**: Visit `http://localhost:3000/test`
- **Direct API Calls**:
  ```bash
  curl http://localhost:8000/
  curl http://localhost:8000/api/test
  ```

## Future Endpoints (Planned)
- `GET /api/news` - Fetch positive news articles
- `POST /api/analyze` - Analyze article sentiment
- `GET /api/health` - Detailed health check

---
*API Version: 0.1.0*