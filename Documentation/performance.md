# Performance Optimization Guide

This guide covers strategies for optimizing the File Search Utility's performance in various scenarios.

## Memory Management

### Excel File Processing

1. **Chunk Size Optimization**
   ```python
   # In config.py
   EXCEL_SETTINGS = {
       'chunk_size': 1000  # Adjust based on available memory
   }
   ```

2. **Memory-Efficient Reading**
   ```python
   # Use specific columns if known
   df = pd.read_excel(
       file_path,
       usecols=['relevant_columns'],
       memory_map=True
   )
   ```

### CSV File Processing

1. **Encoding Detection**
   ```python
   # Optimize encoding detection sample size
   CSV_SETTINGS = {
       'encoding_check_size': 10000  # Adjust based on file characteristics
   }
   ```

2. **Streaming Large Files**
   ```python
   # Process CSV in chunks
   chunk_size = 10000
   for chunk in pd.read_csv(file_path, chunksize=chunk_size):
       process_chunk(chunk)
   ```

## Search Optimization

### File Filtering

1. **Skip Unnecessary Files**
   ```python
   # In config.py
   SEARCH_SETTINGS = {
       'skip_hidden': True,
       'recursive': False  # Set to False for shallow searches
   }
   ```

2. **File Pattern Matching**
   ```python
   FILE_PATTERNS = {
       'excel': ('.xlsx', '.xls'),
       'csv': ('.csv',)
   }
   ```

### Search Algorithm

1. **Regular Expression Optimization**
   ```python
   # Compile regex patterns once
   import re
   patterns = {
       term: re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
       for term in search_terms
   }
   ```

2. **Early Termination**
   ```python
   # Stop searching file after finding match
   if SEARCH_SETTINGS['first_match_only']:
       break
   ```

## Parallel Processing

### Multiprocessing Implementation

```python
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

def parallel_search(folder_path, search_strings):
    cpu_count = multiprocessing.cpu_count()
    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        futures = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                futures.append(
                    executor.submit(search_file, file_path, search_strings)
                )
        
        results = {}
        for future in futures:
            file_results = future.result()
            results.update(file_results)
        
        return results
```

## Caching Strategies

### Results Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cache_search_results(file_path, search_string):
    # Implementation
    pass
```

### File Metadata Caching

```python
# Cache file metadata
file_metadata = {}
def get_file_metadata(file_path):
    if file_path not in file_metadata:
        file_metadata[file_path] = {
            'size': os.path.getsize(file_path),
            'mtime': os.path.getmtime(file_path)
        }
    return file_metadata[file_path]
```

## Monitoring and Profiling

### Performance Metrics

```python
import time
import psutil

def monitor_performance():
    start_time = time.time()
    process = psutil.Process()
    initial_memory = process.memory_info().rss

    # Your search operation here

    end_time = time.time()
    final_memory = process.memory_info().rss
    
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print(f"Memory used: {(final_memory - initial_memory) / 1024 / 1024:.2f} MB")
```

### Profiling Tools

```python
import cProfile
import pstats

def profile_search():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your search operation here
    
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats()
```

## Configuration Templates

### High-Performance Configuration

```python
# For maximum performance
PERFORMANCE_CONFIG = {
    'EXCEL_SETTINGS': {
        'chunk_size': 5000,
        'suppress_warnings': True
    },
    'CSV_SETTINGS': {
        'encoding_check_size': 5000
    },
    'SEARCH_SETTINGS': {
        'recursive': False,
        'first_match_only': True,
        'skip_hidden': True
    }
}
```

### Memory-Efficient Configuration

```python
# For handling large files with limited memory
MEMORY_EFFICIENT_CONFIG = {
    'EXCEL_SETTINGS': {
        'chunk_size': 1000,
        'memory_map': True
    },
    'CSV_SETTINGS': {
        'encoding_check_size': 1000,
        'chunk_processing': True
    }
}
```

## Best Practices

1. **File Organization**
    - Keep similar file types together
    - Use shallow directory structures when possible

2. **Search Patterns**
    - Use specific search terms
    - Implement search term prioritization

3. **Resource Management**
    - Implement proper file closing
    - Clear caches periodically
    - Monitor memory usage

4. **Error Handling**
    - Implement timeouts for long operations
    - Handle resource exhaustion gracefully