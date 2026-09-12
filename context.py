import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY
)

# Initialize message history with system persona
messages = [
    SystemMessage(content="You are a helpful assistant and answer in simple english and in a concise way.")
]

while True:
    question = input("Enter: ")
    if question.lower() == "exit":
        break
    
    # Append user question to history
    messages.append(HumanMessage(content=question))
    
    # Send cumulative conversation history to LLM
    ai_message = llm.invoke(messages)
    
    # Append response back into history to maintain continuous context
    messages.append(ai_message)
    
    print(ai_message.content)