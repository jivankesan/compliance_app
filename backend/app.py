from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os


from utils.config import Config
from utils.extractors import PDFTextExtractor, DOCXTextExtractor, TXTTextExtractor
from utils.embeddings import EmbeddingsManager
from utils.text_processing import TextProcessor
from utils.compliance_agent import ComplianceAgent
from langchain_openai import AzureOpenAIEmbeddings

app = FastAPI()

 

# Configure CORS

origins = [

    http://localhost:3000,

    http://127.0.0.1:3000,

    http://localhost:5173,

    http://127.0.0.1:5173

]

app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

 

# Load environment/config

config = Config()

 

# Initialize EmbeddingsManager

INDEX_FILE = 'embeddings/faiss_index_2.index'

EMBEDDINGS_FILE = 'embeddings/test_case_2.json'

embeddings_manager = EmbeddingsManager(

    embeddings_file_path=EMBEDDINGS_FILE,

    faiss_index_path=INDEX_FILE

)

embeddings_manager.load_data_and_index()

 

# Initialize the embedding model for chunk splitting

azure_embedding_model = AzureOpenAIEmbeddings(

    model="text-embedding-ada-002",

    api_key=config.model_api_key,

    api_version=config.api_version

)

 

# Initialize TextProcessor

text_processor = TextProcessor(

    embedding_model=azure_embedding_model,

    threshold_type="percentile",

    threshold_amount=88.0

)

 

# System prompt

SYSTEM_PROMPT1 = (

    "You are an AI Compliance Agent. Your task is to scan a provided text excerpt from a larger document "

    "and compare it against sections from a compliance guide to ensure it meets "

    "specific criteria. If all criteria are met, respond with 'All criteria met.' "

    "First check that the paragraph has clear language, is not ambiguous and charts/graphs and information have all labels for all axis"

    "If any criteria are not met, provide a list of issues, clearly stating what "

    "is missing or incorrect, limiting your response to at most 7 comments per section. "

    "For any missing or incorrect information, structure your response as a list of items"

    "the first piece of text in the list should be bolded, and outlines the violation, followed by ':'"

    "and then the specific thing to address/change If a specific "

    "disclosure is required, include the exact text of the disclosure from the compliance guide. "

    "Ignore mentions of the word 'Internal' and Unclear Source citations"

    "If the paragraph in question is too short or only 1 sentence, provide minimal to no comments"

    "If the section contains disclosures, only suggest additional disclosures if any"

    "Do not duplicate feedback"

    "Format your response in html, to structure it as a bulleted list. Do not include the ''' html at the beginning"

)

 

SYSTEM_PROMPT = ("""You are an AI Compliance Agent. Your task is to review a given text excerpt from a larger document and assess its adherence to specific criteria outlined in a compliance guide. Follow these detailed instructions:

 

1. **Assess Clarity and Ambiguity:**

   - Evaluate if the language in the paragraph is clear and unambiguous.

 

2. **Evaluate Charts and Graphs:**

   - Ensure all charts and graphs have labels on all axes and other necessary information is clearly labeled.

 

3. **Response if Criteria Met:**

   - If the paragraph meets all criteria, respond with "All criteria met."

 

4. **Response if Criteria Not Met:**

   - If there are any issues, list them clearly, limiting your feedback to a maximum of 7 comments per section.

   - For each issue, include a snippet from the section where the rule was violated so the frontend can highlight it

   - Each comment should be structured as follows:

     - **Bold the issue description**, followed by a colon.

     - Describe the specific thing to address or change.

   - If a specific disclosure is required, include the exact full text from the compliance guide.

 

5. **Special Instructions:**

   - Ignore mentions of the word "Internal" and any unclear source citations.

   - If the paragraph is too short or consists of only one sentence, provide minimal to no comments.

   - If the section includes disclosures, only suggest additional disclosures if needed.

   - Avoid duplicating feedback.

   - INCLUDE THE FULL DISCLOSURE FROM THE COMPLIANCE GUIDE IF IT IS MISSING

 

6. **Response Format:**

   - Format your response as a bulleted list in HTML. Do not include the opening `<html>` tag. For each item in the list, you should include a unique id, which will be the section of the text that corresponds to the issue.

 

Example HTML structure for feedback:

<ul>

  <li  id="section of text that corresponds to this issue"><strong>Issue Description:</strong> Specific thing to address/change.</li>

  <!-- More comments if needed -->

</ul>

""")

 

# Initialize ComplianceAgent

compliance_agent = ComplianceAgent(

    azure_endpoint=config.model_endpoint,

    api_key=config.model_api_key,

    api_version=config.api_version,

    embedding_model="text-embedding-ada-002",  # for embeddings creation

    chat_model="gpt-4o",                      # for chat completions

    system_prompt=SYSTEM_PROMPT,

    embeddings_manager=embeddings_manager,

    text_processor=text_processor

)

 

@app.post("/upload")

async def upload_document(file: UploadFile = File(...)):

    """

    Endpoint to handle file upload, extract text, chunk, run compliance check, return results.

    """

    file_bytes = await file.read()

    filename = file.filename.lower()

 

    # Identify file type by extension

    extractor = None

    if filename.endswith(".pdf"):

        extractor = PDFTextExtractor()

    elif filename.endswith(".docx"):

        extractor = DOCXTextExtractor()

    elif filename.endswith(".txt"):

        extractor = TXTTextExtractor()

    else:

        return {"error": "Unsupported file type."}

 

    # Extract text using the chosen extractor

    extracted_text = extractor.extract_text(file_bytes)

 

    # Run compliance check

    results = compliance_agent.compliance_check(extracted_text)

 

    return {"chunks": results}