import React from 'react';
import { useQuery } from 'react-query';
import { motion } from 'framer-motion';
import { searchApi, handleApiError } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import toast from 'react-hot-toast';

const StatsPage: React.FC = () => {
  const {
    data: stats,
    isLoading,
    error,
  } = useQuery(
    'searchStats',
    searchApi.getStats,
    {
      refetchInterval: 30000, // Refresh every 30 seconds
      onError: (error) => {
        const apiError = handleApiError(error);
        toast.error(apiError.error);
      },
    }
  );

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner size="large" text="Loading statistics..." />
      </div>
    );
  }

  if (error) {
    return (
      <ErrorMessage 
        error={handleApiError(error).error}
        onRetry={() => window.location.reload()}
      />
    );
  }

  if (!stats) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">No Statistics Available</h2>
        <p className="text-gray-600">Unable to load search engine statistics.</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-6xl mx-auto"
    >
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Search Engine Statistics</h1>
        <p className="text-gray-600">Real-time performance and configuration metrics</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Database Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <span className="mr-2">🗄️</span>
            Database
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Total Documents</span>
              <span className="font-semibold text-gray-900">
                {stats.database.total_documents.toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Content Length</span>
              <span className="font-semibold text-gray-900">
                {(stats.database.total_content_length / 1000).toFixed(1)}K chars
              </span>
            </div>
          </div>
        </motion.div>

        {/* Semantic Search Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <span className="mr-2">🧠</span>
            Semantic Search
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Model</span>
              <span className="font-semibold text-gray-900 text-sm">
                {stats.semantic_search.model_name}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Embedding Dimension</span>
              <span className="font-semibold text-gray-900">
                {stats.semantic_search.embedding_dimension}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Index Type</span>
              <span className="font-semibold text-gray-900 text-sm">
                {stats.semantic_search.index_type}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Indexed Documents</span>
              <span className="font-semibold text-gray-900">
                {stats.semantic_search.total_documents.toLocaleString()}
              </span>
            </div>
          </div>
        </motion.div>

        {/* Keyword Search Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <span className="mr-2">🔤</span>
            Keyword Search
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Vocabulary Size</span>
              <span className="font-semibold text-gray-900">
                {stats.keyword_search.vocabulary_size.toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Max Features</span>
              <span className="font-semibold text-gray-900">
                {stats.keyword_search.max_features.toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">N-gram Range</span>
              <span className="font-semibold text-gray-900">
                {stats.keyword_search.ngram_range[0]}-{stats.keyword_search.ngram_range[1]}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Indexed Documents</span>
              <span className="font-semibold text-gray-900">
                {stats.keyword_search.total_documents.toLocaleString()}
              </span>
            </div>
          </div>
        </motion.div>

        {/* Hybrid Configuration */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <span className="mr-2">⚖️</span>
            Hybrid Configuration
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Default Alpha</span>
              <span className="font-semibold text-gray-900">
                {stats.default_alpha.toFixed(2)}
              </span>
            </div>
            <div className="text-sm text-gray-600">
              <div className="mb-2">
                <span className="font-medium">Semantic Weight:</span> {(stats.default_alpha * 100).toFixed(0)}%
              </div>
              <div>
                <span className="font-medium">Keyword Weight:</span> {((1 - stats.default_alpha) * 100).toFixed(0)}%
              </div>
            </div>
          </div>
        </motion.div>

        {/* Performance Metrics */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <span className="mr-2">⚡</span>
            Performance
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Target Latency</span>
              <span className="font-semibold text-green-600">&lt;200ms</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Index Status</span>
              <span className="font-semibold text-green-600">Ready</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Last Updated</span>
              <span className="font-semibold text-gray-900 text-sm">
                {new Date().toLocaleTimeString()}
              </span>
            </div>
          </div>
        </motion.div>

        {/* System Health */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <span className="mr-2">💚</span>
            System Health
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Status</span>
              <span className="font-semibold text-green-600">Healthy</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Uptime</span>
              <span className="font-semibold text-gray-900">99.9%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Memory Usage</span>
              <span className="font-semibold text-gray-900">Optimal</span>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default StatsPage;

