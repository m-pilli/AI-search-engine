import React from 'react';
import { motion } from 'framer-motion';
import { SearchResultsProps } from '../types';
import DocumentCard from './DocumentCard';
import SearchStats from './SearchStats';

const SearchResults: React.FC<SearchResultsProps> = ({
  results,
  loading,
  error,
  responseTime,
  config,
}) => {
  const safeResults = Array.isArray(results) ? results : [];
  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 text-lg font-medium mb-2">Search Error</div>
        <div className="text-gray-600">{error}</div>
      </div>
    );
  }

  if (safeResults.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-12"
      >
        <div className="max-w-md mx-auto">
          <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
            <svg
              className="w-8 h-8 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.29-1.009-5.824-2.709"
              />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            No Results Found
          </h3>
          <p className="text-gray-600">
            Try adjusting your search terms or search configuration.
          </p>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Search Stats */}
      <SearchStats
        totalResults={safeResults.length}
        responseTime={responseTime}
        searchType={config.searchType}
        alpha={config.alpha}
      />

      {/* Results List */}
      <div className="space-y-4">
        {safeResults.map((result, index) => (
          <motion.div
            key={result.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <DocumentCard
              document={result}
              onViewDocument={(id) => {
                // Navigate to document page
                window.open(`/document/${id}`, '_blank');
              }}
            />
          </motion.div>
        ))}
      </div>

      {/* Load More Button (if needed) */}
      {safeResults.length >= config.limit && (
        <div className="text-center pt-6">
          <button
            onClick={() => {
              // Implement load more functionality
              console.log('Load more results');
            }}
            className="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Load More Results
          </button>
        </div>
      )}
    </motion.div>
  );
};

export default SearchResults;

