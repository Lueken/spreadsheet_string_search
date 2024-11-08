# Configuration settings for the file search utility

# Default search directory
# Remove double quotes " after pasting
DEFAULT_SEARCH_PATH = r'INSERT_PATH_HERE'

# Default search terms
DEFAULT_SEARCH_TERMS = ['string1', 'string2']

# File patterns
FILE_PATTERNS = {
    'excel': ('.xlsx', '.xls'),
    'csv': ('.csv',)
}

# Encoding settings for CSV files
CSV_SETTINGS = {
    'fallback_encoding': 'utf-8',
    'encoding_check_size': 10000  # Number of bytes to check for encoding detection
}

# Excel settings
EXCEL_SETTINGS = {
    'suppress_warnings': True,  # Suppress openpyxl warnings
    'chunk_size': 1000  # Number of rows to process at a time for large files
}

# Output formatting
OUTPUT_SETTINGS = {
    'show_full_path': True,  # Show full file path in results
    'sort_results': True,    # Sort results by location
    'verbose': True         # Show detailed error messages
}

# Logging settings
LOGGING = {
    'enabled': True,
    'log_file': 'file_search.log',
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - %(levelname)s - %(message)s'
}

# Search settings
SEARCH_SETTINGS = {
    'case_sensitive': False,
    'word_boundaries': True,  # Use word boundaries in regex
    'recursive': True,       # Search subdirectories
    'skip_hidden': True      # Skip hidden files and directories
}

# Error handling
ERROR_HANDLING = {
    'max_retries': 3,        # Number of times to retry on failure
    'timeout': 30,           # Timeout in seconds for file operations
    'skip_corrupted': True   # Skip corrupted files instead of raising exception
}