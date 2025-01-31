import { useState } from "react";

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

    // Simulate a 10-second upload progress bar
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 1;
      });
    }, 100);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
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
          TD Bank Compliance Checker
        </h1>
        <p className="text-center text-black mb-6">
          *AI can make mistakes, use at your own discretion*
        </p>

        <div className="flex flex-col items-center space-y-4">
          <label
            htmlFor="file-upload"
            className="cursor-pointer bg-green-600 hover:bg-green-700 text-white font-medium px-6 py-3 rounded-lg shadow-md transition-all duration-300"
          >
            Choose a File
          </label>
          <input
            id="file-upload"
            type="file"
            onChange={handleFileChange}
            className="hidden"
          />

          {selectedFile && (
            <p className="text-sm font-medium text-gray-800">
              Selected File:{" "}
              <span className="text-green-600">{selectedFile.name}</span>
            </p>
          )}

          <button
            onClick={handleUpload}
            className="bg-black text-white px-6 py-3 rounded-lg shadow-md hover:bg-green-900 transition-all duration-300"
          >
            Send
          </button>
        </div>

        {/* Progress Bar */}
        {uploading && (
          <div className="w-full mt-6 bg-gray-300 rounded-full overflow-hidden">
            <div
              className="bg-green-600 text-xs font-semibold text-white text-center leading-none py-2"
              style={{ width: `${progress}%` }}
            >
              {progress}%
            </div>
          </div>
        )}

        {/* Display Chunks After Upload Completes */}
        {!uploading && chunks.length > 0 && (
          <div className="mt-8">
            {chunks.map((chunkObj, idx) => (
              <div key={idx} className="mb-6 p-4 border bg-gray-100 rounded-lg">
                <div className="flex space-x-4">
                  <div className="w-1/2">
                    <h2 className="font-bold text-green-800 mb-2">
                      Document Chunk {idx + 1}
                    </h2>
                    <p className="text-sm text-black whitespace-pre-wrap">
                      {chunkObj.chunk}
                    </p>
                  </div>
                  <div className="w-1/2">
                    <h2 className="font-bold text-green-800 mb-2">
                      Generated Comment
                    </h2>
                    <p className="text-sm text-gray-700">{chunkObj.comment}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
