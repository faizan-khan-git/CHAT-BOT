🤖 Full Stack RAG Chatbot with Gemini 2.0 & Local Embeddings

A production-ready Retrieval Augmented Generation (RAG) application that lets you chat with your PDF documents.

This project combines the speed of Google's Gemini 2.0 Flash for generation with HuggingFace Local Embeddings for vectorization, ensuring a completely free and unlimited document processing pipeline.

🚀 Features

📄 Drag & Drop PDF Upload: Instantly process and chunk PDF documents.

🧠 Advanced RAG Pipeline: Retrieves precise context from your document to answer questions.

⚡ Gemini 2.0 Flash: Powered by Google's latest, fastest, and free-tier friendly LLM.

🔒 Local Embeddings: Uses sentence-transformers/all-MiniLM-L6-v2 running locally on your CPU.

Benefit: Zero API costs for embeddings and no "Quota Exceeded" errors for document uploads.

🎨 Modern UI: Responsive interface built with React, Vite, and Tailwind CSS.

🛠️ Robust Backend: FastAPI server with automatic database management (no file locking issues).

🛠️ Tech Stack

Frontend

Framework: React (Vite)

Styling: Tailwind CSS

Icons: Lucide React

HTTP Client: Axios

Backend

Framework: FastAPI (Python)

Orchestration: LangChain

Vector Store: ChromaDB (Persistent local storage)

Embeddings: HuggingFace (Local)

LLM: Google Gemini 2.0 Flash (via langchain-google-genai)

⚙️ Installation & Setup

1. Clone the Repository

git clone [https://github.com/yourusername/rag-chatbot.git](https://github.com/yourusername/rag-chatbot.git)
cd rag-chatbot


2. Backend Setup (Python)

Navigate to the backend folder and set up the environment.

cd backend

# Create virtual environment (Mac/Linux)
python3 -m venv venv
source venv/bin/activate

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


Configuration:
Create a .env file in the backend folder and add your Google Gemini API Key:

GOOGLE_API_KEY=AIzaSyD_YOUR_ACTUAL_KEY_HERE


Note: You can get a free key from Google AI Studio.

3. Frontend Setup (React)

Open a new terminal, navigate to the frontend folder, and install dependencies.

cd frontend
npm install


🏃‍♂️ How to Run

You need to run the Backend and Frontend in two separate terminals.

Terminal 1: Start Backend

cd backend
# Ensure venv is active
python main.py


You should see: Uvicorn running on http://0.0.0.0:8000

Terminal 2: Start Frontend

cd frontend
npm run dev


Open the URL shown (usually http://localhost:5173) in your browser.

💡 Usage Guide

Upload: Click the "Upload PDF" button and select a document.

Wait: The button will show "Processing..." while it generates local embeddings.

Chat: Once finished, type any question related to the document in the chat box.

Reset: If you want to chat with a different file, simply upload a new one. The backend automatically creates a fresh database session.

🔧 Troubleshooting

Error: 429 ResourceExhausted

Cause: You exceeded Google's embedding quota.

Fix: This project already fixes this by using Local Embeddings (HuggingFace) instead of Google's API for document processing.

Error: sqlite3.OperationalError: database is locked

Cause: Trying to delete a database file that Windows/Mac is still holding open.

Fix: The code now generates a unique UUID database folder for every upload (chroma_db_uuid...), preventing file conflicts entirely.

Error: 404 models/gemini-1.5-flash not found

Cause: Google model names vary by region/account.

Fix: The code is configured to use gemini-2.0-flash or gemini-pro, which are widely available.

🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request
