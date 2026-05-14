from dotenv import load_dotenv
import os
from operator import itemgetter
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableParallel
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    ChatPromptTemplate
)
from langchain_core.output_parsers import CommaSeparatedListOutputParser

load_dotenv()

llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)

# ✅ System Prompt (fixed wording)
system_message = SystemMessagePromptTemplate.from_template(
    f"""You are a travel expert.
Suggest best places to visit based on the given location.

Return output in this format:
{CommaSeparatedListOutputParser().get_format_instructions()}
"""
)

# ✅ Human Prompt
human_message = HumanMessagePromptTemplate.from_template(
    "I want to visit {location}"
)

chat_prompt = ChatPromptTemplate([system_message, human_message])

output_parser = CommaSeparatedListOutputParser()

# ✅ Define chains
chain = chat_prompt | llm | output_parser


# ✅ Parallel chain with proper input mapping
chain_combined = RunnableParallel(
    kolkata = itemgetter("kolkata") | chain,
    kashmir = itemgetter("kashmir") | chain
)

# ✅ Correct input structure
response = chain_combined.invoke({
    "kolkata": {"location": "Kolkata"},
    "kashmir": {"location": "Kashmir"}
})

# ✅ Print output
print("Kolkata:", response["kolkata"])
print("Kashmir:", response["kashmir"])