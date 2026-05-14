from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    FewShotChatMessagePromptTemplate,
    SystemMessagePromptTemplate,
    ChatPromptTemplate
)
from langchain_core.output_parsers import CommaSeparatedListOutputParser, JsonOutputParser, PydanticOutputParser
load_dotenv()


llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=100
)

system_message = SystemMessagePromptTemplate.from_template(template=f"""You are an expert travel expert. Based on user location and ocation list best places to visit based on the user query and replay based on below format
Format: {CommaSeparatedListOutputParser().get_format_instructions()}""")

human_message = HumanMessagePromptTemplate.from_template(template="""I want to visit {location} on {ocation}""")

chat_prompt = ChatPromptTemplate([system_message, human_message])

output_parser = CommaSeparatedListOutputParser()

chain = chat_prompt | llm | output_parser

response = chain.batch([
    {
        'location': 'kolkata',
        'ocation':'durga puja'
    },
    {
        'location': 'kashmir',
        'ocation': 'bahu mela'
    }])

# for list in response:
#     print(list)
#     print("\n")

chain.get_graph().print_ascii()
