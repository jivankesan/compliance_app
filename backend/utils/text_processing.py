from langchain_experimental.text_splitter import SemanticChunker

from langchain.text_splitter import RecursiveCharacterTextSplitter

 

class TextProcessor:

    """

    Handles splitting of text into chunks.

    """

    def __init__(self, embedding_model, threshold_type="percentile", threshold_amount=88.0):

        self.text_splitter = SemanticChunker(

            embedding_model,

            breakpoint_threshold_type=threshold_type,

            breakpoint_threshold_amount=threshold_amount

        )

   

    def create_chunks(self, text: str, threshold: int = 55):

        """

        Creates chunks from text using the SemanticChunker.

        Joins chunks that don't make the threshold to the previous chunk.

        Returns a list of Document objects (LangChain style).

        """

        docs = self.text_splitter.create_documents([text])

        combined_docs = []

 

        for doc in docs:

            current_content = doc.page_content.strip()

            if not combined_docs:

                # If combined_docs is empty, just add the first chunk

                combined_docs.append(current_content)

            else:

                # Check if the current chunk meets the threshold

                if len(current_content) < threshold:

                    # Join the current chunk with the last one in combined_docs

                    combined_docs[-1] += " " + current_content

                else:

                    # Otherwise, add the current chunk as a new entry

                    combined_docs.append(current_content)

 

        # Replace newlines with spaces in the combined chunks

        stripped_docs = [doc.replace("\n", " ") for doc in combined_docs]

        return stripped_docs

 

    def create_chunks3(self, text: str, threshold: int = 55):

        """

        Creates chunks from text using the SemanticChunker.

        Returns a list of Document objects (LangChain style).

        """

        docs = self.text_splitter.create_documents([text])

        cleaned_docs = [doc for doc in docs if len(doc.page_content.strip()) >= threshold]

        stripped_docs = [doc.page_content.replace("\n", " ") for doc in cleaned_docs]

        return stripped_docs

   

    def create_chunks2(self, text: str, threshold: int = 60):

        # Split text into lines

        lines = text.split('\n')

        chunks = []

        current_chunk = []

 

        for line in lines:

            # Check if the line is a bold line (assuming bold lines are marked with **)

            if line.startswith('**') and line.endswith('**'):

                # If the current chunk is not empty, add it to the list of chunks

                if current_chunk:

                    chunks.append(' '.join(current_chunk))

                    current_chunk = []

                # Start a new chunk with the bold line

                current_chunk.append(line)

            else:

                # Add non-bold lines to the current chunk

                current_chunk.append(line)

 

        # Add any remaining content in the current_chunk to chunks

        if current_chunk:

            chunks.append(' '.join(current_chunk))

 

        # Merge chunks that are below the threshold

        merged_chunks = []

        temp_chunk = ""

 

        for chunk in chunks:

            if len(temp_chunk) + len(chunk) < threshold:

                temp_chunk += " " + chunk

            else:

                if temp_chunk:

                    merged_chunks.append(temp_chunk.strip())

                temp_chunk = chunk

       

        # Add the last temp_chunk if it exists

        if temp_chunk:

            merged_chunks.append(temp_chunk.strip())

 

        return merged_chunks