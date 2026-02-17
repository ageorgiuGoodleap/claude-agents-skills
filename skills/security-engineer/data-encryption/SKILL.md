---
name: data-encryption
description: |
  Implements comprehensive data encryption strategies including TLS/SSL for data in transit, database
  encryption at rest, field-level encryption for sensitive data (PII, PHI, PCI), and secure key management
  with KMS/HSM integration. Use when implementing encryption, TLS setup, SSL, HTTPS, database encryption,
  field encryption, key management, KMS, HSM, certificate management, data protection, or encrypting PII,
  PHI, or PCI data according to compliance requirements.
---

# Data Encryption

## Overview

This skill implements comprehensive data encryption to protect data throughout its lifecycle - in transit, at rest, and in use. It covers TLS/SSL configuration, database encryption, field-level encryption, and secure key management practices.

**Core Capabilities:**
- TLS/SSL configuration for data in transit
- Database encryption at rest (TDE)
- Field-level encryption for sensitive data
- Key management (KMS/HSM integration)
- Encryption for backups and logs
- Compliance-driven encryption (GDPR, HIPAA, PCI-DSS)

## When to Use This Skill

Trigger this skill when:
- Implementing TLS/SSL for HTTPS
- Setting up database encryption
- Encrypting sensitive fields (PII, PHI, PCI data)
- Configuring key management systems
- Implementing encryption for compliance
- Encrypting backups and logs
- Setting up certificate management

## Implementation Guide

### 1. TLS/SSL Configuration

Encrypt data in transit with properly configured TLS.

#### Web Server TLS Configuration

**Nginx**:
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    # TLS protocol versions (1.2 and 1.3 only)
    ssl_protocols TLSv1.2 TLSv1.3;

    # Strong cipher suites
    ssl_ciphers 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers on;

    # Certificates
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;

    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/ssl/certs/ca-bundle.crt;

    # Diffie-Hellman parameters
    ssl_dhparam /etc/ssl/certs/dhparam.pem;

    location / {
        proxy_pass http://localhost:3000;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

**Apache**:
```apache
<VirtualHost *:443>
    ServerName example.com

    # Enable SSL
    SSLEngine on

    # TLS protocol versions
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1

    # Strong cipher suites
    SSLCipherSuite ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256
    SSLHonorCipherOrder on

    # Certificates
    SSLCertificateFile /etc/ssl/certs/example.com.crt
    SSLCertificateKeyFile /etc/ssl/private/example.com.key
    SSLCertificateChainFile /etc/ssl/certs/ca-bundle.crt

    # HSTS
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"

    # OCSP Stapling
    SSLUseStapling on
    SSLStaplingCache "shmcb:logs/ssl_stapling(32768)"
</VirtualHost>
```

#### Certificate Management

Use Let's Encrypt for free automated certificates:

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renewal (runs twice daily)
sudo certbot renew --dry-run
```

For detailed TLS configuration, see [TLS Best Practices](references/tls-best-practices.md).

### 2. Database Encryption at Rest

Encrypt databases to protect data when stored on disk.

#### Transparent Data Encryption (TDE)

**PostgreSQL**:
```sql
-- Enable pgcrypto extension
CREATE EXTENSION pgcrypto;

-- Encrypt entire database cluster (filesystem level)
-- Use LUKS or similar for volume encryption

-- For column-level encryption
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    ssn BYTEA  -- Store encrypted
);

-- Encrypt on insert
INSERT INTO users (email, ssn)
VALUES ('user@example.com', pgp_sym_encrypt('123-45-6789', 'encryption_key'));

-- Decrypt on select
SELECT email, pgp_sym_decrypt(ssn, 'encryption_key') AS ssn
FROM users;
```

**MySQL**:
```sql
-- Enable InnoDB encryption
SET GLOBAL innodb_encryption_threads = 4;

-- Create encrypted table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255),
    ssn VARBINARY(255)
) ENCRYPTION='Y';

-- Encrypt keyring
[mysqld]
early-plugin-load=keyring_file.so
keyring_file_data=/var/lib/mysql-keyring/keyring
```

**MongoDB**:
```javascript
// Enable encryption at rest
mongod --enableEncryption \
    --encryptionKeyFile /path/to/keyfile

// Client-side field level encryption
const clientEncryption = new ClientEncryption(keyVault, kmsProviders);

// Encrypt field
const encryptedField = await clientEncryption.encrypt(
    "sensitive-data",
    {
        algorithm: "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
        keyId: dataKey
    }
);
```

#### Field-Level Encryption

**Python (Cryptography library)**:
```python
from cryptography.fernet import Fernet
import os

