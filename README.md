# 🌐 Language Translator

A simple, clean web app that lets users enter text, choose a source and target language, and get an instant translation — with optional text-to-speech playback.

Built for the **CodeAlpha AI Internship — Task 1: Language Translation Tool**.

## Features

- Text input box for entering content to translate
- Dropdown selectors for source language (with Auto Detect) and target language
- Translation powered by `deep-translator` (uses Google Translate under the hood, no API key needed)
- Text-to-speech playback of the translated text using `gTTS`
- Copyable output box
- Clean, minimal UI styled with custom CSS

## Tech Stack

- **Frontend/UI:** Streamlit
- **Translation Engine:** `deep-translator` (Google Translate backend)
- **Text-to-Speech:** `gTTS` (Google Text-to-Speech)

## How to Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/khushii-012/CodeAlpha_LanguageTranslator.git
   cd CodeAlpha_LanguageTranslator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Open the local URL Streamlit gives you (usually `http://localhost:8501`) in your browser.

## How It Works

1. User types text into the input box.
2. User selects a source language (or leaves it on Auto Detect) and a target language.
3. On clicking **Translate**, the app sends the text to Google Translate via the `deep-translator` library.
4. The translated text is displayed on screen, with an optional "Listen" button that converts the translation to speech using `gTTS`.

## Notes

- Requires an active internet connection since translation happens via an external API.
- `deep-translator` was chosen over `googletrans` because `googletrans` has known compatibility issues with recent Python/httpx versions.

## Author

Khushi — built as part of the CodeAlpha Artificial Intelligence Internship.