import streamlit as st
import base64, os, json, time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding, hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CipherCore | Crypto Suite",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

:root {
    --bg:     #07090e;
    --surf:   #0d1117;
    --surf2:  #111820;
    --border: #1c2535;
    --accent: #00e5ff;
    --purple: #7c3aed;
    --green:  #00ffaa;
    --red:    #ff4466;
    --yellow: #fbbf24;
    --text:   #c8d6e5;
    --muted:  #4a6080;
}
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }

@keyframes fadein {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:none; }
}

.hero {
    text-align: center;
    padding: 2.8rem 1rem 2rem;
    background: linear-gradient(160deg, #0d1117 0%, #0a111c 100%);
    border: 1px solid var(--border);
    border-radius: 4px;
    margin-bottom: 2rem;
    box-shadow: 0 0 60px rgba(0,229,255,0.05);
    animation: fadein 1s ease;
}
.hero-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 3rem; color: var(--accent);
    text-shadow: 0 0 40px rgba(0,229,255,0.5);
    letter-spacing: 0.12em; margin: 0;
}
.hero-sub {
    color: var(--muted); font-size: 0.78rem;
    letter-spacing: 0.35em; text-transform: uppercase; margin-top: 0.5rem;
}

.sec-header { display: flex; align-items: center; gap: 0.8rem; margin: 2rem 0 0.8rem; }
.sec-num {
    font-family: 'Share Tech Mono', monospace; font-size: 0.65rem; color: var(--accent);
    background: rgba(0,229,255,0.08); border: 1px solid rgba(0,229,255,0.25);
    padding: 0.15rem 0.55rem; border-radius: 2px;
}
.sec-title { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.3em; text-transform: uppercase; color: var(--muted); }

.icard {
    background: var(--surf2); border: 1px solid var(--border);
    border-left: 3px solid var(--accent); padding: 1rem 1.3rem; border-radius: 2px;
    margin: 0.7rem 0; font-family: 'Share Tech Mono', monospace; font-size: 0.8rem;
    line-height: 1.8; word-break: break-all;
    transition: box-shadow 0.25s, transform 0.2s; animation: fadein 0.7s ease;
}
.icard:hover { box-shadow: 0 4px 24px rgba(0,229,255,0.09); transform: translateY(-1px); }
.icard.green  { border-left-color: var(--green); }
.icard.yellow { border-left-color: var(--yellow); }
.icard.red    { border-left-color: var(--red); }
.icard.purple { border-left-color: var(--purple); }

