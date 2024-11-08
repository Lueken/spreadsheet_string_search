# Installation Guide

This guide provides detailed instructions for installing and setting up the File Search Utility in different environments.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Installation Methods

### Method 1: Using Git (Recommended)

```bash
# Clone the repository
git clone [your-repository-url]
cd csv_string_search

# Create virtual environment
python -m venv venv

# Activate virtual environment
## Windows
venv\Scripts\activate
## Unix/MacOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Manual Download

1. Download the project ZIP file
2. Extract to your desired location
3. Open terminal/command prompt in the extracted directory
4. Follow the virtual environment and dependency installation steps above

## Dependencies Explained

### Core Dependencies
- `pandas`: Data manipulation and analysis
- `chardet`: Character encoding detection
- `openpyxl`: Excel (.xlsx) file support
- `xlrd`: Excel (.xls) file support

### Optional Dependencies
- `black`: Code formatting (development only)
- `pytest`: Testing framework (development only)

## Platform-Specific Instructions

### Windows
```batch
# Using Command Prompt
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Using PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux/Unix
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### macOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Verifying Installation

1. Activate your virtual environment
2. Run the verification script:
```python
from file_search import search_files

# Should print version information and availability
print(search_files.__version__)  
```

## Common Installation Issues

### 1. Excel Dependencies
If you encounter Excel-related errors:
```bash
# For .xlsx files
pip install openpyxl

# For .xls files
pip install xlrd==2.0.1
```

### 2. Encoding Issues
If you encounter encoding errors:
```bash
# Install chardet
pip install chardet

# Verify installation
python -c "import chardet; print(chardet.__version__)"
```

### 3. Virtual Environment Issues
If `venv` creation fails:
```bash
# Windows
python -m pip install --user virtualenv
python -m virtualenv venv

# Unix/MacOS
python3 -m pip install --user virtualenv
python3 -m virtualenv venv
```

## Development Installation

For contributing to the project:
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## Docker Installation (Optional)

```dockerfile
# Use the provided Dockerfile
docker build -t file-search-utility .
docker run -v /path/to/search:/data file-search-utility
```

## Next Steps

After installation:
1. Review the [Configuration Guide](Config.md)
2. Try the [Basic Usage Examples](examples/basic_usage.md)
3. Check the [User Guide](user_guide.md) for detailed usage instructions