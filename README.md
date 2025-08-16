# ✈️ AI-Powered Travel Planner

A beautiful Streamlit application that creates comprehensive, personalized travel plans using AI agents and real-time data.

## 🌟 Features

- **Smart Travel Planning**: AI-powered itinerary generation based on your interests
- **Real-time Flight Search**: Find and compare flight options with prices
- **Weather Integration**: Current weather conditions and packing recommendations  
- **Accommodation Suggestions**: Budget, mid-range, and luxury hotel options
- **Local Insights**: Cultural tips, transportation advice, and must-try foods
- **Budget Estimation**: Complete cost breakdown for your trip
- **Beautiful Dark UI**: Modern, responsive interface with smooth animations

## 🚀 Getting Started

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone <your-repo-url>
cd TravelPlanner
pip install -r requirements.txt
```

### 2. API Keys Setup

You'll need to obtain API keys from the following services:

#### Required APIs:
- **OpenAI API** (for AI travel planning)
  - Get from: https://platform.openai.com/api-keys
  
- **Tavily Search API** (for web search)
  - Get from: https://tavily.com/
  
- **WeatherStack API** (for weather data)
  - Get from: https://weatherstack.com/
  
- **AviationStack API** (for flight information)
  - Get from: https://aviationstack.com/

#### Configure Secrets:

1. Open the `.streamlit/secrets.toml` file
2. Replace the placeholder values with your actual API keys:

```toml
# Replace "your_*_api_key_here" with your actual keys
OPENAI_API_KEY = "sk-your-openai-key-here"
TAVILY_API_KEY = "your-tavily-key-here" 
WEATHERSTACK_API_KEY = "your-weatherstack-key-here"
AVIATIONSTACK_API_KEY = "your-aviationstack-key-here"
```

3. Save the file

### 3. Run the Application

```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 How to Use

1. **Enter Departure City**: Where you're traveling from
2. **Destination**: City you want to visit
3. **Duration**: Number of days for your trip
4. **Interests**: What you enjoy (food, culture, museums, etc.)
5. **Travel Time Preference**: When you prefer activities (morning, afternoon, etc.)
6. **Generate Plan**: Click the button to create your personalized itinerary

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **AI Engine**: OpenAI GPT-4 with LangChain agents
- **Real-time Data**: Multiple API integrations
- **Search**: Tavily web search for current information

### Key Components
- `main.py`: Streamlit UI and user interface
- `handle_llm.py`: AI agents and API integrations
- `.streamlit/secrets.toml`: Secure API key storage

## 🔒 Security Notes

- Never commit your `.streamlit/secrets.toml` file to git
- The secrets file is automatically ignored by Streamlit Cloud
- API keys are accessed securely through `st.secrets`

## 📝 Example Output

Your travel plan will include:

✈️ **Flight Options** - Multiple flight choices with prices
🌤️ **Weather & Packing** - Current conditions and clothing advice  
🏨 **Accommodation** - Budget to luxury hotel recommendations
📅 **Daily Itinerary** - Detailed day-by-day activities
💰 **Budget Estimate** - Complete cost breakdown
📝 **Local Tips** - Cultural insights and practical advice

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Note**: Make sure to configure all API keys in the secrets file before running the application. The app will not function without proper API authentication.
