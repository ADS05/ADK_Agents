from dotenv import load_dotenv
load_dotenv()  # This loads the GOOGLE_API_KEY from .env

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city: The name of the city (e.g., 'New York', 'Tokyo', 'London')

    Returns:
        A dictionary with status, city, and time
    """
    # Mock implementation - you could use a real timezone API
    times = {
        "New York": "10:30 AM",
        "Tokyo": "11:30 PM",
        "London": "3:30 PM"
    }

    if city in times:
        return {"status": "success", "city": city, "time": times[city]}
    else:
        return {"status": "error", "message": f"Unknown city: {city}"}

from google.adk.agents import LlmAgent

agent = LlmAgent(
    name="time_assistant",
    model="gemini-2.5-pro",
    tools=[get_current_time],
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose."
)

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
runner = Runner(agent=agent, app_name="time_app", session_service=session_service)

import asyncio
from google.genai import types

async def run_time_assistant():
    # Create session (from Step 3)
    session = await session_service.create_session(
        app_name="time_app",
        user_id="user1",
        session_id="session1"
    )

    # Send message
    content = types.Content(role='user', parts=[types.Part(text="What time is it in Tokyo?")])
    events = runner.run(user_id="user1", session_id="session1", new_message=content)

    # Process response
    for event in events:
        if event.is_final_response() and event.content:
            # Only print text parts, ignore function calls
            for part in event.content.parts:
                if part.text:
                    print(part.text)

# Run the async function
asyncio.run(run_time_assistant())
