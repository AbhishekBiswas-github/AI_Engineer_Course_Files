from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
from langchain_core.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)
from langchain_groq import ChatGroq

load_dotenv()

# pdf loader
pdf_loader = PyPDFLoader(
    file_path="example.pdf"
)

# pdf pages
pdf_pages = pdf_loader.load()

# text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 2000,
    chunk_overlap = 100,
    separators=["\n\n", "\n", "."]
)

# chunking
chunks = text_splitter.split_documents(pdf_pages)

# Embedding model
model_path = 'sentence-transformers/all-MiniLM-L6-v2'
model = SentenceTransformer(model_path)

# Vector Database connection
pinecone_client = Pinecone(
    api_key= os.environ.get('PINECONE_API_KEY')
)

# Index name
INDEX_NAME = 'my-index'

# list of existing indexes
# index_list = [index['name'] for index in pinecone_client.list_indexes()]

# # index creation
# if INDEX_NAME not in index_list:
#     pinecone_client.create_index(
#         name=INDEX_NAME,
#         dimension=model.get_embedding_dimension(),
#         metric='cosine',
#         spec=ServerlessSpec(
#             cloud='aws',
#             region='us-east-1'
#         )
#     )
#     print(f"Index: {INDEX_NAME} created Successfully")
# else:
#     print(f"Index: {INDEX_NAME} already created")


# index initialization
index = pinecone_client.index(name=INDEX_NAME)

# vector creation
# vectors = []
# for i, chunk in enumerate(chunks):
#     chunk_text = chunk.page_content
#     embedding = model.encode(chunk_text)
#     vectors.append({
#         "id": f"chunk_{i}",
#         "values": model.encode(chunk_text).tolist(),
#         "metadata": {
#             "text": chunk_text,
#             'title': chunk.metadata['title'],
#             'total_pages': chunk.metadata['total_pages'],
#             'source': chunk.metadata['source']
#         }
#     })


# # upserting vectors
# index.upsert(
#     vectors=vectors
# )
# print(f"{len(vectors)} vectors inserted successfully")

# querying the vector database
query = "List of Name, address, e-mail ID and contact number of the Grievance Redressal Officer"
query_embedding = model.encode(query).tolist()
response = index.query(
    vector=query_embedding,
    top_k= 3,
    include_metadata= True
)

# printing the chunks
complete_content = ""
for match in response.matches:
    complete_content += f"{match.metadata['text']} \n"


# Prompt creation
TEMPLATE_S = """You are a Smart AI Medical and Health Assistant. Based on the documents provided and the user query. You answer the query in well structured format keeping only the necessary details.
Below is complete content:
{retrieved_document} 
NO HELLUCINATION and NO PREAMBLE"""

system_message = SystemMessagePromptTemplate.from_template(template=TEMPLATE_S)

TEMPLATE_H = """Below is my query: {query}
I want to know everything related to the this query.
"""

human_message = HumanMessagePromptTemplate.from_template(template=TEMPLATE_H)

chat_prompt = ChatPromptTemplate([system_message, human_message])

llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0,
    # max_tokens=1000
)

chain = chat_prompt | llm

response = chain.invoke({
    'query': query,
    'retrieved_document': complete_content
})

print(response.content)

