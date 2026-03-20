async function analyzeDocument() {
  const endpoint = document.getElementById("endpoint").value;
  const key = document.getElementById("apikey").value;
  const file = document.getElementById("fileInput").files[0];
  const url = document.getElementById("urlInput").value;

  const output = document.getElementById("output");
  output.innerHTML = "⏳ Processing...";

  if (!endpoint || !key) {
    output.innerHTML = "⚠️ Please enter endpoint and API key";
    return;
  }

  try {
    let response;

    if (file) {
      let formData = new FormData();
      formData.append("file", file);
      formData.append("endpoint", endpoint);
      formData.append("key", key);

      response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
      });

    } else if (url) {
      response = await fetch("http://127.0.0.1:5000/analyze-url", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url, endpoint, key })
      });

    } else {
      output.innerHTML = "⚠️ Please upload a file or enter URL";
      return;
    }

    const data = await response.json();
    output.textContent = JSON.stringify(data, null, 2);

  } catch (error) {
    output.innerHTML = "❌ Error: " + error;
  }
}