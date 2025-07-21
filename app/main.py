from fastapi import FastAPI
from app.models import QueryRequest, QueryResponse
from app.retrieval import Retriever
from app.generator import Generator

app = FastAPI()
retriever = Retriever()
generator = Generator()

@app.post("/query", response_model=QueryResponse)
def query_route(req: QueryRequest):
    chunks = retriever.retrieve(req.query)
    answer = generator.generate_answer(req.query, chunks)
    citations = [{"text": chunk["text"], "source": chunk["source"]} for chunk in chunks]
    return {"answer": answer, "citations": citations}