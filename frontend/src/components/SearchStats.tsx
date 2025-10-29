import React from 'react';
import { motion } from 'framer-motion';

interface SearchStatsProps {
  totalResults: number;
  responseTime: number;
  searchType: string;
  alpha?: number;
}

const SearchStats: React.FC<SearchStatsProps> = ({
  totalResults,
  responseTime,
  searchType,
  alpha,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="bg-gray-50 rounded-lg p-4 border border-gray-200"
    >
      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center space-x-6">
          <div>
            <span className="text-gray-500">Results:</span>
            <span className="ml-1 font-semibold text-gray-900">{totalResults}</span>
          </div>
          <div>
            <span className="text-gray-500">Response Time:</span>
            <span className="ml-1 font-semibold text-gray-900">{responseTime}ms</span>
          </div>
          <div>
            <span className="text-gray-500">Search Type:</span>
            <span className="ml-1 font-semibold text-gray-900 capitalize">{searchType}</span>
          </div>
          {alpha !== undefined && (
            <div>
              <span className="text-gray-500">Alpha:</span>
              <span className="ml-1 font-semibold text-gray-900">{alpha.toFixed(1)}</span>
            </div>
          )}
        </div>
        
        {/* Performance indicator */}
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${
            responseTime < 200 ? 'bg-green-500' : 
            responseTime < 500 ? 'bg-yellow-500' : 'bg-red-500'
          }`}></div>
          <span className="text-xs text-gray-500">
            {responseTime < 200 ? 'Fast' : 
             responseTime < 500 ? 'Moderate' : 'Slow'}
          </span>
        </div>
      </div>
    </motion.div>
  );
};

export default SearchStats;

