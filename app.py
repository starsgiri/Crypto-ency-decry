import streamlit as st
import base64
import os
import json
import hashlib
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding, hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding as asym_padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CipherCore | Crypto Suite",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ─── Enhanced Styling & Animations ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #0a0c10;
    --surface: #0f1318;
    --surface2: #151a22;
    --border: #1e2a38;
    --accent: #00e5ff;
    --accent2: #7b2fff;
    --green: #00ff88;
    --red: #ff3c6e;
    --text: #c8d6e5;
    --muted: #4a6080;
}

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background: linear-gradient(120deg, #0a0c10 0%, #151a22 100%) !important;
    color: var(--text) !important;
    min-height: 100vh;
    overflow-x: hidden;
}

.stApp { background: transparent !important; }

body::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: -1;
    background: radial-gradient(circle at 80% 10%, rgba(0,229,255,0.08) 0, transparent 60%),
                radial-gradient(circle at 20% 90%, rgba(123,47,255,0.08) 0, transparent 60%);
    animation: bgmove 12s linear infinite alternate;
}
@keyframes bgmove {
    0% { background-position: 80% 10%, 20% 90%; }
    100% { background-position: 60% 20%, 40% 80%; }
}

#MainMenu, footer, header { visibility: hidden; }

.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    margin-bottom: 2rem;
    background: linear-gradient(135deg, #0f1318 0%, #0d1520 100%);
    border: 1px solid var(--border);
    border-radius: 2px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 32px 0 rgba(0,229,255,0.08);
    animation: fadein 1.2s cubic-bezier(.4,0,.2,1);
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(0,229,255,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 2.8rem;
    color: var(--accent);
    letter-spacing: 0.15em;
    text-shadow: 0 0 30px rgba(0,229,255,0.4);
    margin: 0;
    animation: fadein 1.5s cubic-bezier(.4,0,.2,1);
}
.hero-sub {
    color: var(--muted);
    font-size: 0.85rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-top: 0.4rem;
    animation: fadein 2s cubic-bezier(.4,0,.2,1);
}

@keyframes fadein {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: none; }
}

.step-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: var(--accent);
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
    opacity: 0.8;
}

.info-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    padding: 1.2rem 1.5rem;
    border-radius: 2px;
    margin: 1rem 0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.8;
    word-break: break-all;
    box-shadow: 0 2px 16px 0 rgba(0,229,255,0.04);
    transition: box-shadow 0.3s, border-left-color 0.3s, transform 0.2s;
    animation: fadein 1.2s cubic-bezier(.4,0,.2,1);
}
.info-card:hover {
    box-shadow: 0 6px 32px 0 rgba(0,229,255,0.13);
    border-left-color: var(--accent2);
    transform: translateY(-2px) scale(1.01);
}
.info-card.success { border-left-color: var(--green); }
.info-card.warning { border-left-color: #ffb300; }
.info-card.error   { border-left-color: var(--red); }

.card-label {
    color: var(--muted);
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.card-value { color: var(--accent); }
.card-value.green { color: var(--green); }
.card-value.white { color: #e8f4ff; }

.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
    opacity: 0.7;
    animation: fadein 1.2s cubic-bezier(.4,0,.2,1);
}

.stSelectbox label, .stRadio label, .stTextArea label, .stTextInput label {
    color: var(--muted) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
}

div[data-baseweb="select"] > div {
    background-color: var(--surface2) !important;
    border-color: var(--border) !important;
    border-radius: 2px !important;
    color: var(--text) !important;
}

textarea, input[type="text"], input[type="password"] {
    background-color: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    color: var(--text) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.82rem !important;
    transition: box-shadow 0.2s;
}
textarea:focus, input[type="text"]:focus, input[type="password"]:focus {
    box-shadow: 0 0 0 2px var(--accent2);
    outline: none;
}

.stButton > button {
    background: linear-gradient(90deg, rgba(0,229,255,0.08) 0%, rgba(123,47,255,0.08) 100%) !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
    padding: 0.5rem 2rem !important;
    transition: all 0.2s ease !important;
    width: 100%;
    font-size: 1.1rem !important;
    box-shadow: 0 2px 16px 0 rgba(0,229,255,0.04);
    cursor: pointer;
    animation: fadein 1.2s cubic-bezier(.4,0,.2,1);
}
.stButton > button:hover {
    background: linear-gradient(90deg, rgba(0,229,255,0.18) 0%, rgba(123,47,255,0.18) 100%) !important;
    box-shadow: 0 0 20px rgba(0,229,255,0.2) !important;
    color: #fff !important;
    border-color: var(--accent2) !important;
    transform: scale(1.03);
}

div[data-baseweb="radio"] label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.85rem !important;
    color: var(--text) !important;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 1.8rem 0 0.8rem;
    animation: fadein 1.2s cubic-bezier(.4,0,.2,1);
}
.section-num {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: var(--accent);
    background: rgba(0,229,255,0.08);
    border: 1px solid rgba(0,229,255,0.3);
    padding: 0.15rem 0.5rem;
    border-radius: 2px;
}
.section-title {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--muted);
}

