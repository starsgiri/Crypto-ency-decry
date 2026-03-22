# CipherCore — Cryptography & Network Security Suite

A Streamlit web application for encrypting and decrypting messages using 10 algorithms.
All operations run in memory — no data is stored anywhere.

## Setup

```bash
pip install streamlit cryptography
streamlit run ciphercore.py
```

---

## Supported Algorithms

| # | Algorithm          | Key Size | Mode          | KDF                        | Authenticated |
|---|--------------------|----------|---------------|----------------------------|---------------|
| 1 | AES-128-CBC        | 128-bit  | CBC           | PBKDF2-SHA256 (200k)       | No            |
| 2 | AES-192-CBC        | 192-bit  | CBC           | PBKDF2-SHA256 (200k)       | No            |
| 3 | AES-256-CBC        | 256-bit  | CBC           | PBKDF2-SHA256 (200k)       | No            |
| 4 | AES-128-GCM        | 128-bit  | GCM           | PBKDF2-SHA256 (200k)       | Yes           |
| 5 | AES-256-GCM        | 256-bit  | GCM           | PBKDF2-SHA256 (200k)       | Yes           |
| 6 | AES-256-GCM-Scrypt | 256-bit  | GCM           | Scrypt (N=16384, r=8, p=1) | Yes           |
| 7 | AES-256-CTR        | 256-bit  | CTR           | PBKDF2-SHA256 (200k)       | No            |
| 8 | ChaCha20           | 256-bit  | Stream        | PBKDF2-SHA256 (200k)       | No            |
| 9 | ChaCha20-Scrypt    | 256-bit  | Stream        | Scrypt (N=16384, r=8, p=1) | No            |
|10 | 3DES-CBC           | 168-bit  | CBC (legacy)  | PBKDF2-SHA256 (200k)       | No            |

---

## How to Encrypt

1. Select **Encrypt** mode
2. Choose an algorithm from the dropdown
3. Enter a passphrase — a live strength indicator shows Weak / Moderate / Strong
4. Type or paste your message
5. Click **ENCRYPT MESSAGE**

The app displays a summary with the algorithm details, key derivation info, encryption pipeline, and a step-by-step explanation. The encrypted token (Base64) is shown in a copyable text area at the bottom.

---

## How to Decrypt

1. Select **Decrypt** mode
2. Paste the encrypted token
3. Enter the passphrase used during encryption
4. Click **DECRYPT MESSAGE**

The algorithm is **automatically detected** from the token — no manual selection needed. The summary shows the detected algorithm, decryption pipeline, and the recovered plaintext.

---

## Token Format

Each encrypted token is a Base64-encoded JSON object containing everything needed for decryption except the passphrase.

```json
// CBC / CTR / ChaCha20
{ "algo": "AES-256-CBC", "salt": "...", "iv": "...", "ct": "..." }

// GCM (includes auth tag)
{ "algo": "AES-256-GCM", "salt": "...", "nonce": "...", "ct": "...", "tag": "..." }
```

---

## Security Notes

- Share the **encrypted token** freely — it is safe to send over any channel
- Share the **passphrase** only via a separate secure channel (call, Signal, in-person)
- Never send the passphrase and token together in the same message
- GCM variants include an authentication tag — a wrong passphrase or tampered token will fail immediately
- Scrypt variants (AES-256-GCM-Scrypt, ChaCha20-Scrypt) use a memory-hard KDF that is more resistant to brute-force attacks