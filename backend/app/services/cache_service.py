import redis
import json
import pickle
import logging
from typing import Any, Optional, Union
from datetime import datetime, timedelta
import hashlib

logger = logging.getLogger(__name__)

class CacheService:
    """Redis-based caching service for search results and embeddings."""
    
    def __init__(self, redis_url: str, default_ttl: int = 3600):
        self.redis_client = redis.from_url(redis_url, decode_responses=False)
        self.default_ttl = default_ttl
        
        # Test connection
        try:
            self.redis_client.ping()
            logger.info("Redis cache connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    def _generate_key(self, prefix: str, *args) -> str:
        """Generate a cache key from prefix and arguments."""
        key_parts = [prefix] + [str(arg) for arg in args]
        key_string = ":".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            cached_data = self.redis_client.get(key)
            if cached_data:
                return pickle.loads(cached_data)
            return None
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL."""
        try:
            serialized_data = pickle.dumps(value)
            ttl = ttl or self.default_ttl
            self.redis_client.setex(key, ttl, serialized_data)
            return True
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Error checking cache key {key}: {e}")
            return False
    
    def get_ttl(self, key: str) -> int:
        """Get TTL for a key."""
        try:
            return self.redis_client.ttl(key)
        except Exception as e:
            logger.error(f"Error getting TTL for key {key}: {e}")
            return -1
    
    def extend_ttl(self, key: str, additional_seconds: int) -> bool:
        """Extend TTL for a key."""
        try:
            current_ttl = self.get_ttl(key)
            if current_ttl > 0:
                new_ttl = current_ttl + additional_seconds
                self.redis_client.expire(key, new_ttl)
                return True
            return False
        except Exception as e:
            logger.error(f"Error extending TTL for key {key}: {e}")
            return False
    
    # Search-specific cache methods
    def cache_search_result(self, query: str, config: dict, result: dict) -> bool:
        """Cache search result."""
        key = self._generate_key("search", query, str(sorted(config.items())))
        return self.set(key, result, ttl=1800)  # 30 minutes
    
    def get_cached_search_result(self, query: str, config: dict) -> Optional[dict]:
        """Get cached search result."""
        key = self._generate_key("search", query, str(sorted(config.items())))
        return self.get(key)
    
    def cache_embedding(self, text: str, embedding: list) -> bool:
        """Cache text embedding."""
        key = self._generate_key("embedding", text)
        return self.set(key, embedding, ttl=86400)  # 24 hours
    
    def get_cached_embedding(self, text: str) -> Optional[list]:
        """Get cached text embedding."""
        key = self._generate_key("embedding", text)
        return self.get(key)
    
    def cache_document_embedding(self, doc_id: str, embedding: list) -> bool:
        """Cache document embedding."""
        key = self._generate_key("doc_embedding", doc_id)
        return self.set(key, embedding, ttl=86400)  # 24 hours
    
    def get_cached_document_embedding(self, doc_id: str) -> Optional[list]:
        """Get cached document embedding."""
        key = self._generate_key("doc_embedding", doc_id)
        return self.get(key)
    
    def cache_popular_queries(self, queries: list) -> bool:
        """Cache popular queries."""
        key = "popular_queries"
        return self.set(key, queries, ttl=3600)  # 1 hour
    
    def get_cached_popular_queries(self) -> Optional[list]:
        """Get cached popular queries."""
        return self.get("popular_queries")
    
    def cache_search_stats(self, stats: dict) -> bool:
        """Cache search statistics."""
        key = "search_stats"
        return self.set(key, stats, ttl=300)  # 5 minutes
    
    def get_cached_search_stats(self) -> Optional[dict]:
        """Get cached search statistics."""
        return self.get("search_stats")
    
    def invalidate_search_cache(self) -> bool:
        """Invalidate all search-related cache."""
        try:
            # Get all keys with search prefix
            keys = self.redis_client.keys("search:*")
            if keys:
                self.redis_client.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Error invalidating search cache: {e}")
            return False
    
    def invalidate_embedding_cache(self) -> bool:
        """Invalidate all embedding cache."""
        try:
            # Get all keys with embedding prefix
            keys = self.redis_client.keys("embedding:*")
            if keys:
                self.redis_client.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Error invalidating embedding cache: {e}")
            return False
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        try:
            info = self.redis_client.info()
            return {
                'used_memory': info.get('used_memory_human', 'N/A'),
                'connected_clients': info.get('connected_clients', 0),
                'total_commands_processed': info.get('total_commands_processed', 0),
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0),
                'hit_rate': self._calculate_hit_rate(info),
                'total_keys': self.redis_client.dbsize()
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {}
    
    def _calculate_hit_rate(self, info: dict) -> float:
        """Calculate cache hit rate."""
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total = hits + misses
        return (hits / total * 100) if total > 0 else 0.0
    
    def clear_all_cache(self) -> bool:
        """Clear all cache data."""
        try:
            self.redis_client.flushdb()
            logger.info("All cache data cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
    
    def close(self):
        """Close Redis connection."""
        try:
            self.redis_client.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis connection: {e}")

