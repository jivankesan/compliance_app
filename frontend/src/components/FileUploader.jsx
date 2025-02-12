import React from "react";

function FileUploader({ onFileChange, onUpload, selectedFile }) {
  return (
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
        onChange={onFileChange}
        className="hidden"
      />

      {selectedFile && (
        <p className="text-sm font-medium text-gray-800">
          Selected File:{" "}
          <span className="text-green-600">{selectedFile.name}</span>
        </p>
      )}

      <button
        onClick={onUpload}
        className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg shadow-md hover:bg-green-900 transition-all duration-300"
      >
        Check
      </button>
    </div>
  );
}

export default FileUploader;
