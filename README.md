rag-backend-assignment

## Objective
A Retrieval-Augmented Generation (RAG) backend that accepts a legal query, retrieves relevant text chunks from uploaded legal documents (PDF/DOCX), and generates a natural language answer with source citations.

### 1. Clone the Repository
git clone https://github.com/yourusername/rag-backend-assignement.git
cd rag-backend-assignement

### 2. Create and Activate Virtual Environment
python -m venv venv
source venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

##  Add Legal Documents

**must manually add your legal documents** (PDF or DOCX) into the `data/` folder.

Example:
data/
├── example1.pdf
└── example2.docx

You can use real court rulings or sample legal text. If you need help generating test files, ask for sample PDFs/DOCXs.

Once documents are added to `data/`, run:

python app/ingest.py

This will:
- Extract and chunk the text
- Generate vector embeddings
- Save:
  - `embeddings/legal_faiss.index`
  - `embeddings/legal_docs.pkl`

These files are **automatically created** and used for fast document retrieval.


##  Run the FastAPI Server
uvicorn app.main:app --reload
Once documents are added to `data/`, run:
python app/ingest.py
This will:
- Extract and chunk the text
- Generate vector embeddings
- Save:
  - `embeddings/legal_faiss.index`
  - `embeddings/legal_docs.pkl`

These files are **automatically created** and used for fast document retrieval.

##  Run the FastAPI Server
uvicorn app.main:app --reload


**Endpoint**:
```
POST /query
```
**Request Body**:
```json
{
  "query": "Is an insurance company liable to pay compensation if a transport vehicle involved in an accident was being used without a valid permit?"
}
```

**Response**:
```json
{
  "answer": "No, an insurance company is not liable to pay compensation if a transport vehicle is used without a valid permit at the time of the accident...",
  "citations": [
    {
      "text": "Use of a vehicle in a public place without a permit is a fundamental statutory infraction...",
      "source": "example1.docx"
    },
    {
      "text": "Therefore, the tribunal as well as the High Court had directed that the insurer shall be entitled to recover the same...",
      "source": "example2.pdf"
    }
  ]
}

