# Sample API Documentation — User Management Service

## Base URL

```
https://api.example.com/v1
```

## Authentication

All endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <your-api-token>
```

---

## Endpoints

### GET /users

Retrieve a list of all users.

**Query Parameters:**

| Parameter | Type   | Required | Description                     |
|-----------|--------|----------|---------------------------------|
| page      | int    | No       | Page number (default: 1)        |
| limit     | int    | No       | Items per page (default: 20)    |
| role      | string | No       | Filter by role (admin, user)    |

**Response (200 OK):**

```json
{
  "users": [
    {
      "id": "usr_abc123",
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "role": "admin",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "total": 42,
  "page": 1,
  "limit": 20
}
```

**Error Responses:**

- `401 Unauthorized` — Missing or invalid token
- `429 Too Many Requests` — Rate limit exceeded (100 req/min)

---

### GET /users/{id}

Retrieve a single user by ID.

**Path Parameters:**

| Parameter | Type   | Required | Description       |
|-----------|--------|----------|-------------------|
| id        | string | Yes      | The user ID       |

**Response (200 OK):**

```json
{
  "id": "usr_abc123",
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "role": "admin",
  "created_at": "2025-01-15T10:30:00Z",
  "last_login": "2025-03-20T14:22:00Z"
}
```

**Error Responses:**

- `404 Not Found` — User does not exist
- `401 Unauthorized` — Missing or invalid token

---

### POST /users

Create a new user.

**Request Body:**

```json
{
  "name": "Bob Smith",
  "email": "bob@example.com",
  "role": "user",
  "password": "secureP@ss123"
}
```

**Field Validation:**

| Field    | Type   | Required | Constraints                              |
|----------|--------|----------|------------------------------------------|
| name     | string | Yes      | 2–100 characters                         |
| email    | string | Yes      | Valid email format, must be unique        |
| role     | string | Yes      | One of: "admin", "user", "viewer"        |
| password | string | Yes      | Min 8 chars, 1 uppercase, 1 number, 1 special char |

**Response (201 Created):**

```json
{
  "id": "usr_def456",
  "name": "Bob Smith",
  "email": "bob@example.com",
  "role": "user",
  "created_at": "2025-03-25T09:00:00Z"
}
```

**Error Responses:**

- `400 Bad Request` — Validation errors
- `409 Conflict` — Email already exists
- `401 Unauthorized` — Missing or invalid token

---

### PUT /users/{id}

Update an existing user.

**Request Body (partial updates allowed):**

```json
{
  "name": "Robert Smith",
  "role": "admin"
}
```

**Response (200 OK):** Returns the updated user object.

**Error Responses:**

- `400 Bad Request` — Validation errors
- `404 Not Found` — User does not exist
- `401 Unauthorized` — Missing or invalid token

---

### DELETE /users/{id}

Delete a user by ID.

**Response (204 No Content):** Empty response body.

**Error Responses:**

- `404 Not Found` — User does not exist
- `401 Unauthorized` — Missing or invalid token
- `403 Forbidden` — Cannot delete your own account

---

## Rate Limiting

- 100 requests per minute per API key
- `X-RateLimit-Remaining` header shows remaining requests
- `X-RateLimit-Reset` header shows reset time (Unix timestamp)

## Pagination

All list endpoints support `page` and `limit` query parameters.
Maximum `limit` is 100. Default `limit` is 20.
