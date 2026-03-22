import streamlit as st
import base64, os, json, hashlib, time, struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding, hashes, serialization, hmac
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CipherCore | Crypto Suite",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Styling ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #07090e;
    --surface: #0d1117;
    --surface2: #111820;
    --border: #1c2535;
    --accent: #00e5ff;
    --accent2: #7c3aed;
    --green: #00ffaa;
    --red: #ff4466;
    --yellow: #fbbf24;
    --text: #c8d6e5;
    --muted: #4a6080;
}
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }

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
    font-size: 3rem;
    color: var(--accent);
    text-shadow: 0 0 40px rgba(0,229,255,0.5);
    letter-spacing: 0.12em;
    margin: 0;
}
.hero-sub {
    color: var(--muted);
    font-size: 0.78rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}
@keyframes fadein {
    from { opacity:0; transform:translateY(20px); }
    to   { opacity:1; transform:none; }
}

.sec-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 2rem 0 0.8rem;
}
.sec-num {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: var(--accent);
    background: rgba(0,229,255,0.08);
    border: 1px solid rgba(0,229,255,0.25);
    padding: 0.15rem 0.55rem;
    border-radius: 2px;
}
.sec-title {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--muted);
}

.card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    padding: 1.1rem 1.4rem;
    border-radius: 2px;
    margin: 0.8rem 0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.8;
    word-break: break-all;
    transition: box-shadow 0.25s, transform 0.2s;
    animation: fadein 0.8s ease;
}
.card:hover { box-shadow: 0 4px 28px rgba(0,229,255,0.1); transform: translateY(-1px); }
.card.success { border-left-color: var(--green); }
.card.warn    { border-left-color: var(--yellow); }
.card.error   { border-left-color: var(--red); }
.card.purple  { border-left-color: var(--accent2); }

.lbl { color: var(--muted); font-size: 0.65rem; letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 0.25rem; }
.val       { color: var(--accent); }
.val.green { color: var(--green); }
.val.white { color: #e8f4ff; }
.val.yellow { color: var(--yellow); }

hr.div {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.6rem 0;
    opacity: 0.6;
}

/* inputs */
.stSelectbox label, .stRadio label, .stTextArea label, .stTextInput label {
    color: var(--muted) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
}
div[data-baseweb="select"] > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    border-radius: 2px !important;
    color: var(--text) !important;
}
textarea, input[type="text"], input[type="password"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    color: var(--text) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* buttons */
.stButton > button {
    background: linear-gradient(90deg, rgba(0,229,255,0.07), rgba(124,58,237,0.07)) !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
    padding: 0.5rem 2rem !important;
    width: 100%;
    font-size: 1rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(90deg, rgba(0,229,255,0.18), rgba(124,58,237,0.18)) !important;
    box-shadow: 0 0 18px rgba(0,229,255,0.2) !important;
    color: #fff !important;
    border-color: var(--accent2) !important;
    transform: scale(1.02);
}

/* algo grid */
.algo-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.6rem;
    margin: 0.8rem 0;
}
.algo-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'Share Tech Mono', monospace;
}
.algo-card:hover { border-color: var(--accent); box-shadow: 0 0 12px rgba(0,229,255,0.1); }
.algo-card.selected { border-color: var(--accent); background: rgba(0,229,255,0.06); }
.algo-name { color: var(--accent); font-size: 0.8rem; font-weight: 700; }
.algo-desc { color: var(--muted); font-size: 0.65rem; margin-top: 0.2rem; }

