import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';
import { motion } from 'framer-motion';
import SearchBar from '../components/SearchBar';
import SearchResults from '../components/SearchResults';
import SearchConfig from '../components/SearchConfig';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { searchApi, handleApiError } from '../services/api';
import { SearchConfig as SearchConfigType, SearchResult } from '../types';
import toast from 'react-hot-toast';

const SearchPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [searchConfig, setSearchConfig] = useState<SearchConfigType>({
    query: '',
    limit: 10,
    alpha: 0.7,
    searchType: 'hybrid',
  });
  const [hasSearched, setHasSearched] = useState(false);

  // Search query
  const {
    data: searchData,
    isLoading,
    error,
    refetch,
  } = useQuery(
    ['search', query, searchConfig],
    () => searchApi.search(query, searchConfig.limit, searchConfig.alpha, searchConfig.searchType),
    {
      enabled: false, // Don't auto-search
      retry: 1,
      onError: (error) => {
        const apiError = handleApiError(error);
        toast.error(apiError.error);
      },
    }
  );

  // Handle search
  const handleSearch = (searchQuery: string, config: SearchConfigType) => {
    if (!searchQuery.trim()) {
      toast.error('Please enter a search query');
      return;
    }

    setQuery(searchQuery);
    setSearchConfig(config);
    setHasSearched(true);
    refetch();
  };

  // Handle config change
  const handleConfigChange = (config: SearchConfigType) => {
    setSearchConfig(config);
    if (hasSearched && query) {
      refetch();
    }
  };

  // Get suggestions
  const { data: suggestions } = useQuery(
    ['suggestions', query],
    () => searchApi.getSuggestions(query),
    {
      enabled: query.length >= 2,
      staleTime: 5 * 60 * 1000, // 5 minutes
    }
  );

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-8"
      >
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI Search Engine
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Advanced semantic and keyword search powered by machine learning.
          Find relevant results with our hybrid ranking algorithm.
        </p>
      </motion.div>

      {/* Search Configuration */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="mb-8"
      >
        <SearchConfig
          config={searchConfig}
          onConfigChange={handleConfigChange}
        />
      </motion.div>

      {/* Search Bar */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="mb-8"
      >
        <SearchBar
          onSearch={handleSearch}
          loading={isLoading}
          suggestions={suggestions || []}
        />
      </motion.div>

      {/* Search Results */}
      {hasSearched && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          {isLoading ? (
            <div className="flex justify-center py-12">
              <LoadingSpinner size="large" />
            </div>
          ) : error ? (
            <ErrorMessage error={handleApiError(error).error} />
          ) : searchData ? (
            <SearchResults
              results={searchData.results}
              loading={isLoading}
              error={null}
              responseTime={searchData.response_time_ms}
              config={searchConfig}
            />
          ) : null}
        </motion.div>
      )}

      {/* Empty State */}
      {!hasSearched && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="text-center py-16"
        >
          <div className="max-w-md mx-auto">
            <div className="w-24 h-24 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
              <svg
                className="w-12 h-12 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Start Searching
            </h3>
            <p className="text-gray-600">
              Enter your query above to search through our document collection
              using advanced AI-powered semantic and keyword matching.
            </p>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default SearchPage;

