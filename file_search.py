import os
import csv
import chardet
import re
from typing import List, Dict, Set, Optional
import pandas as pd
import warnings
import logging
from time import sleep
from config import (
    CSV_SETTINGS,
    EXCEL_SETTINGS,
    OUTPUT_SETTINGS,
    LOGGING,
    SEARCH_SETTINGS,
    ERROR_HANDLING,
    DEFAULT_SEARCH_PATH,
    DEFAULT_SEARCH_TERMS,
    FILE_PATTERNS
)

def setup_logging():
    """Configure logging based on settings in config.py"""
    if LOGGING['enabled']:
        logging.basicConfig(
            filename=LOGGING['log_file'],
            level=getattr(logging, LOGGING['level']),
            format=LOGGING['format']
        )
    else:
        logging.disable(logging.CRITICAL)

def retry_on_error(func):
    """Decorator to implement retry logic for file operations"""
    def wrapper(*args, **kwargs):
        for attempt in range(ERROR_HANDLING['max_retries']):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < ERROR_HANDLING['max_retries'] - 1:
                    sleep(1)  # Wait before retrying
                else:
                    logging.error(f"All attempts failed for {func.__name__}: {str(e)}")
                    raise
    return wrapper

@retry_on_error
def search_excel_file(file_path: str, search_strings: List[str]) -> Dict[str, Set[tuple]]:
    """
    Search through an Excel file for specific strings.

    Args:
        file_path: Path to the Excel file
        search_strings: List of strings to search for

    Returns:
        Dictionary with search strings as keys and sets of (row_number, column_name, sheet_name) tuples as values
    """
    if EXCEL_SETTINGS['suppress_warnings']:
        warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

    results = {
        search_string.lower() if not SEARCH_SETTINGS['case_sensitive'] else search_string: set()
        for search_string in search_strings
    }

    try:
        # Determine the engine based on file extension
        file_lower = file_path.lower()
        engine = 'xlrd' if file_lower.endswith('.xls') else 'openpyxl'

        excel_file = pd.ExcelFile(file_path, engine=engine)

        for sheet_name in excel_file.sheet_names:
            try:
                # Process large files in chunks if specified
                chunks = pd.read_excel(
                    excel_file,
                    sheet_name=sheet_name,
                    engine=engine,
                    chunksize=EXCEL_SETTINGS['chunk_size']
                )

                headers = None
                for chunk_num, df in enumerate(chunks):
                    if headers is None:
                        headers = df.columns.tolist()

                    df = df.astype(str)
                    _process_dataframe(df, headers, sheet_name, results, search_strings)

            except Exception as sheet_error:
                error_msg = f"Could not read sheet '{sheet_name}' in file {file_path}: {str(sheet_error)}"
                logging.error(error_msg)
                if OUTPUT_SETTINGS['verbose']:
                    print(error_msg)
                if not ERROR_HANDLING['skip_corrupted']:
                    raise

    except Exception as e:
        error_msg = f"Error reading Excel file {file_path}: {str(e)}"
        logging.error(error_msg)
        if OUTPUT_SETTINGS['verbose']:
            print(error_msg)
            if "Missing optional dependency" in str(e):
                print(f"\nTo fix this, please install the required dependency:")
                if "xlrd" in str(e):
                    print("pip install xlrd==2.0.1")
                elif "openpyxl" in str(e):
                    print("pip install openpyxl")
        raise

    return results

def _process_dataframe(
        df: pd.DataFrame,
        headers: List[str],
        sheet_name: Optional[str],
        results: Dict[str, Set[tuple]],
        search_strings: List[str]
) -> None:
    """Helper function to process DataFrame chunks for searching"""
    for row_num, row in df.iterrows():
        for col_num, value in enumerate(row):
            value_str = str(value)
            value_for_comparison = value_str if SEARCH_SETTINGS['case_sensitive'] else value_str.lower()

            for search_string in search_strings:
                search_for_comparison = search_string if SEARCH_SETTINGS['case_sensitive'] else search_string.lower()

                pattern = (
                    r'\b' + re.escape(search_for_comparison) + r'\b'
                    if SEARCH_SETTINGS['word_boundaries']
                    else re.escape(search_for_comparison)
                )

                if re.search(pattern, value_for_comparison):
                    col_identifier = headers[col_num] if col_num < len(headers) else f"Column {col_num + 1}"
                    search_key = search_string if SEARCH_SETTINGS['case_sensitive'] else search_string.lower()
                    results[search_key].add((row_num + 2, col_identifier, sheet_name))

