// scripts.js

const API_BASE = 'http://15.206.92.180:8000';

// --- Upload Document 
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const fileInput = document.getElementById('fileInput');
  const uploadStatus = document.getElementById('uploadStatus');

  if (fileInput.files.length === 0) {
    uploadStatus.textContent = 'Please select a file.';
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  try {
    const res = await fetch(`${API_BASE}/upload`, {  // api 
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    uploadStatus.textContent = `Uploaded: ${data.filename}`;
  } catch (err) {
    console.error(err);
    uploadStatus.textContent = 'Upload failed. Please try again.';
  }
});

// --- Send User Query ---
document.getElementById('queryForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const userInput = document.getElementById('userInput');
  const chatMessages = document.getElementById('chatMessages');
  const message = userInput.value.trim();

  if (!message) return;

  appendMessage('user', message);
  userInput.value = '';

  try {
    const res = await fetch(`${API_BASE}/query`, {  // api
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: message })
    });
    const data = await res.json();
    appendMessage('bot', data.response);
  } catch (err) {
    console.error(err);
    appendMessage('bot', 'Something went wrong. Please try again.');
  }
});

function appendMessage(sender, text) {
  const msg = document.createElement('div');
  msg.className = `message ${sender}-message`;
  msg.textContent = text;
  const chatMessages = document.getElementById('chatMessages');
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}
