from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

class VectorDB:
    def __init__(self, collection_name: str, persist_directory="./chrome_langchain_db"):
        self.embeddings = OllamaEmbeddings(model="mxbai-embed-large")

        self.collection_name = collection_name
        self.persist_directory = persist_directory

        self.db = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def add_documents(self, chunks):
        ids = [str(i) for i in range(len(chunks))]
        self.db.add_texts(texts=chunks, ids=ids)

    def get_retriever(self, k=5):
        return self.db.as_retriever(search_kwargs={"k": k})
