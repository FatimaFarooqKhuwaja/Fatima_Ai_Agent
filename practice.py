from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from dotenv import load_dotenv
import os
from agents.run import RunConfig



load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model =  "gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)
@function_tool
def about_me_tool():
    return "Mujhe Fatima Farooq Khuwaja ne banaya hai. "
    "Woh ek talented Full Stack Developer, Python Expert aur Agentic AI Engineer hain 😊"


coordinator = Agent(
    name="Fatima's AI Assistant",
    instructions="An AI assistant created by Fatima Farooq Khuwaja, a Full Stack Developer and Python Expert.",
    tools=[about_me_tool],
    model=model,
)
