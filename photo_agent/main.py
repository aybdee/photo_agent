from dotenv import load_dotenv
from environment import PhotoEnvironment
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI
from tools import *

load_dotenv()

llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

environment = PhotoEnvironment()

check_photo_state = get_photo_state_tool(environment)
place_subject = get_place_subject_tool(environment)
add_light = get_add_light_tool(environment)

tools = [check_photo_state, place_subject, add_light]
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
)

response = agent.run(
    "Set up a basic photo scene with a subject in the center and two lights.",
)
