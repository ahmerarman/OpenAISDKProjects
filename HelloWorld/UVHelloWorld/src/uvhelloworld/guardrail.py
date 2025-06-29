from agents import Agent, GuardrailFunctionOutput, Runner # type: ignore
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

MODEL=os.getenv("MODEL", "gpt-4o-mini")
if not MODEL:
    raise RuntimeError("Missing MODEL in environment. Set the MODEL environment variable.")

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

class WeatherOutput(BaseModel):
    is_weather: bool
    city: str
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
    model=MODEL
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

weather_guardrail_agent = Agent(
    name="Weather Guardrail check",
    instructions="Check if the user is asking about weather.",
    output_type=WeatherOutput,
    model=MODEL
)

async def weather_guardrail(ctx, agent, input_data):
    result = await Runner.run(weather_guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(WeatherOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_weather,
    )
