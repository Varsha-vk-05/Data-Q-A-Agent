import React from 'react';

const cardColors = [
  'rgba(255, 240, 245, 0.85)', // Lavender blush
  'rgba(240, 248, 255, 0.85)', // Alice blue
  'rgba(245, 255, 250, 0.85)', // Mint cream
  'rgba(255, 250, 240, 0.85)', // Floral white
  'rgba(253, 245, 230, 0.85)', // Old lace
  'rgba(240, 255, 240, 0.85)', // Honeydew
  'rgba(255, 245, 238, 0.85)', // Seashell
  'rgba(230, 230, 250, 0.85)'  // Lavender
];

const borderColors = [
  'rgba(255, 182, 193, 0.5)', // Light pink
  'rgba(173, 216, 230, 0.5)', // Light blue
  'rgba(152, 251, 152, 0.5)', // Pale green
  'rgba(255, 228, 196, 0.5)', // Bisque
  'rgba(255, 222, 173, 0.5)', // Navajo white
  'rgba(144, 238, 144, 0.5)', // Light green
  'rgba(255, 160, 122, 0.5)', // Light salmon
  'rgba(216, 191, 216, 0.5)'  // Thistle
];

export default function QACard({ item, index }) {
  const bgColor = cardColors[index % cardColors.length];
  const borderColor = borderColors[index % borderColors.length];

  return (
    <div 
      className="qa-card" 
      style={{ 
        animationDelay: `${(index % 10) * 0.1}s`,
        backgroundColor: bgColor,
        borderColor: borderColor
      }}
    >
      <div className="question">
        Q{index + 1}: {item.q}
      </div>
      <div className="answer">
        {item.a}
        {item.table && (
          <div className="pre-formatted">
            <pre>{item.table}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
