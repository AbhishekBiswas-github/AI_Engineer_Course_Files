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

TEMPLATE_H = "Text: {text}\nSentiment:"

human_message = HumanMessagePromptTemplate.from_template(template=TEMPLATE_H)

TEMPLATE_AI = """{description}"""

ai_message = AIMessagePromptTemplate.from_template(template=TEMPLATE_AI)

chat_message = ChatPromptTemplate([human_message, ai_message])

example = [{
    'text': 'I loved this movie. The stroy line is awesome',
    'description':'positive'
},{
    'text': 'The product broke in two days',
    'description': 'negative'
}]

few_shot = FewShotChatMessagePromptTemplate(
    examples=example, example_prompt=chat_message
)

final_prompt = ChatPromptTemplate(
    [
        SystemMessagePromptTemplate.from_template(template="""
You are a sentiment classifier.
Always respond with exactly one word: 'positive' or 'negative'.
Do not leave the response empty."""),
        few_shot,
        human_message
    ]
)

chain = few_shot | llm

response = chain.invoke({
    'text':'I love mangoes'
})

# print(response)

print(PydanticOutputParser().get_format_instructions())