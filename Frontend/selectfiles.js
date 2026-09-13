window.addEventListener('load', () => {
  const loader = document.getElementById('page-loader');
  if (loader) setTimeout(() => loader.classList.add('hidden'), 200);
});

function highlightStep() {
  const page = window.location.pathname.split('/').pop();
  const map = { 'user.html': '1', 'upload.html': '2', 'selectfiles.html': '3', 'qualityreport.html': '4' };
  const stepNum = map[page] || '3';
  document.querySelectorAll('.nav-link, .step').forEach(el => el.classList.remove('active'));
  const el = document.querySelector(`.nav-link[data-step="${stepNum}"], .step[data-step="${stepNum}"]`);
  if (el) el.classList.add('active');
}
document.addEventListener('DOMContentLoaded', () => { highlightStep(); initPage(); });

const allFiles = () => document.getElementById('all-files');
const selectedFilesContainer = () => document.getElementById('selected-files');
const dropArea = () => document.getElementById('drop-area');
const analyzeButton = () => document.getElementById('analyze-btn');
const errorMessage = () => document.getElementById('error-message');

let draggedFile = '';
let selectedFiles = [];

function initPage(){
  renderSelectedFiles();
  loadUploadedFiles();
  const da = dropArea();
  if (da){
    da.addEventListener('dragover', e => { e.preventDefault(); da.classList.add('dragover'); });
    da.addEventListener('dragleave', () => da.classList.remove('dragover'));
    da.addEventListener('drop', e => { e.preventDefault(); da.classList.remove('dragover'); addSelectedFile(draggedFile); });
  }
  const btn = analyzeButton(); if (btn) btn.addEventListener('click', startAnalysis);
}

async function loadUploadedFiles(){
  const elAll = allFiles(); const err = errorMessage();
  const user_id = localStorage.getItem('user_id');
  if (!elAll) return;
  if (!user_id){ if (err) err.textContent = 'User not found'; return; }
  try{
    const response = await fetch(`http://127.0.0.1:8000/uploadedfiles/${user_id}`);
    const data = await response.json();
    elAll.innerHTML = '';
    if (!response.ok){ if (err) err.textContent = data.detail || 'Unable to load uploaded files'; return; }
    if (!Array.isArray(data.filenames) || data.filenames.length === 0){ elAll.innerHTML = '<p>No uploaded files found</p>'; return; }
    data.filenames.forEach(filename => {
      const div = document.createElement('div'); div.className = 'file-card'; div.draggable = true;
      div.innerHTML = `<div class="file-details"><i class="fa-solid fa-file"></i><div><div class="file-name">${filename}</div></div></div>`;
      div.addEventListener('dragstart', () => { draggedFile = filename; });
      div.addEventListener('click', () => addSelectedFile(filename));
      elAll.appendChild(div);
    });
    if (err) err.textContent = '';
  }catch(e){ if (err) err.textContent = 'Unable to load uploaded files'; console.error(e); }
}

function addSelectedFile(filename){ if (!filename || selectedFiles.includes(filename)) return; selectedFiles.push(filename); renderSelectedFiles(); }

function renderSelectedFiles(){
  const container = selectedFilesContainer(); if (!container) return; container.innerHTML = '';
  if (selectedFiles.length === 0){ container.innerHTML = `<div class="drop-message"><i class="fa-solid fa-cloud-arrow-down"></i><p>Drag files here</p></div>`; return; }
  selectedFiles.forEach((filename, index) =>{
    const div = document.createElement('div'); div.className = 'selected-file';
    div.innerHTML = `<div class="selected-name"><i class="fa-solid fa-file"></i><span>${filename}</span></div><button class="remove-btn" data-index="${index}"><i class="fa-solid fa-xmark"></i></button>`;
    const btn = div.querySelector('.remove-btn'); btn && btn.addEventListener('click', () => removeFile(index));
    container.appendChild(div);
  });
}

function removeFile(index){ selectedFiles.splice(index,1); renderSelectedFiles(); }

async function startAnalysis(){
  const err = errorMessage(); if (selectedFiles.length === 0){ if (err) err.textContent = 'Please select at least one file'; return; }
  const user_id = localStorage.getItem('user_id'); if (!user_id){ if (err) err.textContent = 'User not found'; return; }
  const loader = document.getElementById('loader'); if (loader) loader.style.display = 'flex';
  try{
    const response = await fetch('http://127.0.0.1:8000/user/file/qualitycheck', {
      method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ user_id, filenames: selectedFiles })
    });
    const data = await response.json();
    if (!response.ok){ if (err) err.textContent = data.detail || 'Unable to start analysis'; return; }
    localStorage.setItem('quality_id', data.quality_id);
    // Directly navigate to the report page (skip popup)
    window.location.href = 'qualityreport.html';
  }catch(e){ console.error(e); if (err) err.textContent = 'Server connection failed'; }
  finally{ if (loader) loader.style.display = 'none'; }
}

window.addEventListener('pageshow', () => { const loader = document.getElementById('loader'); if (loader) loader.style.display = 'none'; });
