import re

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