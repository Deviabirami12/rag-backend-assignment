import faiss
import pickle
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, index_path="embeddings/legal_faiss.index", docs_path="embeddings/legal_docs.pkl"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.read_index(index_path)
        with open(docs_path, "rb") as f:
            self.docs = pickle.load(f)

    def retrieve(self, query, top_k=5):
        q_vec = self.model.encode([query])
        distances, indices = self.index.search(q_vec, top_k)
        return [self.docs[i] for i in indices[0]]