.lbl { color: var(--muted); font-size: 0.63rem; letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 0.25rem; }
.val   { color: var(--accent); }
.val.g { color: var(--green); }
.val.w { color: #e8f4ff; }
.val.y { color: var(--yellow); }
.val.r { color: var(--red); }

hr.div { border: none; border-top: 1px solid var(--border); margin: 1.6rem 0; opacity: 0.6; }

/* Summary table rows */
.srow {
    display: flex; border: 1px solid var(--border); border-radius: 2px;
    margin-bottom: 0.5rem; overflow: hidden; font-family: 'Share Tech Mono', monospace;
    animation: fadein 0.6s ease;
}
.sk {
    background: rgba(0,0,0,0.45); color: var(--muted);
    font-size: 0.63rem; letter-spacing: 0.18em; text-transform: uppercase;
    padding: 0.7rem 1rem; min-width: 190px; display: flex; align-items: center;
    border-right: 1px solid var(--border);
}
.sv {
    background: rgba(0,229,255,0.025); color: var(--accent);
    font-size: 0.8rem; padding: 0.7rem 1rem; flex: 1;
    display: flex; align-items: center; word-break: break-all;
}
.sv.g  { color: var(--green); }
.sv.w  { color: #e8f4ff; }
.sv.y  { color: var(--yellow); }
.sv.m  { color: var(--muted); font-size: 0.7rem; }
.sv.msg { color: #e8f4ff; font-size: 0.9rem; white-space: pre-wrap; word-break: break-word; line-height: 1.8; }

/* Flow pipeline */
.flow-outer {
    border: 1px solid var(--border); border-radius: 2px; margin-bottom: 0.5rem; overflow: hidden;
}
.flow-hdr {
    background: rgba(0,0,0,0.45); color: var(--muted);
    font-family: 'Share Tech Mono', monospace; font-size: 0.63rem;
    letter-spacing: 0.18em; text-transform: uppercase;
    padding: 0.7rem 1rem; border-bottom: 1px solid var(--border);
}
.flow-body {
    background: rgba(0,229,255,0.025); padding: 0.85rem 1rem;
    display: flex; flex-wrap: wrap; align-items: center; gap: 0.35rem;
}
.fstep {
    background: rgba(0,229,255,0.08); border: 1px solid rgba(0,229,255,0.2);
    color: var(--text); font-family: 'Share Tech Mono', monospace; font-size: 0.68rem;
    padding: 0.28rem 0.65rem; border-radius: 2px;
}
.farrow { color: var(--accent); font-size: 0.9rem; font-family: 'Share Tech Mono', monospace; }

/* How-it-works */
.hiw-outer {
    border: 1px solid var(--border); border-radius: 2px; margin-bottom: 0.5rem; overflow: hidden;
}
.hiw-hdr {
    background: rgba(0,0,0,0.45); color: var(--muted);
    font-family: 'Share Tech Mono', monospace; font-size: 0.63rem;
    letter-spacing: 0.18em; text-transform: uppercase;
    padding: 0.7rem 1rem; border-bottom: 1px solid var(--border);
}
.hiw-body { background: rgba(0,229,255,0.025); padding: 0.9rem 1.1rem; }
.hiw-step { display: flex; gap: 0.75rem; margin-bottom: 0.55rem; font-family: 'Share Tech Mono', monospace; font-size: 0.71rem; line-height: 1.7; }
.hiw-n { color: var(--accent); min-width: 18px; font-weight: 700; }
.hiw-t { color: var(--muted); }
.hiw-t strong { color: var(--text); }

/* Security note */
.sec-note {
    border: 1px solid rgba(251,191,36,0.3); border-left: 3px solid var(--yellow);
    background: rgba(251,191,36,0.03); border-radius: 2px; padding: 0.85rem 1.1rem;
    margin-bottom: 0.5rem; font-family: 'Share Tech Mono', monospace; font-size: 0.7rem;
    color: var(--muted); line-height: 1.9;
}
.sec-note strong { color: var(--yellow); }

/* success banner */
.sum-title {
    font-family: 'Share Tech Mono', monospace; font-size: 1.05rem;
    letter-spacing: 0.15em; text-align: center; margin-bottom: 1.2rem;
    padding-bottom: 0.9rem; border-bottom: 1px solid var(--border);
}
.sum-title.enc { color: var(--green); text-shadow: 0 0 18px rgba(0,255,170,0.3); }
.sum-title.dec { color: var(--accent); text-shadow: 0 0 18px rgba(0,229,255,0.3); }

/* inputs */
.stSelectbox label,.stRadio label,.stTextArea label,.stTextInput label {
    color: var(--muted) !important; font-family:'Share Tech Mono',monospace !important;
    font-size:0.72rem !important; letter-spacing:0.15em !important; text-transform:uppercase !important;
}
div[data-baseweb="select"] > div {
    background: var(--surf2) !important; border-color: var(--border) !important;
    border-radius: 2px !important; color: var(--text) !important;
}
textarea, input[type="text"], input[type="password"] {
    background: var(--surf2) !important; border: 1px solid var(--border) !important;
    border-radius: 2px !important; color: var(--text) !important;
    font-family: 'Share Tech Mono', monospace !important; font-size: 0.8rem !important;
}
/* buttons */
.stButton > button {
    background: linear-gradient(90deg,rgba(0,229,255,.07),rgba(124,58,237,.07)) !important;
    border: 1px solid var(--accent) !important; color: var(--accent) !important;
    font-family:'Share Tech Mono',monospace !important; letter-spacing:0.18em !important;
    text-transform:uppercase !important; border-radius:2px !important; padding:0.5rem 2rem !important;
    width:100%; font-size:1rem !important; transition:all 0.2s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(90deg,rgba(0,229,255,.18),rgba(124,58,237,.18)) !important;
    box-shadow: 0 0 18px rgba(0,229,255,.2) !important;
    color:#fff !important; border-color:var(--purple) !important; transform:scale(1.02);
}
.strength { font-family:'Share Tech Mono',monospace; font-size:0.68rem; letter-spacing:0.15em; margin:-0.3rem 0 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ─── Helpers ─────────────────────────────────────────────────────────────────
def b64e(b: bytes) -> str: return base64.b64encode(b).decode()
def b64d(s: str) -> bytes: return base64.b64decode(s.encode())

def derive_key(password: str, salt: bytes, length: int, method: str = "pbkdf2") -> bytes:
    if method == "scrypt":
        kdf = Scrypt(salt=salt, length=length, n=2**14, r=8, p=1, backend=default_backend())
        return kdf.derive(password.encode())
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=length, salt=salt,
                     iterations=200_000, backend=default_backend())
    return kdf.derive(password.encode())

# ─── Algorithm Registry ───────────────────────────────────────────────────────
ALGORITHMS = {
    "AES-128-CBC": {
        "desc": "AES 128-bit - CBC Mode",
        "detail": "Block cipher, 128-bit key, PKCS7 padding, CBC chaining",
        "key_len": 16, "kdf": "pbkdf2", "mode_type": "cbc",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k)", "128-bit Key + 16B IV", "PKCS7 Pad", "AES-CBC Encrypt", "JSON Bundle", "Base64 Out"],
        "enc_steps": [
            ("Random Salt",     "16 random bytes — ensures unique keys every run even with same passphrase"),
            ("PBKDF2-SHA256",   "200,000 iterations stretch passphrase into a 128-bit cryptographic key"),
            ("Random IV",       "16-byte Initialisation Vector randomises CBC block chaining per message"),
            ("PKCS7 Padding",   "Plaintext padded to 16-byte block boundary required by AES block cipher"),
            ("AES-CBC Encrypt", "Each plaintext block XOR'd with prior cipherblock, then AES-encrypted"),
            ("Bundle + Encode", "algo tag + salt + IV + ciphertext packed as JSON, then Base64-encoded"),
        ],
    },
    "AES-256-CBC": {
        "desc": "AES 256-bit - CBC Mode",
        "detail": "Block cipher, 256-bit key, PKCS7 padding, CBC chaining",
        "key_len": 32, "kdf": "pbkdf2", "mode_type": "cbc",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k)", "256-bit Key + 16B IV", "PKCS7 Pad", "AES-CBC Encrypt", "JSON Bundle", "Base64 Out"],
        "enc_steps": [
            ("Random Salt",     "16 random bytes generated for key uniqueness"),
            ("PBKDF2-SHA256",   "200k iterations -> 256-bit key (strongest AES key size)"),
            ("Random IV",       "16-byte IV for CBC block chaining"),
            ("PKCS7 Padding",   "Pad to 16-byte block boundary"),
            ("AES-CBC Encrypt", "CBC mode with 256-bit AES key"),
            ("Bundle + Encode", "Packed JSON -> Base64 output token"),
        ],
    },
    "AES-192-CBC": {
        "desc": "AES 192-bit - CBC Mode",
        "detail": "Block cipher, 192-bit key, PKCS7 padding, CBC chaining",
        "key_len": 24, "kdf": "pbkdf2", "mode_type": "cbc",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k)", "192-bit Key + 16B IV", "PKCS7 Pad", "AES-CBC Encrypt", "JSON Bundle", "Base64 Out"],
        "enc_steps": [
            ("Random Salt",     "16 random bytes generated"),
            ("PBKDF2-SHA256",   "200k iterations -> 192-bit key"),
            ("Random IV",       "16-byte IV for CBC"),
            ("PKCS7 Padding",   "Pad to 16-byte block boundary"),
            ("AES-CBC Encrypt", "CBC mode with 192-bit AES key"),
            ("Bundle + Encode", "Packed JSON -> Base64"),
        ],
    },
    "AES-128-GCM": {
        "desc": "AES 128-bit - GCM Mode (AEAD)",
        "detail": "Authenticated encryption, 128-bit key, 12B nonce, 16B auth tag",
        "key_len": 16, "kdf": "pbkdf2", "mode_type": "gcm",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k)", "128-bit Key + 12B Nonce", "AES-GCM Encrypt", "Auth Tag (16B)", "JSON Bundle", "Base64 Out"],
        "enc_steps": [
            ("Random Salt",    "16 random bytes for key uniqueness"),
            ("PBKDF2-SHA256",  "200k iterations -> 128-bit key"),
            ("Random Nonce",   "12-byte nonce — unique per message, critical for GCM security"),
            ("AES-GCM Encrypt","Authenticated encryption: produces ciphertext + 16-byte auth tag"),
            ("Auth Tag",       "16B tag cryptographically binds key+nonce+plaintext; tampering detected"),
            ("Bundle + Encode","algo + salt + nonce + ct + tag -> JSON -> Base64"),
        ],
    },
    "AES-256-GCM": {
        "desc": "AES 256-bit - GCM Mode (AEAD)",
        "detail": "Authenticated encryption, 256-bit key, 12B nonce, 16B auth tag",
        "key_len": 32, "kdf": "pbkdf2", "mode_type": "gcm",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k)", "256-bit Key + 12B Nonce", "AES-GCM Encrypt", "Auth Tag (16B)", "JSON Bundle", "Base64 Out"],
        "enc_steps": [
            ("Random Salt",    "16 random bytes for key uniqueness"),
            ("PBKDF2-SHA256",  "200k iterations -> 256-bit key (maximum AES strength)"),
            ("Random Nonce",   "12-byte nonce for GCM — reuse would be catastrophic"),
            ("AES-GCM Encrypt","AEAD: ciphertext + 16B auth tag in one pass"),
            ("Auth Tag",       "Tag verifies integrity; wrong key = decryption failure"),
            ("Bundle + Encode","Packed JSON -> Base64"),
        ],
    },
    "AES-256-GCM-Scrypt": {
        "desc": "AES-256-GCM + Scrypt KDF",
        "detail": "Authenticated AES-256-GCM with memory-hard Scrypt key derivation",
        "key_len": 32, "kdf": "scrypt", "mode_type": "gcm",
        "flow": ["Passphrase", "Scrypt (N=16384 r=8 p=1)", "256-bit Key + 12B Nonce", "AES-GCM Encrypt", "Auth Tag (16B)", "JSON Bundle", "Base64 Out"],
        "enc_steps": [
            ("Random Salt",    "16 random bytes"),
            ("Scrypt KDF",     "Memory-hard KDF: N=16384, r=8, p=1 — GPU/ASIC brute-force resistant"),
            ("Random Nonce",   "12-byte nonce for GCM"),
            ("AES-GCM Encrypt","AEAD: ciphertext + 16B auth tag"),
            ("Auth Tag",       "Integrity verification tag"),
            ("Bundle + Encode","Packed JSON -> Base64"),
        ],
    },
    "AES-256-CTR": {
        "desc": "AES 256-bit - CTR Mode",
        "detail": "Counter mode, 256-bit key — turns AES into a stream cipher",
        "key_len": 32, "kdf": "pbkdf2", "mode_type": "ctr",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k)", "256-bit Key + 16B Nonce", "AES-CTR Stream Encrypt", "JSON Bundle", "Base64 Out"],
        "enc_steps": [
            ("Random Salt",       "16 random bytes"),
            ("PBKDF2-SHA256",     "200k iterations -> 256-bit key"),
            ("Random Nonce",      "16-byte counter nonce"),
            ("AES-CTR Encrypt",   "Counter incremented per block, each encrypted, XOR'd with plaintext — no padding needed"),
            ("Bundle + Encode",   "Packed JSON -> Base64"),
        ],
    },
    "ChaCha20": {
        "desc": "ChaCha20 Stream Cipher",
        "detail": "Stream cipher, 256-bit key, 16B nonce — no padding, constant-time",
        "key_len": 32, "kdf": "pbkdf2", "mode_type": "chacha",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k)", "256-bit Key + 16B Nonce", "ChaCha20 Encrypt", "JSON Bundle", "Base64 Out"],
        "enc_steps": [
            ("Random Salt",    "16 random bytes"),
            ("PBKDF2-SHA256",  "200k iterations -> 256-bit key"),
            ("Random Nonce",   "16-byte nonce for ChaCha20"),
            ("ChaCha20",       "20-round quarter-round ARX operations produce pseudorandom keystream XOR'd with plaintext"),
            ("Bundle + Encode","Packed JSON -> Base64"),
        ],
    },
    "ChaCha20-Scrypt": {
        "desc": "ChaCha20 + Scrypt KDF",
        "detail": "ChaCha20 stream cipher with memory-hard Scrypt key derivation",
        "key_len": 32, "kdf": "scrypt", "mode_type": "chacha",
        "flow": ["Passphrase", "Scrypt (N=16384 r=8 p=1)", "256-bit Key + 16B Nonce", "ChaCha20 Encrypt", "JSON Bundle", "Base64 Out"],
        "enc_steps": [
            ("Random Salt",    "16 random bytes"),
            ("Scrypt KDF",     "Memory-hard KDF — very resistant to offline brute-force attacks"),
            ("Random Nonce",   "16-byte nonce"),
            ("ChaCha20",       "ARX stream cipher — no padding, constant-time execution"),
            ("Bundle + Encode","Packed JSON -> Base64"),
        ],
    },
    "3DES-CBC": {
        "desc": "Triple DES - CBC Mode (Legacy)",
        "detail": "Legacy 3DES, 24-byte key (168-bit effective), CBC mode, PKCS7",
        "key_len": 24, "kdf": "pbkdf2", "mode_type": "3des",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k)", "168-bit Key + 8B IV", "PKCS7 Pad", "3DES-CBC Encrypt", "JSON Bundle", "Base64 Out"],
        "enc_steps": [
            ("Random Salt",    "16 random bytes"),
            ("PBKDF2-SHA256",  "200k iterations -> 24-byte (168-bit effective) key"),
            ("Random IV",      "8-byte IV for DES block chaining"),
            ("PKCS7 Padding",  "Pad to 8-byte DES block boundary"),
            ("3DES-CBC",       "Encrypt-Decrypt-Encrypt with 3 DES keys (legacy compatibility mode)"),
            ("Bundle + Encode","Packed JSON -> Base64"),
        ],
    },
}

