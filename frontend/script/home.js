const fileInput = document.getElementById("fileInput");
const analyseBtn = document.getElementById("analyseBtn");
const resultDiv = document.getElementById("result");
const previewDiv = document.getElementById("preview");

// When user chooses file
fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];

    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        previewDiv.innerHTML = `<img src="${e.target.result}" width="200"/>`;
    };
    reader.readAsDataURL(file);
});

// Analyse button click
analyseBtn.addEventListener("click", async () => {
    const file = fileInput.files[0];

    if (!file) {
        resultDiv.innerHTML = "Please upload an image first.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    resultDiv.innerHTML = "Analysing... Please wait.";

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.detail) {
            resultDiv.innerHTML = "Error: " + data.detail;
            return;
        }

        resultDiv.innerHTML = `
            <h3>Disease: ${data.prediction}</h3>
            <p>Confidence: ${data.confidence}%</p>
            <p>Solution: ${data.solution}</p>
        `;
    } catch (error) {
        resultDiv.innerHTML = "Cannot connect to backend.";
        console.error(error);
    }
});
