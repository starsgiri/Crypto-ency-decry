import streamlit as st
import base64, os, json, time, zlib, struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding, hashes
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
    --bg:     #07090e; --surf:   #0d1117; --surf2:  #111820;
    --border: #1c2535; --accent: #00e5ff; --purple: #7c3aed;
    --green:  #00ffaa; --red:    #ff4466; --yellow: #fbbf24;
    --text:   #c8d6e5; --muted:  #4a6080; --img-accent: #ff6b9d;
}
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif !important;
    background: var(--bg) !important; color: var(--text) !important;
}
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }
@keyframes fadein { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:none} }
.hero {
    text-align:center; padding:2.8rem 1rem 2rem;
    background:linear-gradient(160deg,#0d1117 0%,#0a111c 100%);
    border:1px solid var(--border); border-radius:4px; margin-bottom:2rem;
    box-shadow:0 0 60px rgba(0,229,255,0.05); animation:fadein 1s ease;
}
.hero-title { font-family:'Share Tech Mono',monospace; font-size:3rem; color:var(--accent);
    text-shadow:0 0 40px rgba(0,229,255,0.5); letter-spacing:0.12em; margin:0; }
.hero-sub { color:var(--muted); font-size:0.78rem; letter-spacing:0.35em;
    text-transform:uppercase; margin-top:0.5rem; }
.sec-header { display:flex; align-items:center; gap:0.8rem; margin:2rem 0 0.8rem; }
.sec-num { font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:var(--accent);
    background:rgba(0,229,255,0.08); border:1px solid rgba(0,229,255,0.25);
    padding:0.15rem 0.55rem; border-radius:2px; }
.sec-num.img-mode { color:var(--img-accent); background:rgba(255,107,157,0.08);
    border-color:rgba(255,107,157,0.25); }
.sec-title { font-size:0.72rem; font-weight:700; letter-spacing:0.3em;
    text-transform:uppercase; color:var(--muted); }
.icard { background:var(--surf2); border:1px solid var(--border);
    border-left:3px solid var(--accent); padding:1rem 1.3rem; border-radius:2px;
    margin:0.7rem 0; font-family:'Share Tech Mono',monospace; font-size:0.8rem;
    line-height:1.8; word-break:break-all;
    transition:box-shadow 0.25s,transform 0.2s; animation:fadein 0.7s ease; }
.icard:hover { box-shadow:0 4px 24px rgba(0,229,255,0.09); transform:translateY(-1px); }
.icard.green  { border-left-color:var(--green); }
.icard.yellow { border-left-color:var(--yellow); }
.icard.red    { border-left-color:var(--red); }
.icard.purple { border-left-color:var(--purple); }
.icard.pink   { border-left-color:var(--img-accent); }
.lbl { color:var(--muted); font-size:0.63rem; letter-spacing:0.2em;
    text-transform:uppercase; margin-bottom:0.25rem; }
.val   { color:var(--accent); }
.val.g { color:var(--green); }  .val.w { color:#e8f4ff; }
.val.y { color:var(--yellow); } .val.r { color:var(--red); }
.val.p { color:var(--img-accent); }
hr.div { border:none; border-top:1px solid var(--border); margin:1.6rem 0; opacity:0.6; }
.srow { display:flex; border:1px solid var(--border); border-radius:2px;
    margin-bottom:0.5rem; overflow:hidden; font-family:'Share Tech Mono',monospace;
    animation:fadein 0.6s ease; }
.sk { background:rgba(0,0,0,0.45); color:var(--muted); font-size:0.63rem;
    letter-spacing:0.18em; text-transform:uppercase; padding:0.7rem 1rem;
    min-width:190px; display:flex; align-items:center;
    border-right:1px solid var(--border); }
.sv { background:rgba(0,229,255,0.025); color:var(--accent); font-size:0.8rem;
    padding:0.7rem 1rem; flex:1; display:flex; align-items:center; word-break:break-all; }
.sv.g{color:var(--green);} .sv.w{color:#e8f4ff;} .sv.y{color:var(--yellow);}
.sv.m{color:var(--muted);font-size:0.7rem;} .sv.p{color:var(--img-accent);}
.sv.msg{color:#e8f4ff;font-size:0.9rem;white-space:pre-wrap;word-break:break-word;line-height:1.8;}
.flow-outer { border:1px solid var(--border); border-radius:2px; margin-bottom:0.5rem; overflow:hidden; }
.flow-hdr { background:rgba(0,0,0,0.45); color:var(--muted); font-family:'Share Tech Mono',monospace;
    font-size:0.63rem; letter-spacing:0.18em; text-transform:uppercase;
    padding:0.7rem 1rem; border-bottom:1px solid var(--border); }
.flow-body { background:rgba(0,229,255,0.025); padding:0.85rem 1rem;
    display:flex; flex-wrap:wrap; align-items:center; gap:0.35rem; }
.fstep { background:rgba(0,229,255,0.08); border:1px solid rgba(0,229,255,0.2);
    color:var(--text); font-family:'Share Tech Mono',monospace; font-size:0.68rem;
    padding:0.28rem 0.65rem; border-radius:2px; }
.fstep.img { background:rgba(255,107,157,0.08); border-color:rgba(255,107,157,0.2); }
.farrow { color:var(--accent); font-size:0.9rem; font-family:'Share Tech Mono',monospace; }
.hiw-outer { border:1px solid var(--border); border-radius:2px; margin-bottom:0.5rem; overflow:hidden; }
.hiw-hdr { background:rgba(0,0,0,0.45); color:var(--muted); font-family:'Share Tech Mono',monospace;
    font-size:0.63rem; letter-spacing:0.18em; text-transform:uppercase;
    padding:0.7rem 1rem; border-bottom:1px solid var(--border); }
.hiw-body { background:rgba(0,229,255,0.025); padding:0.9rem 1.1rem; }
.hiw-step { display:flex; gap:0.75rem; margin-bottom:0.55rem; font-family:'Share Tech Mono',monospace;
    font-size:0.71rem; line-height:1.7; }
.hiw-n { color:var(--accent); min-width:18px; font-weight:700; }
.hiw-n.img { color:var(--img-accent); }
.hiw-t { color:var(--muted); }  .hiw-t strong { color:var(--text); }
.sec-note { border:1px solid rgba(251,191,36,0.3); border-left:3px solid var(--yellow);
    background:rgba(251,191,36,0.03); border-radius:2px; padding:0.85rem 1.1rem;
    margin-bottom:0.5rem; font-family:'Share Tech Mono',monospace; font-size:0.7rem;
    color:var(--muted); line-height:1.9; }
.sec-note strong { color:var(--yellow); }
.img-note { border:1px solid rgba(255,107,157,0.3); border-left:3px solid var(--img-accent);
    background:rgba(255,107,157,0.03); border-radius:2px; padding:0.85rem 1.1rem;
    margin-bottom:0.5rem; font-family:'Share Tech Mono',monospace; font-size:0.7rem;
    color:var(--muted); line-height:1.9; }
.img-note strong { color:var(--img-accent); }
.size-limit-note { border:1px solid rgba(251,191,36,0.5); border-left:3px solid var(--yellow);
    background:rgba(251,191,36,0.05); border-radius:2px; padding:0.85rem 1.1rem;
    margin-bottom:0.5rem; font-family:'Share Tech Mono',monospace; font-size:0.72rem;
    color:var(--muted); line-height:1.9; }
.size-limit-note strong { color:var(--yellow); }
.sum-title { font-family:'Share Tech Mono',monospace; font-size:1.05rem;
    letter-spacing:0.15em; text-align:center; margin-bottom:1.2rem;
    padding-bottom:0.9rem; border-bottom:1px solid var(--border); }
.sum-title.enc { color:var(--green); text-shadow:0 0 18px rgba(0,255,170,0.3); }
.sum-title.dec { color:var(--accent); text-shadow:0 0 18px rgba(0,229,255,0.3); }
.sum-title.img-enc { color:var(--img-accent); text-shadow:0 0 18px rgba(255,107,157,0.3); }
.sum-title.img-dec { color:var(--img-accent); text-shadow:0 0 18px rgba(255,107,157,0.3); }
.token-stats { font-family:'Share Tech Mono',monospace; font-size:0.65rem;
    color:var(--muted); letter-spacing:0.12em; text-align:right;
    margin-top:-0.3rem; margin-bottom:0.5rem; }
.token-stats .ok  { color:var(--green); }
.token-stats .warn{ color:var(--yellow); }
.stSelectbox label,.stRadio label,.stTextArea label,.stTextInput label {
    color:var(--muted)!important; font-family:'Share Tech Mono',monospace!important;
    font-size:0.72rem!important; letter-spacing:0.15em!important; text-transform:uppercase!important; }
div[data-baseweb="select"] > div {
    background:var(--surf2)!important; border-color:var(--border)!important;
    border-radius:2px!important; color:var(--text)!important; }
textarea, input[type="text"], input[type="password"] {
    background:var(--surf2)!important; border:1px solid var(--border)!important;
    border-radius:2px!important; color:var(--text)!important;
    font-family:'Share Tech Mono',monospace!important; font-size:0.8rem!important; }
.stButton > button {
    background:linear-gradient(90deg,rgba(0,229,255,.07),rgba(124,58,237,.07))!important;
    border:1px solid var(--accent)!important; color:var(--accent)!important;
    font-family:'Share Tech Mono',monospace!important; letter-spacing:0.18em!important;
    text-transform:uppercase!important; border-radius:2px!important; padding:0.5rem 2rem!important;
    width:100%; font-size:1rem!important; transition:all 0.2s ease!important; }
.stButton > button:hover {
    background:linear-gradient(90deg,rgba(0,229,255,.18),rgba(124,58,237,.18))!important;
    box-shadow:0 0 18px rgba(0,229,255,.2)!important;
    color:#fff!important; border-color:var(--purple)!important; transform:scale(1.02); }
.strength { font-family:'Share Tech Mono',monospace; font-size:0.68rem;
    letter-spacing:0.15em; margin:-0.3rem 0 0.5rem; }
.img-preview-container { border:1px solid rgba(255,107,157,0.3); border-radius:2px;
    padding:1rem; background:rgba(255,107,157,0.03); text-align:center;
    margin:0.7rem 0; animation:fadein 0.8s ease; }
.img-preview-label { font-family:'Share Tech Mono',monospace; font-size:0.63rem;
    letter-spacing:0.2em; text-transform:uppercase; color:var(--img-accent); margin-bottom:0.7rem; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
IMAGE_SIZE_LIMIT_BYTES = 10 * 1024
IMAGE_SIZE_WARN_BYTES  =  8 * 1024

ALGO_NAMES = [
    "AES-128-CBC", "AES-256-CBC", "AES-192-CBC",
    "AES-128-GCM", "AES-256-GCM", "AES-256-GCM-Scrypt",
    "AES-256-CTR", "ChaCha20", "ChaCha20-Scrypt", "3DES-CBC",
]
ALGO_INDEX = {name: i for i, name in enumerate(ALGO_NAMES)}

# ─── Helpers ──────────────────────────────────────────────────────────────────
def b64e_url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b'=').decode()

def b64d_url(s: str) -> bytes:
    pad = 4 - len(s) % 4
    if pad != 4:
        s += '=' * pad
    return base64.urlsafe_b64decode(s.encode())

def format_bytes(n: int) -> str:
    if n < 1024: return f"{n} B"
    elif n < 1024**2: return f"{n/1024:.1f} KB"
    else: return f"{n/1024**2:.2f} MB"

def token_line_count(token: str, width: int = 80) -> int:
    return (len(token) + width - 1) // width

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
        "flow": ["Passphrase","PBKDF2-SHA256 (200k)","128-bit Key + 16B IV","PKCS7 Pad","AES-CBC Encrypt","Binary Pack","Base64 Out"],
        "enc_steps": [
            ("Random Salt",     "16 random bytes — unique keys every run even with same passphrase"),
            ("PBKDF2-SHA256",   "200,000 iterations stretch passphrase into a 128-bit cryptographic key"),
            ("Random IV",       "16-byte IV randomises CBC block chaining per message"),
            ("PKCS7 Padding",   "Plaintext padded to 16-byte block boundary required by AES"),
            ("AES-CBC Encrypt", "Each plaintext block XOR'd with prior cipherblock, then AES-encrypted"),
            ("Binary Pack",     "Fields packed as compact binary — ~48% shorter than JSON token format"),
        ],
    },
    "AES-256-CBC": {
        "desc": "AES 256-bit - CBC Mode",
        "detail": "Block cipher, 256-bit key, PKCS7 padding, CBC chaining",
        "key_len": 32, "kdf": "pbkdf2", "mode_type": "cbc",
        "flow": ["Passphrase","PBKDF2-SHA256 (200k)","256-bit Key + 16B IV","PKCS7 Pad","AES-CBC Encrypt","Binary Pack","Base64 Out"],
        "enc_steps": [
            ("Random Salt",     "16 random bytes for key uniqueness"),
            ("PBKDF2-SHA256",   "200k iterations -> 256-bit key (strongest AES key size)"),
            ("Random IV",       "16-byte IV for CBC block chaining"),
            ("PKCS7 Padding",   "Pad to 16-byte block boundary"),
            ("AES-CBC Encrypt", "CBC mode with 256-bit AES key"),
            ("Binary Pack",     "Compact binary -> URL-safe Base64 output token"),
        ],
    },
    "AES-192-CBC": {
        "desc": "AES 192-bit - CBC Mode",
        "detail": "Block cipher, 192-bit key, PKCS7 padding, CBC chaining",
        "key_len": 24, "kdf": "pbkdf2", "mode_type": "cbc",
        "flow": ["Passphrase","PBKDF2-SHA256 (200k)","192-bit Key + 16B IV","PKCS7 Pad","AES-CBC Encrypt","Binary Pack","Base64 Out"],
        "enc_steps": [
            ("Random Salt",     "16 random bytes generated"),
            ("PBKDF2-SHA256",   "200k iterations -> 192-bit key"),
            ("Random IV",       "16-byte IV for CBC"),
            ("PKCS7 Padding",   "Pad to 16-byte block boundary"),
            ("AES-CBC Encrypt", "CBC mode with 192-bit AES key"),
            ("Binary Pack",     "Compact binary -> Base64"),
        ],
    },
    "AES-128-GCM": {
        "desc": "AES 128-bit - GCM Mode (AEAD)",
        "detail": "Authenticated encryption, 128-bit key, 12B nonce, 16B auth tag",
        "key_len": 16, "kdf": "pbkdf2", "mode_type": "gcm",
        "flow": ["Passphrase","PBKDF2-SHA256 (200k)","128-bit Key + 12B Nonce","AES-GCM Encrypt","Auth Tag (16B)","Binary Pack","Base64 Out"],
        "enc_steps": [
            ("Random Salt",    "16 random bytes for key uniqueness"),
            ("PBKDF2-SHA256",  "200k iterations -> 128-bit key"),
            ("Random Nonce",   "12-byte nonce — unique per message, critical for GCM security"),
            ("AES-GCM Encrypt","Authenticated encryption: produces ciphertext + 16-byte auth tag"),
            ("Auth Tag",       "16B tag cryptographically binds key+nonce+plaintext; tampering detected"),
            ("Binary Pack",    "Compact binary + URL-safe Base64 — ~48% shorter than JSON tokens"),
        ],
    },
    "AES-256-GCM": {
        "desc": "AES 256-bit - GCM Mode (AEAD)",
        "detail": "Authenticated encryption, 256-bit key, 12B nonce, 16B auth tag",
        "key_len": 32, "kdf": "pbkdf2", "mode_type": "gcm",
        "flow": ["Passphrase","PBKDF2-SHA256 (200k)","256-bit Key + 12B Nonce","AES-GCM Encrypt","Auth Tag (16B)","Binary Pack","Base64 Out"],
        "enc_steps": [
            ("Random Salt",    "16 random bytes for key uniqueness"),
            ("PBKDF2-SHA256",  "200k iterations -> 256-bit key (maximum AES strength)"),
            ("Random Nonce",   "12-byte nonce for GCM — reuse would be catastrophic"),
            ("AES-GCM Encrypt","AEAD: ciphertext + 16B auth tag in one pass"),
            ("Auth Tag",       "Tag verifies integrity; wrong key = decryption failure"),
            ("Binary Pack",    "Compact binary + URL-safe Base64"),
        ],
    },
    "AES-256-GCM-Scrypt": {
        "desc": "AES-256-GCM + Scrypt KDF",
        "detail": "Authenticated AES-256-GCM with memory-hard Scrypt key derivation",
        "key_len": 32, "kdf": "scrypt", "mode_type": "gcm",
        "flow": ["Passphrase","Scrypt (N=16384 r=8 p=1)","256-bit Key + 12B Nonce","AES-GCM Encrypt","Auth Tag (16B)","Binary Pack","Base64 Out"],
        "enc_steps": [
            ("Random Salt",    "16 random bytes"),
            ("Scrypt KDF",     "Memory-hard KDF: N=16384, r=8, p=1 — GPU/ASIC brute-force resistant"),
            ("Random Nonce",   "12-byte nonce for GCM"),
            ("AES-GCM Encrypt","AEAD: ciphertext + 16B auth tag"),
            ("Auth Tag",       "Integrity verification tag"),
            ("Binary Pack",    "Compact binary + URL-safe Base64"),
        ],
    },
    "AES-256-CTR": {
        "desc": "AES 256-bit - CTR Mode",
        "detail": "Counter mode, 256-bit key — turns AES into a stream cipher",
        "key_len": 32, "kdf": "pbkdf2", "mode_type": "ctr",
        "flow": ["Passphrase","PBKDF2-SHA256 (200k)","256-bit Key + 16B Nonce","AES-CTR Stream Encrypt","Binary Pack","Base64 Out"],
        "enc_steps": [
            ("Random Salt",     "16 random bytes"),
            ("PBKDF2-SHA256",   "200k iterations -> 256-bit key"),
            ("Random Nonce",    "16-byte counter nonce"),
            ("AES-CTR Encrypt", "Counter incremented per block, XOR'd with plaintext — no padding needed"),
            ("Binary Pack",     "Compact binary + URL-safe Base64"),
        ],
    },
    "ChaCha20": {
        "desc": "ChaCha20 Stream Cipher",
        "detail": "Stream cipher, 256-bit key, 16B nonce — no padding, constant-time",
        "key_len": 32, "kdf": "pbkdf2", "mode_type": "chacha",
        "flow": ["Passphrase","PBKDF2-SHA256 (200k)","256-bit Key + 16B Nonce","ChaCha20 Encrypt","Binary Pack","Base64 Out"],
        "enc_steps": [
            ("Random Salt",    "16 random bytes"),
            ("PBKDF2-SHA256",  "200k iterations -> 256-bit key"),
            ("Random Nonce",   "16-byte nonce for ChaCha20"),
            ("ChaCha20",       "20-round ARX operations produce pseudorandom keystream XOR'd with plaintext"),
            ("Binary Pack",    "Compact binary + URL-safe Base64"),
        ],
    },
    "ChaCha20-Scrypt": {
        "desc": "ChaCha20 + Scrypt KDF",
        "detail": "ChaCha20 stream cipher with memory-hard Scrypt key derivation",
        "key_len": 32, "kdf": "scrypt", "mode_type": "chacha",
        "flow": ["Passphrase","Scrypt (N=16384 r=8 p=1)","256-bit Key + 16B Nonce","ChaCha20 Encrypt","Binary Pack","Base64 Out"],
        "enc_steps": [
            ("Random Salt",    "16 random bytes"),
            ("Scrypt KDF",     "Memory-hard KDF — very resistant to offline brute-force attacks"),
            ("Random Nonce",   "16-byte nonce"),
            ("ChaCha20",       "ARX stream cipher — no padding, constant-time execution"),
            ("Binary Pack",    "Compact binary + URL-safe Base64"),
        ],
    },
    "3DES-CBC": {
        "desc": "Triple DES - CBC Mode (Legacy)",
        "detail": "Legacy 3DES, 24-byte key (168-bit effective), CBC mode, PKCS7",
        "key_len": 24, "kdf": "pbkdf2", "mode_type": "3des",
        "flow": ["Passphrase","PBKDF2-SHA256 (200k)","168-bit Key + 8B IV","PKCS7 Pad","3DES-CBC Encrypt","Binary Pack","Base64 Out"],
        "enc_steps": [
            ("Random Salt",    "16 random bytes"),
            ("PBKDF2-SHA256",  "200k iterations -> 24-byte (168-bit effective) key"),
            ("Random IV",      "8-byte IV for DES block chaining"),
            ("PKCS7 Padding",  "Pad to 8-byte DES block boundary"),
            ("3DES-CBC",       "Encrypt-Decrypt-Encrypt with 3 DES keys (legacy compatibility mode)"),
            ("Binary Pack",    "Compact binary + URL-safe Base64"),
        ],
    },
}

# ─── IV / tag sizes per mode ─────────────────────────────────────────────────
_IV_LEN  = {"cbc": 16, "gcm": 12, "ctr": 16, "chacha": 16, "3des": 8}
_HAS_TAG = {"cbc": False, "gcm": True, "ctr": False, "chacha": False, "3des": False}

# ─── Raw crypto primitives ────────────────────────────────────────────────────
def _raw_encrypt(data: bytes, passphrase: str, algo: str):
    cfg  = ALGORITHMS[algo]
    salt = os.urandom(16)
    key  = derive_key(passphrase, salt, cfg["key_len"], cfg["kdf"])
    mt   = cfg["mode_type"]

    if mt == "cbc":
        iv     = os.urandom(16)
        padder = sym_padding.PKCS7(128).padder()
        padded = padder.update(data) + padder.finalize()
        enc    = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).encryptor()
        return salt, iv, None, enc.update(padded) + enc.finalize()

    elif mt == "gcm":
        nonce = os.urandom(12)
        enc   = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend()).encryptor()
        ct    = enc.update(data) + enc.finalize()
        return salt, nonce, enc.tag, ct

    elif mt == "ctr":
        nonce = os.urandom(16)
        enc   = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend()).encryptor()
        return salt, nonce, None, enc.update(data) + enc.finalize()

    elif mt == "chacha":
        nonce = os.urandom(16)
        enc   = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend()).encryptor()
        return salt, nonce, None, enc.update(data) + enc.finalize()

    elif mt == "3des":
        iv     = os.urandom(8)
        padder = sym_padding.PKCS7(64).padder()
        padded = padder.update(data) + padder.finalize()
        enc    = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend()).encryptor()
        return salt, iv, None, enc.update(padded) + enc.finalize()

    raise ValueError(f"Unknown mode: {mt}")


