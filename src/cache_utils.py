# Smart Caching Utilities for MSR Project
import os
import json
import pickle
import pandas as pd
from pathlib import Path
from datetime import datetime
import hashlib

class SmartCache:
    """
    Intelligent caching system for MSR project to avoid expensive recomputation.
    Handles DataFrames, JSON data, API responses, and NLP outputs.
    """
    
    def __init__(self, cache_dir="data/processed"):
        self.cache_dir = Path(cache_dir)
        # Handle relative path from notebooks directory
        if not self.cache_dir.exists() and Path(f"../{cache_dir}").exists():
            self.cache_dir = Path(f"../{cache_dir}")
        elif not self.cache_dir.exists():
            # Try to create the directory, handling relative paths
            try:
                self.cache_dir.mkdir(parents=True, exist_ok=True)
            except FileNotFoundError:
                # If we're in notebooks directory, try with ../ prefix
                self.cache_dir = Path(f"../{cache_dir}")
                self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def _generate_cache_key(self, operation_name, params=None):
        """Generate unique cache key based on operation and parameters"""
        if params:
            param_str = json.dumps(params, sort_keys=True, default=str)
            param_hash = hashlib.md5(param_str.encode()).hexdigest()[:8]
            return f"{operation_name}_{param_hash}"
        return operation_name
    
    def cache_exists(self, cache_key, file_type="json"):
        """Check if cache file exists"""
        cache_file = self.cache_dir / f"{cache_key}.{file_type}"
        return cache_file.exists()
    
    def save_to_cache(self, data, cache_key, metadata=None, file_type="auto"):
        """
        Save data to cache with automatic type detection or specified format
        
        Args:
            data: Data to cache (DataFrame, dict, list, etc.)
            cache_key: Unique identifier for cached data
            metadata: Optional metadata to include
            file_type: 'auto', 'json', 'csv', 'parquet', 'pickle'
        """
        # Auto-detect file type if not specified
        if file_type == "auto":
            if isinstance(data, pd.DataFrame):
                file_type = "parquet"  # Faster than CSV for DataFrames
            elif isinstance(data, (dict, list)):
                file_type = "json"
            else:
                file_type = "pickle"
        
        cache_file = self.cache_dir / f"{cache_key}.{file_type}"
        
        # Add metadata
        if metadata is None:
            metadata = {}
        metadata.update({
            "cached_at": datetime.now().isoformat(),
            "cache_key": cache_key,
            "data_type": type(data).__name__
        })
        
        # Save data based on type
        if file_type == "json":
            cache_data = {
                "metadata": metadata,
                "data": data
            }
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2, default=str)
                
        elif file_type == "csv":
            data.to_csv(cache_file, index=False)
            # Save metadata separately
            meta_file = self.cache_dir / f"{cache_key}_metadata.json"
            with open(meta_file, 'w') as f:
                json.dump(metadata, f, indent=2)
                
        elif file_type == "parquet":
            data.to_parquet(cache_file, index=False)
            # Save metadata separately
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
        
        print(f"[CACHE] Loaded {cache_key} from {cache_file.suffix[1:]} cache")
        return cache_file
    
    def load_from_cache(self, cache_key, file_type="auto"):
        """
        Load data from cache with automatic type detection
        
        Args:
            cache_key: Unique identifier for cached data
            file_type: 'auto', 'json', 'csv', 'parquet', 'pickle'
            
        Returns:
            tuple: (data, metadata) or (None, None) if not found
        """
        # Auto-detect file type if not specified
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
            if file_type == "json":
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                return cache_data.get("data"), cache_data.get("metadata", {})
                
            elif file_type == "csv":
                data = pd.read_csv(cache_file)
                # Load metadata if available
                meta_file = self.cache_dir / f"{cache_key}_metadata.json"
                metadata = {}
                if meta_file.exists():
                    with open(meta_file, 'r') as f:
                        metadata = json.load(f)
                return data, metadata
                
            elif file_type == "parquet":
                data = pd.read_parquet(cache_file)
                # Load metadata if available
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
            print(f"⚠️ Error loading cache {cache_key}: {e}")
            return None, None
    
    def smart_cache_operation(self, operation_func, cache_key, force_refresh=False, **kwargs):
        """
        Smart caching wrapper for expensive operations
        
        Args:
            operation_func: Function to execute if cache miss
            cache_key: Unique cache identifier
            force_refresh: Whether to bypass cache and recompute
            **kwargs: Arguments to pass to operation_func
            
        Returns:
            Result of operation (from cache or fresh computation)
        """
        if not force_refresh:
            data, metadata = self.load_from_cache(cache_key)
            if data is not None:
                print(f"✅ Loaded {cache_key} from cache (created: {metadata.get('cached_at', 'unknown')})")
                return data
        
        print(f"🔄 Computing {cache_key}...")
        result = operation_func(**kwargs)
        
        # Cache the result
        self.save_to_cache(result, cache_key, metadata={"operation": operation_func.__name__})
        
        return result
    
    def list_cache(self):
        """List all cached items with metadata"""
        cache_items = []
        for file_path in self.cache_dir.glob("*"):
            if file_path.is_file() and not file_path.name.endswith("_metadata.json"):
                cache_key = file_path.stem
                file_type = file_path.suffix[1:]  # Remove the dot
                
                # Try to get metadata
                _, metadata = self.load_from_cache(cache_key, file_type)
                
                cache_items.append({
                    "cache_key": cache_key,
                    "file_type": file_type,
                    "size_mb": file_path.stat().st_size / 1024 / 1024,
                    "created": metadata.get("cached_at", "unknown") if metadata else "unknown"
                })
        
        return sorted(cache_items, key=lambda x: x["created"], reverse=True)
    
    def clear_cache(self, pattern="*"):
        """Clear cache files matching pattern"""
        removed_count = 0
        for file_path in self.cache_dir.glob(pattern):
            if file_path.is_file():
                file_path.unlink()
                removed_count += 1
        
        print(f"🗑️ Removed {removed_count} cache files")
        return removed_count