# ─── Crypto Core ──────────────────────────────────────────────────────────────
def do_encrypt(plaintext: str, passphrase: str, algo: str) -> str:
    cfg  = ALGORITHMS[algo]
    data = plaintext.encode()
    salt = os.urandom(16)
    key  = derive_key(passphrase, salt, cfg["key_len"], cfg["kdf"])
    mt   = cfg["mode_type"]

    if mt == "cbc":
        iv     = os.urandom(16)
        padder = sym_padding.PKCS7(128).padder()
        padded = padder.update(data) + padder.finalize()
        enc    = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).encryptor()
        ct     = enc.update(padded) + enc.finalize()
        payload = {"algo": algo, "salt": b64e(salt), "iv": b64e(iv), "ct": b64e(ct)}

    elif mt == "gcm":
        nonce = os.urandom(12)
        enc   = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend()).encryptor()
        ct    = enc.update(data) + enc.finalize()
        payload = {"algo": algo, "salt": b64e(salt), "nonce": b64e(nonce),
                   "ct": b64e(ct), "tag": b64e(enc.tag)}

    elif mt == "ctr":
        nonce = os.urandom(16)
        enc   = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend()).encryptor()
        ct    = enc.update(data) + enc.finalize()
        payload = {"algo": algo, "salt": b64e(salt), "nonce": b64e(nonce), "ct": b64e(ct)}

    elif mt == "chacha":
        nonce = os.urandom(16)
        enc   = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend()).encryptor()
        ct    = enc.update(data) + enc.finalize()
        payload = {"algo": algo, "salt": b64e(salt), "nonce": b64e(nonce), "ct": b64e(ct)}

    elif mt == "3des":
        iv     = os.urandom(8)
        padder = sym_padding.PKCS7(64).padder()
        padded = padder.update(data) + padder.finalize()
        enc    = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend()).encryptor()
        ct     = enc.update(padded) + enc.finalize()
        payload = {"algo": algo, "salt": b64e(salt), "iv": b64e(iv), "ct": b64e(ct)}

    else:
        raise ValueError(f"Unknown mode: {mt}")

    return b64e(json.dumps(payload).encode())


