"""
CodeAlpha_LanguageTranslator
A simple, clean Language Translation Tool built with Streamlit.

Run with:  streamlit run app.py
"""

import streamlit as st
from deep_translator import GoogleTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES as LANGUAGES
from gtts import gTTS
import io

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌐",
    layout="centered"
)

# ---------- CUSTOM CSS (soft, clean aesthetic) ----------
st.markdown("""
    <style>
    .main {
        background-color: #FFF9F5;
    }
    h1 {
        font-family: 'Georgia', serif;
        color: #4A3F35;
        text-align: center;
    }
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #E8D5C4;
    }
    div.stButton > button {
        background-color: #D9A79C;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background-color: #C68F82;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- INIT ----------
lang_names = {name.title(): code for name, code in LANGUAGES.items()}  # e.g. "English": "en"

st.title("🌐 Language Translator")
st.caption("Type text, pick your languages, and translate instantly.")

# ---------- LAYOUT ----------
col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox(
        "Source language",
        options=["Auto Detect"] + sorted(lang_names.keys()),
        index=0
    )

with col2:
    target_lang = st.selectbox(
        "Target language",
        options=sorted(lang_names.keys()),
        index=sorted(lang_names.keys()).index("English") if "English" in lang_names else 0
    )

input_text = st.text_area("Enter text to translate", height=150, placeholder="Type something...")

translate_clicked = st.button("Translate ✨")

# ---------- TRANSLATION LOGIC ----------
if translate_clicked:
    if not input_text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            src_code = "auto" if source_lang == "Auto Detect" else lang_names[source_lang]
            dest_code = lang_names[target_lang]

            translated = GoogleTranslator(source=src_code, target=dest_code).translate(input_text)

            st.session_state["translated_text"] = translated
            st.session_state["detected_lang"] = src_code  # deep-translator doesn't return detected lang directly

        except Exception as e:
            st.error(f"Translation failed: {e}")

# ---------- DISPLAY RESULT ----------
if "translated_text" in st.session_state:
    st.markdown("### Translated Text")
    st.success(st.session_state["translated_text"])

    col_a, col_b = st.columns(2)

    with col_a:
        st.code(st.session_state["translated_text"], language=None)
        st.caption("👆 Click the copy icon in the top-right of the box above")

    with col_b:
        if st.button("🔊 Listen to translation"):
            try:
                tts = gTTS(text=st.session_state["translated_text"], lang=lang_names[target_lang])
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                st.audio(audio_buffer, format="audio/mp3")
            except Exception as e:
                st.error(f"Could not generate audio: {e}")

st.markdown("---")
st.caption("Built for CodeAlpha AI Internship — Task 1: Language Translation Tool")