@retry_on_error
def search_csv_file(file_path: str, search_strings: List[str]) -> Dict[str, Set[tuple]]:
    """Search through a CSV file for specific strings."""
    results = {
        search_string.lower() if not SEARCH_SETTINGS['case_sensitive'] else search_string: set()
        for search_string in search_strings
    }

    try:
        # Detect file encoding
        with open(file_path, 'rb') as f:
            raw_data = f.read(CSV_SETTINGS['encoding_check_size'])
            result = chardet.detect(raw_data)
            encoding = result['encoding'] or CSV_SETTINGS['fallback_encoding']

        with open(file_path, 'r', encoding=encoding) as f:
            csv_reader = csv.reader(f)
            headers = next(csv_reader, [])

            for row_num, row in enumerate(csv_reader, start=1):
                for col_num, value in enumerate(row):
                    value_str = str(value)
                    value_for_comparison = value_str if SEARCH_SETTINGS['case_sensitive'] else value_str.lower()

                    for search_string in search_strings:
                        search_for_comparison = search_string if SEARCH_SETTINGS['case_sensitive'] else search_string.lower()

                        pattern = (
                            r'\b' + re.escape(search_for_comparison) + r'\b'
                            if SEARCH_SETTINGS['word_boundaries']
                            else re.escape(search_for_comparison)
                        )

                        if re.search(pattern, value_for_comparison):
                            col_identifier = headers[col_num] if col_num < len(headers) else f"Column {col_num + 1}"
                            search_key = search_string if SEARCH_SETTINGS['case_sensitive'] else search_string.lower()
                            results[search_key].add((row_num, col_identifier, None))

    except Exception as e:
        error_msg = f"Error reading file {file_path}: {str(e)}"
        logging.error(error_msg)
        if OUTPUT_SETTINGS['verbose']:
            print(error_msg)
        raise

    return results

def search_files(
        folder_path: str = DEFAULT_SEARCH_PATH,
        search_strings: List[str] = DEFAULT_SEARCH_TERMS
) -> Dict[str, Dict[str, Set[tuple]]]:
    """
    Search through CSV and Excel files in a directory for specific strings.

    Args:
        folder_path: Path to the directory containing files
        search_strings: List of strings to search for

    Returns:
        Dictionary with search strings as keys and nested dictionaries containing:
            - file paths as keys
            - sets of (row_number, column_name, [sheet_name]) tuples as values
    """
    results = {
        search_string.lower() if not SEARCH_SETTINGS['case_sensitive'] else search_string: {}
        for search_string in search_strings
    }

    for root, dirs, files in os.walk(folder_path):
        # Skip hidden directories if configured
        if SEARCH_SETTINGS['skip_hidden']:
            dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            # Skip hidden files if configured
            if SEARCH_SETTINGS['skip_hidden'] and file.startswith('.'):
                continue

            file_path = os.path.join(root, file)
            file_lower = file.lower()

            try:
                if file_lower.endswith(FILE_PATTERNS['excel']):
                    excel_results = search_excel_file(file_path, search_strings)
                    for search_string, locations in excel_results.items():
                        if locations:
                            results[search_string][file_path] = locations

                elif file_lower.endswith(FILE_PATTERNS['csv']):
                    csv_results = search_csv_file(file_path, search_strings)
                    for search_string, locations in csv_results.items():
                        if locations:
                            results[search_string][file_path] = locations

            except Exception as e:
                logging.error(f"Error processing file {file_path}: {str(e)}")
                if not ERROR_HANDLING['skip_corrupted']:
                    raise

        # Break after first iteration if not recursive
        if not SEARCH_SETTINGS['recursive']:
            break

    return results

def print_results(results: Dict[str, Dict[str, Set[tuple]]]) -> None:
    """Print the search results in a formatted way."""
    if not any(results.values()):
        print("No matches found.")
        return

    for search_string, file_dict in results.items():
        if file_dict:
            print(f"\nResults for '{search_string}':")

            # Sort files if configured
            files = sorted(file_dict.items()) if OUTPUT_SETTINGS['sort_results'] else file_dict.items()

            for file_path, locations in files:
                # Show full path or just filename based on configuration
                display_path = file_path if OUTPUT_SETTINGS['show_full_path'] else os.path.basename(file_path)
                print(f"\nFile: {display_path}")
                print("Locations:")

                # Sort locations if configured
                location_list = sorted(locations) if OUTPUT_SETTINGS['sort_results'] else locations

                for location in location_list:
                    if location[2]:  # If sheet name exists (Excel file)
                        print(f"  - Sheet '{location[2]}', Row {location[0]}, {location[1]}")
                    else:  # CSV file
                        print(f"  - Row {location[0]}, {location[1]}")
            print()

def main():
    """Main function to run the file search utility."""
    # Setup logging
    setup_logging()
    logging.info("Starting file search utility")

    try:
        # Get search parameters (could be modified to accept command line arguments)
        folder_path = DEFAULT_SEARCH_PATH
        search_strings = DEFAULT_SEARCH_TERMS

        print("Searching files...")
        logging.info(f"Searching in {folder_path} for terms: {search_strings}")

        results = search_files(folder_path, search_strings)
        print_results(results)

        print("Search completed.")
        logging.info("Search completed successfully")

    except Exception as e:
        error_msg = f"Error during execution: {str(e)}"
        logging.error(error_msg)
        if OUTPUT_SETTINGS['verbose']:
            print(f"\nError: {error_msg}")
        else:
            print("\nAn error occurred. Check the log file for details.")

if __name__ == "__main__":
    main()