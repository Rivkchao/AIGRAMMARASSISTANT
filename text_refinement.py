import re

def refine_text(text):
    """
    Performs universal text cleanup by ensuring proper sentence capitalization.
    All specific abbreviation/term standardizations are handled by the AI prompt.
    """
    
    # Split text into sentences using punctuation, and strip whitespace
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    
    # Capitalize the first letter of every sentence (Universal Rule)
    sentences = [s.strip().capitalize() for s in sentences if s]
    refined = " ".join(sentences)

    return refined