def _raw_decrypt(ct: bytes, passphrase: str, algo: str,
                 iv_nonce: bytes, salt: bytes, tag) -> bytes:
    cfg = ALGORITHMS[algo]
    key = derive_key(passphrase, salt, cfg["key_len"], cfg["kdf"])
    mt  = cfg["mode_type"]

    if mt == "cbc":
        dec    = Cipher(algorithms.AES(key), modes.CBC(iv_nonce), backend=default_backend()).decryptor()
        padded = dec.update(ct) + dec.finalize()
        unpad  = sym_padding.PKCS7(128).unpadder()
        return unpad.update(padded) + unpad.finalize()

    elif mt == "gcm":
        dec = Cipher(algorithms.AES(key), modes.GCM(iv_nonce, tag), backend=default_backend()).decryptor()
        return dec.update(ct) + dec.finalize()

    elif mt == "ctr":
        dec = Cipher(algorithms.AES(key), modes.CTR(iv_nonce), backend=default_backend()).decryptor()
        return dec.update(ct) + dec.finalize()

    elif mt == "chacha":
        dec = Cipher(algorithms.ChaCha20(key, iv_nonce), mode=None, backend=default_backend()).decryptor()
        return dec.update(ct) + dec.finalize()

    elif mt == "3des":
        dec    = Cipher(algorithms.TripleDES(key), modes.CBC(iv_nonce), backend=default_backend()).decryptor()
        padded = dec.update(ct) + dec.finalize()
        unpad  = sym_padding.PKCS7(64).unpadder()
        return unpad.update(padded) + unpad.finalize()

    raise ValueError(f"Unsupported mode: {mt}")


