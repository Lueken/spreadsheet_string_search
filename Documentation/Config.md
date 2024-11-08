# Case Sensitivity in File Search

In the current configuration, searches are case-insensitive by default. This behavior is controlled by the `SEARCH_SETTINGS` in the config file where `'case_sensitive': False` is set.

## Implementation Details

### Configuration Setting

In `config.py`, the case sensitivity is defined in the search settings:

```python
SEARCH_SETTINGS = {
    'case_sensitive': False,  # This controls case sensitivity
    'word_boundaries': True,  # Use word boundaries in regex
    'recursive': True,        # Search subdirectories
    'skip_hidden': True       # Skip hidden files and directories
}
```

### Code Implementation

The case sensitivity is implemented in several places throughout the search functions:

```python
# When initializing results dictionary
results = {
    search_string.lower() if not SEARCH_SETTINGS['case_sensitive'] else search_string: set() 
    for search_string in search_strings
}

# When comparing values
value_for_comparison = value_str if SEARCH_SETTINGS['case_sensitive'] else value_str.lower()
search_for_comparison = search_string if SEARCH_SETTINGS['case_sensitive'] else search_string.lower()
```

## Search Behavior

When searching for "Taylor" with case-insensitive matching, it will match:
- "Taylor"
- "TAYLOR"
- "taylor"
- "TaYlOr"

## Modifying Case Sensitivity

You can enable case-sensitive searching in two ways:

### 1. Update the Config File

Modify the `config.py` file:

```python
SEARCH_SETTINGS = {
    'case_sensitive': True,  # Change this to True
    ...
}
```

### 2. Override at Runtime

Temporarily override the setting when calling the function:

```python
# Temporarily override the setting
SEARCH_SETTINGS['case_sensitive'] = True
results = search_files(folder_path, search_strings)
```

When case sensitivity is enabled, "Taylor" will only match exactly "Taylor" and not "taylor" or "TAYLOR".