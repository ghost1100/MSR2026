# Smart caching system for expensive MSR operations
# Optimizes performance for 900K+ dataset processing and API calls
import os
import json
import pickle
import pandas as pd
from pathlib import Path
from datetime import datetime
import hashlib

class SmartCache:
    """
    Intelligent caching system designed for MSR project performance optimization.
    
    Handles multiple data types (DataFrames, JSON, API responses) with automatic
    format detection and metadata tracking. Critical for reducing computation
    time on 900K+ dataset operations and expensive Claude API calls.
    
    Features:
    - Automatic file format selection (parquet for DataFrames, JSON for dicts)
    - Cross-directory path resolution (works from notebooks/ or root)
    - Metadata tracking with timestamps and operation details
    - Smart cache invalidation and cleanup utilities
    """
    
    def __init__(self, cache_dir="data/processed"):
        """
        Initialize cache with intelligent path resolution.
        
        Handles relative path issues when running from different directories
        (notebooks/ vs root). Creates cache directory if missing.
        
        Args:
            cache_dir (str): Cache directory path, defaults to data/processed
        """
        self.cache_dir = Path(cache_dir)
        # Handle execution from notebooks/ subdirectory
        if not self.cache_dir.exists() and Path(f"../{cache_dir}").exists():
            self.cache_dir = Path(f"../{cache_dir}")
        elif not self.cache_dir.exists():
            # Create cache directory with parent handling
            try:
                self.cache_dir.mkdir(parents=True, exist_ok=True)
            except FileNotFoundError:
                # Fallback for notebooks directory execution
                self.cache_dir = Path(f"../{cache_dir}")
                self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def _generate_cache_key(self, operation_name, params=None):
        """
        Generate unique cache key from operation name and parameters.
        
        Creates deterministic hash from parameter values to ensure
        identical inputs produce identical cache keys.
        
        Args:
            operation_name (str): Base operation identifier
            params (dict): Operation parameters for hash generation
            
        Returns:
            str: Unique cache key with optional parameter hash
        """
        if params:
            param_str = json.dumps(params, sort_keys=True, default=str)
            param_hash = hashlib.md5(param_str.encode()).hexdigest()[:8]
            return f"{operation_name}_{param_hash}"
        return operation_name
    
    def cache_exists(self, cache_key, file_type="json"):
        """Check if specific cache file exists on disk."""
        cache_file = self.cache_dir / f"{cache_key}.{file_type}"
        return cache_file.exists()
    
    def save_to_cache(self, data, cache_key, metadata=None, file_type="auto"):
        """
        Save data to cache with automatic format optimization.
        
        Automatically selects best storage format:
        - Parquet for DataFrames (faster I/O than CSV)
        - JSON for dictionaries and lists (human readable)
        - Pickle for complex objects (preserves all Python types)
        
        Args:
            data: Data to cache (any serializable type)
            cache_key (str): Unique identifier for retrieval
            metadata (dict): Optional metadata (timestamps added automatically)
            file_type (str): Force specific format or 'auto' for optimization
            
        Returns:
            Path: Path to created cache file
        """
        # Intelligent format selection based on data type
        if file_type == "auto":
            if isinstance(data, pd.DataFrame):
                file_type = "parquet"  # Superior DataFrame performance
            elif isinstance(data, (dict, list)):
                file_type = "json"  # Human-readable for debugging
            else:
                file_type = "pickle"  # Handles complex Python objects
        
        cache_file = self.cache_dir / f"{cache_key}.{file_type}"
        
        # Enrich metadata with caching details
        if metadata is None:
            metadata = {}
        metadata.update({
            "cached_at": datetime.now().isoformat(),
            "cache_key": cache_key,
            "data_type": type(data).__name__
        })
        
        # Format-specific serialization
        if file_type == "json":
            cache_data = {
                "metadata": metadata,
                "data": data
            }
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2, default=str)
                
        elif file_type == "csv":
            data.to_csv(cache_file, index=False)
            # Separate metadata file for CSV format
            meta_file = self.cache_dir / f"{cache_key}_metadata.json"
            with open(meta_file, 'w') as f:
                json.dump(metadata, f, indent=2)
                
        elif file_type == "parquet":
            data.to_parquet(cache_file, index=False)
            # Separate metadata file for Parquet format
            meta_file = self.cache_dir / f"{cache_key}_metadata.json"
            with open(meta_file, 'w') as f:
                json.dump(metadata, f, indent=2)
                
        elif file_type == "pickle":
            cache_data = {
                "metadata": metadata,
                "data": data
            }
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
        
        print(f"[CACHE] Saved {cache_key} to {cache_file.suffix[1:]} cache")
        return cache_file
    
    def load_from_cache(self, cache_key, file_type="auto"):
        """
        Load data from cache with automatic format detection.
        
        Attempts to locate cached data by trying common formats in order of
        preference. Returns both data and metadata for complete context.
        
        Args:
            cache_key (str): Unique identifier for cached data
            file_type (str): Specific format or 'auto' for detection
            
        Returns:
            tuple: (data, metadata) or (None, None) if cache miss
        """
        # Auto-detect by checking for existing files
        if file_type == "auto":
            for ext in ["parquet", "json", "csv", "pickle"]:
                if (self.cache_dir / f"{cache_key}.{ext}").exists():
                    file_type = ext
                    break
            else:
                return None, None
        
        cache_file = self.cache_dir / f"{cache_key}.{file_type}"
        
        if not cache_file.exists():
            return None, None
        
        try:
            # Format-specific deserialization
            if file_type == "json":
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                return cache_data.get("data"), cache_data.get("metadata", {})
                
            elif file_type == "csv":
                data = pd.read_csv(cache_file)
                # Load separate metadata file if available
                meta_file = self.cache_dir / f"{cache_key}_metadata.json"
                metadata = {}
                if meta_file.exists():
                    with open(meta_file, 'r') as f:
                        metadata = json.load(f)
                return data, metadata
                
            elif file_type == "parquet":
                data = pd.read_parquet(cache_file)
                # Load separate metadata file if available
                meta_file = self.cache_dir / f"{cache_key}_metadata.json"
                metadata = {}
                if meta_file.exists():
                    with open(meta_file, 'r') as f:
                        metadata = json.load(f)
                return data, metadata
                
            elif file_type == "pickle":
                with open(cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                return cache_data.get("data"), cache_data.get("metadata", {})
                
        except Exception as e:
            print(f"Error loading cache {cache_key}: {e}")
            return None, None
    
    def smart_cache_operation(self, operation_func, cache_key, force_refresh=False, **kwargs):
        """
        Intelligent caching wrapper for expensive operations.
        
        Primary interface for cache-or-compute pattern. Checks cache first,
        executes function on cache miss, and stores result for future use.
        Essential for Claude API calls and large dataset processing.
        
        Args:
            operation_func (callable): Function to execute on cache miss
            cache_key (str): Unique cache identifier
            force_refresh (bool): Whether to bypass cache and recompute
            **kwargs: Arguments passed to operation_func
            
        Returns:
            Result of operation (from cache or fresh computation)
        """
        if not force_refresh:
            data, metadata = self.load_from_cache(cache_key)
            if data is not None:
                print(f"Cache hit: {cache_key} (created: {metadata.get('cached_at', 'unknown')})")
                return data
        
        print(f"Computing {cache_key}...")
        result = operation_func(**kwargs)
        
        # Store result for future use
        self.save_to_cache(result, cache_key, metadata={"operation": operation_func.__name__})
        
        return result
    
    def list_cache(self):
        """
        List all cached items with size and timestamp metadata.
        
        Useful for cache management and debugging. Scans cache directory
        and extracts metadata from each cached file.
        
        Returns:
            list: Cache items sorted by creation time (newest first)
        """
        cache_items = []
        for file_path in self.cache_dir.glob("*"):
            if file_path.is_file() and not file_path.name.endswith("_metadata.json"):
                cache_key = file_path.stem
                file_type = file_path.suffix[1:]  # Remove dot prefix
                
                # Extract metadata if available
                _, metadata = self.load_from_cache(cache_key, file_type)
                
                cache_items.append({
                    "cache_key": cache_key,
                    "file_type": file_type,
                    "size_mb": file_path.stat().st_size / 1024 / 1024,
                    "created": metadata.get("cached_at", "unknown") if metadata else "unknown"
                })
        
        return sorted(cache_items, key=lambda x: x["created"], reverse=True)
    
    def clear_cache(self, pattern="*"):
        """
        Clear cache files matching specified pattern.
        
        Useful for cleanup and testing. Supports glob patterns for
        selective deletion (e.g., "analysis_*" for analysis results).
        
        Args:
            pattern (str): Glob pattern for files to remove
            
        Returns:
            int: Number of files removed
        """
        removed_count = 0
        for file_path in self.cache_dir.glob(pattern):
            if file_path.is_file():
                file_path.unlink()
                removed_count += 1
        
        print(f"Removed {removed_count} cache files")
        return removed_count

# Convenience functions for common caching patterns
def cache_api_call(api_func, cache_key, cache_dir="data/processed", **kwargs):
    """
    Cache expensive API calls (especially Claude API operations).
    
    Specialized wrapper for API operations that may fail or timeout.
    Critical for cost optimization when processing 900K+ dataset.
    
    Args:
        api_func (callable): API function to call
        cache_key (str): Unique identifier for this API call
        cache_dir (str): Cache directory path
        **kwargs: Arguments passed to api_func
        
    Returns:
        API response (from cache or fresh call)
    """
    cache = SmartCache(cache_dir)
    return cache.smart_cache_operation(api_func, f"api_{cache_key}", **kwargs)

def cache_nlp_operation(nlp_func, cache_key, cache_dir="data/processed", **kwargs):
    """
    Cache expensive NLP computations (text analysis, embeddings).
    
    Optimizes text processing operations that scale poorly with dataset size.
    
    Args:
        nlp_func (callable): NLP function to execute
        cache_key (str): Unique identifier for this operation
        cache_dir (str): Cache directory path
        **kwargs: Arguments passed to nlp_func
        
    Returns:
        NLP results (from cache or fresh computation)
    """
    cache = SmartCache(cache_dir)
    return cache.smart_cache_operation(nlp_func, f"nlp_{cache_key}", **kwargs)

def cache_analysis_result(analysis_func, cache_key, cache_dir="data/processed", **kwargs):
    """
    Cache statistical analysis results and research question outputs.
    
    Preserves expensive DataFrame operations and statistical computations
    across notebook sessions and analysis iterations.
    
    Args:
        analysis_func (callable): Analysis function to execute
        cache_key (str): Unique identifier for this analysis
        cache_dir (str): Cache directory path
        **kwargs: Arguments passed to analysis_func
        
    Returns:
        Analysis results (from cache or fresh computation)
    """
    cache = SmartCache(cache_dir)
    return cache.smart_cache_operation(analysis_func, f"analysis_{cache_key}", **kwargs)

# Testing and demonstration functions
def example_expensive_operation(data_size):
    """
    Example operation for cache system testing.
    
    Simulates expensive computation with artificial delay.
    Used for cache system validation and performance testing.
    
    Args:
        data_size (int): Size parameter for operation
        
    Returns:
        dict: Mock analysis results with timing information
    """
    import time
    print(f"Performing expensive operation on {data_size} records...")
    time.sleep(1)  # Simulate computation time
    return {"result": f"processed_{data_size}_records", "computation_time": 1.0}

def example_usage():
    """
    Demonstrate smart caching functionality.
    
    Shows cache-or-compute pattern with timing comparison.
    Useful for understanding cache performance benefits.
    """
    cache = SmartCache()
    
    # First call: compute and cache
    result1 = cache.smart_cache_operation(
        example_expensive_operation, 
        "expensive_op_1000", 
        data_size=1000
    )
    
    # Second call: load from cache (much faster)
    result2 = cache.smart_cache_operation(
        example_expensive_operation, 
        "expensive_op_1000", 
        data_size=1000
    )
    
    # Display cache status
    cached_items = cache.list_cache()
    print("\nCached items:")
    for item in cached_items:
        print(f"  {item['cache_key']}: {item['size_mb']:.2f}MB ({item['created']})")

if __name__ == "__main__":
    example_usage()