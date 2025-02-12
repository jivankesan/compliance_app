from openai import AzureOpenAI

import numpy as np

from tqdm import tqdm

from concurrent.futures import ThreadPoolExecutor, as_completed

 

class ComplianceAgent:

    """

    Handles the compliance checking process:

      1. Chunk creation

      2. Embedding of chunk

      3. Vector search

      4. Prompting the model with compliance context

      5. Generating a response

    """

 

    def __init__(self,

                 azure_endpoint: str,

                 api_key: str,

                 api_version: str,

                 embedding_model: str,

                 chat_model: str,

                 system_prompt: str,

                 embeddings_manager,

                 text_processor):

        self.azure_endpoint = azure_endpoint

        self.api_key = api_key

        self.api_version = api_version

        self.embedding_model = embedding_model

        self.chat_model = chat_model

        self.system_prompt = system_prompt

        self.embeddings_manager = embeddings_manager

        self.text_processor = text_processor

 

        # Initialize Azure client

        self.client = AzureOpenAI(

            azure_endpoint=self.azure_endpoint,

            api_key=self.api_key,

            api_version=self.api_version

        )

   

    def create_embedding(self, chunk: str):

        response = self.client.embeddings.create(

            input=chunk,

            model=self.embedding_model

        )

        embedding = response.data[0].embedding

        return embedding

 

    def prompt_model(self, content: str, chunk_text: str):

        chat_prompt = [

            {

                "role": "system",

                "content": self.system_prompt

            },

            {

                "role": "user",

                "content": f"The relevant compliance context from the rules: {content}\n\nHere is the paragraph to check: {chunk_text}"

            },

        ]

 

        completion = self.client.chat.completions.create(

            model=self.chat_model,

            messages=chat_prompt,

            max_tokens=10000,

            temperature=0.7,

            top_p=0.95,

            frequency_penalty=0,

            presence_penalty=0,

            stop=None,

            stream=False

        )

 

        return completion.choices[0].message.content

   

    def process_chunk(self, chunk_text:str):

        """

        Process a single chunk by:

            1. Creating Embedding

            2. Performing vector search for compliance context

            3. Promting the model for a response

        Returns a dict with { chunk: <str>, comment: <str> }

        """

        embedding = self.create_embedding(chunk_text)

        compliance_context = self.embeddings_manager.vector_search(embedding)

        response = self.prompt_model(compliance_context, chunk_text)

        return {

            "chunk": chunk_text,

            "comment": response

        }

 

    def compliance_check(self, text: str):

        """

        Main method to run compliance check on the input text.

        1. Split text into chunks

        2. For each chunk:

           - Create embedding

           - Retrieve relevant compliance context from FAISS

           - Prompt the model

        Returns a list of (chunk, comment) dicts.

        """

        chunks = self.text_processor.create_chunks(text)

        results = []

 

        for chunk_obj in tqdm(chunks, desc="Checking compliance"):

            chunk_text = chunk_obj

            embedding = self.create_embedding(chunk_text)

            compliance_context = self.embeddings_manager.vector_search(embedding)

            response = self.prompt_model(compliance_context, chunk_text)

            results.append({

                "chunk": chunk_text,

                "comment": response

            })

        return results

 

    def compliance_check1(self, text: str, max_workers = 32):

        """

        Main method to run compliance check on the input text in parallel.

        1. Split text into chunks

        2. For each chunk:

           - Create embedding

           - Retrieve relevant compliance context from FAISS

           - Prompt the model

        Returns a list of (chunk, comment) dicts.

        """

        chunks = self.text_processor.create_chunks(text)

        results = [None] * len(chunks)

 

        with ThreadPoolExecutor(max_workers=max_workers) as executor:

            # Start operations

            future_to_index = {

                executor.submit(self.process_chunk, chunk): i

                for i, chunk in enumerate(chunks)

            }

            for future in tqdm(as_completed(future_to_index),

                                total=len(future_to_index),

                                desc="Checking Compliance"):

                index = future_to_index[future]

                try:

                    results[index] = future.result()

                except Exception as exc:

                    print(f"Chunk '{chunk[:30]}...' generated an execption: {exc}")

   

        return results