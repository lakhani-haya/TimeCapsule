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

# Custom CSS for elegant styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.25);
        color: white;
    }
    
    .main-header h1 {
        color: white;
        font-family: 'Georgia', serif;
        font-weight: 300;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }
    
    .main-header h3 {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 300;
        font-style: italic;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
    }
    
    .diary-container {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        padding: 2rem;
        border-radius: 8px;
        border-left: 4px solid #6c757d;
        margin: 1rem 0;
        box-shadow: 0 2px 15px rgba(0,0,0,0.08);
    }
    
    .diary-container h3 {
        color: #495057;
        font-family: 'Georgia', serif;
        font-weight: 400;
        margin-bottom: 0.5rem;
    }
    
    .diary-container p {
        color: #6c757d;
        font-style: italic;
        margin-bottom: 0;
    }
    
    .letter-container {
        background: linear-gradient(145deg, #fff8f0, #f8f5f0);
        padding: 2rem;
        border-radius: 8px;
        border-left: 4px solid #d4a574;
        margin: 1rem 0;
        box-shadow: 0 2px 15px rgba(0,0,0,0.08);
    }
    
    .letter-container h3 {
        color: #8b4513;
        font-family: 'Georgia', serif;
        font-weight: 400;
        margin-bottom: 0.5rem;
    }
    
    .letter-container p {
        color: #a0522d;
        font-style: italic;
        margin-bottom: 0;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        border-left: 4px solid #2196f3;
    }
    
    .stats-container h4 {
        color: #1976d2;
        font-family: 'Georgia', serif;
        margin-bottom: 0.5rem;
    }
    
    .stats-container p {
        color: #1565c0;
        font-style: italic;
        margin-bottom: 0;
    }
    
    .elegant-divider {
        text-align: center;
        margin: 3rem 0;
        color: #6c757d;
    }
    
    .elegant-divider::before {
        content: '';
        display: inline-block;
        width: 100px;
        height: 1px;
        background: #dee2e6;
        vertical-align: middle;
        margin-right: 20px;
    }
    
    .elegant-divider::after {
        content: '';
        display: inline-block;
        width: 100px;
        height: 1px;
        background: #dee2e6;
        vertical-align: middle;
        margin-left: 20px;
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 3px solid #6c757d;
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
    st.markdown("### Your Journey")
    saved_letters_dir = "outputs/saved_letters"
    if os.path.exists(saved_letters_dir):
        letter_count = len([f for f in os.listdir(saved_letters_dir) if f.endswith('.txt')])
    else:
        letter_count = 0
    
    st.markdown(f"""
    <div class="stats-container">
        <h4>Letters Created: {letter_count}</h4>
        <p>Continue building your collection</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tips section
    st.markdown("### Writing Guidelines")
    tips = [
        "Write about your feelings honestly",
        "Include your current goals and aspirations",
        "Mention what you're grateful for",
        "Share challenges you're working through",
        "Practice self-compassion"
    ]
    
    for tip in tips:
        st.markdown(f"• {tip}")
    
    st.markdown("---")
    
    st.markdown("### About")
    st.markdown("""
    <div class="sidebar-section">
        <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">
        This application uses advanced AI to help you reflect on your thoughts 
        and transform them into meaningful letters to your future self.
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
        placeholder="Dear diary, today I experienced...\n\nShare your thoughts, feelings, experiences, goals, or anything on your mind. I'll help transform it into a thoughtful letter to your future self.",
        height=300,
        key="diary_input"
    )
    
    # Generation button
    if st.button("Transform into Letter", type="primary", use_container_width=True):
        if diary_entry.strip():
            with st.spinner("Crafting your personalized letter..."):
                # Load model and generate letter
                model = load_model()
                letter = generate_letter(model, diary_entry, tone, templates)
                st.session_state.generated_letter = letter
                st.session_state.letters_count += 1
                
                # Show success message
                st.success("Your letter has been generated successfully!")
        else:
            st.warning("Please write something in your diary entry first.")

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
        <div style="background: white; padding: 2rem; border-radius: 8px; border-left: 4px solid #667eea; margin: 1rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); font-family: 'Georgia', serif; line-height: 1.6;">
            {st.session_state.generated_letter}
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col_save, col_copy = st.columns(2)
        
        with col_save:
            if st.button("Save Letter", use_container_width=True):
                filename = save_letter(st.session_state.generated_letter, tone)
                st.success(f"Letter saved as {filename}")
        
        with col_copy:
            if st.button("Copy to Clipboard", use_container_width=True):
                st.code(st.session_state.generated_letter, language=None)
                st.info("Letter displayed above for copying")
                
    else:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; color: #6c757d;">
            <h4 style="color: #495057; font-family: 'Georgia', serif; font-weight: 300;">Your letter will appear here</h4>
            <p style="font-style: italic;">Write in your diary and click "Transform into Letter" to begin</p>
            <div style="font-size: 2rem; margin-top: 2rem; opacity: 0.5;">✍</div>
        </div>
        """, unsafe_allow_html=True)

# Elegant divider
st.markdown('<div class="elegant-divider">❋</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
---
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 8px; margin-top: 2rem; border-left: 4px solid #6c757d;">
    <h4 style="color: #495057; font-family: 'Georgia', serif; font-weight: 300;">Crafted for Your Future Self</h4>
    <p style="color: #6c757d; font-style: italic; margin-bottom: 0;">Every entry is an opportunity to connect with tomorrow's you</p>
</div>
""", unsafe_allow_html=True)

# Remove auto-refresh for cleaner performance