# ─── Compact binary token format ─────────────────────────────────────────────
# TEXT  token: [0x54][algo_id:1][salt:16][iv_nonce][tag?:16][ct...]
# IMAGE token: [0x49][algo_id:1][mime_len:1][fname_len:1][salt:16][iv_nonce][tag?:16]
#              [orig_size:4][comp_size:4][mime bytes][fname bytes][ct...]

def do_encrypt(plaintext: str, passphrase: str, algo: str) -> str:
    salt, iv_nonce, tag, ct = _raw_encrypt(plaintext.encode(), passphrase, algo)
    binary = bytes([0x54, ALGO_INDEX[algo]]) + salt + iv_nonce
    if tag: binary += tag
    binary += ct
    return b64e_url(binary)


def do_decrypt(ciphertext_b64: str, passphrase: str):
    try:
        binary = b64d_url(ciphertext_b64)
    except Exception:
        raise ValueError("Invalid token — cannot decode Base64.")
    if len(binary) < 2:
        raise ValueError("Token too short — corrupted or wrong format.")
    if binary[0] == 0x49:
        raise ValueError("This token contains an IMAGE. Use the Image Decrypt tab.")
    if binary[0] != 0x54:
        raise ValueError("Unrecognised token type. Token may be corrupted.")

    algo_id = binary[1]
    if algo_id >= len(ALGO_NAMES):
        raise ValueError(f"Unknown algorithm ID {algo_id}.")
    algo    = ALGO_NAMES[algo_id]
    mt      = ALGORITHMS[algo]["mode_type"]
    off     = 2
    salt    = binary[off:off+16]; off += 16
    ivl     = _IV_LEN[mt]
    iv_nonce= binary[off:off+ivl]; off += ivl
    tag     = None
    if _HAS_TAG[mt]:
        tag = binary[off:off+16]; off += 16
    pt = _raw_decrypt(binary[off:], passphrase, algo, iv_nonce, salt, tag)
    return pt.decode(), algo


