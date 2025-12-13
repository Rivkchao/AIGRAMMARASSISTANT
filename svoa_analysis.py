import os
import re
import json
from typing import Dict, List, Tuple
import pandas as pd
import requests
<<<<<<< HEAD

API_KEY = os.getenv("OPENAI_API_KEY")


def analyze_svoa(text: str) -> Tuple[pd.DataFrame, Dict[str, List[str]]]:
    """
    Analyze the sentence structure (SVOA), Noun/Pronoun, and Tense 
    using a single LLM call for efficiency.
    """
    if not API_KEY:
        empty_df = pd.DataFrame({
            "Sentence Structure": ["Subject", "Verb", "Object", "Adverbial", "Noun", "Pronoun", "Tense"],
            "Result": ["API Key Missing"] * 7
        })
        return empty_df, {"S": [], "P": [], "O": [], "K": []}

    unified_prompt = f"""
    Analyze the following English sentence.
    
    1. Extract the Subject (S), Verb (P, Predicate), Object (O), and Adverbial (K, Keterangan).
    2. Extract all Nouns and Pronouns.
    3. Identify the Tense of the sentence.

    Return ONLY a valid JSON dictionary with the following keys, ensuring all values are lists of strings, except for 'Tense' which is a single string:
    {{
      "S": [], 
      "P": [], 
      "O": [], 
      "K": [], 
      "nouns": [], 
      "pronouns": [], 
      "Tense": ""
    }}

    Sentence: "{text}"
    """
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
=======
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
>>>>>>> 1222afde46f03eac938416a7f62bbb9ea7430ca7
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Return clean JSON only."},
<<<<<<< HEAD
            {"role": "user", "content": unified_prompt}
        ]
    }
    
    # Inisiasi hasil default
    parsed_results = {
        "S": [], "P": [], "O": [], "K": [],
        "nouns": [], "pronouns": [], "Tense": "Error/Unknown"
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers)
        response.raise_for_status()
        out = response.json()["choices"][0]["message"]["content"]
        
        # Pengecekan keamanan: hapus markdown jika ada
        if out.startswith("```json") and out.endswith("```"):
            out = out.strip("```json").strip("```").strip()
            
        parsed_json = json.loads(out)
        
        # Ambil data dari JSON dan update dictionary hasil
        parsed_results.update({
            "S": parsed_json.get("S", []),
            "P": parsed_json.get("P", []),
            "O": parsed_json.get("O", []),
            "K": parsed_json.get("K", []),
            "nouns": parsed_json.get("nouns", []),
            "pronouns": parsed_json.get("pronouns", []),
            "Tense": parsed_json.get("Tense", "Unknown")
        })

    except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
        print(f"Error during unified LLM extraction: {e}")
    
    all_components = {
        "Subject (Subjek)": ", ".join(parsed_results["S"]),
        "Verb (Predikat)": ", ".join(parsed_results["P"]),
        "Object (Objek)": ", ".join(parsed_results["O"]),
        "Adverbial (Keterangan)": ", ".join(parsed_results["K"]),
        "Noun (Kata Benda)": ", ".join(parsed_results["nouns"]),
        "Pronoun (Kata Ganti)": ", ".join(parsed_results["pronouns"]),
        "Tense": parsed_results["Tense"]
    }

    df = pd.DataFrame({
        "Sentence Structure": all_components.keys(),
        "Result": all_components.values()
    })

    # Kembalikan SVOA untuk highlighting
    highlight_tokens = {
        "S": parsed_results["S"], 
        "P": parsed_results["P"], 
        "O": parsed_results["O"], 
        "K": parsed_results["K"]
    }
    
    return df, highlight_tokens
=======
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
>>>>>>> 1222afde46f03eac938416a7f62bbb9ea7430ca7
