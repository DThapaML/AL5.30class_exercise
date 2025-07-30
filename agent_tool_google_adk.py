from google.adk.agents import Agent
from google.adk.tools import FunctionTool,ToolContext
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.google_llm import Gemini
from google.genai import types
import requests
import json
import asyncio
import os

os.environ["GOOGLE_API_KEY"] = "GOOGLE-API-Key"

def get_weather_report(latitude: float, longitude: float):
    """
    Get current weather and forecast for the next 5 hours based on latitude and longitude of provided city.
    
    Args: 
    The function take 2 argument:
    - Latitude: Latitude of the location.
    - Longitude: Longitude of the location.

    """
    try:
        url = (
                f"https://api.open-meteo.com/v1/forecast"
                f"?latitude={latitude}&longitude={longitude}"
                "&current_weather=true"
                "&hourly=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,rain"
                "&timezone=auto"
        )
        response = requests.get(url)
        data = response.json()
        current_weather = data.get("current_weather", {})
        hourly_data = data.get("hourly", {})
        if not current_weather:
            return "No current weather data available. Cannot provide weather information."
        
        result = {
            "current_weather": {
                "temperature": current_weather.get("temperature", "N/A"),
                "wind_speed": current_weather.get("windspeed", "N/A"),
                "time": current_weather.get("time", "N/A"),
            },
            "next_5_hours": [
                {
                    "time": hourly_data.get("time", [])[i],
                    "temperature": hourly_data.get("temperature_2m", [])[i],
                    "apparent_temperature": hourly_data.get("apparent_temperature", [])[i],
                    "relative_humidity": hourly_data.get("relative_humidity_2m", [])[i],
                    "wind_speed": hourly_data.get("wind_speed_10m", [])[i],
                    "rain": hourly_data.get("rain", [])[i],
                }
                for i in range(5)
            ]
        }
           
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": f"Error fetching weather data: {str(e)}"})
    
weather_tool = FunctionTool(func= get_weather_report)

#agent 
weather_agent = Agent(
    model= 'gemini-2.0-flash',
    name='weather_agent',
    tools=[weather_tool],
    instruction= """
 You are a helpful assistant that provides weather information to user.
**If the user asks about the weather in a specific city, first get the latitude and longitude of the specific city.**
**then use 'get_weather_report' tool with the retrive latitude and longitude and returns a json, provide the weather report to the user.**
**If the 'get_weather_report' tool returns an 'error' status, inform the user that the weather information for the specified city is not available and ask if they have another city in mind.**
You can handle these tasks sequentially if needed.
"""
)
#session and runner 
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name="weather_agent",user_id= "user1234", session_id=
                                                   '1234')
    runner = Runner(agent= weather_agent, app_name="weather_agent", session_service=session_service)
    return session,runner

async def call_agent_async(q):
    content = types.Content(role='user', parts=[types.Part(text=q)])
    session,runner = await setup_session_and_runner()
    events = runner.run_async(user_id= "user1234",session_id="1234", new_message= content)
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

asyncio.run(call_agent_async("kathmandu weather"))
