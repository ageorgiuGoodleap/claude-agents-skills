# OpenAPI 3.0 Common Patterns

## Table of Contents
1. [Pagination](#pagination)
2. [Filtering and Searching](#filtering-and-searching)
3. [Sorting](#sorting)
4. [Field Selection](#field-selection)
5. [Batch Operations](#batch-operations)
6. [File Upload](#file-upload)
7. [Versioning](#versioning)
8. [Error Responses](#error-responses)

## Pagination

### Offset-Based Pagination
Most common pattern for simple APIs.

```yaml
parameters:
  - name: page
    in: query
    description: Page number (1-indexed)
    schema:
      type: integer
      minimum: 1
      default: 1
  - name: limit
    in: query
    description: Items per page
    schema:
      type: integer
      minimum: 1
      maximum: 100
      default: 20

responses:
  '200':
    description: Paginated list
    content:
      application/json:
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/components/schemas/User'
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                limit:
                  type: integer
                  example: 20
                total:
                  type: integer
                  description: Total number of items
                  example: 150
                pages:
                  type: integer
                  description: Total number of pages
                  example: 8
                has_next:
                  type: boolean
                  example: true
                has_prev:
                  type: boolean
                  example: false
```

### Cursor-Based Pagination
Better for real-time data and large datasets.

```yaml
parameters:
  - name: cursor
    in: query
    description: Pagination cursor from previous response
    schema:
      type: string
  - name: limit
    in: query
    schema:
      type: integer
      minimum: 1
      maximum: 100
      default: 20

responses:
  '200':
    content:
      application/json:
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/components/schemas/Post'
            pagination:
              type: object
              properties:
                next_cursor:
                  type: string
                  nullable: true
                  description: Cursor for next page (null if last page)
                  example: "eyJpZCI6MTAwfQ=="
                has_more:
                  type: boolean
                  example: true
```

## Filtering and Searching

### Query Parameter Filtering
```yaml
parameters:
  - name: status
    in: query
    description: Filter by status
    schema:
      type: string
      enum: [active, inactive, pending]
  - name: created_after
    in: query
    description: Filter by creation date (ISO 8601)
    schema:
      type: string
      format: date-time
      example: "2025-01-01T00:00:00Z"
  - name: created_before
    in: query
    schema:
      type: string
      format: date-time
  - name: role
    in: query
    description: Filter by role (can specify multiple)
    schema:
      type: array
      items:
        type: string
        enum: [admin, user, guest]
    style: form
    explode: true
```

### Search Parameter
```yaml
parameters:
  - name: q
    in: query
    description: Search query (searches across name, email, bio)
    schema:
      type: string
      minLength: 2
      maxLength: 100
      example: "john doe"
```

## Sorting

### Simple Sorting
```yaml
parameters:
  - name: sort
    in: query
    description: |
      Sort field and direction. Format: field:direction
      Direction: asc (ascending) or desc (descending)
    schema:
      type: string
      pattern: '^[a-z_]+:(asc|desc)$'
      example: "created_at:desc"
```

### Multi-Field Sorting
```yaml
parameters:
  - name: sort
    in: query
    description: |
      Sort by multiple fields. Format: field1:dir,field2:dir
      Example: created_at:desc,name:asc
    schema:
      type: string
      pattern: '^([a-z_]+:(asc|desc))(,[a-z_]+:(asc|desc))*$'
      example: "created_at:desc,name:asc"
```

## Field Selection

### Sparse Fieldsets
Reduce payload size by selecting specific fields.

```yaml
parameters:
  - name: fields
    in: query
    description: |
      Comma-separated list of fields to include in response.
      Example: id,email,name
    schema:
      type: string
      pattern: '^[a-z_]+(,[a-z_]+)*$'
      example: "id,email,name"

responses:
  '200':
    description: User with selected fields only
    content:
      application/json:
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            email:
              type: string
              format: email
            name:
              type: string
          # Only specified fields are included
```

## Batch Operations

### Batch Create
```yaml
/users/batch:
  post:
    summary: Create multiple users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              users:
                type: array
                minItems: 1
                maxItems: 100
                items:
                  $ref: '#/components/schemas/CreateUserRequest'
    responses:
      '207':
        description: Multi-status response
        content:
          application/json:
            schema:
              type: object
              properties:
                results:
                  type: array
                  items:
                    type: object
                    properties:
                      index:
                        type: integer
                        description: Index in original request array
                      status:
                        type: integer
                        description: HTTP status code for this item
                        example: 201
                      data:
                        $ref: '#/components/schemas/User'
                      error:
                        $ref: '#/components/schemas/Error'
```

### Batch Update
```yaml
/users/batch:
  patch:
    summary: Update multiple users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              updates:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: string
                      format: uuid
                    data:
                      $ref: '#/components/schemas/UpdateUserRequest'
```

## File Upload

### Single File Upload
```yaml
/users/{userId}/avatar:
  post:
    summary: Upload user avatar
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: string
          format: uuid
    requestBody:
      required: true
      content:
        multipart/form-data:
          schema:
            type: object
            required:
              - file
            properties:
              file:
                type: string
                format: binary
                description: Image file (JPEG, PNG, GIF)
              description:
                type: string
                maxLength: 500
          encoding:
            file:
              contentType: image/jpeg, image/png, image/gif
    responses:
      '200':
        description: Avatar uploaded successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                url:
                  type: string
                  format: uri
                  example: "https://cdn.example.com/avatars/user-123.jpg"
                size:
                  type: integer
                  description: File size in bytes
                  example: 52438
```

### Multiple File Upload
```yaml
requestBody:
  content:
    multipart/form-data:
      schema:
        type: object
        properties:
          files:
            type: array
            items:
              type: string
              format: binary
```

## Versioning

### URL Path Versioning (Recommended)
```yaml
servers:
  - url: https://api.example.com/v1
    description: Version 1
  - url: https://api.example.com/v2
    description: Version 2
```

### Header Versioning
```yaml
parameters:
  - name: API-Version
    in: header
    required: true
    schema:
      type: string
      enum: ['1.0', '2.0']
      default: '1.0'
```

### Query Parameter Versioning
```yaml
parameters:
  - name: version
    in: query
    schema:
      type: string
      enum: ['1', '2']
      default: '1'
```

## Error Responses

### Standard Error Schema
```yaml
components:
  schemas:
    Error:
      type: object
      required:
        - error
      properties:
        error:
          type: object
          required:
            - code
            - message
          properties:
            code:
              type: string
              description: Machine-readable error code
              enum:
                - VALIDATION_ERROR
                - AUTHENTICATION_ERROR
                - AUTHORIZATION_ERROR
                - NOT_FOUND
                - CONFLICT
                - RATE_LIMIT_EXCEEDED
                - INTERNAL_ERROR
              example: VALIDATION_ERROR
            message:
              type: string
              description: Human-readable error message
              example: Invalid input data
            details:
              type: array
              description: Additional error details (for validation errors)
              items:
                type: object
                properties:
                  field:
                    type: string
                    example: email
                  message:
                    type: string
                    example: Invalid email format
                  code:
                    type: string
                    example: INVALID_FORMAT

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: VALIDATION_ERROR
              message: Invalid input data
              details:
                - field: email
                  message: Invalid email format

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: AUTHENTICATION_ERROR
              message: Invalid or missing authentication token

    Forbidden:
      description: Insufficient permissions
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: AUTHORIZATION_ERROR
              message: Insufficient permissions to access this resource

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: NOT_FOUND
              message: Resource not found

    Conflict:
      description: Resource conflict
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: CONFLICT
              message: Resource already exists

    RateLimitExceeded:
      description: Rate limit exceeded
      headers:
        X-RateLimit-Limit:
          schema:
            type: integer
          description: Request limit
        X-RateLimit-Remaining:
          schema:
            type: integer
          description: Requests remaining
        X-RateLimit-Reset:
          schema:
            type: integer
          description: Unix timestamp when limit resets
        Retry-After:
          schema:
            type: integer
          description: Seconds until retry allowed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: RATE_LIMIT_EXCEEDED
              message: Too many requests. Try again in 3600 seconds.

    InternalServerError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: INTERNAL_ERROR
              message: An unexpected error occurred
```

### Using Reusable Responses
```yaml
paths:
  /users/{userId}:
    get:
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
```
