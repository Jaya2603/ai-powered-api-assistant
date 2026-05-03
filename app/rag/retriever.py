from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from app.config import settings

_vectorstore = None


def get_vectorstore():
    """Get or initialize the ChromaDB vectorstore singleton."""
    global _vectorstore
    if _vectorstore is None:
        embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key,
        )
        _vectorstore = Chroma(
            persist_directory=settings.chroma_persist_dir,
            embedding_function=embeddings,
        )
    return _vectorstore


def retrieve_context(query: str, k: int = 4) -> str:
    """Retrieve relevant document chunks from the vectorstore for a given query."""
    vs = get_vectorstore()
    results = vs.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in results])