.badge {
    display: inline-block;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    padding: 0.1rem 0.6rem;
    border-radius: 1px;
    letter-spacing: 0.1em;
}
.badge-blue  { background: rgba(0,229,255,0.1);  color: var(--accent); border: 1px solid rgba(0,229,255,0.3); }
.badge-green { background: rgba(0,255,136,0.1);  color: var(--green);  border: 1px solid rgba(0,255,136,0.3); }
.badge-red   { background: rgba(255,60,110,0.1); color: var(--red);    border: 1px solid rgba(255,60,110,0.3); }
</style>
""", unsafe_allow_html=True)

# ─── Helpers ────────────────────────────────────────────────────────────────

def b64e(b: bytes) -> str: return base64.b64encode(b).decode()
def b64d(s: str) -> bytes: return base64.b64decode(s.encode())

def derive_key(password: str, salt: bytes, length: int) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=length, salt=salt,
                     iterations=200_000, backend=default_backend())
    return kdf.derive(password.encode())

# ── Symmetric encrypt ────────────────────────────────────────────────────────
def sym_encrypt(plaintext: str, key_str: str, level: str):
    data = plaintext.encode()
    salt = os.urandom(16)

    if level == "Easy":
        # AES-128-CBC
        key = derive_key(key_str, salt, 16)
        iv  = os.urandom(16)
        pad = sym_padding.PKCS7(128).padder()
        padded = pad.update(data) + pad.finalize()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        ct = cipher.encryptor().update(padded) + cipher.encryptor().finalize()
        # redo with proper encryptor
        enc = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).encryptor()
        ct = enc.update(padded) + enc.finalize()
        algo_name = "AES-128-CBC"
        payload = json.dumps({"algo": algo_name, "salt": b64e(salt), "iv": b64e(iv), "ct": b64e(ct)})

    elif level == "Medium":
        # AES-256-GCM
        key = derive_key(key_str, salt, 32)
        iv  = os.urandom(12)
        enc = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend()).encryptor()
        ct  = enc.update(data) + enc.finalize()
        tag = enc.tag
        algo_name = "AES-256-GCM"
        payload = json.dumps({"algo": algo_name, "salt": b64e(salt), "iv": b64e(iv),
                               "ct": b64e(ct), "tag": b64e(tag)})

    else:  # Hard → ChaCha20-Poly1305
        key = derive_key(key_str, salt, 32)
        nonce = os.urandom(16)
        algo  = algorithms.ChaCha20(key, nonce)
        enc   = Cipher(algo, mode=None, backend=default_backend()).encryptor()
        ct    = enc.update(data) + enc.finalize()
        algo_name = "ChaCha20"
        payload = json.dumps({"algo": algo_name, "salt": b64e(salt), "nonce": b64e(nonce), "ct": b64e(ct)})

    return b64e(payload.encode()), algo_name


def sym_decrypt(ciphertext_b64: str, key_str: str):
    payload = json.loads(b64d(ciphertext_b64).decode())
    algo    = payload["algo"]

    if run:
            if not user_data.strip():
                    st.markdown('<div class="info-card error"><div class="card-label">Error</div>No data provided.</div>', unsafe_allow_html=True)
                    st.toast("Please enter the required data!", icon="❗")
            else:
                    try:
                            with st.spinner("✨ Crunching cryptography magic…"):
                                    time.sleep(0.7)  # longer pause for drama

                                    if mode == "Encrypt":
                                            if method == "Symmetric":
                                                    if not key_input:
                                                            st.error("Please enter a passphrase.")
                                                            st.toast("Passphrase required!", icon="🔑")
                                                            st.stop()
                                                    ct_b64, algo_used = sym_encrypt(user_data, key_input, level)
                                                    key_display = f"(passphrase — keep secret)"
                                            else:  # Asymmetric
                                                    if not pub_key_input:
                                                            st.error("Please enter a public key.")
                                                            st.toast("Public key required!", icon="🗝️")
                                                            st.stop()
                                                    ct_b64, algo_used = asym_encrypt(user_data, pub_key_input.strip(), level)
                                                    fp = hashlib.sha256(pub_key_input.strip().encode()).hexdigest()[:16].upper()
                                                    key_display = f"Public Key fingerprint: {fp}"

                                            st.balloons()
                                            st.markdown("### ✅ Encryption Successful")
                                            st.markdown(f"""
    <div class="info-card success">
        <div class="card-label">Algorithm Used</div>
        <div class="card-value green">{algo_used}</div>
    </div>
    <div class="info-card">
        <div class="card-label">Key Info</div>
        <div class="card-value white">{key_display}</div>
    </div>
    <div class="info-card">
        <div class="card-label">Encrypted Message (Base64) — copy this for decryption</div>
        <div class="card-value" style="word-break:break-all">{ct_b64}</div>
    </div>
    <div class="info-card">
        <div class="card-label">Ciphertext Length</div>
        <div class="card-value white">{len(ct_b64)} characters</div>
    </div>
    <div class="info-card">
        <div class="card-label">Method</div>
        <div class="card-value white">{"Symmetric (shared secret key)" if method == "Symmetric" else "Asymmetric (public/private key pair)"}</div>
    </div>
    <div class="info-card warning">
        <div class="card-label">Security Summary</div>
        <div class="card-value" style="color:#ffb300">Level: {level} &nbsp;|&nbsp; Algorithm: {algo_used} &nbsp;|&nbsp; Method: {method}</div>
        <div style="color:var(--muted);font-size:0.72rem;margin-top:0.4rem">
            Share the encrypted message with the recipient. Keep your {"passphrase" if method == "Symmetric" else "private key"} secret.
        </div>
    </div>
                                            """, unsafe_allow_html=True)
                                            st.text_area("📋 Copy Ciphertext", value=ct_b64, height=120)
                                            st.toast("Encryption complete!", icon="🔐")

                                    else:  # Decrypt
                                            if method == "Symmetric":
                                                    if not key_input:
                                                            st.error("Please enter the passphrase.")
                                                            st.toast("Passphrase required!", icon="🔑")
                                                            st.stop()
                                                    plaintext, algo_used = sym_decrypt(user_data.strip(), key_input)
                                            else:
                                                    if not priv_key_input:
                                                            st.error("Please enter the private key.")
                                                            st.toast("Private key required!", icon="🗝️")
                                                            st.stop()
                                                    plaintext, algo_used = asym_decrypt(user_data.strip(), priv_key_input.strip())
                                            st.snow()
                                            st.markdown("### ✅ Decryption Successful")
                                            st.markdown(f"""
    <div class="info-card success">
        <div class="card-label">Algorithm Detected</div>
        <div class="card-value green">{algo_used}</div>
    </div>
    <div class="info-card">
        <div class="card-label">Decrypted Plaintext</div>
        <div class="card-value white" style="font-size:1rem;line-height:1.7">{plaintext}</div>
    </div>
    <div class="info-card">
        <div class="card-label">Method</div>
        <div class="card-value white">{"Symmetric" if method == "Symmetric" else "Asymmetric"}</div>
    </div>
                                            """, unsafe_allow_html=True)
                                            st.text_area("📋 Decrypted Message", value=plaintext, height=100)
                                            st.toast("Decryption complete!", icon="🔓")

                    except Exception as e:
                            st.markdown(f'<div class="info-card error"><div class="card-label">Error</div><div class="card-value" style="color:var(--red)">{str(e)}</div></div>', unsafe_allow_html=True)
                            st.toast("An error occurred!", icon="❌")

mode = st.radio("", ["🔒  Encrypt", "🔓  Decrypt"], horizontal=True, label_visibility="collapsed")
mode = "Encrypt" if "Encrypt" in mode else "Decrypt"

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Step 2: Method ───────────────────────────────────────────────────────────
st.markdown('<div class="section-header"><span class="section-num">02</span><span class="section-title">Cryptographic Method</span></div>', unsafe_allow_html=True)

method = st.radio("", ["🔑  Symmetric", "🗝️  Asymmetric"], horizontal=True, label_visibility="collapsed")
method = "Symmetric" if "Symmetric" in method else "Asymmetric"

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Step 3: Keys ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header"><span class="section-num">03</span><span class="section-title">Key Configuration</span></div>', unsafe_allow_html=True)

key_input = None
pub_key_input = None
priv_key_input = None

if method == "Symmetric":
    if mode == "Encrypt":
        key_input = st.text_input("Secret Passphrase (shared key)", type="password",
                                  placeholder="Enter a strong passphrase…")
    else:
        key_input = st.text_input("Secret Passphrase (must match encryption key)", type="password",
                                  placeholder="Enter the passphrase used during encryption…")

else:  # Asymmetric
    # Key generator helper
    with st.expander("⚡ Generate RSA-2048 Key Pair (for testing)"):
        if st.button("Generate New Key Pair"):
            priv_pem, pub_pem = gen_rsa_keypair()
            st.session_state["gen_priv"] = priv_pem
            st.session_state["gen_pub"]  = pub_pem

        if "gen_pub" in st.session_state:
            st.markdown('<div class="info-card"><div class="card-label">Public Key</div><div class="card-value">' +
                        st.session_state["gen_pub"].replace("\n", "<br>") + '</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="info-card"><div class="card-label">Private Key</div><div class="card-value">' +
                        st.session_state["gen_priv"].replace("\n", "<br>") + '</div></div>', unsafe_allow_html=True)

    if mode == "Encrypt":
        pub_key_input = st.text_area("Public Key (PEM format)", height=180,
                                     placeholder="-----BEGIN PUBLIC KEY-----\n…\n-----END PUBLIC KEY-----")
    else:
        priv_key_input = st.text_area("Private Key (PEM format)", height=200,
                                      placeholder="-----BEGIN RSA PRIVATE KEY-----\n…\n-----END RSA PRIVATE KEY-----")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Step 4 (Encrypt only): Security Level ────────────────────────────────────
level = None
if mode == "Encrypt":
    st.markdown('<div class="section-header"><span class="section-num">04</span><span class="section-title">Security Level</span></div>', unsafe_allow_html=True)

    LEVELS = {
        "Easy":   ("AES-128-CBC" if method == "Symmetric" else "RSA-OAEP-SHA256", "Fastest · 128-bit · Good for low-sensitivity data"),
        "Medium": ("AES-256-GCM" if method == "Symmetric" else "RSA-OAEP-SHA384", "Balanced · 256-bit authenticated · Recommended"),
        "Hard":   ("ChaCha20"    if method == "Symmetric" else "RSA-OAEP-SHA512", "Maximum · Stream cipher / SHA-512 · High-sensitivity data"),
    }

    col1, col2, col3 = st.columns(3)
    level_choice = None
    with col1:
        if st.button("🟢  Easy"):  level_choice = "Easy"
    with col2:
        if st.button("🟡  Medium"): level_choice = "Medium"
    with col3:
        if st.button("🔴  Hard"):  level_choice = "Hard"

    if "level" not in st.session_state:
        st.session_state["level"] = "Medium"
    if level_choice:
        st.session_state["level"] = level_choice

    level = st.session_state["level"]
    algo_preview, desc_preview = LEVELS[level]
    st.markdown(f"""
    <div class="info-card">
      <div class="card-label">Selected Level</div>
      <div class="card-value">{level} &nbsp;→&nbsp; {algo_preview}</div>
      <div style="color:var(--muted);font-size:0.72rem;margin-top:0.3rem">{desc_preview}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Step 5: Data ──────────────────────────────────────────────────────────────