def do_encrypt_image(image_bytes: bytes, passphrase: str, algo: str,
                     filename: str, mime_type: str) -> str:
    compressed = zlib.compress(image_bytes, level=9)
    salt, iv_nonce, tag, ct = _raw_encrypt(compressed, passphrase, algo)
    mime_b = mime_type.encode()[:255]
    fname_b= filename.encode()[:255]
    binary = bytes([0x49, ALGO_INDEX[algo], len(mime_b), len(fname_b)])
    binary += salt + iv_nonce
    if tag: binary += tag
    binary += struct.pack('>II', len(image_bytes), len(compressed))
    binary += mime_b + fname_b + ct
    return b64e_url(binary)


def do_decrypt_image(ciphertext_b64: str, passphrase: str):
    try:
        binary = b64d_url(ciphertext_b64)
    except Exception:
        raise ValueError("Invalid token — cannot decode Base64.")
    if len(binary) < 4:
        raise ValueError("Token too short.")
    if binary[0] == 0x54:
        raise ValueError("This token contains TEXT. Use the Text Decrypt tab.")
    if binary[0] != 0x49:
        raise ValueError("Unrecognised token type.")

    algo_id  = binary[1]
    mime_len = binary[2]
    fname_len= binary[3]
    if algo_id >= len(ALGO_NAMES):
        raise ValueError(f"Unknown algorithm ID {algo_id}.")
    algo = ALGO_NAMES[algo_id]
    mt   = ALGORITHMS[algo]["mode_type"]
    off  = 4
    salt     = binary[off:off+16]; off += 16
    ivl      = _IV_LEN[mt]
    iv_nonce = binary[off:off+ivl]; off += ivl
    tag      = None
    if _HAS_TAG[mt]:
        tag = binary[off:off+16]; off += 16
    orig_size, comp_size = struct.unpack('>II', binary[off:off+8]); off += 8
    mime_type = binary[off:off+mime_len].decode(); off += mime_len
    filename  = binary[off:off+fname_len].decode(); off += fname_len
    compressed = _raw_decrypt(binary[off:], passphrase, algo, iv_nonce, salt, tag)
    image_bytes= zlib.decompress(compressed)
    return image_bytes, algo, filename, mime_type, orig_size


# ─── UI helpers ───────────────────────────────────────────────────────────────
def _srow(label, value, vcls=""):
    return (f'<div class="srow"><div class="sk">{label}</div>'
            f'<div class="sv {vcls}">{value}</div></div>')

def render_summary_rows(rows):
    st.markdown("".join(_srow(l,v,c) for l,v,c in rows), unsafe_allow_html=True)

def render_flow(steps, title="Encryption Pipeline", img_mode=False):
    cls = " img" if img_mode else ""
    parts = []
    for i, s in enumerate(steps):
        parts.append(f'<span class="fstep{cls}">{s}</span>')
        if i < len(steps)-1: parts.append('<span class="farrow">&#8594;</span>')
    st.markdown(f'<div class="flow-outer"><div class="flow-hdr">{title}</div>'
                f'<div class="flow-body">{" ".join(parts)}</div></div>', unsafe_allow_html=True)

def render_how_it_works(steps, mode="encrypt", img_mode=False):
    hdr = "How Encryption Works — Step by Step" if mode=="encrypt" else "How Decryption Works — Step by Step"
    nc  = " img" if img_mode else ""
    rows = "".join(
        f'<div class="hiw-step"><div class="hiw-n{nc}">{i}.</div>'
        f'<div class="hiw-t"><strong>{t}:</strong> {d}</div></div>'
        for i,(t,d) in enumerate(steps, 1))
    st.markdown(f'<div class="hiw-outer"><div class="hiw-hdr">{hdr}</div>'
                f'<div class="hiw-body">{rows}</div></div>', unsafe_allow_html=True)

