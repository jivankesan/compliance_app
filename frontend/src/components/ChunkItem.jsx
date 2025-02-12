import React from "react";
import DOMPurify from "dompurify";

/**
 * Example shape of chunkObj:
 * {
 *   chunk: "Here is some text...",
 *   comment: "<p>This is an HTML comment</p>",
 *   highlights: [
 *     { start: 5, end: 10, color: "yellow" },
 *     { start: 15, end: 25, color: "lightpink" }
 *   ]
 * }
 */

function ChunkItem({ chunkObj, index }) {
  const { chunk, comment, highlights = [] } = chunkObj;

  // Apply highlight styles to portions of the text
  const highlightChunk = (text, highlightsArray) => {
    let result = [];
    let lastIndex = 0;

    highlightsArray.forEach(({ start, end, color }, i) => {
      // Add text before the highlight
      if (start > lastIndex) {
        result.push(
          <span key={`normal-${i}`}>{text.slice(lastIndex, start)}</span>
        );
      }

      // Add highlighted text
      result.push(
        <span key={`highlight-${i}`} style={{ backgroundColor: color }}>
          {text.slice(start, end)}
        </span>
      );

      lastIndex = end;
    });

    // Add any remaining text after the last highlight
    if (lastIndex < text.length) {
      result.push(
        <span key="remaining-text">{text.slice(lastIndex)}</span>
      );
    }

    return result;
  };

  const safeHTML = DOMPurify.sanitize(comment);

  return (
    <div className="mb-6 p-4 border bg-gray-100 rounded-lg">
      <div className="flex space-x-4">
        {/* Left side: Document text chunk (with optional highlights) */}
        <div className="w-1/2">
          <h2 className="font-bold text-green-800 mb-2">
            Document Chunk {index + 1}
          </h2>
          <p className="text-sm text-black whitespace-pre-wrap">
            {highlights && highlights.length > 0
              ? highlightChunk(chunk, highlights)
              : chunk}
          </p>
        </div>

        {/* Right side: Generated comment */}
        <div className="w-1/2">
          <h2 className="font-bold text-green-800 mb-2">
            Generated Comment
          </h2>
          <p dangerouslySetInnerHTML={{ __html: safeHTML }} />
        </div>
      </div>
    </div>
  );
}

export default ChunkItem;
