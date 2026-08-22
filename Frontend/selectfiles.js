window.addEventListener('load', () => {
  const loader = document.getElementById('page-loader');
  if (loader) {
    setTimeout(() => loader.classList.add('hidden'), 250);
  }
});

function highlightStep() {
  const page = window.location.pathname.split('/').pop();
  const map = {
    'user.html': '1',
    'upload.html': '2',
    'selectfiles.html': '3',
    'qualityreport.html': '4'
  };

  const stepNum = map[page] || '3';
  document.querySelectorAll('.nav-link, .step').forEach(el => el.classList.remove('active'));

  const el = document.querySelector(`.nav-link[data-step="${stepNum}"], .step[data-step="${stepNum}"]`);
  if (el) {
    el.classList.add('active');
  }
}

document.addEventListener('DOMContentLoaded', highlightStep);

const allFiles = document.getElementById("all-files");
const selectedFilesContainer = document.getElementById("selected-files");
const dropArea = document.getElementById("drop-area");
const analyzeButton = document.getElementById("analyze-btn");
const errorMessage = document.getElementById("error-message");
const successModal = document.getElementById("success-modal");
const checkQualityBtn = document.getElementById("check-quality-btn");
const skipQualityBtn = document.getElementById("skip-quality-btn");

let draggedFile = "";
let selectedFiles = [];

window.onload = function () {
  renderSelectedFiles();
  loadUploadedFiles();
};

async function loadUploadedFiles() {
  const user_id = localStorage.getItem("user_id");

  if (!user_id) {
    errorMessage.textContent = "User not found";
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/uploadedfiles/${user_id}`);
    const data = await response.json();
    allFiles.innerHTML = "";

    if (!response.ok) {
      errorMessage.textContent = data.detail || "Unable to load uploaded files";
      return;
    }

    if (!Array.isArray(data.filenames) || data.filenames.length === 0) {
      allFiles.innerHTML = "<p>No uploaded files found</p>";
      return;
    }

    data.filenames.forEach((filename) => {
      const div = document.createElement("div");
      div.className = "file-card";
      div.draggable = true;
      div.innerHTML = `
        <div class="file-details">
          <i class="fa-solid fa-file"></i>
          <div>
            <div class="file-name">${filename}</div>
          </div>
        </div>
      `;

      div.addEventListener("dragstart", function () {
        draggedFile = filename;
      });

      div.addEventListener("click", function () {
        addSelectedFile(filename);
      });

      allFiles.appendChild(div);
    });

    errorMessage.textContent = "";
  } catch (error) {
    errorMessage.textContent = "Unable to load uploaded files";
    console.log(error);
  }
}

dropArea.addEventListener("dragover", function (e) {
  e.preventDefault();
  dropArea.classList.add("dragover");
});

dropArea.addEventListener("dragleave", function () {
  dropArea.classList.remove("dragover");
});

dropArea.addEventListener("drop", function (e) {
  e.preventDefault();
  dropArea.classList.remove("dragover");
  addSelectedFile(draggedFile);
});

function addSelectedFile(filename) {
  if (!filename || selectedFiles.includes(filename)) {
    return;
  }

  selectedFiles.push(filename);
  renderSelectedFiles();
}

function renderSelectedFiles() {
  selectedFilesContainer.innerHTML = "";

  if (selectedFiles.length === 0) {
    selectedFilesContainer.innerHTML = `
      <div class="drop-message">
        <i class="fa-solid fa-cloud-arrow-down"></i>
        <p>Drag files here</p>
      </div>
    `;
    return;
  }

  selectedFiles.forEach((filename, index) => {
    const div = document.createElement("div");
    div.className = "selected-file";
    div.innerHTML = `
      <div class="selected-name">
        <i class="fa-solid fa-file"></i>
        <span>${filename}</span>
      </div>
      <button class="remove-btn" onclick="removeFile(${index})">
        <i class="fa-solid fa-xmark"></i>
      </button>
    `;
    selectedFilesContainer.appendChild(div);
  });
}

function removeFile(index) {
  selectedFiles.splice(index, 1);
  renderSelectedFiles();
}

window.removeFile = removeFile;

analyzeButton.addEventListener("click", startAnalysis);

async function startAnalysis() {
  if (selectedFiles.length === 0) {
    errorMessage.textContent = "Please select at least one file";
    return;
  }

  const user_id = localStorage.getItem("user_id");
  if (!user_id) {
    errorMessage.textContent = "User not found";
    return;
  }

  const loader = document.getElementById("loader");
  if (loader) {
    loader.style.display = "flex";
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/user/file/qualitycheck", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id, filenames: selectedFiles })
    });

    const data = await response.json();

    if (!response.ok) {
      errorMessage.textContent = data.detail || "Unable to start analysis";
      return;
    }

    localStorage.setItem("quality_id", data.quality_id);
    successModal.style.display = "flex";
  } catch (error) {
    console.log(error);
    errorMessage.textContent = "Server connection failed";
  } finally {
    if (loader) {
      loader.style.display = "none";
    }
  }
}

window.addEventListener("pageshow", function () {
  const loader = document.getElementById("loader");
  if (loader) loader.style.display = "none";
});

checkQualityBtn.addEventListener("click", function () {
  const quality_id = localStorage.getItem("quality_id");

  if (!quality_id) {
    errorMessage.textContent = "Quality ID not found";
    return;
  }

  window.location.href = "qualityreport.html";
});

skipQualityBtn.addEventListener("click", function () {
  successModal.style.display = "none";
});

successModal.addEventListener("click", function (e) {
  if (e.target === successModal) {
    successModal.style.display = "none";
  }
});
