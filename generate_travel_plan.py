from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_community.tools import tool
import requests
import streamlit as st
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor

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

@tool
def hotel_search(location: str):
    """
    Search for the hotels in a given location.
    """
    response = tavily_search.invoke({"query": f"Hotels in {location}"})
    content = ''
    for result in response.get("results", []):
        content += f"{result.get('content')} "

    print(content, 'hotel_search')
    return content
   

    
def generate_travel_plan(traveling_from, traveling_to, days, interests, prefered_time):
    """
    Generate a comprehensive travel plan for a given user input.
    """
    user_query = f"""Create a travel plan for {traveling_to} for {days} days with {interests} in {prefered_time} and traveling from {traveling_from} starting according to weather. 
    Suggest best hotels in {traveling_to} city.
    Note: Response should be in bullet points.
    ."""

    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm = llm, tools = [web_search, weather_search, hotel_search], prompt=prompt)

    agent_executor = AgentExecutor(agent=agent, tools=[web_search, weather_search, hotel_search], verbose=True)

    response = agent_executor.invoke({"input": user_query})
    print(response.get("output", ""), 'generate_travel_plan')
    return response.get("output", "")





