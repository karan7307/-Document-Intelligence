from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential

# 🔐 Azure credentials
endpoint = "https://document03322.cognitiveservices.azure.com/"
key = "<YOUR_DOCUMENT_INTELLIGENCE_KEY>"

# 🌐 Document URL
document_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"

# 🚀 Initialize client
client = DocumentIntelligenceClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# 📊 Analyze document using layout model
poller = client.begin_analyze_document(
    model_id="prebuilt-layout",
    body=AnalyzeDocumentRequest(url_source=document_url),
)

result = poller.result()

# 📄 Extract text
print("\n📄 Extracted Text:\n")
for page in result.pages:
    for line in page.lines:
        print(line.content)

# 📊 Extract tables (if any)
print("\n📊 Tables Found:\n")
for table in result.tables:
    print(f"Table with {table.row_count} rows and {table.column_count} columns")