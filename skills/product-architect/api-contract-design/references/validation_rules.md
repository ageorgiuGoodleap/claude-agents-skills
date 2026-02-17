# Validation Rules Library

Comprehensive validation patterns for common data types in API contracts.

## Table of Contents
1. [Email Addresses](#email-addresses)
2. [Passwords](#passwords)
3. [Usernames](#usernames)
4. [Phone Numbers](#phone-numbers)
5. [URLs](#urls)
6. [Dates and Times](#dates-and-times)
7. [UUIDs](#uuids)
8. [Names](#names)
9. [Addresses](#addresses)
10. [Financial Data](#financial-data)
11. [File Uploads](#file-uploads)

## Email Addresses

### OpenAPI Schema
```yaml
email:
  type: string
  format: email
  maxLength: 255
  pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
  example: user@example.com
  description: Valid email address (RFC 5322 compliant)
```

### Validation Rules
- **Format**: RFC 5322 compliant
- **Max length**: 255 characters (database standard)
- **Case**: Case-insensitive (normalize to lowercase before storage)
- **Whitespace**: No leading/trailing whitespace
- **Special chars**: Allowed in local part: letters, numbers, `._%+-`
- **Domain**: Must have valid TLD (2+ characters)
- **Storage**: Store normalized (lowercase, trimmed)

### Common Validation Errors
```yaml
error_responses:
  - field: email
    code: INVALID_FORMAT
    message: Invalid email format
  - field: email
    code: EMAIL_EXISTS
    message: Email already registered
  - field: email
    code: DISPOSABLE_EMAIL
    message: Disposable email addresses not allowed
```

## Passwords

### OpenAPI Schema
```yaml
password:
  type: string
  format: password
  minLength: 8
  maxLength: 128
  writeOnly: true
  example: SecureP@ss123
  description: |
    Password requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter (A-Z)
    - At least 1 lowercase letter (a-z)
    - At least 1 number (0-9)
    - At least 1 special character (!@#$%^&*()_+-=[]{}|;:,.<>?)
```

### Validation Rules
- **Min length**: 8 characters (NIST recommendation)
- **Max length**: 128 characters (allow passphrases)
- **Complexity**:
  - At least 1 uppercase letter
  - At least 1 lowercase letter
  - At least 1 number
  - At least 1 special character
- **No common passwords**: Check against list (e.g., "password123", "qwerty")
- **No personal info**: Not similar to email, name, username
- **No sequential**: Avoid "12345", "abcde"
- **Storage**: Hash with bcrypt (cost factor 12+)

### Password Strength Indicator
```yaml
password_strength:
  type: string
  enum: [weak, fair, good, strong]
  description: Calculated password strength
  example: strong
```

### Common Validation Errors
```yaml
error_responses:
  - field: password
    code: TOO_SHORT
    message: Password must be at least 8 characters
  - field: password
    code: NO_UPPERCASE
    message: Password must contain at least one uppercase letter
  - field: password
    code: NO_LOWERCASE
    message: Password must contain at least one lowercase letter
  - field: password
    code: NO_NUMBER
    message: Password must contain at least one number
  - field: password
    code: NO_SPECIAL_CHAR
    message: Password must contain at least one special character
  - field: password
    code: COMMON_PASSWORD
    message: Password is too common. Choose a more unique password
  - field: password
    code: SIMILAR_TO_EMAIL
    message: Password cannot be similar to your email address
```

## Usernames

### OpenAPI Schema
```yaml
username:
  type: string
  minLength: 3
  maxLength: 30
  pattern: '^[a-zA-Z0-9_-]+$'
  example: john_doe_123
  description: Alphanumeric characters, underscores, and hyphens only
```

### Validation Rules
- **Length**: 3-30 characters
- **Characters**: Letters (a-z, A-Z), numbers (0-9), underscore (_), hyphen (-)
- **Start**: Must start with letter or number (not underscore/hyphen)
- **No consecutive**: No consecutive underscores or hyphens
- **Reserved words**: Block system usernames (admin, root, system, api)
- **Case**: Case-insensitive for uniqueness check
- **Profanity**: Check against profanity list

### Common Validation Errors
```yaml
error_responses:
  - field: username
    code: TOO_SHORT
    message: Username must be at least 3 characters
  - field: username
    code: INVALID_CHARACTERS
    message: Username can only contain letters, numbers, underscores, and hyphens
  - field: username
    code: USERNAME_TAKEN
    message: Username already taken
  - field: username
    code: RESERVED_USERNAME
    message: This username is reserved
```

## Phone Numbers

### OpenAPI Schema
```yaml
phone:
  type: string
  pattern: '^\+[1-9]\d{1,14}$'
  example: "+14155552671"
  description: E.164 format (international format with country code)
```

### Validation Rules
- **Format**: E.164 international format
- **Structure**: `+[country code][number]`
- **Length**: 7-15 digits (after country code)
- **Country code**: 1-3 digits, starts with +
- **Validation**: Verify country code is valid
- **Storage**: Store in E.164 format
- **Display**: Format based on country (e.g., +1 (415) 555-2671)

### Alternative Schema (Flexible)
```yaml
phone:
  type: object
  required: [number, country_code]
  properties:
    country_code:
      type: string
      pattern: '^\+[1-9]\d{0,2}$'
      example: "+1"
    number:
      type: string
      pattern: '^\d{7,15}$'
      example: "4155552671"
```

## URLs

### OpenAPI Schema
```yaml
url:
  type: string
  format: uri
  maxLength: 2048
  pattern: '^https?://.+'
  example: "https://example.com/path"
  description: Valid HTTP/HTTPS URL
```

### Validation Rules
- **Protocol**: http:// or https:// (prefer https://)
- **Max length**: 2048 characters (browser standard)
- **Domain**: Valid domain name or IP address
- **Path**: URL-encoded if contains special characters
- **Security**: Validate against SSRF attacks (block internal IPs)

### Specialized URL Types
```yaml
# Avatar/Image URL
avatar_url:
  type: string
  format: uri
  pattern: '^https://.+\.(jpg|jpeg|png|gif|webp)$'
  example: "https://cdn.example.com/avatar.jpg"

# Webhook URL
webhook_url:
  type: string
  format: uri
  pattern: '^https://.+'
  example: "https://api.example.com/webhooks"
  description: HTTPS required for webhooks
```

## Dates and Times

### ISO 8601 Date
```yaml
date:
  type: string
  format: date
  pattern: '^\d{4}-\d{2}-\d{2}$'
  example: "2025-02-08"
  description: Date in ISO 8601 format (YYYY-MM-DD)
```

### ISO 8601 DateTime
```yaml
datetime:
  type: string
  format: date-time
  pattern: '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$'
  example: "2025-02-08T10:30:00Z"
  description: DateTime in ISO 8601 format with UTC timezone
```

### Unix Timestamp
```yaml
timestamp:
  type: integer
  format: int64
  minimum: 0
  example: 1707388200
  description: Unix timestamp (seconds since epoch)
```

### Validation Rules
- **Format**: ISO 8601 recommended
- **Timezone**: Always use UTC (Z suffix)
- **Precision**: Milliseconds optional
- **Past dates**: Validate if past date expected (e.g., birth_date)
- **Future dates**: Validate if future date expected (e.g., appointment)
- **Range**: Check reasonable date ranges (e.g., birth_date must be < today)

## UUIDs

### OpenAPI Schema
```yaml
id:
  type: string
  format: uuid
  pattern: '^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
  example: "550e8400-e29b-41d4-a716-446655440000"
  description: UUID v4
```

### Validation Rules
- **Format**: UUID v4 (random)
- **Structure**: 8-4-4-4-12 hexadecimal digits
- **Version**: 4th group starts with 4 (UUID v4)
- **Variant**: 5th group starts with 8, 9, a, or b
- **Case**: Lowercase recommended (but accept uppercase)

## Names

### Full Name
```yaml
name:
  type: string
  minLength: 1
  maxLength: 255
  pattern: '^[a-zA-Z\s\'-]+$'
  example: "John O'Brien-Smith"
  description: Full name (letters, spaces, hyphens, apostrophes)
```

### First/Last Name
```yaml
first_name:
  type: string
  minLength: 1
  maxLength: 100
  pattern: '^[a-zA-Z\'-]+$'
  example: "John"

last_name:
  type: string
  minLength: 1
  maxLength: 100
  pattern: '^[a-zA-Z\'-]+$'
  example: "O'Brien"
```

### Validation Rules
- **Characters**: Letters, spaces, hyphens, apostrophes
- **No numbers**: Names should not contain digits
- **Whitespace**: Trim leading/trailing, collapse multiple spaces
- **Unicode**: Consider international names (expand pattern if needed)
- **Min length**: At least 1 character
- **Max length**: 255 characters total (100 per field)

## Addresses

### Address Schema
```yaml
address:
  type: object
  required: [line1, city, country, postal_code]
  properties:
    line1:
      type: string
      maxLength: 255
      example: "123 Main Street"
      description: Primary address line
    line2:
      type: string
      maxLength: 255
      nullable: true
      example: "Apt 4B"
      description: Secondary address line (optional)
    city:
      type: string
      maxLength: 100
      example: "San Francisco"
    state:
      type: string
      maxLength: 100
      example: "California"
      description: State/province/region
    postal_code:
      type: string
      maxLength: 20
      example: "94102"
      description: ZIP/postal code
    country:
      type: string
      minLength: 2
      maxLength: 2
      pattern: '^[A-Z]{2}$'
      example: "US"
      description: ISO 3166-1 alpha-2 country code
```

### Postal Code Validation (Country-Specific)
```yaml
# US ZIP Code
postal_code_us:
  type: string
  pattern: '^\d{5}(-\d{4})?$'
  example: "94102"

# UK Postcode
postal_code_uk:
  type: string
  pattern: '^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$'
  example: "SW1A 1AA"

# Canada Postal Code
postal_code_ca:
  type: string
  pattern: '^[A-Z]\d[A-Z] ?\d[A-Z]\d$'
  example: "K1A 0B1"
```

## Financial Data

### Currency Amount
```yaml
amount:
  type: number
  format: decimal
  minimum: 0
  multipleOf: 0.01
  example: 99.99
  description: Amount in specified currency (2 decimal places)

currency:
  type: string
  minLength: 3
  maxLength: 3
  pattern: '^[A-Z]{3}$'
  example: "USD"
  description: ISO 4217 currency code
```

### Money Object
```yaml
money:
  type: object
  required: [amount, currency]
  properties:
    amount:
      type: integer
      minimum: 0
      example: 9999
      description: Amount in smallest currency unit (cents)
    currency:
      type: string
      pattern: '^[A-Z]{3}$'
      example: "USD"
```

### Credit Card (Tokenized)
```yaml
payment_method:
  type: object
  properties:
    type:
      type: string
      enum: [card, bank_account]
    token:
      type: string
      description: Payment token from payment processor
      example: "tok_1234567890"
    last4:
      type: string
      pattern: '^\d{4}$'
      example: "4242"
      description: Last 4 digits of card
    brand:
      type: string
      enum: [visa, mastercard, amex, discover]
      example: "visa"
```

**Security Note**: Never accept raw credit card numbers in API. Use payment processor tokens.

## File Uploads

### File Upload Schema
```yaml
file:
  type: string
  format: binary
  description: File to upload
```

### File Metadata Validation
```yaml
# Image Upload
image_upload:
  type: object
  properties:
    file:
      type: string
      format: binary
    filename:
      type: string
      maxLength: 255
      pattern: '^[\w\-. ]+\.(jpg|jpeg|png|gif|webp)$'
  x-validation:
    max_size: 5242880  # 5MB in bytes
    allowed_mime_types:
      - image/jpeg
      - image/png
      - image/gif
      - image/webp
    min_dimensions:
      width: 100
      height: 100
    max_dimensions:
      width: 4096
      height: 4096

# Document Upload
document_upload:
  type: object
  properties:
    file:
      type: string
      format: binary
  x-validation:
    max_size: 10485760  # 10MB
    allowed_mime_types:
      - application/pdf
      - application/msword
      - application/vnd.openxmlformats-officedocument.wordprocessingml.document
    scan_for_viruses: true
```

### Validation Rules
- **File size**: Enforce maximum size limits
- **MIME type**: Validate actual MIME type (not just extension)
- **File extension**: Whitelist allowed extensions
- **Content validation**: Check file content matches extension
- **Virus scanning**: Scan uploaded files for malware
- **Filename sanitization**: Remove path traversal characters (../, etc.)
