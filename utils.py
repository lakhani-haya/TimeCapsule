import os
import json
from datetime import datetime
from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_model():
    """Load the AI model for generation"""
    try:
        # Using google/flan-t5-base
        model = pipeline(
            "text2text-generation", 
            model="google/flan-t5-base",
            max_length=512,
            do_sample=True,
            temperature=0.7
        )
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.info("Please make sure you have the required packages installed.")
        return None

def generate_letter(model, diary_entry, tone, templates):
    """Generate a letter from diary entry using the specified tone"""
    if not model:
        return "Model not available. Please check your setup."
    
    try:
        # Get the prompt template for the sel
        prompt_template = templates.get(tone, templates["motivational"])
        
        # Format the prompt with the diary entry
        formatted_prompt = prompt_template.format(entry=diary_entry)
        
        # Generate the letter
        result = model(formatted_prompt, max_length=400, num_return_sequences=1)
        
        if result and len(result) > 0:
            generated_text = result[0]['generated_text']
            
            # Post-process the generated text to make it more letter-like
            letter = format_as_letter(generated_text, tone)
            return letter
        else:
            return "I couldn't generate a letter right now. Please try again."
            
    except Exception as e:
        return f"Error generating letter: {str(e)}"

def format_as_letter(text, tone):
    """Format the generated text as a proper letter"""
    # Add letter greeting and closing based on tone
    greetings = {
        "motivational": "Dear Future Self,",
        "gentle": "My Dear Future Self,",
        "funny": "Hey Future Me,"
    }
    
    closings = {
        "motivational": "\n\nWith unwavering belief in your potential,\nYour Past Self",
        "gentle": "\n\nWith all my love and understanding,\nYour caring past self",
        "funny": "\n\nStay amazing (and keep that sense of humor!),\nYour wonderfully past self"
    }
    
    greeting = greetings.get(tone, "Dear Future Self,")
    closing = closings.get(tone, "\n\nWith warm regards,\nYour Past Self")
    
    # Clean up the text
    text = text.strip()
    if not text.startswith(greeting.split()[-1]):  # Don't double-add greeting
        letter = f"{greeting}\n\n{text}{closing}"
    else:
        letter = f"{text}{closing}"
    
    return letter

def save_letter(letter_content, tone):
    """Save the generated letter to a file"""
    try:
        # Create the saved_letters directory if it doesn't exist
        save_dir = "outputs/saved_letters"
        os.makedirs(save_dir, exist_ok=True)
        
        # Generate filename with timestamp and tone
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"letter_{tone}_{timestamp}.txt"
        filepath = os.path.join(save_dir, filename)
        
        # Add metadata header to the saved file
        metadata_header = f"""
AI Time Capsule Letter
Generated on: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
Tone: {tone.title()}
═══════════════════════════════════════════════════════

"""
        
        # Save the letter
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(metadata_header + letter_content)
        
        return filename
        
    except Exception as e:
        st.error(f"Error saving letter: {str(e)}")
        return None

def load_templates():
    """Load prompt templates from JSON file"""
    try:
        templates_path = "prompts/templates.json"
        if os.path.exists(templates_path):
            with open(templates_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Return default templates if file doesn't exist
            return get_default_templates()
    except Exception as e:
        st.error(f"Error loading templates: {str(e)}")
        return get_default_templates()

def get_default_templates():
    """Return default prompt templates"""
    return {
        "motivational": """Transform this diary entry into an uplifting, motivational letter to the writer's future self. Make it encouraging, empowering, and full of belief in their potential. Use an energetic and inspiring tone:

{entry}""",
        
        "gentle": """Rewrite this diary entry as a soft, comforting letter to the writer's future self. Make it warm, nurturing, and full of self-compassion. Use a gentle and loving tone:

{entry}""",
        
        "funny": """Turn this diary entry into a lighthearted, humorous letter to the writer's future self. Make it witty and uplifting while keeping the core message positive. Use a playful and amusing tone:

{entry}"""
    }

def get_letter_stats():
    """Get statistics about saved letters"""
    save_dir = "outputs/saved_letters"
    if not os.path.exists(save_dir):
        return {"total": 0, "by_tone": {}}
    
    files = [f for f in os.listdir(save_dir) if f.endswith('.txt')]
    total = len(files)
    
    # Count by tone
    by_tone = {"motivational": 0, "gentle": 0, "funny": 0}
    for filename in files:
        for tone in by_tone.keys():
            if tone in filename:
                by_tone[tone] += 1
                break
    
    return {"total": total, "by_tone": by_tone}

def validate_diary_entry(entry):
    """Validate diary entry input"""
    if not entry or not entry.strip():
        return False, "Please write something in your diary entry."
    
    if len(entry.strip()) < 10:
        return False, "Your diary entry seems a bit short. Try adding more details."
    
    if len(entry.strip()) > 2000:
        return False, "Your diary entry is quite long. Try shortening it to under 2000 characters."
    
    return True, "Entry looks good."
