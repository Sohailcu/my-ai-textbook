# RAG API Contract

## /api/rag/query
### POST
**Description**: Submit a question to the RAG system for response based on textbook content

#### Request
```json
{
  "question": "string (required)",
  "chapter_id": "string (optional, specify chapter context)",
  "session_id": "string (optional, for anonymous users)",
  "user_id": "string (optional, for authenticated users)"
}
```

#### Response (200 OK)
```json
{
  "query_id": "string",
  "response": "string",
  "source_chapters": ["string"],
  "confidence": "float (0-1)",
  "timestamp": "datetime"
}
```

#### Error Responses
- 400: Invalid request format
- 429: Rate limit exceeded
- 500: Internal server error during query processing

## /api/textbook/chapters
### GET
**Description**: Retrieve list of all textbook chapters

#### Response (200 OK)
```json
{
  "chapters": [
    {
      "id": "string",
      "title": "string",
      "chapter_number": "integer",
      "sections": ["string"]
    }
  ]
}
```

## /api/textbook/chapter/{chapter_id}
### GET
**Description**: Retrieve content of a specific chapter

#### Response (200 OK)
```json
{
  "id": "string",
  "title": "string",
  "chapter_number": "integer",
  "content": "string (markdown)",
  "sections": ["string"]
}
```

## /api/auth/login
### POST
**Description**: Authenticate user for personalization features

#### Request
```json
{
  "email": "string",
  "password": "string"
}
```

#### Response (200 OK)
```json
{
  "user_id": "string",
  "session_id": "string",
  "token": "string",
  "expires_at": "datetime"
}
```

## /api/user/preferences
### GET
**Description**: Retrieve user preferences (requires authentication)

#### Headers
```
Authorization: Bearer {token}
```

#### Response (200 OK)
```json
{
  "language": "string",
  "personalization_enabled": "boolean",
  "preferred_chapters": ["integer"],
  "last_accessed_chapter": "integer"
}
```

### PUT
**Description**: Update user preferences (requires authentication)

#### Headers
```
Authorization: Bearer {token}
```

#### Request
```json
{
  "language": "string (optional)",
  "personalization_enabled": "boolean (optional)",
  "preferred_chapters": ["integer] (optional)",
  "last_accessed_chapter": "integer (optional)"
}
```

#### Response (200 OK)
```json
{
  "success": "boolean",
  "message": "string"
}
```