/* summary */
.summary-wrap {
    background: linear-gradient(135deg, #0d1117 0%, #0a111c 100%);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 2rem;
    margin: 1.5rem 0;
    animation: fadein 0.8s ease;
}
.summary-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.2rem;
    color: var(--green);
    letter-spacing: 0.15em;
    margin-bottom: 1.5rem;
    text-align: center;
    text-shadow: 0 0 20px rgba(0,255,170,0.3);
}
.summary-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.s-item { background: rgba(0,0,0,0.3); border: 1px solid var(--border); border-radius: 2px; padding: 0.8rem 1rem; }
.s-item.full { grid-column: 1/-1; }
.s-lbl { color: var(--muted); font-family: 'Share Tech Mono', monospace; font-size: 0.62rem; letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 0.3rem; }
.s-val { color: var(--accent); font-family: 'Share Tech Mono', monospace; font-size: 0.82rem; word-break: break-all; }
.s-val.green { color: var(--green); }
.s-val.white { color: #e8f4ff; font-size: 0.9rem; }
.s-val.yellow { color: var(--yellow); }

.flow-box {
    background: rgba(0,0,0,0.3);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 1rem 1.2rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    line-height: 2;
    margin-top: 0.5rem;
}
.flow-step { color: var(--text); }
.flow-arrow { color: var(--accent); margin: 0 0.5rem; }
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

# ─── Algorithm Definitions ───────────────────────────────────────────────────
ALGORITHMS = {
    "AES-128-CBC": {
        "desc": "AES 128-bit · CBC Mode",
        "detail": "Block cipher, 128-bit key, PKCS7 padding, CBC chaining",
        "key_len": 16, "kdf": "pbkdf2",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k iter)", "128-bit key + 16B IV", "PKCS7 Pad", "AES-CBC Encrypt", "Base64 Output"]
    },
    "AES-256-CBC": {
        "desc": "AES 256-bit · CBC Mode",
        "detail": "Block cipher, 256-bit key, PKCS7 padding, CBC chaining",
        "key_len": 32, "kdf": "pbkdf2",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k iter)", "256-bit key + 16B IV", "PKCS7 Pad", "AES-CBC Encrypt", "Base64 Output"]
    },
    "AES-256-GCM": {
        "desc": "AES 256-bit · GCM Mode",
        "detail": "Authenticated encryption, 256-bit key, 12B nonce, 16B auth tag",
        "key_len": 32, "kdf": "pbkdf2",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k iter)", "256-bit key + 12B nonce", "AES-GCM Encrypt", "Auth Tag appended", "Base64 Output"]
    },
    "AES-128-GCM": {
        "desc": "AES 128-bit · GCM Mode",
        "detail": "Authenticated encryption, 128-bit key, 12B nonce, 16B auth tag",
        "key_len": 16, "kdf": "pbkdf2",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k iter)", "128-bit key + 12B nonce", "AES-GCM Encrypt", "Auth Tag appended", "Base64 Output"]
    },
    "ChaCha20": {
        "desc": "ChaCha20 Stream Cipher",
        "detail": "Stream cipher, 256-bit key, 16B nonce, no padding needed",
        "key_len": 32, "kdf": "pbkdf2",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k iter)", "256-bit key + 16B nonce", "ChaCha20 Stream Encrypt", "Base64 Output"]
    },
    "ChaCha20-Scrypt": {
        "desc": "ChaCha20 + Scrypt KDF",
        "detail": "ChaCha20 stream cipher with memory-hard Scrypt key derivation",
        "key_len": 32, "kdf": "scrypt",
        "flow": ["Passphrase", "Scrypt (N=16384, r=8, p=1)", "256-bit key + 16B nonce", "ChaCha20 Stream Encrypt", "Base64 Output"]
    },
    "AES-256-CTR": {
        "desc": "AES 256-bit · CTR Mode",
        "detail": "Counter mode, 256-bit key, turns AES into stream cipher",
        "key_len": 32, "kdf": "pbkdf2",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k iter)", "256-bit key + 16B nonce", "AES-CTR Stream Encrypt", "Base64 Output"]
    },
    "AES-192-CBC": {
        "desc": "AES 192-bit · CBC Mode",
        "detail": "Block cipher, 192-bit key, PKCS7 padding, CBC chaining",
        "key_len": 24, "kdf": "pbkdf2",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k iter)", "192-bit key + 16B IV", "PKCS7 Pad", "AES-CBC Encrypt", "Base64 Output"]
    },
    "AES-256-GCM-Scrypt": {
        "desc": "AES-256-GCM + Scrypt KDF",
        "detail": "Authenticated AES-256-GCM with memory-hard Scrypt key derivation",
        "key_len": 32, "kdf": "scrypt",
        "flow": ["Passphrase", "Scrypt (N=16384, r=8, p=1)", "256-bit key + 12B nonce", "AES-GCM Encrypt + Auth Tag", "Base64 Output"]
    },
    "3DES-CBC": {
        "desc": "Triple DES · CBC Mode",
        "detail": "Legacy 3DES, 24-byte key (168-bit effective), CBC mode, PKCS7",
        "key_len": 24, "kdf": "pbkdf2",
        "flow": ["Passphrase", "PBKDF2-SHA256 (200k iter)", "168-bit key + 8B IV", "PKCS7 Pad", "3DES-CBC Encrypt", "Base64 Output"]
    },
}