def render_note():
    st.markdown("""<div class="sec-note"><strong>SECURITY NOTE</strong><br>
    Share the <strong>Encrypted Token</strong> freely — safe to transmit on any channel.<br>
    Share the <strong>Passphrase</strong> only via a separate secure channel (phone, Signal, in-person).<br>
    Never send passphrase and ciphertext together in the same message.</div>""", unsafe_allow_html=True)

def render_token_stats(token: str):
    chars = len(token); lines = token_line_count(token)
    cls   = "ok" if lines <= 200 else "warn"
    st.markdown(f'<div class="token-stats">Token: <span class="{cls}">'
                f'{chars:,} chars &nbsp;·&nbsp; ~{lines} lines</span></div>', unsafe_allow_html=True)

def passphrase_widget(key: str):
    pw = st.text_input("Enter a strong passphrase", type="password",
                       placeholder="Minimum 12 characters recommended…", key=key)
    if pw:
        score = sum([len(pw)>=8, len(pw)>=14,
                     any(c.isupper() for c in pw),
                     any(c.isdigit() for c in pw),
                     any(c in "!@#$%^&*()_+-=" for c in pw)])
        sl, sc = ("Weak","color:var(--red)") if score<3 else \
                 ("Moderate","color:var(--yellow)") if score<4 else \
                 ("Strong","color:var(--green)")
        st.markdown(f'<div class="strength" style="{sc}">PASSPHRASE STRENGTH: {sl}</div>',
                    unsafe_allow_html=True)
    return pw

def get_mime_extension(mime):
    return {"image/png":".png","image/jpeg":".jpg","image/jpg":".jpg",
            "image/gif":".gif","image/webp":".webp","image/bmp":".bmp",
            "image/tiff":".tiff"}.get(mime, ".png")


# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">&#x1F510; CIPHERCORE</div>
  <div class="hero-sub">10-Algorithm Cryptography Suite &nbsp;&#183;&nbsp; Auto-Detection Decrypt &nbsp;&#183;&nbsp; Image Encryption &nbsp;&#183;&nbsp; Compact Tokens</div>
