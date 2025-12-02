// ---------------- DOM ELEMENTS ----------------
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

// Your backend URL
const BACKEND_URL = "http://localhost:8000";

let selectedFile = null;
let stream = null;


// ---------------- SHOW/HIDE UPLOAD OPTIONS ----------------
openUploadOptions.addEventListener("click", () => {
  uploadOptions.style.display =
    uploadOptions.style.display === "flex" ? "none" : "flex";
});


// ---------------- SELECT FILE ----------------
chooseFileBtn.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    selectedFile = fileInput.files[0];
    showPreview(URL.createObjectURL(selectedFile));
    uploadOptions.style.display = "none";
  }
});


// ---------------- CAMERA CAPTURE ----------------
capturePhotoBtn.addEventListener("click", async () => {
  try {
    uploadOptions.style.display = "none";

    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" }
    });

    cameraStream.srcObject = stream;
    cameraStream.classList.add("show");
    takePhotoBtn.classList.add("show");

  } catch (err) {
    alert("Camera access blocked.");
    console.error(err);
  }
});


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

  // stop camera
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }

  cameraStream.classList.remove("show");
  takePhotoBtn.classList.remove("show");
});


// ---------------- SHOW PREVIEW ----------------
function showPreview(url) {
  preview.innerHTML = `<img src="${url}" alt="Preview Image" />`;
  resultBox.innerHTML = "";
  analyseBtn.classList.add("show");
}


// ---------------- ANALYZE BUTTON ----------------
analyseBtn.addEventListener("click", async () => {
  if (!selectedFile) {
    alert("Upload or capture a photo first!");
    return;
  }

  resultBox.innerHTML = "<p>🔍 Analyzing…</p>";

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch(`${BACKEND_URL}/predict`, {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (!response.ok || data.error) {
      resultBox.innerHTML = `<p class="error">❌ ${data.error || "Server error"}</p>`;
      return;
    }

    // Show results
    const confidence = (data.confidence * 100).toFixed(2);

    resultBox.innerHTML = `
      <div class="result-card">
        <h3>🌿 Analysis Complete</h3>
        <p><strong>Disease:</strong> ${data.prediction.replace(/_/g, " ")}</p>
        <p><strong>Confidence:</strong> ${confidence}%</p>

        <div class="solution-box">
          <h4>💡 Recommended Solution</h4>
          <p>${data.solution}</p>
        </div>
      </div>
    `;

  } catch (err) {
    console.error(err);
    resultBox.innerHTML = `
      <p class="error">❌ Cannot reach backend at ${BACKEND_URL}</p>
    `;
  }
});
