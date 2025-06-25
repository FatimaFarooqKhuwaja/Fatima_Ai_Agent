# Fatima AI Assistant - Streamlit App
import streamlit as st
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
import os
from dotenv import load_dotenv
import asyncio

# 🌱 Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    st.error("GEMINI_API_KEY environment variable is not set.")
    st.stop()

# 🌐 Setup Gemini client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 💬 Gemini Model Configuration
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

# 🛠️ Function Tool - about me
@function_tool
def about_me_tool(query: str) -> str:
    """Responds based on query: who made you, who are you vs who is Fatima vs tell me about yourself."""
    
    query_lower = query.lower()

    if "who made you" in query_lower or "who is your creator" in query_lower:
        return (
            "Mujhe Fatima Farooq Khuwaja ne banaya hai. "
            "Woh ek talented Full Stack Developer , Python Expert our Agentic Ai Engineer hain 😊"
        )
    
    elif "who is fatima" in query_lower or "tell me about fatima" in query_lower:
        return (
            "Fatima Farooq Khuwaja ek passionate Full Stack Engineer hain jo currently 2nd year (Intermediate) ki student hain. "
            "Woh Next.js aur Python dono me expert hain. "
            "Fatima GIAIC ki student hain aur abhi Quarter 3 me Agentic AI parh rahi hain. "
            "Unhon ne 100+ websites develop ki hain, jisme eCommerce, banking, QCommerce, music gallery, portfolio, blog, fullstack form, committee apps waghera shamil hain. "
            "Python me unke projects me password strength meter,personal library manager, password generator,unit converter, money generator, calculator aur random joke generator jaise apps shamil hain. "
            "Unka aim AI aur software engineering me excellence hasil karna hai. 🚀"
        )

    else:
        return (
            "Main ek AI chatbot hoon jo Fatima Farooq Khuwaja ne banaya hai. "
            "Woh ek Full Stack Developer aur Python expert hain. "
            "Agar aap Fatima ke baare me detail se jan'na chahte hain to poochh sakte hain. 😊"
        )


# 🧠 Coordinator Agent with tool
coordinator_agent = Agent(
    name="coordinator",
    instructions="""
You are a smart AI assistant that decides how to respond based on the user's input.

🔹 If the user asks **about your creator** (e.g. "Who made you?", "Who created you?", "What do you know about yourself?"),
   then call the `about_me_tool` to give a brief response stating that you were created by Fatima Farooq Khuwaja.

🔹 If the user asks **about Fatima Farooq** specifically (e.g. "Who is Fatima?", "Tell me about Fatima Farooq", "Who is your developer?"),
   then call the `about_me_tool` and provide detailed information about her background, work, and achievements.

🔹 For all other general questions (e.g. stories, facts, casual chats), respond directly using your own model knowledge.

🔸 Do not overshare or give extra personal information unless the user explicitly asks for it.
""",
    tools=[about_me_tool],
)


# 🧠 Streamlit Chat UI
st.set_page_config(page_title="Fatima AI Assistant", page_icon="🤖")

st.title("🤖Fatima's Assistant")

st.write("""
Welcome! I'm an intelligent assistant created by **Fatima Farooq Khuwaja**.  
What can I help with?
""")


# 🗨️ Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 📥 User input
user_input = st.chat_input("Say something...")

# ⚙️ Async call to coordinator agent
async def get_response(prompt):
    result = await Runner.run(
        coordinator_agent,
        input=prompt,
        run_config=config,
    )
    return result.final_output.strip()

# ▶️ Handle user input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        bot_response = asyncio.run(get_response(user_input))

    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# 💬 Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

