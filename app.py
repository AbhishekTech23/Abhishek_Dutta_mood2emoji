import streamlit as st
from textblob import TextBlob
import re

# Configure the page
st.set_page_config(
    page_title="Mood2Emoji - Text Mood Detector",
    page_icon="😊",
    layout="centered"
)

# Safety filter - basic inappropriate word detection
INAPPROPRIATE_WORDS = {
    'bad', 'hate', 'stupid', 'dumb', 'ugly', 'kill', 'hurt', 'fight'
}

def is_text_safe(text):
    """Check if text contains inappropriate content"""
    text_lower = text.lower()
    for word in INAPPROPRIATE_WORDS:
        if word in text_lower:
            return False
    return True

def analyze_mood(text):
    """
    Analyze text mood using a combination of TextBlob and rule-based approach
    Returns: (emoji, explanation, sentiment_score)
    """
    if not text.strip():
        return "🤔", "Please enter some text!", 0
    
    # Safety check first
    if not is_text_safe(text):
        return "🚫", "Let's keep it positive and kind!", 0
    
    # Analyze with TextBlob
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    
    # Rule-based enhancement for common phrases
    text_lower = text.lower()
    
    # Happy indicators
    happy_words = {'happy', 'good', 'great', 'awesome', 'amazing', 'love', 'like', 'fun', 'excited', 'yay', 'yes', 'wonderful'}
    # Sad indicators  
    sad_words = {'sad', 'bad', 'terrible', 'hate', 'angry', 'upset', 'cry', 'sorry', 'no', 'awful', 'horrible'}
    
    happy_count = sum(1 for word in happy_words if word in text_lower)
    sad_count = sum(1 for word in sad_words if word in text_lower)
    
    # Combined scoring
    final_score = sentiment + (happy_count * 0.1) - (sad_count * 0.1)
    
    # Determine mood
    if final_score > 0.1:
        return "😀", "Sounds positive and happy!", final_score
    elif final_score < -0.1:
        return "😞", "This sounds a bit sad.", final_score
    else:
        return "😐", "This seems pretty neutral.", final_score

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
    TextBlob Analysis (Sentiment Score: -1 to +1)
        ↓
    Rule-based Enhancement (Keyword Counting)
        ↓
    Combined Scoring
        ↓
    Final Decision:
        > +0.1  → 😀 Happy
        < -0.1  → 😞 Sad  
        else    → 😐 Neutral
    ```
    
    ### Key Concepts Taught
    
    1. **Sentiment Analysis**: Computers can estimate emotions in text
    2. **Rule-based Systems**: Simple if-then logic for classification
    3. **Safety First**: Always filter content for age-appropriateness
    4. **Combined Approaches**: Using both ML and rules for better accuracy
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
        emoji, explanation, score = analyze_mood(user_input)
        
        # Display result
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"# {emoji}")
        with col2:
            st.markdown(f"### {explanation}")
            st.caption(f"Confidence score: {score:.2f}")
        
        # Show analysis details
        with st.expander("See analysis details"):
            st.write(f"**Original text:** '{user_input}'")
            st.write(f"**Sentiment score:** {score:.2f} (range: -1 to +1)")
            st.write(f"**Safety check:** {'✅ Passed' if is_text_safe(user_input) else '❌ Filtered'}")
            
    else:
        st.warning("Please enter some text to analyze!")

# Teacher mode toggle
if st.checkbox("Enable Teacher Mode"):
    show_teacher_mode()

# Footer
st.markdown("---")
st.caption("Built for learning - Safe for ages 12-16 | Uses TextBlob sentiment analysis")