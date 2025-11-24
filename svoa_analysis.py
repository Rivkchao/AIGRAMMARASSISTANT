import re
import pandas as pd
import spacy
from tense_detection import detect_tense_openai

nlp = spacy.load("en_core_web_sm")

def analyze_svoa(text):
    words = text.split()
    
    subjects = list(set([w for w in words if w.lower() in ["i","you","he","she","it","we","they"]]))
    verbs = list(set([w for w in words if re.match(r"(am|is|are|was|were|do|does|did|have|has|had|will|'m|'re|'s|\w+ed|\w+s)", w.lower())]))
    objects = list(set([w for w in words if w.lower() in ["me","him","her","us","them","it","you","that"]]))
    adverbs = list(set([w for w in words if w.lower() in ["yesterday","today","tomorrow","now","after","before","then","later","soon","already","still","yet"]]))

    tense = detect_tense_openai(text)
    doc = nlp(text)
    
    nouns = list(set([t.text for t in doc if t.pos_ == "NOUN"]))
    pronouns = list(set([t.text for t in doc if t.pos_ == "PRON"]))

    df = pd.DataFrame({
        "Sentence Structure": [
            "Subject (Subjek)", "Verb (Predikat)", "Object (Objek)", 
            "Adverbial (Keterangan)", "Noun (Kata Benda)", 
            "Pronoun (Kata Ganti)", "Tense"
        ],
        "Result": [
            ", ".join(subjects), " ".join(verbs), ", ".join(objects),
            ", ".join(adverbs), ", ".join(nouns), ", ".join(pronouns), tense
        ]
    })

    return df, {"S": subjects, "P": verbs, "O": objects, "K": adverbs}