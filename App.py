"""
CodeAlpha_LanguageTranslator
A vibrant, aesthetic Language Translation Tool built with Streamlit.

Run with:  streamlit run app.py
"""

import streamlit as st
from deep_translator import GoogleTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES as RAW_LANGUAGES
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
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
        background: linear-gradient(160deg, #FDEBF3 0%, #F3E8FB 35%, #FFF3E0 70%, #E6F7F1 100%);
        font-family: 'DM Sans', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ---------- HEADER ---------- */
    .eyebrow {
        text-align: center;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #C44FA0;
        margin-bottom: 0.3rem;
    }

    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.3rem;
        letter-spacing: 0.2px;
        background: linear-gradient(90deg, #D6336C 0%, #F5A623 45%, #2BB6A3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-rule {
        width: 70px;
        height: 4px;
        background: linear-gradient(90deg, #D6336C, #F5A623, #2BB6A3);
        margin: 0 auto 1.6rem auto;
        border-radius: 4px;
    }

    /* ---------- TICKET-STYLE CARD ---------- */
    .ticket-card {
        background: #FFFFFF;
        border-radius: 22px;
        padding: 1.6rem 1.8rem 1rem 1.8rem;
        box-shadow: 0 12px 32px rgba(214, 51, 108, 0.16);
        border: 1px solid #F6D9EA;
        position: relative;
        margin-bottom: 1.4rem;
    }

    .ticket-perforation {
        border-bottom: 2px dashed #E8C4DC;
        margin: 1rem 0 1.2rem 0;
        position: relative;
    }
    .ticket-perforation::before, .ticket-perforation::after {
        content: '';
        position: absolute;
        top: -10px;
        width: 20px;
        height: 20px;
        background: radial-gradient(circle, #F3E8FB 60%, transparent 60%);
        border-radius: 50%;
    }
    .ticket-perforation::before { left: -1.8rem; }
    .ticket-perforation::after { right: -1.8rem; }

    label, .stSelectbox label, .stTextArea label {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 700 !important;
        color: #C44FA0 !important;
        font-size: 0.72rem !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }

    .stSelectbox > div > div {
        background-color: #FFF8FC;
        border-radius: 14px !important;
        border: 1.5px solid #F3D3E8 !important;
    }

    .stTextArea textarea {
        background-color: #FFF8FC;
        border-radius: 14px !important;
        border: 1.5px solid #F3D3E8 !important;
        font-family: 'DM Sans', sans-serif;
        color: #3D1F33;
    }

    /* Translate button (primary) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #D6336C 0%, #F5A623 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.65rem 2rem;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.3px;
        box-shadow: 0 6px 18px rgba(214, 51, 108, 0.35);
        width: 100%;
        transition: all 0.2s ease;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 8px 22px rgba(214, 51, 108, 0.5);
        transform: translateY(-1px);
    }

    /* Swap button - scoped ONLY to its container, so it never leaks onto other buttons */
    div[class*="st-key-swap_container"] div.stButton > button {
        background: #FFFFFF;
        color: #2BB6A3;
        border: 2px solid #2BB6A3;
        border-radius: 50%;
        width: 46px;
        height: 46px;
        padding: 0;
        font-size: 1.2rem;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(43, 182, 163, 0.25);
    }
    div[class*="st-key-swap_container"] div.stButton > button:hover {
        background: #2BB6A3;
        color: white;
    }
    div[class*="st-key-swap_container"] {
        display: flex;
        align-items: flex-end;
        justify-content: center;
        height: 100%;
        padding-bottom: 6px;
    }

    /* Listen button - scoped ONLY to its container, distinct teal pill */
    div[class*="st-key-listen_container"] div.stButton > button {
        background: linear-gradient(135deg, #2BB6A3 0%, #1F9385 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.55rem 1.4rem;
        font-weight: 700;
        font-size: 0.9rem;
        width: 100%;
        box-shadow: 0 6px 16px rgba(43, 182, 163, 0.35);
    }
    div[class*="st-key-listen_container"] div.stButton > button:hover {
        box-shadow: 0 8px 20px rgba(43, 182, 163, 0.45);
        transform: translateY(-1px);
    }

    .result-label {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 1.25rem;
        color: #3D1F33;
        margin-bottom: 0.7rem;
    }

    .result-box {
        background: linear-gradient(135deg, #FDEBF3 0%, #FFF3E0 100%);
        border-left: 4px solid #D6336C;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        font-family: 'DM Sans', sans-serif;
        color: #3D1F33;
        font-size: 1.08rem;
        line-height: 1.65;
        margin-bottom: 0.8rem;
    }

    .reading-aid {
        background: #E6F7F1;
        border-left: 4px solid #2BB6A3;
        border-radius: 12px;
        padding: 0.9rem 1.5rem;
        font-family: 'DM Sans', sans-serif;
        color: #1F6B5F;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .reading-aid-label {
        font-weight: 700;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #2BB6A3;
        margin-bottom: 0.3rem;
    }

    .footer-note {
        text-align: center;
        color: #C48FB0;
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

# Language codes whose native script can be transliterated into Devanagari
# so Hindi readers can sound out the translation
SCRIPT_MAP = {
    'pa': sanscript.GURMUKHI,
    'bn': sanscript.BENGALI,
    'as': sanscript.BENGALI,      # Assamese shares the Bengali-Assamese script
    'gu': sanscript.GUJARATI,
    'kn': sanscript.KANNADA,
    'ml': sanscript.MALAYALAM,
    'or': sanscript.ORIYA,
    'ta': sanscript.TAMIL,
    'te': sanscript.TELUGU,
}

def get_reading_aid(text, target_code):
    """Return a Devanagari (Hindi-script) reading aid if the target script
    is a different Indic script we can transliterate. Returns None otherwise."""
    scheme = SCRIPT_MAP.get(target_code)
    if not scheme:
        return None
    try:
        return transliterate(text, scheme, sanscript.DEVANAGARI)
    except Exception:
        return None

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
    with st.container(key="swap_container"):
        st.button("⇄", key="swap_btn", on_click=swap_languages)

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

    reading_aid = get_reading_aid(st.session_state["translated_text"], st.session_state["target_code"])
    if reading_aid:
        st.markdown(
            f'<div class="reading-aid"><div class="reading-aid-label">📖 Read as (Hindi script)</div>{reading_aid}</div>',
            unsafe_allow_html=True
        )

    st.write("")
    col_a, col_b = st.columns(2)

    with col_a:
        st.code(st.session_state["translated_text"], language=None)
        st.caption("👆 Click the copy icon in the top-right of the box above")

    with col_b:
        with st.container(key="listen_container"):
            listen_clicked = st.button("🔊 Listen to translation")
        if listen_clicked:
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