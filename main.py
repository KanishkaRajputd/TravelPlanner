import streamlit as st
import time
from handle_llm import generate_travel_plan

# Page configuration
st.set_page_config(
    page_title="AI-Powered Travel Planner",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }
    
    .stApp {
        background-color: #0f1419;
        color: #ffffff;
    }
    
    .main-header {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #ffffff;
    }
    
    .sub-header {
        text-align: center;
        font-size: 1.2rem;
        color: #a8b3c1;
        margin-bottom: 3rem;
        line-height: 1.5;
    }
    
    .form-container {
        background: linear-gradient(135deg, #1a2332 0%, #2d3748 100%);
        border-radius: 20px;
        padding: 2.5rem;
        border: 1px solid #374151;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
    }
    
    .stTextInput > div > div > input {
        background-color: #374151;
        border: 1px solid #4b5563;
        border-radius: 12px;
        color: #ffffff;
        font-size: 1.1rem;
        padding: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    .stSelectbox > div > div > div {
        background-color: #374151;
        border: 1px solid #4b5563;
        border-radius: 12px;
        color: #ffffff;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #374151;
        border: 1px solid #4b5563;
        border-radius: 12px;
        color: #ffffff;
        font-size: 1.1rem;
        padding: 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: #ffffff;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
    }
    
    .field-label {
        color: #e5e7eb;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .loading-container {
        background: #1f2937;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        border: 1px solid #374151;
        margin-top: 2rem;
    }
    
    .loading-text {
        color: #f472b6;
        font-size: 1.2rem;
        font-weight: 500;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stSelectbox label {
        color: #e5e7eb !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    
    .stTextInput label {
        color: #e5e7eb !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    
    .stTextArea label {
        color: #e5e7eb !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    
</style>
""", unsafe_allow_html=True)

def main():
    # Header section
    st.markdown('<h1 class="main-header">✈️ AI-Powered Travel Planner</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Get real-time travel plans, weather, and hotel recommendations powered by Open AI.</p>', unsafe_allow_html=True)
    
    # Form container
    with st.container():
        
        # Form inputs
        departure_city = st.text_input(
            "Enter the city you're traveling from:",
            placeholder="Enter the city you're traveling from: ",
            key="departure_input"
        )
        
        city = st.text_input(
            "Enter the city you're visiting:",
            placeholder="Enter the city you're visiting: ",
            key="city_input"
        )
        
        days = st.text_input(
            "How many days are you staying?",
            placeholder="Enter the number of days you're staying: ",
            key="days_input"
        )
        
        interests = st.text_area(
            "What are your interests?",
            placeholder="What are your interests? eg:Food, culture, museums, historical sites",
            height=100,
            key="interests_input"
        )
        
        travel_time = st.selectbox(
            "Preferred travel time:",
            ["full-day", "half-day", "morning", "afternoon", "evening"],
            index=0,
            key="travel_time_input"
        )
        
        date = st.date_input(
            "Enter the date of your travel:",
            key="date_input"
        )
        
        # Generate button
        generate_clicked = st.button("Generate Travel Plan", key="generate_btn")
    
    # Travel plan generation
    if generate_clicked:
        # Validate inputs
        if not city or not days or not interests:
            st.error("Please fill in all required fields: destination city, number of days, and interests.")
        else:
            try:
                # Convert days to integer
                days_int = int(days)
                if days_int <= 0:
                    st.error("Please enter a valid number of days (greater than 0).")
                else:
                    st.markdown('''
                    <div class="loading-container">
                        <p class="loading-text">🌸 Generating travel plan...</p>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Show loading progress
                    for i in range(1, 31, 5):
                        progress_bar.progress(i)
                        if i < 15:
                            status_text.text("Analyzing destination and searching flights...")
                        elif i < 25:
                            status_text.text("Finding best attractions and activities...")
                        else:
                            status_text.text("Checking weather and accommodation options...")
                        time.sleep(0.2)
                    
                    # Generate the actual travel plan
                    try:
                        result = generate_travel_plan(
                            traveling_to=city,
                            traveling_from=departure_city,
                            date=date,
                            days=str(days_int),
                            interests=interests,
                            prefered_time=travel_time
                        )
                        
                        progress_bar.progress(100)
                        status_text.text("Travel plan generated successfully!")
                        
                        # Display the travel plan
                        st.success(f"🎉 Your personalized travel plan for {city} is ready!")
                        
                        # Create expandable sections for better organization
                        with st.expander("📋 Complete Travel Plan", expanded=True):
                            st.markdown(result)
                        
                        # Add some action buttons
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("Generate New Plan", key="new_plan"):
                                st.rerun()
                        with col2:
                            if st.button("Modify Preferences", key="modify"):
                                st.info("Change your preferences above and generate again!")
                        with col3:
                            if st.button("Save Plan", key="save"):
                                st.info("Plan saved to your session!")
                                
                    except Exception as e:
                        st.error(f"Sorry, there was an error generating your travel plan: {str(e)}")
                        st.info("Please check that your API keys are properly configured in the .streamlit/secrets.toml file.")
                        
            except ValueError:
                st.error("Please enter a valid number for days.")

if __name__ == "__main__":
    main()