def do_decrypt(ciphertext_b64: str, passphrase: str):
    try:
        payload = json.loads(b64d(ciphertext_b64).decode())
    except Exception:
        raise ValueError("Invalid token — cannot parse encrypted payload.")

    algo = payload.get("algo")
    if not algo or algo not in ALGORITHMS:
        raise ValueError(f"Unrecognised algorithm in token: '{algo}'")

    cfg  = ALGORITHMS[algo]
    salt = b64d(payload["salt"])
    key  = derive_key(passphrase, salt, cfg["key_len"], cfg["kdf"])
    mt   = cfg["mode_type"]

    if mt == "cbc":
        iv     = b64d(payload["iv"])
        ct     = b64d(payload["ct"])
        dec    = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).decryptor()
        padded = dec.update(ct) + dec.finalize()
        unpad  = sym_padding.PKCS7(128).unpadder()
        pt     = unpad.update(padded) + unpad.finalize()

    elif mt == "gcm":
        nonce = b64d(payload["nonce"])
        ct    = b64d(payload["ct"])
        tag   = b64d(payload["tag"])
        dec   = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend()).decryptor()
        pt    = dec.update(ct) + dec.finalize()

    elif mt == "ctr":
        nonce = b64d(payload["nonce"])
        ct    = b64d(payload["ct"])
        dec   = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend()).decryptor()
        pt    = dec.update(ct) + dec.finalize()

    elif mt == "chacha":
        nonce = b64d(payload["nonce"])
        ct    = b64d(payload["ct"])
        dec   = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend()).decryptor()
        pt    = dec.update(ct) + dec.finalize()

    elif mt == "3des":
        iv     = b64d(payload["iv"])
        ct     = b64d(payload["ct"])
        dec    = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend()).decryptor()
        padded = dec.update(ct) + dec.finalize()
        unpad  = sym_padding.PKCS7(64).unpadder()
        pt     = unpad.update(padded) + unpad.finalize()

    else:
        raise ValueError(f"Unsupported mode: {mt}")

    return pt.decode(), algo


