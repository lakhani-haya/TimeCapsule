import streamlit as st
import json
import os
from datetime import datetime
from utils import load_model, generate_letter, save_letter
import time

# Page configuration
st.set_page_config(
    page_title="AI Time Capsule",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for sophisticated styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@300;400;500;700&family=Source+Sans+Pro:wght@300;400;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 4rem 3rem;
        margin: -1rem -1rem 3rem -1rem;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-family: 'Playfair Display', serif;
        font-weight: 400;
        font-size: 3.5rem;
        letter-spacing: 3px;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header h3 {
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 300;
        font-size: 1.3rem;
        font-style: italic;
        margin-bottom: 1rem;
        letter-spacing: 1px;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.8);
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 0.95rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    .content-section {
        background: white;
        border-radius: 12px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        position: relative;
    }
    
    .content-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #d4af37 0%, #ffd700 50%, #d4af37 100%);
        border-radius: 12px 12px 0 0;
    }
    
    .diary-container {
        background: white;
        border-radius: 12px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        position: relative;
    }
    
    .diary-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #8b9dc3 0%, #dfe4ea 50%, #8b9dc3 100%);
        border-radius: 12px 12px 0 0;
    }
    
    .diary-container h3 {
        color: #2c3e50;
        font-family: 'Playfair Display', serif;
        font-weight: 500;
        font-size: 1.8rem;
        margin-bottom: 0.8rem;
        letter-spacing: 1px;
    }
    
    .diary-container p {
        color: #5a6c7d;
        font-family: 'Source Sans Pro', sans-serif;
        font-style: italic;
        font-size: 1rem;
        margin-bottom: 0;
        opacity: 0.8;
    }
    
    .letter-container {
        background: white;
        border-radius: 12px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        position: relative;
    }
    
    .letter-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #c9a876 0%, #f4e7d1 50%, #c9a876 100%);
        border-radius: 12px 12px 0 0;
    }
    
    .letter-container h3 {
        color: #8b4513;
        font-family: 'Playfair Display', serif;
        font-weight: 500;
        font-size: 1.8rem;
        margin-bottom: 0.8rem;
        letter-spacing: 1px;
    }
    
    .letter-container p {
        color: #a0522d;
        font-family: 'Source Sans Pro', sans-serif;
        font-style: italic;
        font-size: 1rem;
        margin-bottom: 0;
        opacity: 0.8;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        text-align: center;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .stats-container h4 {
        color: #2c3e50;
        font-family: 'Playfair Display', serif;
        font-weight: 500;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
    }
    
    .stats-container p {
        color: #5a6c7d;
        font-family: 'Source Sans Pro', sans-serif;
        font-style: italic;
        margin-bottom: 0;
        font-size: 0.9rem;
    }
    
    .sidebar-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .elegant-divider {
        text-align: center;
        margin: 4rem 0;
        position: relative;
    }
    
    .elegant-divider::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #d4af37 20%, #ffd700 50%, #d4af37 80%, transparent 100%);
    }
    
    .elegant-divider span {
        background: #f5f7fa;
        color: #8b9dc3;
        padding: 0 2rem;
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        position: relative;
        z-index: 1;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(44, 62, 80, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        box-shadow: 0 6px 20px rgba(44, 62, 80, 0.3);
        transform: translateY(-2px);
    }
    
    /* Custom selectbox styling */
    .stSelectbox > div > div {
        font-family: 'Source Sans Pro', sans-serif;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        font-family: 'Source Sans Pro', sans-serif;
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #8b9dc3;
        box-shadow: 0 0 0 3px rgba(139, 157, 195, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_letter' not in st.session_state:
    st.session_state.generated_letter = ""
if 'letters_count' not in st.session_state:
    st.session_state.letters_count = 0

# Main header
st.markdown("""
<div class="main-header">
    <h1>AI Time Capsule</h1>
    <h3>Transform your diary entries into thoughtful letters to your future self</h3>
    <p>Powered by local AI • Completely Private • Free to Use</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Personalization")
    st.markdown("---")
    
    # Load tone templates
    with open('prompts/templates.json', 'r') as f:
        templates = json.load(f)
    
    tone = st.selectbox(
        "Choose your letter tone:",
        options=list(templates.keys()),
        format_func=lambda x: f"{x.title()}"
    )
    
    st.markdown("---")
    
    # Stats section
    st.markdown("### Your Progress")
    saved_letters_dir = "outputs/saved_letters"
    if os.path.exists(saved_letters_dir):
        letter_count = len([f for f in os.listdir(saved_letters_dir) if f.endswith('.txt')])
    else:
        letter_count = 0
    
    st.markdown(f"""
    <div class="stats-container">
        <h4>Letters Created: {letter_count}</h4>
        <p>Building your personal archive</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Guidelines section
    st.markdown("### Writing Guidelines")
    st.markdown("""
    <div class="sidebar-section">
        <p style="font-size: 0.9rem; color: #5a6c7d; margin: 0.5rem 0; line-height: 1.5;">
        • Express your authentic feelings<br>
        • Include current aspirations<br>  
        • Note moments of gratitude<br>
        • Share personal challenges<br>
        • Practice self-compassion
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### About This Experience")
    st.markdown("""
    <div class="sidebar-section">
        <p style="font-size: 0.9rem; color: #5a6c7d; margin: 0; line-height: 1.6;">
        This sophisticated application employs advanced AI to transform your personal reflections 
        into thoughtful correspondence with your future self, creating a bridge between who you are today 
        and who you aspire to become.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="diary-container">
        <h3>Your Diary Entry</h3>
        <p>Express your thoughts and feelings here</p>
    </div>
    """, unsafe_allow_html=True)
    
    diary_entry = st.text_area(
        "",
        placeholder="Begin your reflection...\n\nShare your thoughts, experiences, aspirations, or any meaningful moments from today. This space is yours to explore your inner world—every word becomes part of your personal time capsule.",
        height=320,
        key="diary_input"
    )
    
    # Generation button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("Transform into Letter", type="primary", use_container_width=True):
            if diary_entry.strip():
                with st.spinner("Crafting your personalized correspondence..."):
                    # Load model and generate letter
                    model = load_model()
                    letter = generate_letter(model, diary_entry, tone, templates)
                    st.session_state.generated_letter = letter
                    st.session_state.letters_count += 1
                    
                    # Show success message
                    st.success("Your letter has been crafted successfully")
            else:
                st.warning("Please share your thoughts before proceeding")

with col2:
    st.markdown("""
    <div class="letter-container">
        <h3>Your Future Self Letter</h3>
        <p>A thoughtful message from present you to future you</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.generated_letter:
        # Display the generated letter
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fafbfc 0%, #f8f9fb 100%); padding: 3rem; border-radius: 12px; border: 1px solid rgba(0,0,0,0.05); margin: 1rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.08); font-family: 'Source Sans Pro', sans-serif; line-height: 1.8; color: #2c3e50; position: relative;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #c9a876 0%, #f4e7d1 50%, #c9a876 100%); border-radius: 12px 12px 0 0;"></div>
            <div style="margin-top: 1rem;">{st.session_state.generated_letter}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col_save, col_spacer, col_copy = st.columns([2, 1, 2])
        
        with col_save:
            if st.button("Archive Letter", use_container_width=True):
                filename = save_letter(st.session_state.generated_letter, tone)
                st.success(f"Archived as {filename}")
        
        with col_copy:
            if st.button("Copy Text", use_container_width=True):
                st.code(st.session_state.generated_letter, language=None)
                st.info("Letter text displayed above for copying")
                
    else:
        st.markdown("""
        <div style="text-align: center; padding: 5rem 2rem; color: #8b9dc3;">
            <h4 style="color: #5a6c7d; font-family: 'Playfair Display', serif; font-weight: 300; font-size: 1.5rem; margin-bottom: 1rem;">Your Personal Letter Awaits</h4>
            <p style="font-family: 'Source Sans Pro', sans-serif; font-style: italic; font-size: 1.1rem; line-height: 1.6;">Express yourself in the space to the left, then witness the transformation of your thoughts into a meaningful correspondence with your future self.</p>
            <div style="font-size: 3rem; margin-top: 2rem; opacity: 0.3;">✒</div>
        </div>
        """, unsafe_allow_html=True)

# Elegant divider
st.markdown('<div class="elegant-divider"><span>✦</span></div>', unsafe_allow_html=True)

# Footer
st.markdown("""
---
<div style="text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, #fafbfc 0%, #f0f2f5 100%); border-radius: 12px; margin-top: 3rem; border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 8px 25px rgba(0,0,0,0.05);">
    <h4 style="color: #2c3e50; font-family: 'Playfair Display', serif; font-weight: 400; font-size: 1.5rem; margin-bottom: 1rem;">Crafted for Tomorrow's You</h4>
    <p style="color: #5a6c7d; font-family: 'Source Sans Pro', sans-serif; font-style: italic; margin-bottom: 0; font-size: 1rem; line-height: 1.6;">Each reflection becomes a bridge between your present consciousness and future wisdom</p>
</div>
""", unsafe_allow_html=True)

# Remove auto-refresh for cleaner performance
