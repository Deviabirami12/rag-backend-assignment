import os
import docx
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import pickle

CHUNK_SIZE = 300

def extract_text_from_pdf(path):
    reader = PdfReader(path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def chunk_text(text, chunk_size=CHUNK_SIZE):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i+chunk_size])

def ingest_documents(data_dir="data"):
    docs = []
    for file in os.listdir(data_dir):
        path = os.path.join(data_dir, file)
        if file.endswith(".pdf"):
            text = extract_text_from_pdf(path)
        elif file.endswith(".docx"):
            text = extract_text_from_docx(path)
        else:
            continue

        for i, chunk in enumerate(chunk_text(text)):
            docs.append({"text": chunk, "source": file, "chunk_id": i})
    return docs

def build_index(docs):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [doc['text'] for doc in docs]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, "embeddings/legal_faiss.index")
    with open("embeddings/legal_docs.pkl", "wb") as f:
        pickle.dump(docs, f)

if __name__ == "__main__":
    os.makedirs("embeddings", exist_ok=True)
    docs = ingest_documents()
    build_index(docs)