from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import ollama
import streamlit as st
from pathlib import Path
from pypdf import PdfReader
import pandas as pd
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter

from vector import VectorDB

if "retriever" not in st.session_state:
    st.session_state["retriever"] = VectorDB("restaurant_reviews").get_retriever()


# Streamlit page set-up
st.title("Ollama Python Chatbot")

# Initialise model
model = OllamaLLM(model="llama3.2")

#Define prompt template
template = """
Use the following context to answer the user's question.
If the answer is not in the context, say you don't know.

Context:
{reviews}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def save_uploaded_pdf(file) -> Path:
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(parents=True, exist_ok=True)

    file_path = uploads_dir / file.name
    file_bytes = file.getbuffer()
    file_path.write_bytes(file_bytes)
    return file_path

def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def pdf_to_chunks(path):
    text = extract_text_from_pdf(path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    return splitter.split_text(text)

def ingest_pdf_into_vector_store(pdf_path, collection_name="user_pdf"):
    chunks = pdf_to_chunks(pdf_path)

    vectordb = VectorDB(collection_name)
    vectordb.add_documents(chunks)

    return vectordb.get_retriever()

def docs_to_text(docs):
    return "\n\n".join([d.page_content for d in docs])


# Maintain chat hostory in streamlit session
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous chat message
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ask your question (q to quit): "):
    # show user message
    st.session_state['messages'].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # retrieve PDF context from Chroma
    raw_docs = st.session_state["retriever"].invoke(question)
    reviews = docs_to_text(raw_docs)

    # Generate model reponse
    message = chain.invoke({"reviews": reviews, "question": question})

    # Show assistant message
    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        streamed_text = ""

        for chunk in chain.stream({"reviews": reviews, "question": question}):
            streamed_text += chunk
            message_placeholder.markdown(streamed_text + "▌")  # cursor effect

        message_placeholder.markdown(streamed_text)  # final message


        #st.markdown(message)
    st.session_state["messages"].append({"role": "assistant", "content": message})

uploaded_files = st.file_uploader(
    "Upload data", accept_multiple_files=True, type='pdf'
)

if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        with st.spinner("Uploading"):
            path = save_uploaded_pdf(uploaded_file)
            # Small pause for user feedback continuity
            time.sleep(0.3)

        status_box = st.empty()

        status_box.success(f"successfully uploaded: {path.name}")
        time.sleep(2)

        #inject into vector DB
        status_box.info("Processing PDF and updating vector database...")
        time.sleep(2)
        new_reteiever = ingest_pdf_into_vector_store(path, collection_name="user_pdf")
        st.session_state["retriever"] = new_reteiever
        status_box.success("PDF ingested into your chatbot knowledge base!")
        time.sleep(2)

        status_box.caption("You can upload another PDF if you like.")
        time.sleep(2)
        status_box.empty()