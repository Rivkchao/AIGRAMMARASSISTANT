import re
import pandas as pd
import requests
from tense_detection import detect_tense_openai

import streamlit as st
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

def analyze_svoa(text):
    words = text.split()

    # Original rule-based extraction
    subjects = list(set([w for w in words if w.lower() in ["i","you","he","she","it","we","they"]]))
    verbs = list(set([w for w in words if re.match(r"(am|is|are|was|were|do|does|did|have|has|had|will|'m|'re|'s|\w+ed|\w+s)", w.lower())]))
    objects = list(set([w for w in words if w.lower() in ["me","him","her","us","them","it","you","that"]]))
    adverbs = list(set([w for w in words if w.lower() in [
        "yesterday","today","tomorrow","now","after","before","then","later","soon","already","still","yet"
    ]]))

    tense = detect_tense_openai(text)

    # Ask LLM for nouns + pronouns
    llm_prompt = f"""
Extract all nouns and pronouns from the following sentence.
Return ONLY a JSON dictionary like:
{{
  "nouns": ["..."],
  "pronouns": ["..."]
}}

Sentence: "{text}"
"""

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Return clean JSON only."},
            {"role": "user", "content": llm_prompt}
        ]
    }

    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers)
        out = r.json()["choices"][0]["message"]["content"]
        # Safe-ish eval
        parsed = eval(out)
        nouns = parsed.get("nouns", [])
        pronouns = parsed.get("pronouns", [])
    except:
        nouns = []
        pronouns = []

    df = pd.DataFrame({
        "Sentence Structure": [
            "Subject (Subjek)", "Verb (Predikat)", "Object (Objek)",
            "Adverbial (Keterangan)", "Noun (Kata Benda)",
            "Pronoun (Kata Ganti)", "Tense"
        ],
        "Result": [
            ", ".join(subjects),
            " ".join(verbs),
            ", ".join(objects),
            ", ".join(adverbs),
            ", ".join(nouns),
            ", ".join(pronouns),
            tense
        ]
    })

    return df, {"S": subjects, "P": verbs, "O": objects, "K": adverbs}
