"""
CodeAlpha_LanguageTranslator
An aesthetic Language Translation Tool built with Streamlit.

Run with:  streamlit run app.py
"""

import streamlit as st
from deep_translator import GoogleTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES as RAW_LANGUAGES
from gtts import gTTS
import io

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌐",
    layout="centered"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap');

    .stApp {
        background: radial-gradient(ellipse at top, #FDF4EE 0%, #F7E9DE 100%);
        font-family: 'DM Sans', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ---------- HEADER ---------- */
    .eyebrow {
        text-align: center;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #B8785F;
        margin-bottom: 0.3rem;
    }

    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.7rem;
        font-weight: 800;
        color: #3D2B24;
        text-align: center;
        margin-bottom: 0.3rem;
        letter-spacing: 0.2px;
    }

    .hero-rule {
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #C97B63, #8B9A7D);
        margin: 0 auto 1.6rem auto;
        border-radius: 3px;
    }

    /* ---------- TICKET-STYLE CARD ---------- */
    .ticket-card {
        background: #FFFDFB;
        border-radius: 22px;
        padding: 1.6rem 1.8rem 1rem 1.8rem;
        box-shadow: 0 10px 32px rgba(140, 95, 70, 0.14);
        border: 1px solid #F0DED0;
        position: relative;
        margin-bottom: 1.4rem;
    }

    .ticket-perforation {
        border-bottom: 2px dashed #E3CBB8;
        margin: 1rem 0 1.2rem 0;
        position: relative;
    }
    .ticket-perforation::before, .ticket-perforation::after {
        content: '';
        position: absolute;
        top: -10px;
        width: 20px;
        height: 20px;
        background: radial-gradient(circle, #F7E9DE 60%, transparent 60%);
        border-radius: 50%;
    }
    .ticket-perforation::before { left: -1.8rem; }
    .ticket-perforation::after { right: -1.8rem; }

    label, .stSelectbox label, .stTextArea label {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 700 !important;
        color: #A9765F !important;
        font-size: 0.72rem !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }

    .stSelectbox > div > div {
        background-color: #FFFBF8;
        border-radius: 14px !important;
        border: 1.5px solid #EFDBCB !important;
    }

    .stTextArea textarea {
        background-color: #FFFBF8;
        border-radius: 14px !important;
        border: 1.5px solid #EFDBCB !important;
        font-family: 'DM Sans', sans-serif;
        color: #3D2B24;
    }

    /* Swap button - the signature element */
    div[data-testid="column"]:has(button[kind="secondary"]) {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    div.stButton > button {
        font-family: 'DM Sans', sans-serif;
        font-weight: 700;
        border-radius: 30px;
        border: none;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #C97B63 0%, #B8654C 100%);
        color: white;
        padding: 0.65rem 2rem;
        font-size: 0.95rem;
        letter-spacing: 0.3px;
        box-shadow: 0 6px 18px rgba(201, 123, 99, 0.4);
        width: 100%;
        transition: all 0.2s ease;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 8px 22px rgba(201, 123, 99, 0.5);
        transform: translateY(-1px);
    }

    div.stButton > button[kind="secondary"] {
        background: #FFFFFF;
        color: #8B9A7D;
        border: 1.5px solid #D7E0CC;
        width: 44px;
        height: 44px;
        padding: 0;
        font-size: 1.1rem;
        box-shadow: 0 4px 10px rgba(139, 154, 125, 0.2);
    }
    div.stButton > button[kind="secondary"]:hover {
        background: #F1F5EB;
        border-color: #8B9A7D;
    }

    .result-label {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 1.25rem;
        color: #3D2B24;
        margin-bottom: 0.7rem;
    }

    .result-box {
        background: linear-gradient(135deg, #F6EFE8 0%, #F1EAE0 100%);
        border-left: 4px solid #8B9A7D;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        font-family: 'DM Sans', sans-serif;
        color: #3D2B24;
        font-size: 1.08rem;
        line-height: 1.65;
    }

    .footer-note {
        text-align: center;
        color: #C4A794;
        font-size: 0.78rem;
        margin-top: 1.6rem;
        letter-spacing: 0.3px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- LANGUAGE SETUP ----------
INDIAN_LANGUAGE_KEYS = [
    'hindi', 'bengali', 'punjabi', 'marathi', 'gujarati', 'tamil', 'telugu',
    'kannada', 'malayalam', 'urdu', 'odia (oriya)', 'assamese', 'sindhi',
    'konkani', 'sanskrit', 'nepali', 'maithili', 'dogri', 'bhojpuri',
    'meiteilon (manipuri)'
]

lang_names = {name.title(): code for name, code in RAW_LANGUAGES.items()}
indian_display_names = [name.title() for name in INDIAN_LANGUAGE_KEYS if name in RAW_LANGUAGES]
other_display_names = sorted(name for name in lang_names.keys() if name not in indian_display_names)
ordered_languages = [f"🇮🇳 {name}" for name in indian_display_names] + other_display_names

def resolve_lang(display_name):
    return lang_names[display_name.replace("🇮🇳 ", "")]

# ---------- SESSION STATE DEFAULTS ----------
if "source_choice" not in st.session_state:
    st.session_state.source_choice = "Auto Detect"
if "target_choice" not in st.session_state:
    st.session_state.target_choice = "🇮🇳 Hindi" if "🇮🇳 Hindi" in ordered_languages else ordered_languages[0]

def swap_languages():
    if st.session_state.source_choice != "Auto Detect":
        st.session_state.source_choice, st.session_state.target_choice = (
            st.session_state.target_choice, st.session_state.source_choice
        )

# ---------- HEADER ----------
st.markdown('<div class="eyebrow">AI Translation Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">🌐 Language Translator</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-rule"></div>', unsafe_allow_html=True)

# ---------- TICKET CARD ----------
st.markdown('<div class="ticket-card">', unsafe_allow_html=True)

col1, col_swap, col2 = st.columns([5, 1, 5])

with col1:
    source_lang = st.selectbox(
        "From",
        options=["Auto Detect"] + ordered_languages,
        key="source_choice"
    )

with col_swap:
    st.write("")
    st.button("⇄", key="swap_btn", on_click=swap_languages, type="secondary")

with col2:
    target_lang = st.selectbox(
        "To",
        options=ordered_languages,
        key="target_choice"
    )

st.markdown('<div class="ticket-perforation"></div>', unsafe_allow_html=True)

input_text = st.text_area("Enter text to translate", height=140, placeholder="Type something...")
translate_clicked = st.button("Translate ✨", type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- TRANSLATION LOGIC ----------
if translate_clicked:
    if not input_text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            src_code = "auto" if source_lang == "Auto Detect" else resolve_lang(source_lang)
            dest_code = resolve_lang(target_lang)

            translated = GoogleTranslator(source=src_code, target=dest_code).translate(input_text)

            st.session_state["translated_text"] = translated
            st.session_state["target_code"] = dest_code

        except Exception as e:
            st.error(f"Translation failed: {e}")

# ---------- DISPLAY RESULT ----------
if "translated_text" in st.session_state:
    st.markdown('<div class="ticket-card">', unsafe_allow_html=True)
    st.markdown('<div class="result-label">Translated Text</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-box">{st.session_state["translated_text"]}</div>', unsafe_allow_html=True)

    st.write("")
    col_a, col_b = st.columns(2)

    with col_a:
        st.code(st.session_state["translated_text"], language=None)
        st.caption("👆 Click the copy icon in the top-right of the box above")

    with col_b:
        if st.button("🔊 Listen to translation"):
            try:
                tts = gTTS(text=st.session_state["translated_text"], lang=st.session_state["target_code"])
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                st.audio(audio_buffer, format="audio/mp3")
            except Exception as e:
                st.error(f"Could not generate audio: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer-note">Built for CodeAlpha AI Internship — Task 1: Language Translation Tool</div>', unsafe_allow_html=True)