import re

def highlight_svoa(text, tokens):
    color_map = {"S": "#4ade80", "P": "#60a5fa", "O": "#facc15", "K": "#c084fc"}
    highlighted_text = text # Mulai dengan teks mentah

    all_elements = []
    
    token_map = {"S": tokens["S"], "P": tokens["P"], "O": tokens["O"], "K": tokens["K"]} 
    
    for tag, phrases in token_map.items():
        for phrase in phrases:
            if phrase and isinstance(phrase, str):
                all_elements.append((phrase, tag))
                
    all_elements.sort(key=lambda x: len(x[0].split()), reverse=True)
    
    for phrase, tag in all_elements:
        html_tag = f"<span style='background-color:{color_map[tag]}; color:black; padding:3px 6px; border-radius:5px; margin:2px;'>{phrase}</span>"
        
        try:
            highlighted_text = re.sub(
                re.escape(phrase), 
                html_tag, 
                highlighted_text, 
                flags=re.IGNORECASE,
                count=1 
            )
        except Exception as e:
            print(f"Error during replacement for phrase '{phrase}': {e}")
            
    return highlighted_text.strip()