# Convenience functions for common caching patterns
def cache_api_call(api_func, cache_key, cache_dir="data/processed", **kwargs):
    """Cache expensive API calls"""
    cache = SmartCache(cache_dir)
    return cache.smart_cache_operation(api_func, f"api_{cache_key}", **kwargs)

def cache_nlp_operation(nlp_func, cache_key, cache_dir="data/processed", **kwargs):
    """Cache expensive NLP computations"""
    cache = SmartCache(cache_dir)
    return cache.smart_cache_operation(nlp_func, f"nlp_{cache_key}", **kwargs)

def cache_analysis_result(analysis_func, cache_key, cache_dir="data/processed", **kwargs):
    """Cache analysis results"""
    cache = SmartCache(cache_dir)
    return cache.smart_cache_operation(analysis_func, f"analysis_{cache_key}", **kwargs)

# Example usage functions
def example_expensive_operation(data_size):
    """Example of an expensive operation that should be cached"""
    import time
    print(f"Performing expensive operation on {data_size} records...")
    time.sleep(1)  # Simulate expensive computation
    return {"result": f"processed_{data_size}_records", "computation_time": 1.0}

def example_usage():
    """Demonstrate smart caching usage"""
    cache = SmartCache()
    
    # Example 1: Cache expensive operation
    result1 = cache.smart_cache_operation(
        example_expensive_operation, 
        "expensive_op_1000", 
        data_size=1000
    )
    
    # Example 2: Load from cache on second call
    result2 = cache.smart_cache_operation(
        example_expensive_operation, 
        "expensive_op_1000", 
        data_size=1000
    )
    
    # List cached items
    cached_items = cache.list_cache()
    print("\\nCached items:")
    for item in cached_items:
        print(f"  {item['cache_key']}: {item['size_mb']:.2f}MB ({item['created']})")

if __name__ == "__main__":
    example_usage()