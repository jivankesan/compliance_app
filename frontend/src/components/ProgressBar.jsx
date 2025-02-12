import React from "react";

function ProgressBar({ progress }) {
  return (
    <div className="w-full mt-6 bg-gray-300 rounded-full overflow-hidden">
      <div
        className="bg-green-600 text-xs font-semibold text-white text-center leading-none py-2"
        style={{ width: `${progress}%` }}
      >
        {progress}%
      </div>
    </div>
  );
}

export default ProgressBar;
