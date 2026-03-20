# Azure Document Intelligence Web App

A clean web interface and Flask backend to analyze documents using Azure AI Document Intelligence.

You can submit documents in two ways:
- URL-based analysis
- File upload analysis

The app extracts text lines and reports table structure (row/column counts).

## Highlights

- Web UI with enhanced 3D styling (white background, modern depth effects)
- Flask API backend
- Azure Document Intelligence `prebuilt-layout` model integration
- Automatic endpoint/key swap recovery (if pasted in the wrong fields)
- Simple JSON output for quick testing and debugging

## Tech Stack

- Python + Flask
- Azure SDK: `azure-ai-documentintelligence`
- HTML/CSS/JavaScript frontend

## Project Structure

- `app.py` - Flask server, routing, and Azure analysis logic
- `index.html` - Main UI page
- `style.css` - UI styling
- `script.js` - Frontend logic and API calls
- `app1.py` - Standalone script test for Document Intelligence SDK

## Prerequisites

- Python 3.10+
- Azure AI Document Intelligence resource
- Azure endpoint URL and API key

Expected endpoint format:

```text
https://<your-resource-name>.cognitiveservices.azure.com/
```

## Local Setup

1. Create virtual environment:

```powershell
python -m venv .venv
```

2. Activate environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
python -m pip install flask azure-ai-documentintelligence azure-core
```

## Run the App

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## How to Use

1. Enter Azure endpoint and API key.
2. Choose one input method:
   - Upload a file, or
   - Paste a document URL.
3. Click `Analyze`.
4. See output in the result panel.

## API Endpoints

### `GET /`
Serves the web UI.

### `POST /analyze-url`
Analyze document by URL.

Request body:

```json
{
  "endpoint": "https://<resource>.cognitiveservices.azure.com/",
  "key": "<api-key>",
  "url": "https://example.com/sample.pdf"
}
```

### `POST /upload`
Analyze uploaded file.

Form fields:
- `file`: document file
- `endpoint`: Azure endpoint
- `key`: Azure API key

### Typical Success Response

```json
{
  "text": "...extracted lines...",
  "tables": [
    { "row_count": 5, "column_count": 3 }
  ]
}
```

## Error Handling Behavior

- Missing fields return `400` with clear message
- Invalid Azure request returns `400` with service error
- Unexpected server error returns `500`
- If endpoint and key are accidentally swapped, backend attempts auto-correction

## Troubleshooting

1. `No connection adapters were found`
Cause: endpoint/key mix-up.
Fix: verify endpoint is URL and key is raw key value.

2. `InvalidContent` / URL download error
Cause: document URL not publicly reachable by Azure.
Fix: use a direct, publicly accessible document URL.

3. `401/403` authentication errors
Cause: wrong key, endpoint, or mismatched Azure resource.
Fix: copy endpoint/key from the same Document Intelligence resource.

## Security Notes

- Do not hardcode secrets in production.
- Use environment variables or secret managers.
- Rotate API keys regularly.
- Add backend auth/rate-limits before public deployment.

## Future Improvements

- Save endpoint locally in browser settings (optional)
- Pretty-format text/table outputs in separate tabs
- Add downloadable JSON/text report
- Add deployment guide (App Service / container)

## License

Use this project for learning and internal demos. Add your own license if needed.
