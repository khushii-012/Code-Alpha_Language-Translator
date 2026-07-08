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
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap');

    html, body, .stApp, [class^="st-"] {
        color: #1E5A54;
    }

    .stApp {
        background: linear-gradient(180deg, #E8F6F3 0%, #DCF0EB 100%) !important;
        font-family: 'DM Sans', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ---------- HEADER ---------- */
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2.3rem;
        font-weight: 800;
        text-align: center;
        color: #1E5A54 !important;
        margin-bottom: 0.6rem;
    }

    .lang-pair-pill {
        display: block;
        width: fit-content;
        margin: 0 auto 1.6rem auto;
        background: #1E5A54;
        color: #FFFFFF !important;
        font-family: 'DM Sans', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        padding: 0.5rem 1.4rem;
        border-radius: 30px;
        letter-spacing: 0.3px;
        box-shadow: 0 6px 16px rgba(30, 90, 84, 0.25);
    }

    /* ---------- SOURCE CARD (real container, properly scoped) ---------- */
    div[class*="st-key-source_card"] {
        background: #FFFFFF;
        border-radius: 22px;
        border-bottom-left-radius: 6px;
        padding: 1.3rem 1.6rem;
        box-shadow: 0 8px 24px rgba(30, 90, 84, 0.10);
        margin-bottom: 1.1rem;
    }
    div[class*="st-key-source_card"] * {
        color: #1E5A54 !important;
    }

    /* ---------- TARGET CARD (real container, properly scoped) ---------- */
    div[class*="st-key-target_card"] {
        background: #2BAFA0;
        border-radius: 22px;
        border-bottom-right-radius: 6px;
        padding: 1.3rem 1.6rem;
        box-shadow: 0 8px 24px rgba(30, 90, 84, 0.18);
        margin-bottom: 1.1rem;
    }

    .bubble-label {
        font-family: 'DM Sans', sans-serif;
        font-weight: 700 !important;
        font-size: 0.72rem !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 0.5rem;
        color: #2BAFA0 !important;
    }

    .bubble-label-target {
        font-family: 'DM Sans', sans-serif;
        font-weight: 700 !important;
        font-size: 0.72rem !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 0.5rem;
        color: #EAFBF8 !important;
    }

    .translated-text {
        font-size: 1.15rem !important;
        line-height: 1.6;
        font-weight: 500;
        color: #FFFFFF !important;
    }

    label, .stSelectbox label, .stTextArea label {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 700 !important;
        color: #2BAFA0 !important;
        font-size: 0.72rem !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }

    .stSelectbox > div > div {
        background-color: #F2FAF9 !important;
        border-radius: 14px !important;
        border: 1.5px solid #CFEEE8 !important;
    }
    .stSelectbox [data-baseweb="select"] * {
        color: #1E5A54 !important;
    }

    .stTextArea textarea {
        background-color: #F2FAF9 !important;
        border-radius: 14px !important;
        border: 1.5px solid #CFEEE8 !important;
        font-family: 'DM Sans', sans-serif;
        color: #1E5A54 !important;
    }

    /* Translate button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2BAFA0 0%, #1E5A54 100%) !important;
        color: white !important;
        border: none;
        border-radius: 30px;
        padding: 0.65rem 2rem;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.3px;
        box-shadow: 0 6px 18px rgba(30, 90, 84, 0.3);
        width: 100%;
        transition: all 0.2s ease;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 8px 22px rgba(30, 90, 84, 0.4);
        transform: translateY(-1px);
    }

    /* Swap icon button - scoped only to its own container */
    div[class*="st-key-swap_container"] div.stButton > button {
        background: #FFFFFF !important;
        color: #2BAFA0 !important;
        border: 2px solid #2BAFA0;
        border-radius: 50%;
        width: 44px;
        height: 44px;
        padding: 0;
        font-size: 1.15rem;
        font-weight: 700;
        box-shadow: 0 4px 10px rgba(43, 175, 160, 0.2);
    }
    div[class*="st-key-swap_container"] div.stButton > button:hover {
        background: #2BAFA0 !important;
        color: white !important;
    }
    div[class*="st-key-swap_container"] {
        display: flex;
        align-items: flex-end;
        justify-content: center;
        height: 100%;
        padding-bottom: 6px;
    }

    /* Speaker icon button - small round icon, scoped only to its own container */
    div[class*="st-key-listen_container"] div.stButton > button {
        background: rgba(255, 255, 255, 0.25) !important;
        color: white !important;
        border: 1.5px solid rgba(255, 255, 255, 0.6);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        padding: 0;
        font-size: 1.05rem;
    }
    div[class*="st-key-listen_container"] div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.4) !important;
    }

    .reading-aid {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        margin-top: 0.8rem;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.92rem;
        line-height: 1.5;
    }
    .reading-aid, .reading-aid * {
        color: #1E5A54 !important;
    }

    .reading-aid-label {
        font-weight: 700 !important;
        font-size: 0.68rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.25rem;
        color: #2BAFA0 !important;
    }

    .footer-note {
        text-align: center;
        color: #4C8A82 !important;
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

def clean_name(display_name):
    return display_name.replace("🇮🇳 ", "")

SCRIPT_MAP = {
    'pa': sanscript.GURMUKHI,
    'bn': sanscript.BENGALI,
    'as': sanscript.BENGALI,
    'gu': sanscript.GUJARATI,
    'kn': sanscript.KANNADA,
    'ml': sanscript.MALAYALAM,
    'or': sanscript.ORIYA,
    'ta': sanscript.TAMIL,
    'te': sanscript.TELUGU,
}

def get_reading_aid(text, target_code):
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
st.markdown('<div class="hero-title">🌐 Language Translator</div>', unsafe_allow_html=True)

pair_label = f"{clean_name(st.session_state.source_choice)}  ⇄  {clean_name(st.session_state.target_choice)}"
st.markdown(f'<div class="lang-pair-pill">{pair_label}</div>', unsafe_allow_html=True)

# ---------- SOURCE CARD ----------
with st.container(key="source_card"):
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

    input_text = st.text_area("Enter text to translate", height=130, placeholder="Type something...", label_visibility="collapsed")
    translate_clicked = st.button("Translate ✨", type="primary")

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

# ---------- TARGET CARD (result) ----------
if "translated_text" in st.session_state:
    with st.container(key="target_card"):
        col_t1, col_t2 = st.columns([6, 1])
        with col_t1:
            st.markdown(f'<div class="bubble-label-target">{clean_name(st.session_state.target_choice)}</div>', unsafe_allow_html=True)
        with col_t2:
            with st.container(key="listen_container"):
                listen_clicked = st.button("🔊", key="listen_btn")

        st.markdown(f'<div class="translated-text">{st.session_state["translated_text"]}</div>', unsafe_allow_html=True)

        reading_aid = get_reading_aid(st.session_state["translated_text"], st.session_state["target_code"])
        if reading_aid:
            st.markdown(
                f'<div class="reading-aid"><div class="reading-aid-label">📖 Read as (Hindi script)</div>{reading_aid}</div>',
                unsafe_allow_html=True
            )

    if listen_clicked:
        try:
            tts = gTTS(text=st.session_state["translated_text"], lang=st.session_state["target_code"])
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            st.audio(audio_buffer, format="audio/mp3")
        except Exception as e:
            st.error(f"Could not generate audio: {e}")

    with st.expander("📋 Copy translated text"):
        st.code(st.session_state["translated_text"], language=None)

st.markdown('<div class="footer-note">Built for CodeAlpha AI Internship — Task 1: Language Translation Tool</div>', unsafe_allow_html=True)