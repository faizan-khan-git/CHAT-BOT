import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# AI Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY is missing. Please check your .env file.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- AI CONFIGURATION ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Global variables to track the current database
vector_store = None
current_db_path = None

class QueryRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    global vector_store, current_db_path
    
    # 1. Create a UNIQUE folder for this new upload
    # This prevents the "Read-only database" error
    new_db_folder = f"chroma_db_{uuid.uuid4().hex}"
    
    # 2. Save the PDF
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3. Process the PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 4. Create the new Database
    vector_store = Chroma(
        persist_directory=new_db_folder,
        embedding_function=embeddings
    )
    vector_store.add_documents(documents=splits)
    
    # 5. (Optional) Cleanup the OLD database folder to save space
    if current_db_path and os.path.exists(current_db_path):
        try:
            shutil.rmtree(current_db_path)
        except:
            pass # If it fails, just ignore it. Don't crash the server.
            
    current_db_path = new_db_folder
    
    return {"message": "Document processed successfully!", "filename": file.filename}

@app.post("/chat")
async def chat(request: QueryRequest):
    global vector_store
    
    if vector_store is None:
        return {"answer": "Please upload a document first!"}
        
    retriever = vector_store.as_retriever()
    
    system_prompt = (
        "You are a helpful assistant. Use the provided context to answer the user's question. "
        "If the answer is not in the context, say you don't know. "
        "Keep your answer concise (max 3 sentences)."
        "\n\n"
        "Context: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    response = rag_chain.invoke({"input": request.question})
    
    return {"answer": response["answer"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)