import React from 'react';
import { motion } from 'framer-motion';
import { SearchConfigProps } from '../types';

const SearchConfig: React.FC<SearchConfigProps> = ({ config, onConfigChange }) => {
  const handleAlphaChange = (alpha: number) => {
    onConfigChange({ ...config, alpha });
  };

  const handleLimitChange = (limit: number) => {
    onConfigChange({ ...config, limit });
  };

  const handleSearchTypeChange = (searchType: 'hybrid' | 'semantic' | 'keyword') => {
    onConfigChange({ ...config, searchType });
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Search Configuration</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Search Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Search Type
          </label>
          <div className="space-y-2">
            {[
              { value: 'hybrid', label: 'Hybrid', description: 'Combines semantic and keyword search' },
              { value: 'semantic', label: 'Semantic', description: 'AI-powered meaning-based search' },
              { value: 'keyword', label: 'Keyword', description: 'Traditional text matching' },
            ].map((option) => (
              <label key={option.value} className="flex items-start">
                <input
                  type="radio"
                  name="searchType"
                  value={option.value}
                  checked={config.searchType === option.value}
                  onChange={() => handleSearchTypeChange(option.value as any)}
                  className="mt-1 mr-3 text-blue-600 focus:ring-blue-500"
                />
                <div>
                  <div className="text-sm font-medium text-gray-900">{option.label}</div>
                  <div className="text-xs text-gray-500">{option.description}</div>
                </div>
              </label>
            ))}
          </div>
        </div>

        {/* Alpha Weight (for hybrid search) */}
        {config.searchType === 'hybrid' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Semantic Weight (α): {config.alpha.toFixed(1)}
            </label>
            <div className="space-y-2">
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={config.alpha}
                onChange={(e) => handleAlphaChange(parseFloat(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              />
              <div className="flex justify-between text-xs text-gray-500">
                <span>Keyword Focus</span>
                <span>Semantic Focus</span>
              </div>
              <div className="text-xs text-gray-600">
                {config.alpha === 0.5 ? 'Balanced' : 
                 config.alpha > 0.5 ? 'Semantic-leaning' : 'Keyword-leaning'}
              </div>
            </div>
          </div>
        )}

        {/* Results Limit */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Results Limit
          </label>
          <select
            value={config.limit}
            onChange={(e) => handleLimitChange(parseInt(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value={5}>5 results</option>
            <option value={10}>10 results</option>
            <option value={20}>20 results</option>
            <option value={50}>50 results</option>
          </select>
        </div>
      </div>

      {/* Search Type Info */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="mt-4 p-3 bg-gray-50 rounded-md"
      >
        <div className="text-sm text-gray-600">
          <strong>{config.searchType.charAt(0).toUpperCase() + config.searchType.slice(1)} Search:</strong>{' '}
          {config.searchType === 'hybrid' && 
            `Combines ${(config.alpha * 100).toFixed(0)}% semantic understanding with ${((1 - config.alpha) * 100).toFixed(0)}% keyword matching for optimal relevance.`
          }
          {config.searchType === 'semantic' && 
            'Uses AI embeddings to understand meaning and context, finding documents that are conceptually similar even without exact keyword matches.'
          }
          {config.searchType === 'keyword' && 
            'Traditional text search using TF-IDF scoring to find documents containing the exact words in your query.'
          }
        </div>
      </motion.div>
    </div>
  );
};

export default SearchConfig;

