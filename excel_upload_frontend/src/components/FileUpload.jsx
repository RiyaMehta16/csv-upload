import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResponse(res.data);
    } catch (error) {
      console.error("Upload failed:", error);
    }
  };

  return (
    <div>
      <h2>Upload an Excel File</h2>
      <input type="file" accept=".csv,.xls,.xlsx" onChange={handleFileChange} />

      <button onClick={handleUpload}>Upload</button>

      {response && (
        <div>
          <h3>Response:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
