import streamlit as st
from grammar_correction import correct_grammar_openai
from text_refinement import refine_text
from svoa_analysis import analyze_svoa
from highlight import highlight_svoa
import time  

st.set_page_config(
    page_title="AI Grammar Assistant", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

st.title("📝 AI Grammar Assistant: Polish & Analyze")
st.markdown("Use the power of AI to fix your grammar, refine your writing, and analyze sentence structure.")

user_text = st.text_area("✍️ Input your text here:", height=200, placeholder="Type or paste the text you want to check...")

if st.button("✨ Fix & Analyze Text", use_container_width=True, type="primary"):
    if not user_text.strip():
        st.warning("⚠️ Please input some text before analyzing.")
    else:
        with st.status("Analyzing and polishing your text...", expanded=True) as status:
            
            # Step 1: Grammar Correction
            st.write("🔍 Correcting grammar using AI...")
            time.sleep(0.5)
            corrected, explanation = correct_grammar_openai(user_text)

            # Step 2: Text Refinement
            st.write("🪶 Applying final text refinement...")
            time.sleep(0.5)
            final = refine_text(corrected)

            # Step 3: Structure Analysis
            st.write("📊 Performing SVOA and Tense analysis...")
            time.sleep(0.5)
            df, tokens = analyze_svoa(final)
            
            status.update(label="Analysis Complete!", state="complete", expanded=False)
            st.balloons() # A celebratory visual

        # We use two columns: one for the final text and one for the SVOA highlighting
        col_fixed_text, col_highlight = st.columns([3, 2])
        
        with col_fixed_text:
            st.subheader("✅ Polished Text")
            st.info(f"**{final}**")
            
            tab_explanation, tab_svoa = st.tabs(["💬 AI Explanation", "📊 Detailed Structure Data"])
            
            with tab_explanation:
                st.markdown("#### What the AI Changed:")
                st.write(explanation)
                st.markdown("---")
                tense_result = df[df['Sentence Structure'] == 'Tense']['Result'].iloc[0]
                st.metric(label="Detected Tense", value=tense_result, help="Identified by the AI model.")
                
            with tab_svoa:
                st.markdown("#### Found Grammatical Elements")
                st.dataframe(df, use_container_width=True, hide_index=True)

        with col_highlight:
            st.subheader("🌈 Structure Highlight")
            st.markdown(
                """
                <div style="padding: 10px; border-radius: 8px; background-color: #f0f2f6; margin-bottom: 15px;">
                    **Legend:** <span style="color:#16a34a; font-weight: bold;">🟩 Subject</span> | 
                    <span style="color:#2563eb; font-weight: bold;">🟦 Verb</span> | 
                    <span style="color:#d97706; font-weight: bold;">🟨 Object</span> | 
                    <span style="color:#9333ea; font-weight: bold;">🟪 Adverbial</span>
                </div>
                """, unsafe_allow_html=True
            )
            
            highlighted_html = highlight_svoa(final, tokens)
            st.markdown(
                f"<div style='border: 1px solid #ddd; padding: 15px; border-radius: 10px;'>{highlighted_html}</div>", 
                unsafe_allow_html=True
            )
        
        st.markdown("---")