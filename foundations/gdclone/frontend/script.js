const API_URL = 'http://localhost:5000'; // Change to your EC2 public IP when deployed

function fetchFiles() {
  fetch(`${API_URL}/files`)
    .then(res => res.json())
    .then(files => {
      const list = document.getElementById('fileList');
      list.innerHTML = '';
      files.forEach(file => {
        const li = document.createElement('li');
        li.textContent = file.name;
        const delBtn = document.createElement('button');
        delBtn.textContent = 'Delete';
        delBtn.className = 'delete-btn';
        delBtn.onclick = () => deleteFile(file.id);
        li.appendChild(delBtn);
        list.appendChild(li);
      });
    });
}

function deleteFile(id) {
  fetch(`${API_URL}/delete/${id}`, { method: 'DELETE' })
    .then(res => res.json())
    .then(() => fetchFiles());
}

document.getElementById('uploadForm').onsubmit = function(e) {
  e.preventDefault();
  const fileInput = document.getElementById('fileInput');
  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  fetch(`${API_URL}/upload`, {
    method: 'POST',
    body: formData
  })
    .then(res => res.json())
    .then(() => {
      fileInput.value = '';
      fetchFiles();
    });
};

window.onload = fetchFiles;
