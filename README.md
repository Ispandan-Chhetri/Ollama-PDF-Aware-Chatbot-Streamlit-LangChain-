# Ollama-PDF-Aware-Chatbot-Streamlit-LangChain-

This project is a local, privacy-friendly chatbot built with Streamlit, LangChain, and Ollama that allows users to chat with PDF documents using a locally hosted large language model.

Users can upload one or more PDF files, which are automatically processed and added to a vector database. The chatbot then uses retrieval-augmented generation (RAG) to answer questions based only on the uploaded documents.

If the answer is not present in the document context, the model is instructed to clearly say that it does not know.

**✨  Features**

📄 Upload and ingest PDF documents
🔎 Semantic search over document content
💬 Conversational chat interface with memory
🧠 Local LLM inference using Ollama (no cloud APIs)
⚡ Streaming responses for real-time feedback
🗂️ Vector database integration via a custom VectorDB class


**🛠️ Tech Stack**

- Python
- Streamlit – Web UI
- LangChain – Prompting & orchestration
- Ollama – Local LLM runtime (llama3.2)
- Chroma / Vector Store (via VectorDB)
- PyPDF – PDF text extraction

**🧩 How It Works**

- PDFs are uploaded through the Streamlit UI
- Text is extracted and split into overlapping chunks
- Chunks are embedded and stored in a vector database
- User questions trigger a similarity search
- Relevant chunks are injected into the LLM prompt
- The model generates an answer grounded in the document context

**📌 Notes**

- All inference is performed locally — no data is sent to external APIs
- Uploaded PDFs are stored locally in an uploads/ directory
- Vector embeddings are stored locally and regenerated as needed
- Uploaded files and vector databases are excluded from version control via .gitignore

**🧠 Use Cases**

- Chat with research papers or reports
- Internal document Q&A (local, private)
- Learning and experimentation with RAG pipelines
- Portfolio project demonstrating LLM + vector search integration

📜 License
This project is intended for educational and experimental use.
