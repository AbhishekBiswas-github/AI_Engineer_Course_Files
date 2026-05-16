from langchain_core.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

TEMPLATE_S = """
{description}
"""

system_message = SystemMessagePromptTemplate.from_template(template=TEMPLATE_S)

TEMPLATE_H = """
I have resently adopted a {pet}. Give me names of {pet}
"""

human_message = HumanMessagePromptTemplate.from_template(template=TEMPLATE_H)

chat_prompt = ChatPromptTemplate(
    [system_message, human_message]
)

chat = chat_prompt.invoke({
    'description': "You are pet consultant. Suggest best 5 names of both male and Female Gender of the pet mentioned. No Extra names",
    'pet': 'Golden Retriever'
})

# print(f"""
# System Message: {chat.messages[0].content}
# Human Message: {chat.messages[1].content}
# """)

llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=100
)

chain = chat_prompt | llm

print(chain.invoke({
    'description': "You are pet consultant.",
    'pet': 'Golden Retriever'    
}).content)

# chain.get_graph().print_ascii()