from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# pdf loader
pdf_loader = PyPDFLoader(
    file_path="example.pdf"
)

# pdf pages
pdf_pages = pdf_loader.load()

# complete content
# content = ""
for i in pdf_pages:
    i = " ".join(i.page_content.split())

# text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 2000,
    chunk_overlap = 100,
    separators=["\n\n", "\n", "."]
)

# # chunking
chunks = text_splitter.split_documents(documents=pdf_pages)
# for i, chunk in enumerate(chunks):
#     print(f"chunk number {i}\nChunk: {chunk}", end="\n\n")

# Embedding model
# model_path = 'all-MiniLM-L6-v2'
model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=model,
    persist_directory="./new_vector_db",
    collection_metadata={
        "hnsw:space": "cosine"
    }
)

retrieved_docs = vectorstore.similarity_search(
    query="Hospitalization Expenses",
    k=3
)

for doc in retrieved_docs:
    print(f"""
Document Content: {" ".join(doc.page_content.split())}
Document ID: {doc.id}
Document Metadata: {doc.metadata}
\n
""")
