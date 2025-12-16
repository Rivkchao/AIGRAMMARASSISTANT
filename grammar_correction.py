import streamlit as st
import re
import requests

API_KEY = st.secrets["OPENAI_API_KEY"]

def correct_grammar_openai(text):
    """
    Uses OpenAI (via OpenRouter) to correct grammar and explain changes.
    """
    prompt = f"""
You are an expert English grammar assistant. **ONLY process and correct the grammar of English sentences. If the input sentence is not English, return the original sentence in 'corrected' and an explanation 'Input is not an English sentence and cannot be corrected.'**
Correct the grammar of this sentence and explain the changes briefly.

Sentence: {text}

Respond in JSON with two fields:
- corrected: the corrected version
- explanation: short explanation (in Indonesian) of the changes made.
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                             headers=headers, json=data)
    result = response.json()
    text_out = result.get("choices", [{}])[0].get("message", {}).get("content", "")

    corrected = re.search(r'"corrected"\s*:\s*"([^"]+)"', text_out)
    explanation = re.search(r'"explanation"\s*:\s*"([^"]+)"', text_out)

    return (
        corrected.group(1) if corrected else text,
        explanation.group(1) if explanation else "No explanation provided.",
    )
