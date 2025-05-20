# generate_docs.py
import os
from pathlib import Path
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

# === Settings ===
REPO_PATH = "./repos/passforge"
OUTPUT_DIR = Path("generated_docs")
PRESET_QUESTIONS = [
    "Create a high-level architecture diagram in mermaid syntax representing the system components and their interactions.",
    # "Summarize the purpose and functionality of this repository.",
    # "List and describe the main components or modules.",
    # "Explain how a developer can get started with this project.",
    # "Document the public APIs or functions available in this codebase.",
    # "What are the dependencies and external libraries used?"
]

# === Ensure repo is available ===
assert os.path.exists(REPO_PATH), f"Repository not found at {REPO_PATH}"
OUTPUT_DIR.mkdir(exist_ok=True)

# === Load documents ===
loader = DirectoryLoader(REPO_PATH, glob="**/*.md", loader_cls=TextLoader)
documents = loader.load()

# === Chunking ===
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(documents)

# === Embedding and Vectorstore ===
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(chunks, embedding=embedding)

# === LLM and Retrieval QA ===
llm = Ollama(model="llama2", base_url="http://localhost:11434")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

# === Generate docs for each question ===
for question in PRESET_QUESTIONS:
    print(f"\n🤖 Asking: {question}")
    try:
        answer = qa_chain.run(question)
    except Exception as e:
        print(f"❌ Error answering question: {e}")
        continue

    filename = question.lower().replace(" ", "_").replace(".", "")[:50] + ".md"
    filepath = OUTPUT_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {question}\n\n{answer}\n")

    print(f"✅ Written to {filepath}")
