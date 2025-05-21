const API_BASE = 'http://15.206.92.180:8000/api';

async function fetchDocuments() {
  const res = await fetch(`${API_BASE}/documents`);
  const data = await res.json();
  const list = data.documents.map(doc => `<div>${doc}</div>`).join('');
  document.getElementById('documentList').innerHTML = list || 'No documents found.';
}

async function fetchThemes() {
  const res = await fetch(`${API_BASE}/query/themes`);
  const data = await res.json();
  document.getElementById('themeResults').textContent = data.themes?.join('\n') || 'No themes found.';
}

async function fetchCitations() {
  const res = await fetch(`${API_BASE}/query/citations`);
  const data = await res.json();
  document.getElementById('citationMap').textContent = JSON.stringify(data.citations, null, 2);
}

async function exportToPDF() {
  const res = await fetch(`${API_BASE}/export/pdf`);
  const blob = await res.blob();
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'document_results.pdf';
  link.click();
}

async function applyFilter() {
  const type = document.getElementById('filterType').value;
  const value = document.getElementById('filterValue').value;
  if (!type || !value) {
    alert('Please select a filter type and enter a value.');
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/query/filter`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, value })
    });
    const data = await res.json();
    alert(`Filtered Results:\n${JSON.stringify(data.results, null, 2)}`);
  } catch (err) {
    alert('Failed to apply filter. Please try again.');
  }
}

function applyFilters() {
  const type = document.getElementById('filterType').value;
  const author = document.getElementById('filterAuthor').value;
  const date = document.getElementById('filterDate').value;

  alert(`Filters applied:\nType: ${type}\nAuthor: ${author}\nDate: ${date}`);
}

function identifyThemes() {
  alert("Theme identification in progress...");
}

function viewCitationMap() {
  alert("Opening citation map...");
}

function exportToPDF() {
  alert("Exporting document to PDF...");
}
