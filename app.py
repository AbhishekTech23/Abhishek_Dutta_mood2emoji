import streamlit as st

# Configure the page
st.set_page_config(
    page_title="Mood2Emoji - Text Mood Detector",
    page_icon="😊",
    layout="centered"
)

# Safety filter - basic inappropriate word detection
INAPPROPRIATE_WORDS = {'hate', 'stupid', 'ugly', 'kill', 'hurt', 'fight'}

def is_text_safe(text):
    """Check if text contains inappropriate content"""
    text_lower = text.lower()
    for word in INAPPROPRIATE_WORDS:
        if word in text_lower:
            return False
    return True

def analyze_mood(text):
    """
    Analyze text mood using simple rule-based approach
    Returns: (emoji, explanation)
    """
    if not text.strip():
        return "🤔", "Please enter some text!"
    
    # Safety check first
    if not is_text_safe(text):
        return "🚫", "Let's keep it positive and kind!"
    
    text_lower = text.lower()
    
    # Happy indicators
    happy_words = {'happy', 'good', 'great', 'awesome', 'love', 'like', 'fun', 'excited', 'yay', 'yes', 'wonderful', 'best', 'nice', 'cool', 'fantastic'}
    
    # Sad indicators  
    sad_words = {'sad', 'bad', 'terrible', 'angry', 'upset', 'cry', 'sorry', 'no', 'awful', 'horrible', 'worst', 'hate', 'miss'}
    
    happy_count = sum(1 for word in happy_words if word in text_lower)
    sad_count = sum(1 for word in sad_words if word in text_lower)
    
    # Determine mood
    if happy_count > sad_count:
        return "😀", "Sounds positive and happy!"
    elif sad_count > happy_count:
        return "😞", "This sounds a bit sad."
    else:
        return "😐", "This seems pretty neutral."

def show_teacher_mode():
    """Show how the app works for teachers/advanced students"""
    st.markdown("---")
    st.subheader("🧠 Teacher Mode: How It Works")
    
    st.markdown("""
    ### Decision Process
    
    ```
    Input Text
        ↓
    Safety Check → If inappropriate → 🚫 "Let's keep it positive!"
        ↓
    Count Happy Words (good, great, love, etc.)
        ↓
    Count Sad Words (sad, bad, terrible, etc.)
        ↓
    Compare Counts:
        Happy > Sad → 😀 Happy
        Sad > Happy → 😞 Sad  
        Equal      → 😐 Neutral
    ```
    
    ### What You're Learning
    
    1. **Text Classification**: Computers can categorize text
    2. **Rule-based Systems**: Simple if-then logic
    3. **Safety First**: Always filter content
    4. **Problem Solving**: Breaking down complex tasks
    """)

# Main app interface
st.title("🎭 Mood2Emoji")
st.markdown("Type a sentence and I'll detect the mood with an emoji!")

# Input section
user_input = st.text_area(
    "Enter your text here:",
    placeholder="Example: I had a great day today!",
    height=100
)

# Analyze button
if st.button("Analyze Mood 🎯"):
    if user_input:
        emoji, explanation = analyze_mood(user_input)
        
        # Display result
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"# {emoji}")
        with col2:
            st.markdown(f"### {explanation}")
        
        # Show analysis details
        with st.expander("See how I decided"):
            st.write(f"**Your text:** '{user_input}'")
            st.write(f"**Safety check:** {'✅ Passed' if is_text_safe(user_input) else '❌ Filtered'}")
            
    else:
        st.warning("Please enter some text to analyze!")

# Teacher mode toggle
if st.checkbox("Enable Teacher Mode"):
    show_teacher_mode()

# Footer
st.markdown("---")
st.caption("Built for learning - Safe for ages 12-16 | Uses rule-based analysis")