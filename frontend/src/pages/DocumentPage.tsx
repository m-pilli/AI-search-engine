import React from 'react';
import { useQuery } from 'react-query';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { documentsApi, handleApiError } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import toast from 'react-hot-toast';

const DocumentPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  const {
    data: document,
    isLoading,
    error,
  } = useQuery(
    ['document', id],
    () => documentsApi.getDocument(id!),
    {
      enabled: !!id,
      onError: (error) => {
        const apiError = handleApiError(error);
        toast.error(apiError.error);
      },
    }
  );

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner size="large" text="Loading document..." />
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

  if (!document) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Document Not Found</h2>
        <p className="text-gray-600">The requested document could not be found.</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto"
    >
      {/* Document Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          {document.title}
        </h1>
        
        <div className="flex items-center justify-between text-sm text-gray-500 mb-6">
          <div className="flex items-center space-x-6">
            <span>
              Created: {new Date(document.created_at).toLocaleDateString()}
            </span>
            <span>
              Updated: {new Date(document.updated_at).toLocaleDateString()}
            </span>
            <span>
              {document.content.length} characters
            </span>
          </div>
        </div>

        {/* Metadata */}
        {document.metadata && Object.keys(document.metadata).length > 0 && (
          <div className="flex flex-wrap gap-2 mb-6">
            {Object.entries(document.metadata).map(([key, value]) => (
              <span
                key={key}
                className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
              >
                {key}: {String(value)}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Document Content */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Content</h2>
        <div className="prose max-w-none">
          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
            {document.content}
          </p>
        </div>
      </div>

      {/* Actions */}
      <div className="mt-6 flex justify-center">
        <button
          onClick={() => window.history.back()}
          className="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
        >
          Back to Search
        </button>
      </div>
    </motion.div>
  );
};

export default DocumentPage;

