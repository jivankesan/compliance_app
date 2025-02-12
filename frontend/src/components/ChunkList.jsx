import React from "react";
import ChunkItem from "./ChunkItem.jsx";

function ChunkList({ chunks }) {
  return (
    <div className="mt-8">
      {chunks.map((chunkObj, idx) => (
        <ChunkItem key={idx} chunkObj={chunkObj} index={idx} />
      ))}
    </div>
  );
}

export default ChunkList;
