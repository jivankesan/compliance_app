import React, { useState } from "react";
import FileUploader from "./components/FileUploader.jsx";
import ProgressBar from "./components/ProgressBar.jsx";
import ChunkList from "./components/ChunkList.jsx";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [chunks, setChunks] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first.");
      return;
    }

    setUploading(true);
    setProgress(0);

    // Simulate a 20-second upload progress bar
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 99) {
          clearInterval(interval);
          return 99;
        }
        return prev + 1;
      });
    }, 400);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      // Use your actual backend endpoint here:
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        alert("Failed to upload file");
        setUploading(false);
        return;
      }

      const data = await response.json();
      setChunks(data.chunks);
      setUploading(false);
    } catch (error) {
      console.error(error);
      alert("An error occurred while uploading the file");
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen w-screen flex items-center justify-center bg-green-700 p-8">
      <div className="w-5/6 bg-white shadow-lg rounded-lg p-6">
        <h1 className="text-2xl font-bold text-green-800 mb-6 text-center">
          TDAM Compliance Checker
        </h1>
        <p className="text-center text-black mb-6">
          *Language models can make mistakes, use at your own discretion*
        </p>

        <FileUploader
          onFileChange={handleFileChange}
          onUpload={handleUpload}
          selectedFile={selectedFile}
        />

        {uploading && <ProgressBar progress={progress} />}

        {!uploading && chunks.length > 0 && <ChunkList chunks={chunks} />}
      </div>
    </div>
  );
}

export default App;
