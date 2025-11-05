# pip install streamlit transformers torch spacy pandas
# python -m spacy download en_core_web_sm


import streamlit as st
from transformers import pipeline
import re
import pandas as pd
import spacy
nlp = spacy.load("en_core_web_sm")

# =====================
# APP SETUP
# =====================
st.set_page_config(page_title="AI-Powered Grammar Assistant", layout="wide")
st.title("🧠 Grammar Assistant ARAGROUP — Fix & Analysis")

# =====================
# LOAD MODEL (Cached)
# =====================
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="grammarly/coedit-large")

corrector = load_model()

# =====================
# GRAMMAR CORRECTION
# =====================
def grammar_correction(text):
    result = corrector(text, max_length=256, do_sample=False, num_beams=5)
    return result[0]['generated_text']

# =====================
# REFINEMENT & POLISH
# =====================
def refine_text(text):
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    sentences = [s.strip().capitalize() for s in sentences if s]
    refined = " ".join(sentences)
    refined = re.sub(r"\bim\b", "I'm", refined, flags=re.IGNORECASE)
    refined = re.sub(r"\bi\b", "I", refined)
    refined = re.sub(r"\bieee sb\b", "IEEE SB", refined, flags=re.IGNORECASE)
    refined = re.sub(r"\bbahasa indonesia\b", "Indonesian", refined)
    return refined

# =====================
# SVOA + TENSE DETECTION + POS DETAIL
# =====================
def analyze_svoa(text):
    words = text.split()

    subjects = [w for w in words if w.lower() in ["i","you","he","she","it","we","they"]]
    verbs = [w for w in words if re.match(r"(am|is|are|was|were|do|does|did|have|has|had|will|'m|'re|'s|\w+ed|\w+s)", w.lower())]
    objects = [w for w in words if w.lower() in ["me","him","her","us","them","it","you","that"]]
    adverbs = [w for w in words if w.lower() in ["yesterday","today","tomorrow","now","after","before","then","later","soon","already","still","yet"]]

    # === Tense Detection ===
    text_lower = text.lower()
    if any(x in text_lower for x in ["will ", "shall "]):
        tense = "Future"
    elif re.search(r"\b(did|was|were|\w+ed)\b", text_lower):
        tense = "Past"
    elif re.search(r"\b(do|does|am|is|are|don’t|doesn’t|donot|doesnot)\b", text_lower):
        tense = "Present"
    else:
        tense = "Unknown"

    # === POS Tagging (Noun & Pronoun) ===
    doc = nlp(text)
    nouns = [t.text for t in doc if t.pos_ == "NOUN"]
    pronouns = [t.text for t in doc if t.pos_ == "PRON"]

    # === DataFrame result ===
    df = pd.DataFrame({
        "Sentence Structure": [
            "Subject (Subjek)", "Verb (Predikat)", "Object (Objek)", 
            "Adverbial (Keterangan)", "Noun (Kata Benda)", 
            "Pronoun (Kata Ganti)", "Tense"
        ],
        "Result": [
            ", ".join(subjects), ", ".join(verbs), ", ".join(objects),
            ", ".join(adverbs), ", ".join(nouns), ", ".join(pronouns), tense
        ]
    })

    return df, {"S": subjects, "P": verbs, "O": objects, "K": adverbs}

# =====================
# COLOR HIGHLIGHT FUNCTION
# =====================
def highlight_svoa(text, tokens):
    color_map = {"S": "#4ade80", "P": "#60a5fa", "O": "#facc15", "K": "#c084fc"}
    html = ""
    for word in text.split():
        tag = None
        w = re.sub(r'[^\w\s]', '', word).lower()
        if w in [x.lower() for x in tokens["S"]]: tag = "S"
        elif w in [x.lower() for x in tokens["P"]]: tag = "P"
        elif w in [x.lower() for x in tokens["O"]]: tag = "O"
        elif w in [x.lower() for x in tokens["K"]]: tag = "K"

        if tag:
            html += f"<span style='background-color:{color_map[tag]}; color:black; padding:3px 6px; border-radius:5px; margin:2px;'>{word}</span> "
        else:
            html += f"{word} "
    return html.strip()

# =====================
# STREAMLIT UI
# =====================
user_text = st.text_area("Input your text:", height=150, placeholder="contoh: she dont like me after that all what i doo")

if st.button("Fix & Analysis ✨"):
    if user_text.strip():
        with st.spinner("Step 1: Grammar correction..."):
            tahap1 = grammar_correction(user_text)
        with st.spinner("Step 2: Refining text..."):
            final = refine_text(tahap1)

        st.success("✅ End result:")
        st.markdown(final)

        st.markdown("---")
        st.info(f"🔹 Result of Step 1: {tahap1}")

        df, tokens = analyze_svoa(final)
        st.markdown("### 🧩 Grammar Analysis (SVOA + Noun + Pronoun + Tense)")
        st.dataframe(df, width='content', hide_index=True)

        st.markdown("### 🪶 Highlighted Text (SVOA Colorized)")
        st.markdown("""
        🟩 Subject | 🟦 Verb | 🟨 Object | 🟪 Adverbial
        """)
        st.markdown(highlight_svoa(final, tokens), unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please input some text before analyzing.")
