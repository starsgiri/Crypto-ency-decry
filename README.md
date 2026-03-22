# CipherCore — Cryptography & Network Security Suite

A Streamlit web application for symmetric and asymmetric encryption/decryption.
No database, no backend — all crypto runs in memory.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Algorithm Selection Logic

| Method     | Security Level | Algorithm         | Notes                          |
|------------|---------------|-------------------|--------------------------------|
| Symmetric  | Easy          | AES-128-CBC       | PKCS7 padding, PBKDF2 key derive |
| Symmetric  | Medium        | AES-256-GCM       | Authenticated encryption        |
| Symmetric  | Hard          | ChaCha20          | Stream cipher, 256-bit key      |
| Asymmetric | Easy          | RSA-OAEP-SHA256   | 2048-bit RSA                   |
| Asymmetric | Medium        | RSA-OAEP-SHA384   | 2048-bit RSA                   |
| Asymmetric | Hard          | RSA-OAEP-SHA512   | 2048-bit RSA                   |

## Usage Flow

1. **Choose Operation** — Encrypt or Decrypt
2. **Choose Method** — Symmetric (shared key) or Asymmetric (public/private key pair)
3. **Enter Key** — passphrase for symmetric; public key for encryption, private key for decryption
4. **Security Level** *(Encrypt only)* — Easy / Medium / Hard → auto-selects algorithm
5. **Enter Data** — plaintext to encrypt, or ciphertext (Base64) to decrypt
6. **Execute** — results displayed with algorithm info, key fingerprint, and copyable ciphertext

## Key Generation

Use the built-in **Generate RSA-2048 Key Pair** expander under Asymmetric mode to generate test keys.