class FieldEncryption:
    def __init__(self):
        # Load key from environment
        key = os.getenv('FIELD_ENCRYPTION_KEY').encode()
        self.cipher = Fernet(key)

    def encrypt(self, plaintext: str) -> bytes:
        """Encrypt sensitive field"""
        return self.cipher.encrypt(plaintext.encode())

    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypt sensitive field"""
        return self.cipher.decrypt(ciphertext).decode()

# Usage in application
encryption = FieldEncryption()

# Encrypt before storing
encrypted_ssn = encryption.encrypt("123-45-6789")
db.execute("INSERT INTO users (ssn) VALUES (?)", (encrypted_ssn,))

# Decrypt after retrieving
row = db.execute("SELECT ssn FROM users WHERE id = ?", (user_id,)).fetchone()
decrypted_ssn = encryption.decrypt(row['ssn'])
```

**Node.js (crypto module)**:
```javascript
const crypto = require('crypto');

class FieldEncryption {
    constructor() {
        this.key = Buffer.from(process.env.FIELD_ENCRYPTION_KEY, 'hex');
        this.algorithm = 'aes-256-gcm';
    }

    encrypt(plaintext) {
        const iv = crypto.randomBytes(16);
        const cipher = crypto.createCipheriv(this.algorithm, this.key, iv);

        let encrypted = cipher.update(plaintext, 'utf8', 'hex');
        encrypted += cipher.final('hex');

        const authTag = cipher.getAuthTag();

        return {
            iv: iv.toString('hex'),
            encrypted: encrypted,
            authTag: authTag.toString('hex')
        };
    }

    decrypt(encryptedData) {
        const decipher = crypto.createDecipheriv(
            this.algorithm,
            this.key,
            Buffer.from(encryptedData.iv, 'hex')
        );

        decipher.setAuthTag(Buffer.from(encryptedData.authTag, 'hex'));

        let decrypted = decipher.update(encryptedData.encrypted, 'hex', 'utf8');
        decrypted += decipher.final('utf8');

        return decrypted;
    }
}
```

For detailed database encryption patterns, see [Database Encryption](references/database-encryption.md).

### 3. Application-Level Encryption

Implement envelope encryption for application data.

**Envelope Encryption Pattern**:
```python
import boto3
import os
from cryptography.fernet import Fernet

class EnvelopeEncryption:
    def __init__(self):
        self.kms_client = boto3.client('kms')
        self.master_key_id = os.getenv('KMS_MASTER_KEY_ID')

    def encrypt_data(self, plaintext: bytes) -> dict:
        """
        Encrypt data using envelope encryption:
        1. Generate data encryption key (DEK)
        2. Encrypt data with DEK
        3. Encrypt DEK with KMS master key
        4. Return encrypted data and encrypted DEK
        """
        # Generate DEK
        response = self.kms_client.generate_data_key(
            KeyId=self.master_key_id,
            KeySpec='AES_256'
        )

        plaintext_dek = response['Plaintext']
        encrypted_dek = response['CiphertextBlob']

        # Encrypt data with DEK
        cipher = Fernet(plaintext_dek)
        encrypted_data = cipher.encrypt(plaintext)

        return {
            'encrypted_data': encrypted_data,
            'encrypted_dek': encrypted_dek
        }

    def decrypt_data(self, encrypted_data: bytes, encrypted_dek: bytes) -> bytes:
        """
        Decrypt data using envelope encryption:
        1. Decrypt DEK with KMS
        2. Decrypt data with DEK
        """
        # Decrypt DEK
        response = self.kms_client.decrypt(
            CiphertextBlob=encrypted_dek
        )
        plaintext_dek = response['Plaintext']

        # Decrypt data
        cipher = Fernet(plaintext_dek)
        plaintext = cipher.decrypt(encrypted_data)

        return plaintext
```

### 4. Key Management

Implement secure key generation, storage, rotation, and revocation.

#### Key Management Service (KMS) Integration

**AWS KMS**:
```python
import boto3

kms = boto3.client('kms')

# Create master key
response = kms.create_key(
    Description='Master encryption key',
    KeyUsage='ENCRYPT_DECRYPT',
    Origin='AWS_KMS',
    MultiRegion=False
)
key_id = response['KeyMetadata']['KeyId']

# Encrypt data
response = kms.encrypt(
    KeyId=key_id,
    Plaintext=b'sensitive data'
)
ciphertext = response['CiphertextBlob']

# Decrypt data
response = kms.decrypt(
    CiphertextBlob=ciphertext
)
plaintext = response['Plaintext']

# Enable automatic key rotation
kms.enable_key_rotation(KeyId=key_id)
```

**Azure Key Vault**:
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

credential = DefaultAzureCredential()
key_client = KeyClient(vault_url="https://myvault.vault.azure.net/", credential=credential)

# Create key
key = key_client.create_rsa_key("encryption-key", size=4096)

# Get crypto client
crypto_client = CryptographyClient(key, credential=credential)

# Encrypt
result = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, b"sensitive data")
ciphertext = result.ciphertext

# Decrypt
result = crypto_client.decrypt(EncryptionAlgorithm.rsa_oaep, ciphertext)
plaintext = result.plaintext
```

**Google Cloud KMS**:
```python
from google.cloud import kms

client = kms.KeyManagementServiceClient()

# Create key ring and key
key_ring_path = client.key_ring_path('project-id', 'us-east1', 'my-key-ring')
key_path = client.crypto_key_path('project-id', 'us-east1', 'my-key-ring', 'my-key')

# Encrypt
response = client.encrypt(
    request={'name': key_path, 'plaintext': b'sensitive data'}
)
ciphertext = response.ciphertext

# Decrypt
response = client.decrypt(
    request={'name': key_path, 'ciphertext': ciphertext}
)
plaintext = response.plaintext
```

For detailed key management practices, see [Key Management Guide](references/key-management.md).

### 5. Backup and Log Encryption

Ensure backups and logs are encrypted.

**Database Backup Encryption**:
```bash
# PostgreSQL encrypted backup
pg_dump dbname | gpg --encrypt --recipient admin@example.com > backup.sql.gpg

# Restore
gpg --decrypt backup.sql.gpg | psql dbname

# MySQL encrypted backup
mysqldump --all-databases | openssl enc -aes-256-cbc -salt -out backup.sql.enc

# Restore
openssl enc -aes-256-cbc -d -in backup.sql.enc | mysql
```

**Log Encryption**:
```python
import logging
from cryptography.fernet import Fernet

class EncryptedFileHandler(logging.FileHandler):
    def __init__(self, filename, key):
        super().__init__(filename)
        self.cipher = Fernet(key)

    def emit(self, record):
        msg = self.format(record)
        encrypted = self.cipher.encrypt(msg.encode())
        with open(self.baseFilename, 'ab') as f:
            f.write(encrypted + b'\n')
```

## Implementation Checklist

- [ ] **TLS/SSL**
  - [ ] TLS 1.2+ only (no TLS 1.0, 1.1, SSLv3)
  - [ ] Strong cipher suites configured
  - [ ] HSTS header enabled (max-age ≥31536000)
  - [ ] Certificates from trusted CA
  - [ ] Automated certificate renewal configured

- [ ] **Database Encryption**
  - [ ] TDE enabled for entire database
  - [ ] Sensitive columns encrypted (PII, PHI, PCI)
  - [ ] Encryption keys stored in KMS
  - [ ] Key rotation implemented

- [ ] **Application Encryption**
  - [ ] AES-256-GCM for symmetric encryption
  - [ ] RSA-4096 or ECDSA P-384 for asymmetric
  - [ ] Envelope encryption for large data
  - [ ] Unique IV/nonce per encryption

- [ ] **Key Management**
  - [ ] Keys stored in KMS/HSM, never in code
  - [ ] Automatic key rotation (90 days)
  - [ ] Key backup and recovery procedures
  - [ ] Key access auditing enabled

- [ ] **Backup Encryption**
  - [ ] All backups encrypted
  - [ ] Separate encryption keys from production
  - [ ] Encrypted backup restoration tested
  - [ ] Backup key rotation implemented

- [ ] **Compliance**
  - [ ] GDPR: Personal data encrypted
  - [ ] HIPAA: PHI encrypted at rest and in transit
  - [ ] PCI-DSS: Cardholder data encrypted
  - [ ] Encryption audit logging enabled

## Security Best Practices

### TLS/SSL
- Use TLS 1.2 or 1.3 only (disable older versions)
- Configure strong cipher suites (ECDHE-RSA-AES256-GCM-SHA384)
- Enable HSTS with long max-age (1 year minimum)
- Use automated certificate management (Let's Encrypt + Certbot)
- Monitor certificate expiration

### Encryption Algorithms
- Symmetric: AES-256-GCM (authenticated encryption)
- Asymmetric: RSA-4096 or ECDSA P-384
- Hashing: SHA-256 or SHA-512
- Never use: DES, 3DES, RC4, MD5, SHA1

### Key Management
- Generate keys with cryptographically secure random (secrets module)
- Store keys in KMS/HSM, never in application code
- Implement automatic key rotation (90-day cycle)
- Separate key management permissions from data access
- Log all key access and usage

### Data Classification
- **Critical** (PII, PHI, PCI): Encrypt at rest and in transit, field-level encryption
- **Confidential**: Encrypt at rest and in transit, database-level encryption
- **Internal**: Encrypt in transit (TLS)
- **Public**: No encryption required (still use TLS for integrity)

## References

For detailed implementation guidance:
- [TLS Best Practices](references/tls-best-practices.md)
- [Database Encryption](references/database-encryption.md)
- [Key Management Guide](references/key-management.md)

## Integration

This skill works with:
- **Backend Developer agent**: For implementing encryption in applications
- **DevOps Engineer agent**: For TLS/SSL configuration and certificate management
- **System Architect agent**: For encryption architecture decisions
- **Compliance Auditing skill**: For validating encryption implementations