# ─── Summary Renderers (pure HTML strings, no f-string variable injection issues) ──

def _srow(label: str, value: str, vcls: str = "") -> str:
    """Build one summary row HTML string."""
    return (
        f'<div class="srow">'
        f'<div class="sk">{label}</div>'
        f'<div class="sv {vcls}">{value}</div>'
        f'</div>'
    )

def render_summary_rows(rows: list):
    """rows = list of (label, value, vcls) tuples. Rendered as one block."""
    html = "".join(_srow(lbl, val, cls) for lbl, val, cls in rows)
    st.markdown(html, unsafe_allow_html=True)


def render_flow(steps: list, title: str = "Encryption Pipeline"):
    parts = []
    for i, s in enumerate(steps):
        parts.append(f'<span class="fstep">{s}</span>')
        if i < len(steps) - 1:
            parts.append('<span class="farrow">&#8594;</span>')
    inner = " ".join(parts)
    st.markdown(
        f'<div class="flow-outer">'
        f'<div class="flow-hdr">{title}</div>'
        f'<div class="flow-body">{inner}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def render_how_it_works(steps: list, mode: str = "encrypt"):
    hdr = "How Encryption Works — Step by Step" if mode == "encrypt" else "How Decryption Works — Step by Step"
    rows_html = ""
    for i, (title, detail) in enumerate(steps, 1):
        rows_html += (
            f'<div class="hiw-step">'
            f'<div class="hiw-n">{i}.</div>'
            f'<div class="hiw-t"><strong>{title}:</strong> {detail}</div>'
            f'</div>'
        )
    st.markdown(
        f'<div class="hiw-outer">'
        f'<div class="hiw-hdr">{hdr}</div>'
        f'<div class="hiw-body">{rows_html}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def render_note():
    st.markdown("""
    <div class="sec-note">
      <strong>SECURITY NOTE</strong><br>
      Share the <strong>Encrypted Token</strong> freely — it is safe to transmit on any channel.<br>
      Share the <strong>Passphrase</strong> only via a separate secure channel (phone, Signal, in-person).<br>
      Never send passphrase and ciphertext together in the same message.
    </div>
    """, unsafe_allow_html=True)


# ─── UI ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">&#x1F510; CIPHERCORE</div>
  <div class="hero-sub">10-Algorithm Cryptography Suite &nbsp;&#183;&nbsp; Auto-Detection Decrypt &nbsp;&#183;&nbsp; Zero Storage</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sec-header"><span class="sec-num">01</span><span class="sec-title">Operation Mode</span></div>', unsafe_allow_html=True)
mode_raw = st.radio("", ["🔒  Encrypt", "🔓  Decrypt"], horizontal=True, label_visibility="collapsed")
mode = "Encrypt" if "Encrypt" in mode_raw else "Decrypt"
st.markdown('<hr class="div">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  ENCRYPT FLOW
# ══════════════════════════════════════════════════════════════════════════════
if mode == "Encrypt":

    st.markdown('<div class="sec-header"><span class="sec-num">02</span><span class="sec-title">Choose Encryption Algorithm</span></div>', unsafe_allow_html=True)
    algo_names = list(ALGORITHMS.keys())
    if "chosen_algo" not in st.session_state:
        st.session_state["chosen_algo"] = "AES-256-GCM"

    chosen_algo = st.selectbox(
        "Algorithm",
        algo_names,
        index=algo_names.index(st.session_state["chosen_algo"]),
        format_func=lambda x: f"{x}  —  {ALGORITHMS[x]['desc']}",
        label_visibility="collapsed"
    )
    st.session_state["chosen_algo"] = chosen_algo
    cfg = ALGORITHMS[chosen_algo]

    kdf_label = "Scrypt (memory-hard)" if cfg["kdf"] == "scrypt" else "PBKDF2-SHA256 (200k iterations)"
    st.markdown(
        f'<div class="icard">'
        f'<div class="lbl">Selected Algorithm</div>'
        f'<div class="val">{chosen_algo}</div>'
        f'<div style="color:var(--muted);font-size:0.72rem;margin-top:0.25rem">{cfg["detail"]}</div>'
        f'<div style="color:var(--muted);font-size:0.68rem;margin-top:0.15rem">KDF: {kdf_label} &nbsp;&#183;&nbsp; Key: {cfg["key_len"]*8}-bit</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown('<hr class="div">', unsafe_allow_html=True)
    st.markdown('<div class="sec-header"><span class="sec-num">03</span><span class="sec-title">Secret Passphrase</span></div>', unsafe_allow_html=True)
    passphrase = st.text_input("Enter a strong passphrase", type="password",
                               placeholder="Minimum 12 characters recommended…")
    if passphrase:
        score = sum([
            len(passphrase) >= 8, len(passphrase) >= 14,
            any(c.isupper() for c in passphrase),
            any(c.isdigit() for c in passphrase),
            any(c in "!@#$%^&*()_+-=" for c in passphrase)
        ])
        sl, sc = ("Weak", "color:var(--red)") if score < 3 else \
                 ("Moderate", "color:var(--yellow)") if score < 4 else \
                 ("Strong", "color:var(--green)")
        st.markdown(f'<div class="strength" style="{sc}">PASSPHRASE STRENGTH: {sl}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="div">', unsafe_allow_html=True)
    st.markdown('<div class="sec-header"><span class="sec-num">04</span><span class="sec-title">Plaintext Message</span></div>', unsafe_allow_html=True)
    plaintext = st.text_area("Message to encrypt", height=150,
                             placeholder="Type or paste the message you want to encrypt…")
    st.markdown('<hr class="div">', unsafe_allow_html=True)

    if st.button("⚡  ENCRYPT MESSAGE"):
        if not plaintext.strip():
            st.markdown('<div class="icard red"><div class="lbl">Error</div><div class="val r">No message provided.</div></div>', unsafe_allow_html=True)
        elif not passphrase:
            st.markdown('<div class="icard red"><div class="lbl">Error</div><div class="val r">Passphrase is required.</div></div>', unsafe_allow_html=True)
        else:
            try:
                with st.spinner("Encrypting…"):
                    time.sleep(0.4)
                    ct_b64 = do_encrypt(plaintext, passphrase, chosen_algo)
                st.balloons()

                # ── ENCRYPTION SUMMARY ──────────────────────────────
                st.markdown('<div class="sum-title enc">&#x2705; ENCRYPTION SUCCESSFUL — SUMMARY</div>', unsafe_allow_html=True)

                integrity = "Yes — Authentication Tag included (AEAD)" if cfg["mode_type"] == "gcm" \
                            else "No — use GCM/Scrypt variant for AEAD"
                integrity_cls = "g" if cfg["mode_type"] == "gcm" else "y"

                kdf_full = "Scrypt  (N=16384, r=8, p=1) — memory-hard" \
                           if cfg["kdf"] == "scrypt" \
                           else "PBKDF2-SHA256 — 200,000 iterations"

                render_summary_rows([
                    ("Algorithm Used",    chosen_algo,                                  "g"),
                    ("Algorithm Detail",  cfg["detail"],                                "m"),
                    ("Key Derivation",    kdf_full,                                     ""),
                    ("Effective Key Size", f"{cfg['key_len']*8} bits ({cfg['key_len']} bytes)", ""),
                    ("Mode of Operation", cfg["mode_type"].upper(),                     ""),
                    ("Integrity / AEAD",  integrity,                                    integrity_cls),
                    ("Plaintext Length",  f"{len(plaintext)} characters",               "w"),
                    ("Ciphertext Length", f"{len(ct_b64)} characters (Base64-encoded)", "w"),
                ])

                render_flow(cfg["flow"], title="Encryption Pipeline")
                render_how_it_works(cfg["enc_steps"], mode="encrypt")
                render_note()

                st.markdown('<div class="sec-header"><span class="sec-num">&#8595;</span><span class="sec-title">Encrypted Token — Copy and Share With Recipient</span></div>', unsafe_allow_html=True)
                st.text_area("Encrypted Token (Base64)", value=ct_b64, height=160,
                             help="The algorithm is embedded in this token. Recipient only needs this token + the passphrase.")
                st.toast("Encryption complete!", icon="✅")

            except Exception as e:
                st.markdown(f'<div class="icard red"><div class="lbl">Encryption Error</div><div class="val r">{str(e)}</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  DECRYPT FLOW
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("""
    <div class="icard purple">
      <div class="lbl">Auto-Detection Active</div>
      <div class="val">Algorithm is automatically read from the encrypted token — no manual selection needed.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-header"><span class="sec-num">02</span><span class="sec-title">Paste Encrypted Token</span></div>', unsafe_allow_html=True)
    ct_input = st.text_area("Encrypted Token (Base64)", height=160,
                            placeholder="Paste the Base64 encrypted token received from the sender…")

    st.markdown('<hr class="div">', unsafe_allow_html=True)
    st.markdown('<div class="sec-header"><span class="sec-num">03</span><span class="sec-title">Passphrase</span></div>', unsafe_allow_html=True)
    dec_pass = st.text_input("Enter the passphrase shared by the sender", type="password",
                             placeholder="Enter the shared passphrase…")
    st.markdown('<hr class="div">', unsafe_allow_html=True)

    if st.button("⚡  DECRYPT MESSAGE"):
        if not ct_input.strip():
            st.markdown('<div class="icard red"><div class="lbl">Error</div><div class="val r">No encrypted token provided.</div></div>', unsafe_allow_html=True)
        elif not dec_pass:
            st.markdown('<div class="icard red"><div class="lbl">Error</div><div class="val r">Passphrase is required.</div></div>', unsafe_allow_html=True)
        else:
            try:
                with st.spinner("Decrypting…"):
                    time.sleep(0.4)
                    plaintext_out, algo_det = do_decrypt(ct_input.strip(), dec_pass)
                st.snow()

                cfg_d = ALGORITHMS[algo_det]
                kdf_full = "Scrypt (N=16384, r=8, p=1) — memory-hard" \
                           if cfg_d["kdf"] == "scrypt" \
                           else "PBKDF2-SHA256 — 200,000 iterations"
                integrity = "Yes — Auth Tag verified (AEAD)" if cfg_d["mode_type"] == "gcm" else "N/A — non-authenticated mode"
                integrity_cls = "g" if cfg_d["mode_type"] == "gcm" else "y"

                # ── DECRYPTION SUMMARY ──────────────────────────────
                st.markdown('<div class="sum-title dec">&#x1F513; DECRYPTION SUCCESSFUL — SUMMARY</div>', unsafe_allow_html=True)

                render_summary_rows([
                    ("Algorithm Detected",  algo_det,                                           "g"),
                    ("Algorithm Detail",    cfg_d["detail"],                                    "m"),
                    ("Key Derivation",      kdf_full,                                           ""),
                    ("Effective Key Size",  f"{cfg_d['key_len']*8} bits ({cfg_d['key_len']} bytes)", ""),
                    ("Mode of Operation",   cfg_d["mode_type"].upper(),                         ""),
                    ("Integrity Verified",  integrity,                                          integrity_cls),
                ])

                # Decrypted message row — separate call to use msg style
                st.markdown(
                    f'<div class="srow">'
                    f'<div class="sk">Decrypted Message</div>'
                    f'<div class="sv msg">{plaintext_out}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                dec_steps = [
                    ("Parse Token",       "Base64 decoded, JSON parsed — algo tag, salt, nonce/IV, ciphertext extracted"),
                    ("Detect Algorithm",  f"Tag '{algo_det}' matched from registry — fully automatic, no user input needed"),
                    ("Re-derive Key",     f"{kdf_full} — same salt re-run with provided passphrase produces identical key"),
                    ("Decrypt",           f"{algo_det} decryption using recovered key + stored nonce/IV from token"),
                    ("Verify / Unpad",    "Auth tag verified (GCM) or padding stripped (CBC) — wrong key raises error"),
                    ("Output Plaintext",  "Decrypted bytes decoded to UTF-8 string and displayed"),
                ]

                render_flow(
                    ["Base64 Input", "JSON Parse", "Algo Detection", "Key Re-Derivation", "Decrypt", "Verify/Unpad", "Plaintext Out"],
                    title="Decryption Pipeline"
                )
                render_how_it_works(dec_steps, mode="decrypt")

                st.markdown('<div class="sec-header"><span class="sec-num">&#8595;</span><span class="sec-title">Decrypted Message</span></div>', unsafe_allow_html=True)
                st.text_area("Plaintext Output", value=plaintext_out, height=120)
                st.toast("Decryption complete!", icon="✅")

            except Exception as e:
                err = str(e)
                hint = ""
                if "padding" in err.lower() or "mac" in err.lower() or "tag" in err.lower():
                    hint = " — Incorrect passphrase or corrupted ciphertext."
                elif "parse" in err.lower() or "invalid" in err.lower():
                    hint = " — Token appears malformed or incomplete."
                st.markdown(
                    f'<div class="icard red"><div class="lbl">Decryption Failed</div><div class="val r">{err}{hint}</div></div>',
                    unsafe_allow_html=True
                )
                st.toast("Decryption failed", icon="❗")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3.5rem;padding:1.5rem 0;border-top:1px solid var(--border)">
  <div style="font-family:'Share Tech Mono',monospace;font-size:0.62rem;color:var(--muted);letter-spacing:0.22em">
    CIPHERCORE &#183; 10-ALGORITHM SUITE &#183; AES-CBC/GCM/CTR &#183; CHACHA20 &#183; 3DES &#183; SCRYPT &#183; PBKDF2 &#183; ZERO STORAGE
  </div>
  <div style="font-size:0.62rem;color:#1e2a38;margin-top:0.3rem">All operations run in memory only &#183; Keys never leave this session</div>
</div>
""", unsafe_allow_html=True)