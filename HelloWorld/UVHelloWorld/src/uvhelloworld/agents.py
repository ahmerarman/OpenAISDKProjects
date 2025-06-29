from agents import Agent, InputGuardrail # type: ignore
from dotenv import load_dotenv
import os

import src.uvhelloworld.guardrail as gd
import src.uvhelloworld.tools as tl

load_dotenv()

MODEL=os.getenv("MODEL", "gpt-4o-mini")
if not MODEL:
    raise RuntimeError("Missing MODEL in environment. Set the MODEL environment variable.")

agent = Agent(
    name="Assistant",
    handoff_description="Helpful assistant for general purpose questions",
    instructions="You are a helpful assistant",
    model=MODEL,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
    model=MODEL,
    input_guardrails=[
        InputGuardrail(guardrail_function=gd.homework_guardrail),
        ]
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    model=MODEL,
    input_guardrails=[
        InputGuardrail(guardrail_function=gd.homework_guardrail),
        ]
)

weather_agent = Agent(
    name="Weather agent",
    instructions="Always show response as received from the get_weather tool. Do not add any additional information.",
    model=MODEL,
    handoff_description="Specialist agent for weather questions",
    tools=[tl.get_weather],
    input_guardrails=[
        InputGuardrail(guardrail_function=gd.weather_guardrail),
        ]
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="""You determine which agent to use based on the user's question.
                    If the user asks so many questions at a time,
                    you will break the question into separate parts,
                    and call the corresponding agent for each part.
                    If the user asks about homework,
                    you will call the history_tutor_agent or math_tutor_agent.
                    If the user asks about weather, you will call the weather_agent.
                    Otherwise, you will call the assistant agent.""",
    model=MODEL,
    handoffs=[agent, history_tutor_agent, math_tutor_agent, weather_agent],
)
