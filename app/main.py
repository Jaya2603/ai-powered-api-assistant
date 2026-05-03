from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import query, testgen
from app.rag.ingester import ingest_docs
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ingest docs on startup if ChromaDB doesn't exist yet."""
    if not os.path.exists("./chroma_db"):
        try:
            print("Ingesting API docs into ChromaDB...")
            ingest_docs()
        except Exception as e:
            print(f"WARNING: Doc ingestion failed ({e}). "
                  "Set a valid OPENAI_API_KEY in .env and restart, "
                  "or run ingestion manually later.")
    yield


app = FastAPI(
    title="AI-Powered API Assistant",
    description="Natural language interface for interacting with APIs",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(query.router, prefix="/api/v1", tags=["Query"])
app.include_router(testgen.router, prefix="/api/v1", tags=["Test Generation"])

@app.get("/")
def read_root():
    """Welcome message for the API."""
    return {
        "message": "Welcome to the AI-Powered API Assistant",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}
