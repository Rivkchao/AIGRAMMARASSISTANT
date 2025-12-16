import re

def highlight_svoa(text, tokens):
    # Mapping warna untuk SVOA
    color_map = {"S": "#4ade80", "P": "#60a5fa", "O": "#facc15", "K": "#c084fc"}
    highlighted_text = text # Mulai dengan teks mentah (clean text)

    all_elements = []
    
    token_map = {"S": tokens["S"], "P": tokens["P"], "O": tokens["O"], "K": tokens["K"]}  
    
    # 1. Kumpulkan semua phrase dan tag-nya
    for tag, phrases in token_map.items():
        for phrase in phrases:
            # Pastikan phrase adalah string non-kosong dan bersih
            if phrase and isinstance(phrase, str):
                # Kita strip whitespace di sini
                all_elements.append((phrase.strip(), tag))
                
    # 2. Urutkan dari phrase terpanjang ke terpendek. Ini KRITIS.
    all_elements.sort(key=lambda x: len(x[0].split()), reverse=True)
    
    # Set untuk melacak kata/frase yang sudah berhasil di-highlight
    highlighted_phrases = set()

    for phrase, tag in all_elements:
        
        # Cek duplikasi, meskipun pengurutan sudah membantu
        if phrase in highlighted_phrases:
            continue
        
        # Buat tag HTML untuk phrase ini
        html_tag = f"<span style='background-color:{color_map[tag]}; color:black; padding:3px 6px; border-radius:5px; margin:2px;'>{phrase}</span>"
        
        # Strategi Penggantian:
        # Kita harus mencari phrase yang *belum* di-highlight di dalam highlighted_text.
        
        # Coba Strategi 1: Menggunakan Word Boundary (\b). Paling akurat, tapi gagal pada apostrof (i'm, king's).
        try:
            # Escape phrase, lalu tambahkan boundary
            pattern_boundary = r'\b' + re.escape(phrase) + r'\b'
            
            # Cek apakah pola ini cocok di teks saat ini
            if re.search(pattern_boundary, highlighted_text, flags=re.IGNORECASE):
                highlighted_text = re.sub(
                    pattern_boundary, 
                    html_tag, 
                    highlighted_text, 
                    flags=re.IGNORECASE,
                    count=1 
                )
                highlighted_phrases.add(phrase)
                continue # Lanjut ke phrase berikutnya
                
        except Exception as e:
             # Jika terjadi error pada regex, coba fallback
             pass
        
        # Strategi 2: Fallback (Tanpa Word Boundary, lebih berisiko tapi menangani apostrof)
        # Gunakan hanya re.escape(). Ini menggantikan phrase di mana pun ia ditemukan.
        try:
            pattern_no_boundary = re.escape(phrase)
            
            if re.search(pattern_no_boundary, highlighted_text, flags=re.IGNORECASE):
                highlighted_text = re.sub(
                    pattern_no_boundary, 
                    html_tag, 
                    highlighted_text, 
                    flags=re.IGNORECASE,
                    count=1 
                )
                highlighted_phrases.add(phrase)

        except Exception as e_inner:
            # Jika semua gagal, log error (optional)
            print(f"Error final replacement for phrase '{phrase}': {e_inner}")

    return highlighted_text.strip()
