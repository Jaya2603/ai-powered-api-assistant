from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from app.config import settings


def ingest_docs():
    """Load documents from the docs directory, split them, and embed into ChromaDB."""
    loader = DirectoryLoader(
        settings.docs_dir,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()

    if not docs:
        print("No documents found in the docs directory. Skipping ingestion.")
        return None

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )
    vectorstore = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=settings.chroma_persist_dir,
    )
    print(f"Ingested {len(chunks)} chunks into ChromaDB.")
    return vectorstore
