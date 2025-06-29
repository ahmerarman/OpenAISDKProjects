from dotenv import load_dotenv
import os, openai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in environment")
openai.api_key = OPENAI_API_KEY

from agents import Runner # type: ignore
import src.uvhelloworld.agents as ag

def main():
    try:
        while True:
            user_input = input("Enter your question (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break

            # Run the triage agent with the user's input
            result = Runner.run_sync(ag.triage_agent, user_input)
            print(result.final_output)
#        result = Runner.run_sync(ag.triage_agent, "who was the first president of the united states?")
#        print(result.final_output)

#        result = Runner.run_sync(ag.triage_agent, "write an essay on, what is life?")
#        print(result.final_output)

#        result = Runner.run_sync(ag.triage_agent, "How is the weather in Karachi?")
#        print(result.final_output)

    except Exception as e:
        print(f"An error occured: {e}")

main()