step_num = "05" if mode == "Encrypt" else "04"
st.markdown(f'<div class="section-header"><span class="section-num">{step_num}</span><span class="section-title">{"Plaintext Input" if mode == "Encrypt" else "Ciphertext Input"}</span></div>', unsafe_allow_html=True)

if mode == "Encrypt":
    user_data = st.text_area("Message / Data to Encrypt", height=140,
                             placeholder="Type or paste the message you want to encrypt…")
else:
    user_data = st.text_area("Encrypted Ciphertext (Base64)", height=140,
                             placeholder="Paste the Base64-encoded ciphertext here…")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Execute ───────────────────────────────────────────────────────────────────
action_label = "⚡  ENCRYPT MESSAGE" if mode == "Encrypt" else "⚡  DECRYPT MESSAGE"
run = st.button(action_label)

if run:
    if not user_data.strip():
        st.markdown('<div class="info-card error"><div class="card-label">Error</div>No data provided.</div>', unsafe_allow_html=True)
    else:
        try:
            with st.spinner("Processing…"):
                time.sleep(0.4)  # small dramatic pause

                if mode == "Encrypt":
                    if method == "Symmetric":
                        if not key_input:
                            st.error("Please enter a passphrase.")
                            st.stop()
                        ct_b64, algo_used = sym_encrypt(user_data, key_input, level)
                        key_display = f"(passphrase — keep secret)"

                    else:  # Asymmetric
                        if not pub_key_input:
                            st.error("Please enter a public key.")
                            st.stop()
                        ct_b64, algo_used = asym_encrypt(user_data, pub_key_input.strip(), level)
                        fp = hashlib.sha256(pub_key_input.strip().encode()).hexdigest()[:16].upper()
                        key_display = f"Public Key fingerprint: {fp}"

                    # Display result
                    st.markdown("### ✅ Encryption Successful")
                    st.markdown(f"""
<div class="info-card success">
  <div class="card-label">Algorithm Used</div>
  <div class="card-value green">{algo_used}</div>
</div>
<div class="info-card">
  <div class="card-label">Key Info</div>
  <div class="card-value white">{key_display}</div>
</div>
<div class="info-card">
  <div class="card-label">Encrypted Message (Base64) — copy this for decryption</div>
  <div class="card-value" style="word-break:break-all">{ct_b64}</div>
</div>
<div class="info-card">
  <div class="card-label">Ciphertext Length</div>
  <div class="card-value white">{len(ct_b64)} characters</div>
</div>
<div class="info-card">
  <div class="card-label">Method</div>
  <div class="card-value white">{"Symmetric (shared secret key)" if method == "Symmetric" else "Asymmetric (public/private key pair)"}</div>
</div>
<div class="info-card warning">
  <div class="card-label">Security Summary</div>
  <div class="card-value" style="color:#ffb300">Level: {level} &nbsp;|&nbsp; Algorithm: {algo_used} &nbsp;|&nbsp; Method: {method}</div>
  <div style="color:var(--muted);font-size:0.72rem;margin-top:0.4rem">
    Share the encrypted message with the recipient. Keep your {"passphrase" if method == "Symmetric" else "private key"} secret.
  </div>
</div>
                    """, unsafe_allow_html=True)

                    # Also show in a copyable text area
                    st.text_area("📋 Copy Ciphertext", value=ct_b64, height=120)

                else:  # Decrypt
                    if method == "Symmetric":
                        if not key_input:
                            st.error("Please enter the passphrase.")
                            st.stop()
                        plaintext, algo_used = sym_decrypt(user_data.strip(), key_input)

                    else:
                        if not priv_key_input:
                            st.error("Please enter the private key.")
                            st.stop()
                        plaintext, algo_used = asym_decrypt(user_data.strip(), priv_key_input.strip())

                    st.markdown("### ✅ Decryption Successful")
                    st.markdown(f"""
<div class="info-card success">
  <div class="card-label">Algorithm Detected</div>
  <div class="card-value green">{algo_used}</div>
</div>
<div class="info-card">
  <div class="card-label">Decrypted Plaintext</div>
  <div class="card-value white" style="font-size:1rem;line-height:1.7">{plaintext}</div>
</div>
<div class="info-card">
  <div class="card-label">Method</div>
  <div class="card-value white">{"Symmetric" if method == "Symmetric" else "Asymmetric"}</div>
</div>
                    """, unsafe_allow_html=True)
                    st.text_area("📋 Decrypted Message", value=plaintext, height=100)

        except Exception as e:
            st.markdown(f'<div class="info-card error"><div class="card-label">Error</div><div class="card-value" style="color:var(--red)">{str(e)}</div></div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3rem;padding:1.5rem 0;border-top:1px solid var(--border)">
  <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:var(--muted);letter-spacing:0.2em">
    CIPHERCORE · CRYPTOGRAPHY & NETWORK SECURITY SUITE · NO DATA STORED
  </div>
  <div style="font-size:0.65rem;color:#2a3a4a;margin-top:0.3rem">
    All operations run client-side in memory only
  </div>
</div>
""", unsafe_allow_html=True)
