const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");
const resultBox = document.getElementById("result");

const uploadOptions = document.getElementById("uploadOptions");
const openUploadOptions = document.getElementById("openUploadOptions");

const capturePhotoBtn = document.getElementById("capturePhotoBtn");
const chooseFileBtn = document.getElementById("chooseFileBtn");
const analyseBtn = document.getElementById("analyseBtn");

const cameraStream = document.getElementById("cameraStream");
const takePhotoBtn = document.getElementById("takePhotoBtn");

let selectedFile = null;
let stream;

// Show upload options when main button clicked
openUploadOptions.addEventListener("click", () => {
  if (uploadOptions.style.display === "flex") {
    uploadOptions.style.display = "none";
  } else {
    uploadOptions.style.display = "flex";
  }
});

// Choose File
chooseFileBtn.addEventListener("click", () => {
  fileInput.click();
});

// File selected — show preview
fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    selectedFile = fileInput.files[0];
    showPreview(URL.createObjectURL(selectedFile));
    uploadOptions.style.display = "none";
  }
});

// Capture Photo using camera
capturePhotoBtn.addEventListener("click", async () => {
  try {
    uploadOptions.style.display = "none";

    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
    cameraStream.srcObject = stream;
    cameraStream.classList.add("show");
    takePhotoBtn.classList.add("show");
  } catch (error) {
    alert("Unable to access camera. Please check permissions.");
    console.error("Camera error:", error);
  }
});

// Take photo from camera
takePhotoBtn.addEventListener("click", () => {
  const canvas = document.createElement("canvas");
  canvas.width = cameraStream.videoWidth;
  canvas.height = cameraStream.videoHeight;

  const ctx = canvas.getContext("2d");
  ctx.drawImage(cameraStream, 0, 0, canvas.width, canvas.height);

  canvas.toBlob((blob) => {
    selectedFile = new File([blob], "captured.jpg", { type: "image/jpeg" });
    showPreview(URL.createObjectURL(selectedFile));
  });

  // Stop camera
  if (stream) {
    stream.getTracks().forEach(t => t.stop());
  }
  cameraStream.classList.remove("show");
  takePhotoBtn.classList.remove("show");
});

// Show preview and Analyse Button
function showPreview(url) {
  preview.innerHTML = `<img src="${url}" alt="Preview" />`;
  analyseBtn.classList.add("show");
  resultBox.innerHTML = "";
}

// Analyse Button Click
analyseBtn.addEventListener("click", async () => {
  if (!selectedFile) {
    alert("Please upload or capture a photo!");
    return;
  }

  resultBox.innerHTML = "<p>🔍 Analyzing... Please wait.</p>";

  const API_URL = "https://api-inference.huggingface.co/models/spaces/akhaliq/Plant-Disease-Model";
  const API_KEY = "YOUR_HF_API_KEY"; // Replace with your actual API key

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { Authorization: `Bearer ${API_KEY}` },
      body: formData
    });

    const result = await response.json();

    if (!response.ok) {
      resultBox.innerHTML = `<p class="error">❌ Error: ${result.error || "Unable to analyze image"}</p>`;
      return;
    }

    if (result && result.length > 0) {
      const top = result[0];
      resultBox.innerHTML = `
        <p><strong>Prediction:</strong> ${top.label}</p>
        <p><strong>Confidence:</strong> ${(top.score * 100).toFixed(2)}%</p>
      `;
    } else {
      resultBox.innerHTML = `<p class="error">❌ No results found. Please try another image.</p>`;
    }

  } catch (e) {
    console.error("Analysis error:", e);
    resultBox.innerHTML = `<p class="error">❌ Network error. Please check your connection and try again.</p>`;
  }
});