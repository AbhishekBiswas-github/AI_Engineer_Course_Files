🚀 Thrilled to share my latest project: #QuickQuery — A Natural Language to SQL RAG Pipeline!

Bridge the gap between plain English and structured SQL. Instead of requiring users to know database syntax, #QuickQuery allows anyone to chat with their MySQL database naturally and get validated, optimized SQL queries in real-time.

While many Text-to-SQL setups struggle with large database schemas or hallucinated column names, I engineered this project with a robust production-grade architecture to maximize query accuracy and minimize latency.

🛠️ Key Technical Highlights:
1. Two-Stage Schema Retrieval: Avoided the "lost in the middle" token trap by not dumping the entire database schema into the LLM prompt. Instead, I built a two-stage pipeline: a Bi-encoder (via SentenceTransformers and Pinecone) casts a wide net for relevant tables, followed by a Cross-encoder (ms-marco-MiniLM-L6-v2) re-ranker for high-precision context filtering.
2. Semantic Schema Enrichment: Enriched standard DESCRIBE table outputs with 93 semantic column descriptions. This gives the LLM precise context on ambiguous column values (e.g., specific status flags like pending, shipped, cancelled), heavily increasing generation accuracy.
3. Self-Correcting Auto-Retry Loop: If a generated query fails live execution, an automated loop captures the native database error message and feeds it back into a focused regeneration prompt. The pipeline dynamically self-corrects up to 3 times before returning a result.
4. Context-Aware Chat: Built a sliding window memory system via LangChain that tracks the last 5 conversation turns, enabling seamless follow-up questions (e.g., "Show me last month's orders" followed by "Now group that by customer").

💻 The Tech Stack:
1. Orchestration: LangChain
2. LLM Inference: Groq Cloud (llama-3.1-8b-instant / llama-3.3-70b-versatile)
3. Vector DB: Pinecone (Serverless)
4. Database Engine: MySQL
5. UI Frontend: Streamlit (Featuring a professional dark-theme interface, query viewer, and live 5-row table browser)

Building this project deepened my understanding of combining vector search with traditional relational databases, tuning cross-encoder thresholds, and handling deterministic code generation with non-deterministic LLMs.

Check out the architecture diagram and codebase below! 👇

📁 GitHub Repository: https://github.com/AbhishekBiswas-github/AI-Engineer-Projects/tree/main/Streamlit_Projects/QuickQuery
#AI #MachineLearning #GenerativeAI #RAG #LLM #TextToSQL #DataEngineering #LangChain #Streamlit #Python #VectorDatabase
