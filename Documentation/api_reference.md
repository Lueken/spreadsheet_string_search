# API Reference

## Core Functions

### search_files

```python
def search_files(
    folder_path: str = DEFAULT_SEARCH_PATH,
    search_strings: List[str] = DEFAULT_SEARCH_TERMS
) -> Dict[str, Dict[str, Set[tuple]]]
```

The main function for searching through files in a directory.

#### Parameters
- `folder_path` (str): Directory path to search
- `search_strings` (List[str]): List of strings to search for

#### Returns
- Dictionary with search strings as keys and nested dictionaries containing:
    - File paths as keys
    - Sets of (row_number, column_name, sheet_name) tuples as values

#### Example
```python
results = search_files(
    folder_path="path/to/search",
    search_strings=["search", "terms"]
)
```

### search_excel_file

```python
def search_excel_file(
    file_path: str,
    search_strings: List[str]
) -> Dict[str, Set[tuple]]
```

Search through an Excel file for specific strings.

#### Parameters
- `file_path` (str): Path to the Excel file
- `search_strings` (List[str]): List of strings to search for

#### Returns
- Dictionary with search strings as keys and sets of matching locations as values

### search_csv_file

```python
def search_csv_file(
    file_path: str,
    search_strings: List[str]
) -> Dict[str, Set[tuple]]
```

Search through a CSV file for specific strings.

#### Parameters
- `file_path` (str): Path to the CSV file
- `search_strings` (List[str]): List of strings to search for

#### Returns
- Dictionary with search strings as keys and sets of matching locations as values

### print_results

```python
def print_results(
    results: Dict[str, Dict[str, Set[tuple]]]
) -> None
```

Print search results in a formatted way.

#### Parameters
- `results`: Results dictionary from search_files function

## Utility Functions

### setup_logging

```python
def setup_logging() -> None
```

Configure logging based on settings in config.py.

### retry_on_error

```python
@retry_on_error
def function_name():
    ...
```

Decorator to implement retry logic for file operations.

## Type Definitions

```python
from typing import List, Dict, Set, Optional, Tuple

# Common type aliases
FilePath = str
RowNumber = int
ColumnName = str
SheetName = Optional[str]
Location = Tuple[RowNumber, ColumnName, SheetName]

# Result types
FileResults = Dict[str, Set[Location]]
SearchResults = Dict[str, Dict[FilePath, Set[Location]]]
```

## Error Handling

The API uses a comprehensive error handling system:

```python
try:
    results = search_files(folder_path, search_strings)
except Exception as e:
    if ERROR_HANDLING['verbose']:
        print(f"Error: {str(e)}")
    logging.error(f"Search failed: {str(e)}")
```

## Configuration Integration

All functions integrate with the configuration system:

```python
from config import (
    CSV_SETTINGS,
    EXCEL_SETTINGS,
    SEARCH_SETTINGS,
    ERROR_HANDLING
)
```

## Performance Considerations

- Use chunked processing for large Excel files
- Configure chunk size in EXCEL_SETTINGS
- Set appropriate encoding detection size in CSV_SETTINGS

## Thread Safety

The API is not explicitly thread-safe. For concurrent operations:
- Use separate instances
- Implement your own synchronization
- Consider using ProcessPoolExecutor for parallel processing