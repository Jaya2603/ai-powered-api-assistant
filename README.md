# 🤖 AI-Powered API Assistant

An intelligent, agent-based system that allows you to interact with REST APIs using natural language. Built with **FastAPI**, **LangChain**, and **ChromaDB**.

---

## 🚀 Features

- **Natural Language API Interaction**: Talk to your APIs instead of writing manual `curl` commands.
- **RAG-Powered Context**: Automatically indexes your API documentation (Markdown/Text) for contextual understanding.
- **Dynamic Tool Execution**: The agent autonomously decides when to search docs, call endpoints, or generate tests.
- **Automated Test Generation**: Instantly generate comprehensive JSON test cases for any API endpoint.
- **Modern Architecture**: Uses LangChain's latest agentic patterns and FastAPI's high-performance framework.

---

## 📂 Project Structure

```text
ai-api-assistant/
├── app/
│   ├── agent/       # LangChain agent and custom tool definitions
│   ├── rag/         # Document ingestion and retrieval pipeline
│   ├── routers/     # API endpoints (Query, Test Generation)
│   ├── config.py    # Configuration management
│   └── main.py      # Application entry point
├── docs/            # Put your API documentation here (.md files)
├── chroma_db/       # Vector database (Auto-generated)
├── .env             # Environment variables (Sensitive!)
└── requirements.txt # Python dependencies
```

---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ai-api-assistant.git
cd ai-api-assistant
```

### 2. Set up the environment
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Install dependencies
```bash
# Using pip
pip install -r requirements.txt

# Or using uv (recommended)
uv pip install -r requirements.txt
```

---

## 🚦 How to Use

### 1. Add your API Docs
Place any Markdown files describing your API in the `docs/` folder. A sample is already provided in `docs/sample_api.md`.

### 2. Run the Server
```bash
python -m uvicorn app.main:app --reload
```

### 3. Start Chatting
Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to use the interactive Swagger UI.

**Example Prompts:**
- *"What is the endpoint for creating a new user?"*
- *"Get user 'usr_123' and show me the response."*
- *"Generate 5 edge-case test scenarios for the POST /users endpoint."*

---

## 🛡️ Security Note

The [`.env`](file:///.env) file contains your sensitive API keys. It is **already added to `.gitignore`** to prevent it from being pushed to GitHub. Never share this file publicly.

---

## ⚖️ License
MIT License - feel free to use this for your own projects!
