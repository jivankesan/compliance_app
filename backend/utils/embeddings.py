import json

import faiss

import numpy as np

 

def load_embeddings_from_json(file_path: str):

    embeddings = []

    chunk_summaries = []

    doc_texts = []

    file_names = []

 

    with open(file_path, 'r') as f:

        data = json.load(f)

        for item in data:

            embeddings.append(item['embedding'])

            chunk_summaries.append(item['chunk_summary'])

            doc_texts.append(item['doc_text'])

            file_names.append(item['file_name'])

 

    return np.array(embeddings), chunk_summaries, doc_texts, file_names

 

def normalize_embeddings(embeddings: np.ndarray) -> np.ndarray:

    norm = np.linalg.norm(embeddings, axis=1, keepdims=True)

    return embeddings / norm

 

def create_faiss_index(embeddings: np.ndarray):

    embeddings = embeddings.astype('float32')

    embeddings = normalize_embeddings(embeddings)

    dimension = embeddings.shape[1]

    faiss_index = faiss.IndexFlatIP(dimension)

    faiss_index.add(embeddings)

    return faiss_index

 

def save_faiss_index(faiss_index, index_file: str):

    faiss.write_index(faiss_index, index_file)

 

def load_faiss_index(index_file: str):

    return faiss.read_index(index_file)

 

def search_faiss_index(faiss_index, query_embedding, k=5):

    query_embedding = np.array(query_embedding).astype('float32')

    # Reshape to 2D for searching

    query_embedding = normalize_embeddings(query_embedding.reshape(1, -1))

    distances, indices = faiss_index.search(query_embedding, k)

    return distances, indices

 

class EmbeddingsManager:

    """

    Manages embeddings data and the FAISS index.

    """

    def __init__(self, embeddings_file_path: str, faiss_index_path: str):

        self.embeddings_file_path = embeddings_file_path

        self.faiss_index_path = faiss_index_path

        self.embeddings = None

        self.chunk_summaries = None

        self.doc_texts = None

        self.file_names = None

        self.faiss_index = None

 

    def load_data_and_index(self):

        """

        Loads embedding data from JSON and either loads or creates a FAISS index.

        """

        import os

 

        # Load embeddings data

        self.embeddings, self.chunk_summaries, self.doc_texts, self.file_names = load_embeddings_from_json(self.embeddings_file_path)

 

        # Check if FAISS index file exists

        if os.path.isfile(self.faiss_index_path):

            self.faiss_index = load_faiss_index(self.faiss_index_path)

        else:

            self.faiss_index = create_faiss_index(self.embeddings)

            save_faiss_index(self.faiss_index, self.faiss_index_path)

 

    def vector_search(self, query_embedding, k=15):

        """

        Searches the FAISS index and returns the concatenated doc texts of top-k neighbors.

        """

        content = ""

        distances, indices = search_faiss_index(self.faiss_index, query_embedding, k)

        for i in range(len(distances[0])):

            idx = indices[0][i]

            content += self.doc_texts[idx]

        return content