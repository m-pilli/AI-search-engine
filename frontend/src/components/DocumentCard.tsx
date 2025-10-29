import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { DocumentCardProps } from '../types';

const DocumentCard: React.FC<DocumentCardProps> = ({ document, onViewDocument }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  // Truncate content for preview
  const previewLength = 200;
  const shouldTruncate = document.content.length > previewLength;
  const displayContent = isExpanded || !shouldTruncate 
    ? document.content 
    : document.content.substring(0, previewLength) + '...';

  // Format score for display
  const formatScore = (score: number) => (score * 100).toFixed(1);

  // Get score color based on value
  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <motion.div
      whileHover={{ y: -2 }}
      className="result-card"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <h3 className="text-xl font-semibold text-gray-900 flex-1 mr-4">
          {document.title}
        </h3>
        <div className="flex items-center space-x-2">
          {/* Overall Score */}
          <div className={`score-badge score-hybrid ${getScoreColor(document.score)}`}>
            {formatScore(document.score)}%
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="mb-4">
        <p className="text-gray-700 leading-relaxed">
          {displayContent}
        </p>
        {shouldTruncate && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium mt-2"
          >
            {isExpanded ? 'Show Less' : 'Show More'}
          </button>
        )}
      </div>

      {/* Metadata */}
      <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
        <div className="flex items-center space-x-4">
          <span>
            Created: {new Date(document.created_at).toLocaleDateString()}
          </span>
          <span>
            Updated: {new Date(document.updated_at).toLocaleDateString()}
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-xs text-gray-400">
            {document.content.length} characters
          </span>
        </div>
      </div>

      {/* Score Breakdown */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-1">
            <span className="text-xs text-gray-500">Semantic:</span>
            <span className={`text-sm font-medium ${getScoreColor(document.semantic_score)}`}>
              {formatScore(document.semantic_score)}%
            </span>
          </div>
          <div className="flex items-center space-x-1">
            <span className="text-xs text-gray-500">Keyword:</span>
            <span className={`text-sm font-medium ${getScoreColor(document.keyword_score)}`}>
              {formatScore(document.keyword_score)}%
            </span>
          </div>
        </div>
        
        <button
          onClick={() => onViewDocument(document.id)}
          className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors"
        >
          View Document
        </button>
      </div>

      {/* Metadata Tags */}
      {document.metadata && Object.keys(document.metadata).length > 0 && (
        <div className="flex flex-wrap gap-2">
          {Object.entries(document.metadata).map(([key, value]) => (
            <span
              key={key}
              className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full"
            >
              {key}: {String(value)}
            </span>
          ))}
        </div>
      )}
    </motion.div>
  );
};

export default DocumentCard;

