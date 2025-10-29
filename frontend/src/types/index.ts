// API Response Types
export interface SearchResult {
  id: string;
  title: string;
  content: string;
  metadata: Record<string, any>;
  score: number;
  semantic_score: number;
  keyword_score: number;
  created_at: string;
  updated_at: string;
}

export interface SearchResponse {
  results: SearchResult[];
  query: string;
  total_results: number;
  response_time_ms: number;
  alpha?: number;
  search_stats?: {
    semantic_results_count: number;
    keyword_results_count: number;
    unique_documents: number;
  };
}

export interface Document {
  _id: string;
  title: string;
  content: string;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface DocumentResponse {
  documents: Document[];
  pagination: {
    page: number;
    per_page: number;
    total: number;
    pages: number;
  };
}

export interface SearchStats {
  semantic_search: {
    total_documents: number;
    model_name: string;
    embedding_dimension: number;
    index_type: string;
  };
  keyword_search: {
    total_documents: number;
    vocabulary_size: number;
    max_features: number;
    ngram_range: [number, number];
  };
  database: {
    total_documents: number;
    total_content_length: number;
  };
  default_alpha: number;
}

export interface HealthStatus {
  status: 'healthy' | 'unhealthy' | 'degraded';
  timestamp: number;
  service: string;
  version: string;
  services?: Record<string, {
    status: string;
    type?: string;
    connected?: boolean;
    error?: string;
  }>;
}

// Search Configuration Types
export interface SearchConfig {
  query: string;
  limit: number;
  alpha: number;
  searchType: 'hybrid' | 'semantic' | 'keyword';
}

// UI State Types
export interface SearchState {
  query: string;
  results: SearchResult[];
  loading: boolean;
  error: string | null;
  config: SearchConfig;
  responseTime: number;
}

export interface FilterState {
  minScore: number;
  maxResults: number;
  searchType: 'hybrid' | 'semantic' | 'keyword';
  alpha: number;
}

// Component Props Types
export interface SearchBarProps {
  onSearch: (query: string, config: SearchConfig) => void;
  loading: boolean;
  suggestions?: string[];
}

export interface SearchResultsProps {
  results: SearchResult[];
  loading: boolean;
  error: string | null;
  responseTime: number;
  config: SearchConfig;
}

export interface SearchConfigProps {
  config: SearchConfig;
  onConfigChange: (config: SearchConfig) => void;
}

export interface DocumentCardProps {
  document: SearchResult;
  onViewDocument: (id: string) => void;
}

// API Error Types
export interface ApiError {
  error: string;
  message?: string;
  status?: number;
}

