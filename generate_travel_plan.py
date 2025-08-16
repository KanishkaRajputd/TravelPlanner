from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_community.tools import tool
import requests
import streamlit as st
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from pydantic import BaseModel, Field

openai_api_key = st.secrets["OPENAI_API_KEY"]
tavily_api_key = st.secrets["TAVILY_API_KEY"]
weatherstack_api_key = st.secrets["WEATHERSTACK_API_KEY"]
aviationstack_api_key = st.secrets["AVIATIONSTACK_API_KEY"]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_api_key)
tavily_search = TavilySearch(max_results=5, topic="general", tavily_api_key=tavily_api_key)


@tool
def web_search(query):
    """
    Search the web for the given query.
    """
    response = tavily_search.invoke({"query": query})
    content = ''
    for result in response.get("results", []):
        content += f"{result.get('content')} "

    print(content, 'web_search')
    return content


@tool
def weather_search(location):
    """
    Search for the weather in a given location.
    """
    response = requests.get(f"https://api.weatherstack.com/current?access_key={st.secrets['WEATHERSTACK_API_KEY']}&query={location}")
    json_response = response.json()
    print(json_response.get("current", {}).get("temperature", 0), 'weather_search')
    return json_response.get("current", {}).get("temperature", 0)

class HotelSearchArgs(BaseModel):
    """Arguments for hotel search tool"""
    location: str = Field(description="The city name where to search for hotels (e.g., 'Paris', 'Mumbai', 'London')")
    prefered_time: int = Field(default=7, description="Number of days for the hotel stay (default: 7 days)")

@tool(args_schema=HotelSearchArgs)
def hotel_search(location: str, prefered_time: int = 7):
    """
    Search for hotels in a given city for a specific number of days.
    
    Args:
        location: The city name (e.g., 'Paris', 'Mumbai', 'London')
        prefered_time: Number of days for hotel stay (defaults to 7 if not provided)
    """
    try:
        response = tavily_search.invoke({"query": f"best hotels in {location} for {prefered_time} days booking recommendations"})
        content = ''
        for result in response.get("results", []):
            content += f"{result.get('content')} "

        print(f"Hotel search for {location} ({prefered_time} days): {content[:100]}...", 'hotel_search')
        return content if content else f"No hotel information found for {location}"
    except Exception as e:
        print(f"Error in hotel_search: {e}")
        return f"Error searching hotels for {location}: {str(e)}"
   

    
def generate_travel_plan(traveling_from, traveling_to, days, interests, prefered_time):
    """
    Generate a comprehensive travel plan for a given user input.
    """
    user_query = f"""Create a comprehensive travel plan for {traveling_to} for {days} days with interests in {interests}, preferred activity time: {prefered_time}, traveling from {traveling_from}.

Tasks to complete:
1. Get current weather information for {traveling_to}
2. Search for best hotels in {traveling_to} for {days} days (use hotel_search tool with location="{traveling_to}" and prefered_time={days})
3. Research top attractions and activities matching the interests: {interests}
4. Create a detailed itinerary optimized for {prefered_time} activities

Format the response in bullet points with clear sections:
- Weather Information
- Hotel Recommendations 
- Daily Itinerary
- Local Tips and Recommendations"""

    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm = llm, tools = [web_search, weather_search, hotel_search], prompt=prompt)

    agent_executor = AgentExecutor(agent=agent, tools=[web_search, weather_search, hotel_search], verbose=True)

    response = agent_executor.invoke({"input": user_query})
    print(response.get("output", ""), 'generate_travel_plan')
    return response.get("output", "")





