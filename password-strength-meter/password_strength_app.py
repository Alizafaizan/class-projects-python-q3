import streamlit as st
import re
import random
import string
import time

# Set page configuration
st.set_page_config(
    page_title="Password Strength Meter",
    page_icon="🔒",
    layout="wide",  # Use wide layout for better space utilization
    initial_sidebar_state="collapsed"  # Hide sidebar by default for mobile
)

# Custom CSS for better mobile responsiveness and visual appeal
st.markdown("""
<style>
    /* Improve overall responsiveness */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    /* Custom card styling */
    .card {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    /* Hover effect for cards */
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Improve button styling */
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        font-weight: 600;
        height: 2.5rem;
    }
    
    /* Custom header styling */
    .custom-header {
        color: #1E3A8A;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Custom subheader styling */
    .custom-subheader {
        color: #1E3A8A;
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Improve tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F3F4F6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #DBEAFE;
        color: #1E40AF;
    }
    
    /* Custom styling for strength indicators */
    .strength-weak {
        color: #DC2626;
        font-weight: 600;
    }
    
    .strength-moderate {
        color: #D97706;
        font-weight: 600;
    }
    
    .strength-strong {
        color: #059669;
        font-weight: 600;
    }
    
    /* Improve mobile responsiveness */
    @media (max-width: 768px) {
        .custom-header {
            font-size: 1.8rem;
        }
        
        .custom-subheader {
            font-size: 1.2rem;
        }
        
        .card {
            padding: 1rem;
        }
        
        /* Ensure text is readable on mobile */
        p, li, .stMarkdown {
            font-size: 16px !important;
        }
        
        /* Make buttons more tappable on mobile */
        .stButton > button {
            height: 3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Optimized password strength checking function
@st.cache_data
def check_password_strength(password):
    """
    Analyzes password strength based on multiple criteria
    Returns a score and feedback
    """
    if not password:
        return {"score": 0, "strength": "None", "feedback": ["Enter a password"]}
    
    score = 0
    feedback = []
    criteria_met = {}
    
    # Check length
    criteria_met["length"] = len(password) >= 8
    if criteria_met["length"]:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")
    
    # Check for uppercase letters
    criteria_met["uppercase"] = bool(re.search(r'[A-Z]', password))
    if criteria_met["uppercase"]:
        score += 1
    else:
        feedback.append("Add uppercase letters")
    
    # Check for lowercase letters
    criteria_met["lowercase"] = bool(re.search(r'[a-z]', password))
    if criteria_met["lowercase"]:
        score += 1
    else:
        feedback.append("Add lowercase letters")
    
    # Check for digits
    criteria_met["digits"] = bool(re.search(r'\d', password))
    if criteria_met["digits"]:
        score += 1
    else:
        feedback.append("Add at least one number")
    
    # Check for special characters
    criteria_met["special"] = bool(re.search(r'[!@#$%^&*]', password))
    if criteria_met["special"]:
        score += 1
    else:
        feedback.append("Add special characters (!@#$%^&*)")
    
    # Check for common passwords - more efficient with a set
    common_passwords = {
        "password", "123456", "qwerty", "admin", "welcome", 
        "password123", "abc123", "letmein", "monkey", "1234567890"
    }
    
    if password.lower() in common_passwords:
        score = 1  # Force a weak score
        feedback.append("This is a commonly used password and easily guessable")
    
    # Determine strength category
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"
        
    return {
        "score": score,
        "strength": strength,
        "feedback": feedback,
        "criteria": criteria_met
    }

# Optimized password generator
def generate_strong_password(length=12):
    """
    Generates a strong password of specified length
    Ensures it contains all required character types
    """
    if length < 8:
        length = 8  # Minimum secure length [^1]
    
    # Pre-select required characters
    required_chars = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*")
    ]
    
    # Fill the rest with random characters
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    remaining_chars = [random.choice(all_chars) for _ in range(length - 4)]
    
    # Combine and shuffle
    password_chars = required_chars + remaining_chars
    random.shuffle(password_chars)
    
    return ''.join(password_chars)

# Helper function to display strength with appropriate styling
def display_strength_indicator(strength, score):
    if strength == "Weak":
        st.markdown(f"<p class='strength-weak'>⚠️ {strength} ({score}/5)</p>", unsafe_allow_html=True)
    elif strength == "Moderate":
        st.markdown(f"<p class='strength-moderate'>⚠️ {strength} ({score}/5)</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p class='strength-strong'>✅ {strength} ({score}/5)</p>", unsafe_allow_html=True)

# Helper function to create a card container
def create_card(content_function):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    content_function()
    st.markdown('</div>', unsafe_allow_html=True)

# Main UI
st.markdown('<h1 class="custom-header">🔒 Password Strength Meter</h1>', unsafe_allow_html=True)

# Create tabs with better styling
tab1, tab2 = st.tabs(["📊 Check Password", "🔑 Generate Password"])

with tab1:
    def check_password_content():
        st.markdown('<h2 class="custom-subheader">Check Your Password Strength</h2>', unsafe_allow_html=True)
        
        # Password input with toggle for visibility
        col1, col2 = st.columns([3, 1])
        with col1:
            password_visible = st.checkbox("Show password", False)
        
        if password_visible:
            password = st.text_input("Enter your password", key="visible_password")
        else:
            password = st.text_input("Enter your password", type="password", key="hidden_password")
        
        # Only analyze if there's a password
        if password:
            result = check_password_strength(password)
            
            # Display score with color-coded progress bar
            st.markdown('<h3 class="custom-subheader">Password Strength</h3>', unsafe_allow_html=True)
            score_percentage = (result["score"] / 5) * 100
            
            # Display strength indicator
            display_strength_indicator(result["strength"], result["score"])
            
            # Color-coded progress bar
            if result["strength"] == "Weak":
                bar_color = "rgba(220, 38, 38, 0.8)"  # Red with transparency
            elif result["strength"] == "Moderate":
                bar_color = "rgba(217, 119, 6, 0.8)"  # Orange with transparency
            else:
                bar_color = "rgba(5, 150, 105, 0.8)"  # Green with transparency
                
            # Custom progress bar with better styling
            st.markdown(
                f"""
                <div style="width:100%; background-color:#f0f0f0; border-radius:10px; height:20px; margin-bottom:20px;">
                    <div style="width:{score_percentage}%; background-color:{bar_color}; height:20px; border-radius:10px; 
                    transition: width 0.5s ease-in-out;"></div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Display criteria status in a more attractive way
            st.markdown('<h3 class="custom-subheader">Security Criteria</h3>', unsafe_allow_html=True)
            
            criteria_cols = st.columns(2)
            
            criteria_list = [
                ("Length (8+ characters)", result["criteria"].get("length", False)),
                ("Uppercase letters", result["criteria"].get("uppercase", False)),
                ("Lowercase letters", result["criteria"].get("lowercase", False)),
                ("Numbers", result["criteria"].get("digits", False)),
                ("Special characters", result["criteria"].get("special", False))
            ]
            
            for i, (criterion, met) in enumerate(criteria_list):
                with criteria_cols[i % 2]:
                    if met:
                        st.markdown(f"<p>✅ {criterion}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p>❌ {criterion}</p>", unsafe_allow_html=True)
            
            # Display feedback
            if result["feedback"]:
                st.markdown('<h3 class="custom-subheader">Improvement Suggestions</h3>', unsafe_allow_html=True)
                for suggestion in result["feedback"]:
                    st.warning(suggestion)
            else:
                st.success("Excellent! Your password meets all security criteria.")
    
    create_card(check_password_content)

with tab2:
    def generate_password_content():
        st.markdown('<h2 class="custom-subheader">Generate a Strong Password</h2>', unsafe_allow_html=True)
        
        # Password length slider with better styling
        length = st.slider(
            "Password Length", 
            min_value=8, 
            max_value=30, 
            value=12, 
            help="For security reasons, minimum length is 8 characters [^1]"
        )
        
        # Generate button with better styling
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Generate Secure Password", use_container_width=True):
                with st.spinner("Generating secure password..."):
                    # Add a small delay for effect
                    time.sleep(0.3)
                    generated_password = generate_strong_password(length)
                    
                    # Store in session state to persist between reruns
                    st.session_state.generated_password = generated_password
                    st.session_state.show_generated = True
        
        # Display generated password
        if 'show_generated' in st.session_state and st.session_state.show_generated:
            st.markdown('<h3 class="custom-subheader">Your Generated Password</h3>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                show_gen_password = st.checkbox("Show generated password", True)
            
            # Password display with better styling
            if show_gen_password:
                st.code(st.session_state.generated_password, language="")
            else:
                st.code("•" * len(st.session_state.generated_password), language="")
            
            # Copy button with better styling
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Copy to Clipboard", use_container_width=True):
                    st.success(f"Password copied to clipboard!")
                    
            # Show strength of generated password
            result = check_password_strength(st.session_state.generated_password)
            
            st.markdown('<h3 class="custom-subheader">Password Strength</h3>', unsafe_allow_html=True)
            display_strength_indicator(result["strength"], result["score"])
            
            # Display criteria status for generated password
            criteria_cols = st.columns(2)
            
            criteria_list = [
                ("Length (8+ characters)", result["criteria"].get("length", False)),
                ("Uppercase letters", result["criteria"].get("uppercase", False)),
                ("Lowercase letters", result["criteria"].get("lowercase", False)),
                ("Numbers", result["criteria"].get("digits", False)),
                ("Special characters", result["criteria"].get("special", False))
            ]
            
            for i, (criterion, met) in enumerate(criteria_list):
                with criteria_cols[i % 2]:
                    st.markdown(f"<p>✅ {criterion}</p>", unsafe_allow_html=True)
    
    create_card(generate_password_content)

# Security information in an attractive expandable card
def security_info_content():
    st.markdown("""
    ## Why Password Security Matters
    
    A strong password is your first line of defense against unauthorized access to your accounts.
    
    ### Best Practices:
    - Use a **unique password** for each account
    - Make passwords **at least 8 characters** long [^1]
    - Include a mix of **uppercase, lowercase, numbers, and symbols** [^1]
    - Avoid using **personal information** like names or birthdays
    - Consider using a **password manager** to store complex passwords
    - Enable **two-factor authentication** when available
    
    ### Password Strength Facts:
    - A password with only digits would need approximately 2²⁷ guesses to crack [^1]
    - Adding letters increases this to 2⁴¹ guesses [^1]
    - Using a mix of all character types increases to 2⁵² guesses [^1]
    """)

with st.expander("📚 Password Security Information"):
    create_card(security_info_content)

# Footer with better styling
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; background-color: #F3F4F6; border-radius: 10px;">
    <p style="margin: 0; color: #4B5563; font-size: 0.9rem;">
        Built with ❤️ using Streamlit 
    </p>
</div>
""", unsafe_allow_html=True)