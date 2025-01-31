from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import io
from typing import List
import time

# Example for PDFs/Docs
import PyPDF2
import docx

app = FastAPI()

# db = faiss.db

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Example function using PyPDF2 to extract text from PDF.
    """
    text = ""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Example function using python-docx to extract text from docx.
    """
    text = ""
    doc = docx.Document(io.BytesIO(file_bytes))
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_txt(file_bytes: bytes) -> str:
    """
    Straight text reading.
    """
    text = file_bytes.decode("utf-8")
    return text

def chunk_text(text: str, chunk_size: int = 200) -> List[str]:
    """
    Example chunking logic: 
    Splits the text into chunks of `chunk_size` words for demonstration.
    Adjust chunk_size or logic as needed.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def run_rag_search_on_chunks(chunks: List[str]) -> List[str]:
    """
    TO REPLACE WITH OUR ACTUAL RAG MODEL
    """
    results = []
    for chunk in chunks:
        results.append("Generated comment for: " + chunk[:50] + "...")
    return results

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Endpoint to handle file upload, extract text, chunk, run RAG, return results.
    """
    file_bytes = await file.read()
    filename = file.filename

    # Identify file type by extension
    extracted_text = ""
    if filename.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_bytes)
    elif filename.endswith(".docx"):
        extracted_text = extract_text_from_docx(file_bytes)
    elif filename.endswith(".txt"):
        extracted_text = extract_text_from_txt(file_bytes)
    else:
        return {"error": "Unsupported file type."}

    # chunk the extracted text
    chunks = chunk_text(extracted_text, chunk_size=200)
    # run RAG/compliance check
    comments = run_rag_search_on_chunks(chunks)
    time.sleep(5)
    # Return structure for each chunk + comment
    response = []
    for c, comm in zip(chunks, comments):
        response.append({"chunk": c, "comment": comm})

    return {"chunks": response}