# ─── Encrypt Core ─────────────────────────────────────────────────────────────
def do_encrypt(plaintext: str, passphrase: str, algo: str) -> str:
    cfg = ALGORITHMS[algo]
    data = plaintext.encode()
    salt = os.urandom(16)
    key = derive_key(passphrase, salt, cfg["key_len"], cfg["kdf"])

    if algo in ("AES-128-CBC", "AES-256-CBC", "AES-192-CBC"):
        iv = os.urandom(16)
        pad = sym_padding.PKCS7(128).padder()
        padded = pad.update(data) + pad.finalize()
        enc = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).encryptor()
        ct = enc.update(padded) + enc.finalize()
        payload = {"algo": algo, "salt": b64e(salt), "iv": b64e(iv), "ct": b64e(ct)}

    elif algo in ("AES-256-GCM", "AES-128-GCM", "AES-256-GCM-Scrypt"):
        nonce = os.urandom(12)
        enc = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend()).encryptor()
        ct = enc.update(data) + enc.finalize()
        tag = enc.tag
        payload = {"algo": algo, "salt": b64e(salt), "nonce": b64e(nonce), "ct": b64e(ct), "tag": b64e(tag)}

    elif algo in ("ChaCha20", "ChaCha20-Scrypt"):
        nonce = os.urandom(16)
        enc = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend()).encryptor()
        ct = enc.update(data) + enc.finalize()
        payload = {"algo": algo, "salt": b64e(salt), "nonce": b64e(nonce), "ct": b64e(ct)}

    elif algo == "AES-256-CTR":
        nonce = os.urandom(16)
        enc = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend()).encryptor()
        ct = enc.update(data) + enc.finalize()
        payload = {"algo": algo, "salt": b64e(salt), "nonce": b64e(nonce), "ct": b64e(ct)}

    elif algo == "3DES-CBC":
        iv = os.urandom(8)
        pad = sym_padding.PKCS7(64).padder()
        padded = pad.update(data) + pad.finalize()
        enc = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend()).encryptor()
        ct = enc.update(padded) + enc.finalize()
        payload = {"algo": algo, "salt": b64e(salt), "iv": b64e(iv), "ct": b64e(ct)}

    else:
        raise ValueError(f"Unknown algorithm: {algo}")

    return b64e(json.dumps(payload).encode())


# ─── Decrypt Core ─────────────────────────────────────────────────────────────
def do_decrypt(ciphertext_b64: str, passphrase: str) -> tuple[str, str]:
    try:
        payload = json.loads(b64d(ciphertext_b64).decode())
    except Exception:
        raise ValueError("Invalid ciphertext — could not parse encrypted payload.")

    algo = payload.get("algo")
    if not algo or algo not in ALGORITHMS:
        raise ValueError(f"Unknown or missing algorithm tag in payload: {algo}")

    cfg = ALGORITHMS[algo]
    salt = b64d(payload["salt"])
    key = derive_key(passphrase, salt, cfg["key_len"], cfg["kdf"])

    if algo in ("AES-128-CBC", "AES-256-CBC", "AES-192-CBC"):
        iv = b64d(payload["iv"])
        ct = b64d(payload["ct"])
        dec = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).decryptor()
        padded = dec.update(ct) + dec.finalize()
        unpad = sym_padding.PKCS7(128).unpadder()
        pt = unpad.update(padded) + unpad.finalize()

    elif algo in ("AES-256-GCM", "AES-128-GCM", "AES-256-GCM-Scrypt"):
        nonce = b64d(payload["nonce"])
        ct = b64d(payload["ct"])
        tag = b64d(payload["tag"])
        dec = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend()).decryptor()
        pt = dec.update(ct) + dec.finalize()

    elif algo in ("ChaCha20", "ChaCha20-Scrypt"):
        nonce = b64d(payload["nonce"])
        ct = b64d(payload["ct"])
        dec = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend()).decryptor()
        pt = dec.update(ct) + dec.finalize()

    elif algo == "AES-256-CTR":
        nonce = b64d(payload["nonce"])
        ct = b64d(payload["ct"])
        dec = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend()).decryptor()
        pt = dec.update(ct) + dec.finalize()

    elif algo == "3DES-CBC":
        iv = b64d(payload["iv"])
        ct = b64d(payload["ct"])
        dec = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend()).decryptor()
        padded = dec.update(ct) + dec.finalize()
        unpad = sym_padding.PKCS7(64).unpadder()
        pt = unpad.update(padded) + unpad.finalize()

    else:
        raise ValueError(f"Unsupported algorithm: {algo}")

    return pt.decode(), algo


