import { useEffect, useState } from "react";

const API_URL = "http://localhost:8000"; // Flask backend URL

export default function App() {
  const [files, setFiles] = useState([]);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  // Fetch files from backend
  const fetchFiles = async () => {
    const res = await fetch(`${API_URL}/list-files`);
    const data = await res.json();
    console.log('Files response:', data);
    setFiles(data);
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    await fetch(`${API_URL}/upload-file`, {
      method: "POST",
      body: formData,
    });
    setFile(null);
    setUploading(false);
    fetchFiles();
  };

  const handleDelete = async (file_name) => {
    await fetch(`${API_URL}/delete-file/${encodeURIComponent(file_name)}`, { method: "DELETE" });
    fetchFiles();
  };

  const handleView = (file_name) => {
    window.open(`${API_URL}/download-file/${encodeURIComponent(file_name)}`, "_blank");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="gdrive-navbar">
        <div className="gdrive-logo">
          <svg width="32" height="32" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <polygon points="24,6 44,42 4,42" fill="#4285F4"/>
            <polygon points="24,6 44,42 34,42 14,6" fill="#34A853"/>
            <polygon points="4,42 24,6 14,6 4,42" fill="#FBBC05"/>
          </svg>
          Drive
        </div>
        <div className="text-gray-500 font-medium">My Drive</div>
      </nav>
      {/* Main Content */}
      <main className="gdrive-main">
        <form onSubmit={handleUpload} className="gdrive-upload-form">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="gdrive-file-input"
            required
          />
          <button
            type="submit"
            disabled={uploading}
            className="gdrive-upload-btn"
          >
            {uploading ? "Uploading..." : "Upload"}
          </button>
        </form>
        <h2 className="text-xl font-semibold mb-4">Files</h2>
        <ul className="gdrive-file-list">
          {files.map((f) => (
            <li key={f.file_name} className="gdrive-file-item">
              <span>{f.file_name}</span>
              <div className="flex gap-2">
                <button
                  onClick={() => handleView(f.file_name)}
                  className="gdrive-view-btn bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600 transition"
                >
                  View
                </button>
                <button
                  onClick={() => handleDelete(f.file_name)}
                  className="gdrive-delete-btn"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      </main>
    </div>
  );
}
