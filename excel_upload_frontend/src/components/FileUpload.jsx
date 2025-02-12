import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null); //response: Stores the response from the backend.

  const handleFileChange = (e) => {
    setFile(e.target.files[0]); //e.target.files[0] extracts the first selected file.
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!"); //If no file is selected, show an alert and exit.
      return;
    }

    const formData = new FormData();
    //formData.append("file", file); attaches the file under the key "file".
    formData.append("file", file);
    //This is needed because files cannot be sent as JSON.

    try {
      //Sends data to Flask backend (/upload).
      const res = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        //headers: { "Content-Type": "multipart/form-data" } tells Flask not to expect JSON but rather a file upload.
      });
      setResponse(res.data);
      //setResponse(res.data); saves the server response to response, which will be displayed later.
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
/*

=====Headers (Content-Type)
    "Content-Type": "multipart/form-data":
    This tells Flask to expect a file upload instead of JSON.
    If not set, Flask might try to parse the file as JSON and throw an error.
===== AXIOS
    axios.post(url, data, config)   
    What it does: A library for making HTTP requests.
    Why use it? It simplifies API calls and provides features like automatic JSON conversion and error handling.
===== FORMDATA
    What it does: Helps send files and other data in multipart/form-data format.
        Example:
    const formData = new FormData();
    formData.append("key", value);

==== 🔹 JSON (JSON.stringify())
    Converts JavaScript objects into readable JSON format.
    Example:
        const obj = { name: "John", age: 25 };
        console.log(JSON.stringify(obj, null, 2));
    Output:
        {
        "name": "John",
        "age": 25
        }
*/