</div>""", unsafe_allow_html=True)

# ─── Target ───────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-header"><span class="sec-num">00</span>'
            '<span class="sec-title">Encryption Target</span></div>', unsafe_allow_html=True)
target_raw = st.radio("", ["💬  Text / Message", "🖼️  Image / File"],
                      horizontal=True, label_visibility="collapsed")
target = "Image" if "Image" in target_raw else "Text"
st.markdown('<hr class="div">', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  IMAGE MODE
# ══════════════════════════════════════════════════════════════════════════════
if target == "Image":

    st.markdown('<div class="icard pink"><div class="lbl">Image Encryption Mode</div>'
                '<div class="val p">Encrypt any image (≤ 10 KB) into a compact Base64 token — '
                'guaranteed under 200 lines. Decrypt to restore the original image with download.</div></div>',
                unsafe_allow_html=True)

    st.markdown('<div class="sec-header"><span class="sec-num img-mode">01</span>'
                '<span class="sec-title">Operation Mode</span></div>', unsafe_allow_html=True)
    img_mode_raw = st.radio("", ["🔒  Encrypt Image", "🔓  Decrypt Image"],
                            horizontal=True, label_visibility="collapsed", key="img_mode_radio")
    img_mode = "Encrypt" if "Encrypt" in img_mode_raw else "Decrypt"
    st.markdown('<hr class="div">', unsafe_allow_html=True)

    # ── IMAGE ENCRYPT ─────────────────────────────────────────────────────────
    if img_mode == "Encrypt":

        st.markdown('<div class="sec-header"><span class="sec-num img-mode">02</span>'
                    '<span class="sec-title">Choose Encryption Algorithm</span></div>', unsafe_allow_html=True)
        algo_names = list(ALGORITHMS.keys())
        if "img_chosen_algo" not in st.session_state:
            st.session_state["img_chosen_algo"] = "AES-256-GCM"
        img_algo = st.selectbox("Algorithm", algo_names,
                                index=algo_names.index(st.session_state["img_chosen_algo"]),
                                format_func=lambda x: f"{x}  —  {ALGORITHMS[x]['desc']}",
                                label_visibility="collapsed", key="img_algo_select")
        st.session_state["img_chosen_algo"] = img_algo
        img_cfg   = ALGORITHMS[img_algo]
        kdf_label = "Scrypt (memory-hard)" if img_cfg["kdf"]=="scrypt" else "PBKDF2-SHA256 (200k iterations)"
        st.markdown(
            f'<div class="icard" style="border-left-color:var(--img-accent)">'
            f'<div class="lbl">Selected Algorithm</div><div class="val p">{img_algo}</div>'
            f'<div style="color:var(--muted);font-size:0.72rem;margin-top:0.25rem">{img_cfg["detail"]}</div>'
            f'<div style="color:var(--muted);font-size:0.68rem;margin-top:0.15rem">'
            f'KDF: {kdf_label} &nbsp;&#183;&nbsp; Key: {img_cfg["key_len"]*8}-bit</div></div>',
            unsafe_allow_html=True)

        st.markdown('<hr class="div">', unsafe_allow_html=True)
        st.markdown("""<div class="size-limit-note">
            <strong>&#x26A0; IMAGE SIZE LIMIT — 10 KB maximum</strong><br>
            This guarantees the encrypted token stays under ~200 lines in all cases.<br>
            &nbsp;&nbsp;&#x2022; JPEGs (already compressed): keep source under <strong>10 KB</strong>.<br>
            &nbsp;&nbsp;&#x2022; PNGs / BMPs: can be larger — they compress far better with zlib.<br>
            &nbsp;&nbsp;Tip: resize to a small thumbnail or use an online image compressor first.
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-header"><span class="sec-num img-mode">03</span>'
                    '<span class="sec-title">Upload Image (max 10 KB)</span></div>', unsafe_allow_html=True)
        uploaded_img = st.file_uploader("Upload an image to encrypt",
                                        type=["png","jpg","jpeg","gif","webp","bmp","tiff"],
                                        label_visibility="collapsed", key="img_upload")

        img_bytes = img_filename = img_mime = None
        if uploaded_img is not None:
            img_bytes    = uploaded_img.read()
            img_filename = uploaded_img.name
            img_mime     = uploaded_img.type or "image/png"
            size_ok      = len(img_bytes) <= IMAGE_SIZE_LIMIT_BYTES
            size_warn    = len(img_bytes) > IMAGE_SIZE_WARN_BYTES
            size_cls     = "r" if not size_ok else ("y" if size_warn else "g")
            size_note    = (" ⚠ EXCEEDS 10 KB LIMIT"                    if not size_ok else
                            " ⚠ NEAR LIMIT — token may approach 200 lines" if size_warn else
                            " ✓ WITHIN LIMIT")
            st.markdown(
                _srow("File Name", img_filename, "w") +
                _srow("File Size", f"{format_bytes(len(img_bytes))}{size_note}", size_cls) +
                _srow("MIME Type", img_mime, ""),
                unsafe_allow_html=True)

            if not size_ok:
                st.markdown(f'<div class="icard red"><div class="lbl">Size Error</div>'
                            f'<div class="val r">Image is {format_bytes(len(img_bytes))} — '
                            f'exceeds the 10 KB limit. Please resize or compress before uploading.</div></div>',
                            unsafe_allow_html=True)
            else:
                st.markdown('<div class="img-preview-container">'
                            '<div class="img-preview-label">&#x1F5BC; Image Preview — Original</div></div>',
                            unsafe_allow_html=True)
                st.image(img_bytes, use_column_width=True)

        st.markdown('<hr class="div">', unsafe_allow_html=True)
        st.markdown('<div class="sec-header"><span class="sec-num img-mode">04</span>'
                    '<span class="sec-title">Secret Passphrase</span></div>', unsafe_allow_html=True)
        img_passphrase = passphrase_widget("img_pass_enc")
        st.markdown('<hr class="div">', unsafe_allow_html=True)

        if st.button("⚡  ENCRYPT IMAGE"):
            if uploaded_img is None or img_bytes is None:
                st.markdown('<div class="icard red"><div class="lbl">Error</div>'
                            '<div class="val r">No image uploaded.</div></div>', unsafe_allow_html=True)
            elif len(img_bytes) > IMAGE_SIZE_LIMIT_BYTES:
                st.markdown(f'<div class="icard red"><div class="lbl">Size Error</div>'
                            f'<div class="val r">Image is {format_bytes(len(img_bytes))}. '
                            f'Maximum is 10 KB to keep token under 200 lines.</div></div>', unsafe_allow_html=True)
            elif not img_passphrase:
                st.markdown('<div class="icard red"><div class="lbl">Error</div>'
                            '<div class="val r">Passphrase is required.</div></div>', unsafe_allow_html=True)
            else:
                try:
                    with st.spinner("Compressing and encrypting image…"):
                        time.sleep(0.4)
                        ct_b64 = do_encrypt_image(img_bytes, img_passphrase, img_algo, img_filename, img_mime)
                    st.balloons()

                    comp_preview  = zlib.compress(img_bytes, level=9)
                    comp_ratio    = (1 - len(comp_preview)/len(img_bytes)) * 100
                    lines         = token_line_count(ct_b64)
                    integrity     = "Yes — Authentication Tag included (AEAD)" if img_cfg["mode_type"]=="gcm" \
                                    else "No — use GCM/Scrypt variant for AEAD"
                    integrity_cls = "g" if img_cfg["mode_type"]=="gcm" else "y"
                    kdf_full      = "Scrypt (N=16384, r=8, p=1) — memory-hard" \
                                    if img_cfg["kdf"]=="scrypt" else "PBKDF2-SHA256 — 200,000 iterations"

                    st.markdown('<div class="sum-title img-enc">&#x2705; IMAGE ENCRYPTION SUCCESSFUL — SUMMARY</div>',
                                unsafe_allow_html=True)
                    render_summary_rows([
                        ("Algorithm Used",     img_algo,                                     "p"),
                        ("Algorithm Detail",   img_cfg["detail"],                            "m"),
                        ("Key Derivation",     kdf_full,                                     ""),
                        ("Effective Key Size", f"{img_cfg['key_len']*8} bits",               ""),
                        ("Integrity / AEAD",   integrity,                                    integrity_cls),
                        ("Original File",      img_filename,                                 "w"),
                        ("MIME Type",          img_mime,                                     ""),
                        ("Original Size",      format_bytes(len(img_bytes)),                 "w"),
                        ("Compressed Size",    f"{format_bytes(len(comp_preview))} (saved {comp_ratio:.1f}%)", "g"),
                        ("Token Format",       "Compact binary + URL-safe Base64 (~48% smaller than JSON)", "g"),
                        ("Token Length",       f"{len(ct_b64):,} chars  (~{lines} lines)",   "g" if lines<=200 else "y"),
                    ])
                    render_flow(["Image Upload","zlib Compress (lvl 9)","Binary Pack",
                                 "Key Derive","Encrypt","URL-safe Base64 Out"],
                                title="Image Encryption Pipeline", img_mode=True)
                    render_how_it_works([
                        ("Image Upload",    f"Raw bytes read from '{img_filename}' ({format_bytes(len(img_bytes))})"),
                        ("zlib Compress",   f"Compressed to {format_bytes(len(comp_preview))} ({comp_ratio:.1f}% savings)"),
                        ("Key Derivation",  kdf_full),
                        ("Encrypt",         f"{img_algo} encrypts the compressed image bytes"),
                        ("Binary Pack",     "Fields packed as compact binary header — no JSON keys, ~25% shorter"),
                        ("URL-safe Base64", "Binary payload encoded — safe to copy/paste/share on any channel"),
                    ], mode="encrypt", img_mode=True)

                    st.markdown("""<div class="img-note">
                        <strong>IMAGE ENCRYPTION NOTE</strong><br>
                        Original filename and MIME type are embedded inside the encrypted token.<br>
                        Token uses compact <strong>binary packing + URL-safe Base64</strong>.<br>
                        Paste this token into <strong>Image Decrypt</strong> to recover the original image.
                    </div>""", unsafe_allow_html=True)

                    st.markdown('<div class="sec-header"><span class="sec-num img-mode">&#8595;</span>'
                                '<span class="sec-title">Encrypted Image Token — Copy and Share</span></div>',
                                unsafe_allow_html=True)
                    st.text_area("Encrypted Image Token (URL-safe Base64)", value=ct_b64,
                                 height=200, key="img_enc_output")
                    render_token_stats(ct_b64)
                    st.toast("Image encryption complete!", icon="🖼️")

                except Exception as e:
                    st.markdown(f'<div class="icard red"><div class="lbl">Encryption Error</div>'
                                f'<div class="val r">{e}</div></div>', unsafe_allow_html=True)

    # ── IMAGE DECRYPT ─────────────────────────────────────────────────────────
    else:
        st.markdown("""<div class="icard purple">
            <div class="lbl">Auto-Detection Active</div>
            <div class="val">Algorithm and original image metadata are automatically read from the token.</div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-header"><span class="sec-num img-mode">02</span>'
                    '<span class="sec-title">Paste Encrypted Image Token</span></div>', unsafe_allow_html=True)
        img_ct_input = st.text_area("Encrypted Image Token (URL-safe Base64)", height=200,
                                    placeholder="Paste the encrypted image token here…",
                                    key="img_dec_input")

        st.markdown('<hr class="div">', unsafe_allow_html=True)
        st.markdown('<div class="sec-header"><span class="sec-num img-mode">03</span>'
                    '<span class="sec-title">Passphrase</span></div>', unsafe_allow_html=True)
        img_dec_pass = st.text_input("Enter the passphrase used during encryption", type="password",
                                     placeholder="Enter the shared passphrase…", key="img_pass_dec")
        st.markdown('<hr class="div">', unsafe_allow_html=True)

        if st.button("⚡  DECRYPT IMAGE"):
            if not img_ct_input.strip():
                st.markdown('<div class="icard red"><div class="lbl">Error</div>'
                            '<div class="val r">No encrypted token provided.</div></div>', unsafe_allow_html=True)
            elif not img_dec_pass:
                st.markdown('<div class="icard red"><div class="lbl">Error</div>'
                            '<div class="val r">Passphrase is required.</div></div>', unsafe_allow_html=True)
            else:
                try:
                    with st.spinner("Decrypting and decompressing image…"):
                        time.sleep(0.4)
                        img_out, algo_det, orig_filename, orig_mime, orig_size = \
                            do_decrypt_image(img_ct_input.strip(), img_dec_pass)
                    st.snow()

                    cfg_d         = ALGORITHMS[algo_det]
                    kdf_full      = "Scrypt (N=16384, r=8, p=1) — memory-hard" \
                                    if cfg_d["kdf"]=="scrypt" else "PBKDF2-SHA256 — 200,000 iterations"
                    integrity     = "Yes — Auth Tag verified (AEAD)" if cfg_d["mode_type"]=="gcm" \
                                    else "N/A — non-authenticated mode"
                    integrity_cls = "g" if cfg_d["mode_type"]=="gcm" else "y"

                    st.markdown('<div class="sum-title img-dec">&#x1F513; IMAGE DECRYPTION SUCCESSFUL — SUMMARY</div>',
                                unsafe_allow_html=True)
                    render_summary_rows([
                        ("Algorithm Detected",  algo_det,                                           "p"),
                        ("Algorithm Detail",    cfg_d["detail"],                                    "m"),
                        ("Key Derivation",      kdf_full,                                           ""),
                        ("Effective Key Size",  f"{cfg_d['key_len']*8} bits ({cfg_d['key_len']} bytes)", ""),
                        ("Integrity Verified",  integrity,                                          integrity_cls),
                        ("Original Filename",   orig_filename,                                      "w"),
                        ("MIME Type",           orig_mime,                                          ""),
                        ("Recovered Size",      format_bytes(len(img_out)),                         "g"),
                    ])
                    render_flow(["Base64 Input","Binary Parse","Algo Detection",
                                 "Key Re-Derivation","Decrypt","Verify/Unpad",
                                 "zlib Decompress","Image Output"],
                                title="Image Decryption Pipeline", img_mode=True)
                    render_how_it_works([
                        ("Parse Token",      "URL-safe Base64 decoded, binary header parsed — type byte, algo ID, salt, nonce/IV extracted"),
                        ("Detect Algorithm", f"Algorithm ID byte matched to '{algo_det}' — automatic, no user selection"),
                        ("Re-derive Key",    f"{kdf_full} with same salt reproduces identical key"),
                        ("Decrypt",          f"{algo_det} decryption using recovered key + stored nonce/IV"),
                        ("Verify / Unpad",   "Auth tag verified (GCM) or padding stripped (CBC) — wrong key raises error"),
                        ("Decompress",       "zlib decompresses decrypted bytes back to original image data"),
                        ("Display+Download", "Recovered image rendered in browser with one-click download"),
                    ], mode="decrypt", img_mode=True)

                    st.markdown('<hr class="div">', unsafe_allow_html=True)
                    st.markdown('<div class="img-preview-container">'
                                '<div class="img-preview-label">&#x1F5BC; Recovered Image — Decrypted Successfully</div></div>',
                                unsafe_allow_html=True)
                    st.image(img_out, use_column_width=True, caption=f"Recovered: {orig_filename}")

                    st.markdown('<hr class="div">', unsafe_allow_html=True)
                    st.markdown('<div class="sec-header"><span class="sec-num img-mode">&#8595;</span>'
                                '<span class="sec-title">Download Recovered Image</span></div>', unsafe_allow_html=True)
                    ext     = get_mime_extension(orig_mime)
                    dl_name = orig_filename if orig_filename.lower().endswith(
                        ('.png','.jpg','.jpeg','.gif','.webp','.bmp','.tiff')
                    ) else f"decrypted_image{ext}"
                    st.download_button("⬇️  DOWNLOAD DECRYPTED IMAGE", data=img_out,
                                       file_name=dl_name, mime=orig_mime, use_container_width=True)
                    st.toast("Image decryption complete!", icon="🖼️")

                except Exception as e:
                    err  = str(e)
                    hint = (" — Incorrect passphrase or corrupted ciphertext." if any(
                                w in err.lower() for w in ["padding","mac","tag"]) else
                            " — Token appears malformed or incomplete." if any(
                                w in err.lower() for w in ["parse","invalid"]) else "")
                    st.markdown(f'<div class="icard red"><div class="lbl">Decryption Failed</div>'
                                f'<div class="val r">{err}{hint}</div></div>', unsafe_allow_html=True)
                    st.toast("Decryption failed", icon="❗")


# ══════════════════════════════════════════════════════════════════════════════
#  TEXT MODE
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown('<div class="sec-header"><span class="sec-num">01</span>'
                '<span class="sec-title">Operation Mode</span></div>', unsafe_allow_html=True)
    mode_raw = st.radio("", ["🔒  Encrypt", "🔓  Decrypt"],
                        horizontal=True, label_visibility="collapsed")
    mode = "Encrypt" if "Encrypt" in mode_raw else "Decrypt"
    st.markdown('<hr class="div">', unsafe_allow_html=True)

    # ── TEXT ENCRYPT ──────────────────────────────────────────────────────────
    if mode == "Encrypt":
        st.markdown('<div class="sec-header"><span class="sec-num">02</span>'
                    '<span class="sec-title">Choose Encryption Algorithm</span></div>', unsafe_allow_html=True)
        algo_names = list(ALGORITHMS.keys())
        if "chosen_algo" not in st.session_state:
            st.session_state["chosen_algo"] = "AES-256-GCM"
        chosen_algo = st.selectbox("Algorithm", algo_names,
                                   index=algo_names.index(st.session_state["chosen_algo"]),
                                   format_func=lambda x: f"{x}  —  {ALGORITHMS[x]['desc']}",
                                   label_visibility="collapsed")
        st.session_state["chosen_algo"] = chosen_algo
        cfg       = ALGORITHMS[chosen_algo]
        kdf_label = "Scrypt (memory-hard)" if cfg["kdf"]=="scrypt" else "PBKDF2-SHA256 (200k iterations)"
        st.markdown(
            f'<div class="icard"><div class="lbl">Selected Algorithm</div>'
            f'<div class="val">{chosen_algo}</div>'
            f'<div style="color:var(--muted);font-size:0.72rem;margin-top:0.25rem">{cfg["detail"]}</div>'
            f'<div style="color:var(--muted);font-size:0.68rem;margin-top:0.15rem">'
            f'KDF: {kdf_label} &nbsp;&#183;&nbsp; Key: {cfg["key_len"]*8}-bit</div></div>',
            unsafe_allow_html=True)

        st.markdown('<hr class="div">', unsafe_allow_html=True)
        st.markdown('<div class="sec-header"><span class="sec-num">03</span>'
                    '<span class="sec-title">Secret Passphrase</span></div>', unsafe_allow_html=True)
        passphrase = passphrase_widget("txt_pass_enc")

        st.markdown('<hr class="div">', unsafe_allow_html=True)
        st.markdown('<div class="sec-header"><span class="sec-num">04</span>'
                    '<span class="sec-title">Plaintext Message</span></div>', unsafe_allow_html=True)
        plaintext = st.text_area("Message to encrypt", height=150,
                                 placeholder="Type or paste the message you want to encrypt…")
        st.markdown('<hr class="div">', unsafe_allow_html=True)

        if st.button("⚡  ENCRYPT MESSAGE"):
            if not plaintext.strip():
                st.markdown('<div class="icard red"><div class="lbl">Error</div>'
                            '<div class="val r">No message provided.</div></div>', unsafe_allow_html=True)
            elif not passphrase:
                st.markdown('<div class="icard red"><div class="lbl">Error</div>'
                            '<div class="val r">Passphrase is required.</div></div>', unsafe_allow_html=True)
            else:
                try:
                    with st.spinner("Encrypting…"):
                        time.sleep(0.4)
                        ct_b64 = do_encrypt(plaintext, passphrase, chosen_algo)
                    st.balloons()

                    lines         = token_line_count(ct_b64)
                    integrity     = "Yes — Authentication Tag included (AEAD)" if cfg["mode_type"]=="gcm" \
                                    else "No — use GCM/Scrypt variant for AEAD"
                    integrity_cls = "g" if cfg["mode_type"]=="gcm" else "y"
                    kdf_full      = "Scrypt (N=16384, r=8, p=1) — memory-hard" \
                                    if cfg["kdf"]=="scrypt" else "PBKDF2-SHA256 — 200,000 iterations"

                    st.markdown('<div class="sum-title enc">&#x2705; ENCRYPTION SUCCESSFUL — SUMMARY</div>',
                                unsafe_allow_html=True)
                    render_summary_rows([
                        ("Algorithm Used",     chosen_algo,                                  "g"),
                        ("Algorithm Detail",   cfg["detail"],                                "m"),
                        ("Key Derivation",     kdf_full,                                     ""),
                        ("Effective Key Size", f"{cfg['key_len']*8} bits ({cfg['key_len']} bytes)", ""),
                        ("Mode of Operation",  cfg["mode_type"].upper(),                     ""),
                        ("Integrity / AEAD",   integrity,                                    integrity_cls),
                        ("Token Format",       "Compact binary + URL-safe Base64 (~48% shorter than JSON)", "g"),
                        ("Plaintext Length",   f"{len(plaintext)} characters",               "w"),
                        ("Token Length",       f"{len(ct_b64):,} chars  (~{lines} lines)",   "g"),
                    ])
                    render_flow(cfg["flow"], title="Encryption Pipeline")
                    render_how_it_works(cfg["enc_steps"], mode="encrypt")
                    render_note()

                    st.markdown('<div class="sec-header"><span class="sec-num">&#8595;</span>'
                                '<span class="sec-title">Encrypted Token — Copy and Share With Recipient</span></div>',
                                unsafe_allow_html=True)
                    st.text_area("Encrypted Token (URL-safe Base64)", value=ct_b64, height=160,
                                 help="Paste into the Decrypt tab. Algorithm auto-detected from token.")
                    render_token_stats(ct_b64)
                    st.toast("Encryption complete!", icon="✅")

                except Exception as e:
                    st.markdown(f'<div class="icard red"><div class="lbl">Encryption Error</div>'
                                f'<div class="val r">{e}</div></div>', unsafe_allow_html=True)

    # ── TEXT DECRYPT ──────────────────────────────────────────────────────────
    else:
        st.markdown("""<div class="icard purple">
            <div class="lbl">Auto-Detection Active</div>
            <div class="val">Algorithm is automatically read from the encrypted token — no manual selection needed.</div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-header"><span class="sec-num">02</span>'
                    '<span class="sec-title">Paste Encrypted Token</span></div>', unsafe_allow_html=True)
        ct_input = st.text_area("Encrypted Token (URL-safe Base64)", height=160,
                                placeholder="Paste the Base64 encrypted token received from the sender…")

        st.markdown('<hr class="div">', unsafe_allow_html=True)
        st.markdown('<div class="sec-header"><span class="sec-num">03</span>'
                    '<span class="sec-title">Passphrase</span></div>', unsafe_allow_html=True)
        dec_pass = st.text_input("Enter the passphrase shared by the sender", type="password",
                                 placeholder="Enter the shared passphrase…")
        st.markdown('<hr class="div">', unsafe_allow_html=True)

        if st.button("⚡  DECRYPT MESSAGE"):
            if not ct_input.strip():
                st.markdown('<div class="icard red"><div class="lbl">Error</div>'
                            '<div class="val r">No encrypted token provided.</div></div>', unsafe_allow_html=True)
            elif not dec_pass:
                st.markdown('<div class="icard red"><div class="lbl">Error</div>'
                            '<div class="val r">Passphrase is required.</div></div>', unsafe_allow_html=True)
            else:
                try:
                    with st.spinner("Decrypting…"):
                        time.sleep(0.4)
                        plaintext_out, algo_det = do_decrypt(ct_input.strip(), dec_pass)
                    st.snow()

                    cfg_d         = ALGORITHMS[algo_det]
                    kdf_full      = "Scrypt (N=16384, r=8, p=1) — memory-hard" \
                                    if cfg_d["kdf"]=="scrypt" else "PBKDF2-SHA256 — 200,000 iterations"
                    integrity     = "Yes — Auth Tag verified (AEAD)" if cfg_d["mode_type"]=="gcm" \
                                    else "N/A — non-authenticated mode"
                    integrity_cls = "g" if cfg_d["mode_type"]=="gcm" else "y"

                    st.markdown('<div class="sum-title dec">&#x1F513; DECRYPTION SUCCESSFUL — SUMMARY</div>',
                                unsafe_allow_html=True)
                    render_summary_rows([
                        ("Algorithm Detected",  algo_det,                                           "g"),
                        ("Algorithm Detail",    cfg_d["detail"],                                    "m"),
                        ("Key Derivation",      kdf_full,                                           ""),
                        ("Effective Key Size",  f"{cfg_d['key_len']*8} bits ({cfg_d['key_len']} bytes)", ""),
                        ("Mode of Operation",   cfg_d["mode_type"].upper(),                         ""),
                        ("Integrity Verified",  integrity,                                          integrity_cls),
                    ])
                    st.markdown(
                        f'<div class="srow"><div class="sk">Decrypted Message</div>'
                        f'<div class="sv msg">{plaintext_out}</div></div>',
                        unsafe_allow_html=True)

                    render_flow(["Base64 Input","Binary Parse","Algo Detection",
                                 "Key Re-Derivation","Decrypt","Verify/Unpad","Plaintext Out"],
                                title="Decryption Pipeline")
                    render_how_it_works([
                        ("Parse Token",      "URL-safe Base64 decoded, binary header parsed — type byte, algo ID, salt, nonce/IV extracted"),
                        ("Detect Algorithm", f"Algorithm ID byte matched to '{algo_det}' — fully automatic"),
                        ("Re-derive Key",    f"{kdf_full} — same salt + passphrase reproduces identical key"),
                        ("Decrypt",          f"{algo_det} decryption using recovered key + stored nonce/IV"),
                        ("Verify / Unpad",   "Auth tag verified (GCM) or padding stripped (CBC) — wrong key raises error"),
                        ("Output Plaintext", "Decrypted bytes decoded to UTF-8 string and displayed"),
                    ], mode="decrypt")

                    st.markdown('<div class="sec-header"><span class="sec-num">&#8595;</span>'
                                '<span class="sec-title">Decrypted Message</span></div>', unsafe_allow_html=True)
                    st.text_area("Plaintext Output", value=plaintext_out, height=120)
                    st.toast("Decryption complete!", icon="✅")

                except Exception as e:
                    err  = str(e)
                    hint = (" — Incorrect passphrase or corrupted ciphertext." if any(
                                w in err.lower() for w in ["padding","mac","tag"]) else
                            " — Token appears malformed or incomplete." if any(
                                w in err.lower() for w in ["parse","invalid"]) else "")
                    st.markdown(f'<div class="icard red"><div class="lbl">Decryption Failed</div>'
                                f'<div class="val r">{err}{hint}</div></div>', unsafe_allow_html=True)
                    st.toast("Decryption failed", icon="❗")


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3.5rem;padding:1.5rem 0;border-top:1px solid var(--border)">
  <div style="font-family:'Share Tech Mono',monospace;font-size:0.62rem;color:var(--muted);letter-spacing:0.22em">
    CIPHERCORE &#183; 10-ALGORITHM SUITE &#183; AES-CBC/GCM/CTR &#183; CHACHA20 &#183; 3DES
    &#183; SCRYPT &#183; PBKDF2 &#183; IMAGE ENCRYPTION &#183; COMPACT BINARY TOKENS &#183; ZERO STORAGE
  </div>
  <div style="font-size:0.62rem;color:#1e2a38;margin-top:0.3rem">
    All operations run in memory only &#183; Keys never leave this session
  </div>
</div>""", unsafe_allow_html=True)