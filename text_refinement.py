import re

def refine_text(text):
    """
    Performs universal text cleanup by ensuring proper sentence capitalization.
    All specific abbreviation/term standardizations are handled by the AI prompt.
    """
    # Pisahkan teks menjadi kalimat menggunakan tanda baca, dan hilangkan spasi
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    
    # Huruf pertama setiap kalimat harus dikapitalisasi
    sentences = [s.strip().capitalize() for s in sentences if s]
    refined = " ".join(sentences)

    return refined