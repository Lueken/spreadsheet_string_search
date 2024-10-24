import os
import csv
import chardet
import re
from typing import List, Dict, Set

def search_csv_files(folder_path: str, search_strings: List[str]) -> Dict[str, Dict[str, Set[tuple]]]:
    """
    Search through CSV files in a directory for specific strings.

    Args:
        folder_path: Path to the directory containing CSV files
        search_strings: List of strings to search for

    Returns:
        Dictionary with search strings as keys and nested dictionaries containing:
            - file paths as keys
            - sets of (row_number, column_name) tuples as values
    """
    results = {search_string.lower(): {} for search_string in search_strings}

    # Walk through the directory
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                try:
                    # Detect the file encoding
                    with open(file_path, 'rb') as f:
                        raw_data = f.read()
                        result = chardet.detect(raw_data)
                        encoding = result['encoding']

                    # Read the CSV file with the detected encoding
                    with open(file_path, 'r', encoding=encoding) as f:
                        csv_reader = csv.reader(f)

                        # Get headers
                        headers = next(csv_reader, [])

                        # Read through each row
                        for row_num, row in enumerate(csv_reader, start=1):
                            for col_num, value in enumerate(row):
                                value_lower = value.lower()

                                # Check each search string
                                for search_string in search_strings:
                                    search_lower = search_string.lower()
                                    if re.search(r'\b' + re.escape(search_lower) + r'\b', value_lower):
                                        # Initialize nested dictionary if needed
                                        if file_path not in results[search_lower]:
                                            results[search_lower][file_path] = set()

                                        # Add tuple of row number and column name/number
                                        col_identifier = headers[col_num] if col_num < len(headers) else f"Column {col_num + 1}"
                                        results[search_lower][file_path].add((row_num, col_identifier))

                except Exception as e:
                    print(f"Error reading file {file_path}: {str(e)}")

    return results

def print_results(results: Dict[str, Dict[str, Set[tuple]]]) -> None:
    """
    Print the search results in a formatted way.
    """
    if not any(results.values()):
        print("No matches found.")
        return

    for search_string, file_dict in results.items():
        if file_dict:
            print(f"\nResults for '{search_string}':")
            for file_path, locations in file_dict.items():
                print(f"\nFile: {file_path}")
                print("Locations:")
                for row_num, col_name in sorted(locations):
                    print(f"  - Row {row_num}, {col_name}")
            print()

def main():
    # Example usage
    folder_path = r'C:\Users\31686\Desktop\SAT test import check'  # Replace with your directory path
    search_strings = ['4183062915', '155153', 'Bodnar']    # Replace with your search terms

    print("Searching CSV files...")
    results = search_csv_files(folder_path, search_strings)
    print_results(results)
    print("Search completed.")

if __name__ == "__main__":
    main()