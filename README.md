# document-analyzer-api

A small FastAPI service that accepts documents (PDF, HTML, Markdown, TXT), extracts text, and performs a simple analysis: summary, named entities, and keywords.

## Tech Stack

- **Backend Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **Text Extraction:** PyMuPDF (PDF), BeautifulSoup4 (HTML), built-in Markdown/text parsing
- **NLP & Analysis:** spaCy, Transformers, Torch
- **Data Validation:** Pydantic
- **File Handling:** python-multipart

---

## Quick Setup (macOS / Linux)

```bash
# 1. Clone the repo
git clone https://github.com/atharvadudhe/document-analyzer-api.git
cd document-analyzer-api

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Download spaCy English model
python -m spacy download en_core_web_sm

# 5. Run the server
uvicorn app.main:app --reload


## Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload
```

## Endpoints

### POST /upload
- Accepts file upload (`multipart/form-data`) field named `file`.
- Supported MIME types / extensions: `.pdf`, `.html` / `.htm`, `.md`, `.markdown`, `.txt`.
- Returns extracted raw text as JSON `{ "filename": ..., "text": ... }`.
```
{
  "filename": "example.pdf",
  "text": "Extracted text here..."
}
```

### POST /analyze
- Accepts JSON `{ "text": "..." }`.
```
{
  "text": "Paste long text here or use text from /upload response"
}
```
- Returns structured JSON with `summary`, `entities`, and `keywords`.
```
{
  "summary": "Short summary of the text",
  "entities": ["Entity1", "Entity2", "..."],
  "keywords": ["keyword1", "keyword2", "..."]
}
```

## Example Postman requests

**Upload**
- Method: POST
- URL: `http://127.0.0.1:8000/upload`
- Body: form-data -> key `file` -> type `File` -> choose a PDF/HTML/MD

**Analyze**
- Method: POST
- URL: `http://127.0.0.1:8000/analyze`
- Body: raw JSON
```
{
  "text": "Paste long text here or use text from /upload response"
}
```

