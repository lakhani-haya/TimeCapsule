import streamlit as st
import json
import os
from datetime import datetime
from utils import load_model, generate_letter, save_letter
import time

# Page configuration
st.set_page_config(
    page_title="🌟 AI Time Capsule",
    page_icon="💌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cute styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(255, 154, 158, 0.37);
    }
    
    .diary-container {
        background: linear-gradient(145deg, #f0f8ff, #e6f3ff);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid #b8d4f0;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .letter-container {
        background: linear-gradient(145deg, #fff5ee, #ffeee6);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid #ffcba4;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .tone-button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.25rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .cute-divider {
        text-align: center;
        margin: 2rem 0;
        font-size: 2rem;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
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
    <h1>🌟 AI Time Capsule 💌</h1>
    <h3>Transform your diary entries into loving letters to your future self ✨</h3>
    <p>🤖 Powered by local AI • 🔒 100% Private • 💝 Completely Free</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎨 Personalization")
    
    # Load tone templates
    with open('prompts/templates.json', 'r') as f:
        templates = json.load(f)
    
    tone = st.selectbox(
        "💭 Choose your letter tone:",
        options=list(templates.keys()),
        format_func=lambda x: f"✨ {x.title()}"
    )
    
    st.markdown("---")
    
    # Stats section
    st.markdown("### 📊 Your Journey")
    saved_letters_dir = "outputs/saved_letters"
    if os.path.exists(saved_letters_dir):
        letter_count = len([f for f in os.listdir(saved_letters_dir) if f.endswith('.txt')])
    else:
        letter_count = 0
    
    st.markdown(f"""
    <div class="stats-container">
        <h4>💌 Letters Created: {letter_count}</h4>
        <p>🌱 Keep growing your future self!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tips section
    st.markdown("### 💡 Writing Tips")
    tips = [
        "🌸 Write about your feelings honestly",
        "🌟 Include your current goals and dreams",
        "💭 Mention what you're grateful for",
        "🎯 Share challenges you're working through",
        "💕 Be kind to yourself"
    ]
    
    for tip in tips:
        st.markdown(f"- {tip}")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="diary-container">
        <h3>📖 Your Diary Entry</h3>
        <p>Pour your heart out here... ✍️</p>
    </div>
    """, unsafe_allow_html=True)
    
    diary_entry = st.text_area(
        "",
        placeholder="Dear diary, today I felt...\n\nTell me about your day, your thoughts, your dreams, or anything on your mind. I'll help you turn it into a beautiful letter to your future self! 💭✨",
        height=300,
        key="diary_input"
    )
    
    # Generation button
    if st.button("🌟 Transform into Letter", type="primary", use_container_width=True):
        if diary_entry.strip():
            with st.spinner("🤖 AI is crafting your beautiful letter... ✨"):
                # Load model and generate letter
                model = load_model()
                letter = generate_letter(model, diary_entry, tone, templates)
                st.session_state.generated_letter = letter
                st.session_state.letters_count += 1
                
                # Show success message
                st.success("🎉 Your letter is ready!")
        else:
            st.warning("📝 Please write something in your diary entry first!")

with col2:
    st.markdown("""
    <div class="letter-container">
        <h3>💌 Your Future Self Letter</h3>
        <p>A loving message from you to you... 💕</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.generated_letter:
        # Display the generated letter
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; border-left: 5px solid #ff9a9e; margin: 1rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            {st.session_state.generated_letter}
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col_save, col_copy = st.columns(2)
        
        with col_save:
            if st.button("💾 Save Letter", use_container_width=True):
                filename = save_letter(st.session_state.generated_letter, tone)
                st.success(f"💌 Letter saved as {filename}!")
        
        with col_copy:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.code(st.session_state.generated_letter, language=None)
                st.info("📋 Letter displayed above for copying!")
                
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #888;">
            <h4>🌟 Your beautiful letter will appear here!</h4>
            <p>✍️ Write in your diary and click "Transform into Letter" to see the magic happen</p>
            <p style="font-size: 3rem;">📝✨💌</p>
        </div>
        """, unsafe_allow_html=True)

# Cute divider
st.markdown('<div class="cute-divider">🌸 ✨ 🌸 ✨ 🌸</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
---
<div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #ffeaa7, #fab1a0); border-radius: 15px; margin-top: 2rem;">
    <h4>💝 Made with love for your future self</h4>
    <p>🤗 Remember: Every day is a chance to write a beautiful story to tomorrow's you!</p>
    <p style="font-size: 1.5rem;">🌟 ✨ 💫 ⭐ ✨ 🌟</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh for real-time updates
if st.session_state.letters_count > 0:
    time.sleep(0.1)  # Small delay for smooth UI updates
