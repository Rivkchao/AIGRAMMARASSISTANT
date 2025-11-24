import streamlit as st
import requests

OPENROUTER_API_KEY = st.secrets["OPENAI_API_KEY"]

def detect_tense_openai(text):
    """
    Uses OpenAI (via OpenRouter) to detect the tense of a sentence.
    """
    if not text.strip():
        return "Unknown"

    prompt = f"""
You are an expert English linguist.
Identify the tense of the following sentence.
Answer with only the tense name (e.g., Present Simple, Past Perfect, Future Continuous). If multiple tenses are found, separate them with a comma.

Sentence: {text}
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        tense_raw = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        tenses_list = tense_raw.split(',')
        unique_tenses = set(t.strip() for t in tenses_list if t.strip())
        clean_tense_string = ", ".join(sorted(list(unique_tenses)))

        return clean_tense_string or "Unknown"

    except requests.exceptions.RequestException as e:
        print(f"Error during API call for tense detection: {e}")
        return "Detection Error"