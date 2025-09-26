# document-analyzer-api

A small FastAPI service that accepts documents (PDF, HTML, Markdown), extracts text, and performs a simple analysis: summary, named entities, and keywords.

## Quick setup

```bash
mkdir document-analyzer-api
cd document-analyzer-api

# 2. create virtual env
python3 -m venv .venv
source .venv/bin/activate

# 3. install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. download spaCy model
python -m spacy download en_core_web_sm

# 5. run the server
uvicorn app.main:app --reload
```

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

### POST /analyze
- Accepts JSON `{ "text": "..." }`.
- Returns structured JSON with `summary`, `entities`, and `keywords`.

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

## Notes & Caveats
- Transformer summarization models can be heavy and may download weights on the first run.
- For production use, pin model choices and consider using a GPU-backed environment or a hosted inference API.