# ─── UI ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">🔐 CIPHERCORE</div>
  <div class="hero-sub">10-Algorithm Cryptography Suite · Auto-Detection Decrypt · Zero Storage</div>
</div>
""", unsafe_allow_html=True)

# Mode toggle
st.markdown('<div class="sec-header"><span class="sec-num">01</span><span class="sec-title">Operation Mode</span></div>', unsafe_allow_html=True)
mode_raw = st.radio("", ["🔒  Encrypt", "🔓  Decrypt"], horizontal=True, label_visibility="collapsed")
mode = "Encrypt" if "Encrypt" in mode_raw else "Decrypt"

st.markdown('<hr class="div">', unsafe_allow_html=True)

# ── ENCRYPT FLOW ──────────────────────────────────────────────────────────────
if mode == "Encrypt":

    # Algorithm picker
    st.markdown('<div class="sec-header"><span class="sec-num">02</span><span class="sec-title">Choose Encryption Algorithm</span></div>', unsafe_allow_html=True)

    algo_names = list(ALGORITHMS.keys())
    if "chosen_algo" not in st.session_state:
        st.session_state["chosen_algo"] = "AES-256-GCM"

    # Display as selectbox (clean, no JS needed)
    chosen_algo = st.selectbox(
        "Select Algorithm",
        algo_names,
        index=algo_names.index(st.session_state["chosen_algo"]),
        format_func=lambda x: f"{x}  —  {ALGORITHMS[x]['desc']}",
        label_visibility="collapsed"
    )
    st.session_state["chosen_algo"] = chosen_algo

    cfg = ALGORITHMS[chosen_algo]
    st.markdown(f"""
    <div class="card">
      <div class="lbl">Algorithm Details</div>
      <div class="val">{chosen_algo}</div>
      <div style="color:var(--muted);font-size:0.72rem;margin-top:0.3rem">{cfg['detail']}</div>
      <div style="color:var(--muted);font-size:0.68rem;margin-top:0.2rem">KDF: {'Scrypt (memory-hard)' if cfg['kdf']=='scrypt' else 'PBKDF2-SHA256 (200k iterations)'} · Key: {cfg['key_len']*8}-bit</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="div">', unsafe_allow_html=True)

    # Passphrase
    st.markdown('<div class="sec-header"><span class="sec-num">03</span><span class="sec-title">Secret Passphrase</span></div>', unsafe_allow_html=True)
    passphrase = st.text_input("Enter a strong passphrase (share this with the recipient)", type="password",
                               placeholder="Minimum 12 characters recommended…")

    strength_color = "var(--red)"
    strength_label = "Weak"
    if passphrase:
        score = sum([len(passphrase) >= 8, len(passphrase) >= 14, any(c.isupper() for c in passphrase),
                     any(c.isdigit() for c in passphrase), any(c in "!@#$%^&*()_+-=" for c in passphrase)])
        if score >= 4:
            strength_color, strength_label = "var(--green)", "Strong"
        elif score >= 3:
            strength_color, strength_label = "var(--yellow)", "Moderate"

        st.markdown(f"""
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.68rem;color:{strength_color};
                    letter-spacing:0.15em;margin:-0.3rem 0 0.5rem">
            PASSPHRASE STRENGTH: {strength_label}
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="div">', unsafe_allow_html=True)

    # Message input
    st.markdown('<div class="sec-header"><span class="sec-num">04</span><span class="sec-title">Plaintext Message</span></div>', unsafe_allow_html=True)
    plaintext = st.text_area("Message to encrypt", height=150,
                             placeholder="Type or paste the message you want to encrypt…")

    st.markdown('<hr class="div">', unsafe_allow_html=True)

    if st.button("⚡  ENCRYPT MESSAGE"):
        if not plaintext.strip():
            st.markdown('<div class="card error"><div class="lbl">Error</div><div class="val" style="color:var(--red)">No message provided.</div></div>', unsafe_allow_html=True)
        elif not passphrase:
            st.markdown('<div class="card error"><div class="lbl">Error</div><div class="val" style="color:var(--red)">Passphrase is required.</div></div>', unsafe_allow_html=True)
        else:
            try:
                with st.spinner("Encrypting…"):
                    time.sleep(0.5)
                    ct_b64 = do_encrypt(plaintext, passphrase, chosen_algo)

                st.balloons()

                # Build encryption flow steps
                flow_steps = cfg["flow"]
                flow_html = " ".join([
                    f'<span class="flow-step">{s}</span>' + (f'<span class="flow-arrow">→</span>' if i < len(flow_steps)-1 else "")
                    for i, s in enumerate(flow_steps)
                ])

                st.markdown(f"""
                <div class="summary-wrap">
                  <div class="summary-title">✅ ENCRYPTION SUCCESSFUL</div>
                  <div class="summary-grid">

                    <div class="s-item">
                      <div class="s-lbl">Algorithm Used</div>
                      <div class="s-val green">{chosen_algo}</div>
                    </div>

                    <div class="s-item">
                      <div class="s-lbl">Key Derivation</div>
                      <div class="s-val">{'Scrypt (N=16384)' if cfg['kdf']=='scrypt' else 'PBKDF2-SHA256 (200k)'}</div>
                    </div>

                    <div class="s-item">
                      <div class="s-lbl">Effective Key Size</div>
                      <div class="s-val">{cfg['key_len']*8} bits</div>
                    </div>

                    <div class="s-item">
                      <div class="s-lbl">Ciphertext Length</div>
                      <div class="s-val">{len(ct_b64)} characters</div>
                    </div>

                    <div class="s-item">
                      <div class="s-lbl">Plaintext Length</div>
                      <div class="s-val">{len(plaintext)} characters</div>
                    </div>

                    <div class="s-item">
                      <div class="s-lbl">Algorithm Detail</div>
                      <div class="s-val" style="font-size:0.72rem;color:var(--muted)">{cfg['detail']}</div>
                    </div>

                    <div class="s-item full">
                      <div class="s-lbl">Encryption Flow</div>
                      <div class="flow-box">{flow_html}</div>
                    </div>

                    <div class="s-item full">
                      <div class="s-lbl">How it works</div>
                      <div style="font-family:'Share Tech Mono',monospace;font-size:0.72rem;color:var(--muted);line-height:1.9;margin-top:0.3rem">
                        1. A random <strong style="color:var(--text)">salt</strong> is generated and your passphrase is stretched into a cryptographic key using <strong style="color:var(--text)">{cfg['kdf'].upper()}</strong>.<br>
                        2. A random <strong style="color:var(--text)">nonce/IV</strong> is generated for this message — each encryption is unique even with the same key.<br>
                        3. The plaintext is encrypted using <strong style="color:var(--text)">{chosen_algo}</strong> producing indistinguishable ciphertext.<br>
                        4. The salt, nonce/IV, algorithm tag, and ciphertext are bundled and Base64-encoded into the output token.<br>
                        5. The recipient uses the same passphrase — the algorithm is <strong style="color:var(--accent)">auto-detected from the token</strong>; no manual selection needed.
                      </div>
                    </div>

                    <div class="s-item full">
                      <div class="s-lbl">⚠️ Security Note</div>
                      <div style="color:var(--yellow);font-family:'Share Tech Mono',monospace;font-size:0.72rem;line-height:1.8">
                        Share the <strong>Encrypted Token</strong> freely — it's safe to transmit.<br>
                        Share the <strong>Passphrase</strong> only via a secure, separate channel (call, Signal, etc.).<br>
                        Never send both in the same message/email.
                      </div>
                    </div>

                  </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="sec-header"><span class="sec-num">↓</span><span class="sec-title">Copy Encrypted Token — Share This With Recipient</span></div>', unsafe_allow_html=True)
                st.text_area("Encrypted Token (Base64)", value=ct_b64, height=160,
                             help="Copy this entire string and give it to the person who needs to decrypt it.")
                st.toast("Encryption complete! 🔐", icon="✅")

            except Exception as e:
                st.markdown(f'<div class="card error"><div class="lbl">Encryption Error</div><div class="val" style="color:var(--red)">{str(e)}</div></div>', unsafe_allow_html=True)

# ── DECRYPT FLOW ──────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div class="card purple">
      <div class="lbl">Auto-Detection Mode</div>
      <div class="val">Algorithm is automatically detected from the encrypted token — no manual selection needed.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-header"><span class="sec-num">02</span><span class="sec-title">Encrypted Token</span></div>', unsafe_allow_html=True)
    ct_input = st.text_area("Paste the encrypted token here", height=160,
                            placeholder="Paste the Base64 encrypted token received from the sender…")

    st.markdown('<hr class="div">', unsafe_allow_html=True)

    st.markdown('<div class="sec-header"><span class="sec-num">03</span><span class="sec-title">Passphrase</span></div>', unsafe_allow_html=True)
    dec_pass = st.text_input("Enter the passphrase shared by the sender", type="password",
                             placeholder="Enter the shared passphrase…")

    st.markdown('<hr class="div">', unsafe_allow_html=True)

    if st.button("⚡  DECRYPT MESSAGE"):
        if not ct_input.strip():
            st.markdown('<div class="card error"><div class="lbl">Error</div><div class="val" style="color:var(--red)">No encrypted token provided.</div></div>', unsafe_allow_html=True)
        elif not dec_pass:
            st.markdown('<div class="card error"><div class="lbl">Error</div><div class="val" style="color:var(--red)">Passphrase is required.</div></div>', unsafe_allow_html=True)
        else:
            try:
                with st.spinner("Decrypting…"):
                    time.sleep(0.4)
                    plaintext_out, algo_detected = do_decrypt(ct_input.strip(), dec_pass)

                st.snow()
                cfg_d = ALGORITHMS[algo_detected]

                st.markdown(f"""
                <div class="summary-wrap">
                  <div class="summary-title">🔓 DECRYPTION SUCCESSFUL</div>
                  <div class="summary-grid">

                    <div class="s-item">
                      <div class="s-lbl">Algorithm Detected</div>
                      <div class="s-val green">{algo_detected}</div>
                    </div>

                    <div class="s-item">
                      <div class="s-lbl">Key Derivation</div>
                      <div class="s-val">{'Scrypt (N=16384)' if cfg_d['kdf']=='scrypt' else 'PBKDF2-SHA256 (200k)'}</div>
                    </div>

                    <div class="s-item">
                      <div class="s-lbl">Effective Key Size</div>
                      <div class="s-val">{cfg_d['key_len']*8} bits</div>
                    </div>

                    <div class="s-item">
                      <div class="s-lbl">Algorithm Detail</div>
                      <div class="s-val" style="font-size:0.72rem;color:var(--muted)">{cfg_d['detail']}</div>
                    </div>

                    <div class="s-item full">
                      <div class="s-lbl">Decrypted Message</div>
                      <div class="s-val white" style="margin-top:0.4rem;font-size:1rem;line-height:1.8;
                           background:rgba(0,255,170,0.04);border:1px solid rgba(0,255,170,0.15);
                           border-radius:2px;padding:0.8rem 1rem">
                        {plaintext_out}
                      </div>
                    </div>

                  </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="sec-header"><span class="sec-num">↓</span><span class="sec-title">Decrypted Message</span></div>', unsafe_allow_html=True)
                st.text_area("Plaintext", value=plaintext_out, height=120)
                st.toast("Decryption complete! 🔓", icon="✅")

            except Exception as e:
                err = str(e)
                hint = ""
                if "padding" in err.lower() or "mac" in err.lower() or "tag" in err.lower():
                    hint = " — Likely incorrect passphrase or corrupted ciphertext."
                elif "invalid" in err.lower():
                    hint = " — Token may be malformed or incomplete."
                st.markdown(f'<div class="card error"><div class="lbl">Decryption Failed</div><div class="val" style="color:var(--red)">{err}{hint}</div></div>', unsafe_allow_html=True)
                st.toast("Decryption failed ❌", icon="❗")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3.5rem;padding:1.5rem 0;border-top:1px solid var(--border)">
  <div style="font-family:'Share Tech Mono',monospace;font-size:0.62rem;color:var(--muted);letter-spacing:0.22em">
    CIPHERCORE · 10-ALGORITHM SUITE · AES · CHACHA20 · 3DES · SCRYPT · PBKDF2 · NO DATA STORED
  </div>
  <div style="font-size:0.62rem;color:#1e2a38;margin-top:0.3rem">
    All cryptographic operations run locally in memory · Keys never leave this session
  </div>
</div>
""", unsafe_allow_html=True)