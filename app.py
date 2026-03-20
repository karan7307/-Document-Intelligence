from pathlib import Path

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from flask import Flask, jsonify, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")


def _client(endpoint: str, key: str) -> DocumentIntelligenceClient:
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def _normalize_endpoint(endpoint: str) -> str:
    return endpoint.strip().rstrip("/") + "/"


def _looks_like_url(value: str) -> bool:
    value = (value or "").strip().lower()
    return value.startswith("http://") or value.startswith("https://")


def _sanitize_endpoint_key(endpoint: str, key: str):
    endpoint = (endpoint or "").strip()
    key = (key or "").strip()

    # If user accidentally swapped endpoint and key, fix it automatically.
    if not _looks_like_url(endpoint) and _looks_like_url(key):
        endpoint, key = key, endpoint

    if not _looks_like_url(endpoint):
        return "", "", "Invalid endpoint. Use full URL like https://<resource>.cognitiveservices.azure.com/"

    if not key or _looks_like_url(key):
        return "", "", "Invalid API key. Paste only the key value, not a URL."

    return _normalize_endpoint(endpoint), key, None


def _shape_response(result) -> dict:
    lines = []
    for page in result.pages or []:
        for line in page.lines or []:
            lines.append(line.content)

    tables = []
    for table in result.tables or []:
        tables.append({"row_count": table.row_count, "column_count": table.column_count})

    return {
        "text": "\n".join(lines),
        "tables": tables,
    }


@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.post("/analyze-url")
def analyze_url():
    payload = request.get_json(silent=True) or {}
    endpoint = payload.get("endpoint", "")
    key = payload.get("key", "")
    url = payload.get("url", "")

    if not endpoint or not key or not url:
        return jsonify({"error": "endpoint, key, and url are required"}), 400

    endpoint, key, validation_error = _sanitize_endpoint_key(endpoint, key)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        poller = _client(endpoint, key).begin_analyze_document(
            model_id="prebuilt-layout",
            body=AnalyzeDocumentRequest(url_source=url),
        )
        result = poller.result()
        return jsonify(_shape_response(result))
    except HttpResponseError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"Unexpected error: {exc}"}), 500


@app.post("/upload")
def upload_file():
    file = request.files.get("file")
    endpoint = request.form.get("endpoint", "")
    key = request.form.get("key", "")

    if not endpoint or not key or not file:
        return jsonify({"error": "file, endpoint, and key are required"}), 400

    endpoint, key, validation_error = _sanitize_endpoint_key(endpoint, key)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        content = file.read()
        poller = _client(endpoint, key).begin_analyze_document(
            model_id="prebuilt-layout",
            body=AnalyzeDocumentRequest(bytes_source=content),
        )
        result = poller.result()
        return jsonify(_shape_response(result))
    except HttpResponseError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"Unexpected error: {exc}"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
