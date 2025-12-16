import re

def highlight_svoa(text, tokens):
    color_map = {"S": "#4ade80", "P": "#60a5fa", "O": "#facc15", "K": "#c084fc"}
    highlighted_text = text 

    token_map = {"S": tokens["S"], "P": tokens["P"], "O": tokens["O"], "K": tokens["K"]}  
    
    # --- 1. Penyesuaian Subjek Kontraksi (I'm, You're, dll.) ---
    
    adjusted_subjects = []
    
    for subject_phrase in token_map["S"]:
        # Hanya fokus pada pronoun tunggal yang merupakan subjek umum
        if subject_phrase.lower() in ['i', 'you', 'he', 'she', 'it', 'we', 'they']:
            
            # Pola untuk mencari Subject pronoun diikuti kontraksi ('m, 're, 've, 'd, 'll) di teks asli
            # Group 1: (m|re|ve|d|ll)
            contraction_pattern = r'\b' + re.escape(subject_phrase) + r"['](m|re|ve|d|ll)\b"
            
            match = re.search(contraction_pattern, text, flags=re.IGNORECASE)
            
            if match:
                # Jika kontraksi ditemukan (misalnya I'm), gunakan bentuk kontraksi penuh
                full_contraction = match.group(0) # Contoh: "i'm"
                adjusted_subjects.append(full_contraction)
                
                # Mendapatkan fragmen P yang dikontraksi (misalnya 'm)
                fragment_p = match.group(1) # <-- PERBAIKAN: Menggunakan Group 1
                
                # Hapus fragmen P dan bentuk lengkapnya dari list P (Predicate)
                
                # 1. Coba hapus fragmen pendek yang dikontraksi ('m, 're, dll.)
                try:
                    if fragment_p in token_map["P"]:
                        token_map["P"].remove(fragment_p)
                except ValueError:
                    pass

                # 2. Coba hapus bentuk kata kerja penuh yang sesuai (am, are, have, would/had, will/shall)
                if fragment_p == 'm' and 'am' in token_map["P"]:
                    try: token_map["P"].remove('am')
                    except ValueError: pass
                elif fragment_p == 're' and 'are' in token_map["P"]:
                    try: token_map["P"].remove('are')
                    except ValueError: pass
                # Anda bisa menambahkan logika tambahan untuk 've, 'd, 'll jika diperlukan
                
            else:
                # Jika tidak ada kontraksi, gunakan phrase asli ("I")
                adjusted_subjects.append(subject_phrase)
        else:
            # Jika bukan pronoun, gunakan phrase asli
            adjusted_subjects.append(subject_phrase)

    # Ganti list Subject di token_map dengan yang sudah disesuaikan
    token_map["S"] = adjusted_subjects
    # ----------------------------------------------------
    
    # --- 2. Kumpulkan semua elemen ---
    all_elements = []
    
    unique_phrases = set() 
    
    for tag, phrases in token_map.items():
        for phrase in phrases:
            if phrase and isinstance(phrase, str):
                stripped_phrase = phrase.strip()
                if stripped_phrase not in unique_phrases:
                    all_elements.append((stripped_phrase, tag))
                    unique_phrases.add(stripped_phrase)
                
    # 3. Urutkan dari phrase terpanjang ke terpendek. KRITIS untuk highlight yang benar.
    all_elements.sort(key=lambda x: len(x[0].split()), reverse=True)
    
    
    # --- 4. Lakukan Penggantian HTML ---
    for phrase, tag in all_elements:
        
        html_tag = f"<span style='background-color:{color_map[tag]}; color:black; padding:3px 6px; border-radius:5px; margin:2px;'>{phrase}</span>"
        
        # Strategi 1: Coba dengan word boundary (\b). Paling aman.
        try:
            pattern_boundary = r'\b' + re.escape(phrase) + r'\b'
            
            if re.search(pattern_boundary, highlighted_text, flags=re.IGNORECASE):
                highlighted_text = re.sub(
                    pattern_boundary, 
                    html_tag, 
                    highlighted_text, 
                    flags=re.IGNORECASE,
                    count=1 
                )
                continue
                
        except Exception:
             pass
        
        # Strategi 2: Fallback (Tanpa Word Boundary). Diperlukan untuk frase dengan apostrof/tanda baca.
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

        except Exception as e:
            print(f"Error final replacement for phrase '{phrase}': {e}")

    return highlighted_text.strip()
