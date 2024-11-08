# Installation Guide

This comprehensive guide will walk you through setting up the File Search Utility on a new workstation.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Dependency Installation](#dependency-installation)
- [Verification Steps](#verification-steps)
- [Common Issues](#common-issues)
- [Development Setup](#development-setup)

## Prerequisites

### Python Installation

1. **Windows**:
    - Download Python 3.7+ from [python.org](https://python.org)
    - Run installer
    - ✅ Check "Add Python to PATH"
    - ✅ Check "Install pip"
    - Verify in Command Prompt:
      ```batch
      python --version
      pip --version
      ```

2. **MacOS**:
    - Using Homebrew:
      ```bash
      brew install python
      ```
    - Or download from [python.org](https://python.org)
    - Verify:
      ```bash
      python3 --version
      pip3 --version
      ```

3. **Linux**:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-venv

   # Fedora
   sudo dnf install python3 python3-pip python3-venv

   # Verify
   python3 --version
   pip3 --version
   ```

### Git Installation (Optional)

1. **Windows**:
    - Download from [git-scm.com](https://git-scm.com/downloads)
    - Use default installation options
    - Verify:
      ```batch
      git --version
      ```

2. **MacOS**:
   ```bash
   brew install git
   ```

3. **Linux**:
   ```bash
   # Ubuntu/Debian
   sudo apt install git

   # Fedora
   sudo dnf install git
   ```

## Installation Steps

### 1. Get the Code

#### Option A - Using Git:
```bash
# HTTPS clone
git clone https://github.com/yourusername/csv_string_search.git

# OR SSH clone (if configured)
git clone git@github.com:yourusername/csv_string_search.git

cd csv_string_search
```

#### Option B - Direct Download:
1. Download ZIP from repository
2. Extract to desired location
3. Open terminal in extracted directory

### 2. Virtual Environment Setup

#### Windows:
```batch
# Command Prompt
python -m pip install --upgrade pip
python -m pip install virtualenv
python -m venv venv
venv\Scripts\activate

# PowerShell (if above doesn't work)
python -m venv venv
.\venv\Scripts\Activate.ps1

# If PowerShell execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### MacOS/Linux:
```bash
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Core dependencies
pip install pandas chardet openpyxl xlrd==2.0.1

# OR using requirements file
pip install -r requirements.txt
```

## Dependency Details

### Core Dependencies
| Package   | Version  | Purpose                    | Installation                    |
|-----------|----------|----------------------------|--------------------------------|
| pandas    | >=1.3.0  | Data processing           | `pip install pandas`           |
| chardet   | >=4.0.0  | Character encoding        | `pip install chardet`          |
| openpyxl  | >=3.0.0  | Excel (.xlsx) support     | `pip install openpyxl`        |
| xlrd      | ==2.0.1  | Excel (.xls) support      | `pip install xlrd==2.0.1`     |

### Optional Dependencies
| Package   | Purpose              | Installation                    |
|-----------|---------------------|--------------------------------|
| black     | Code formatting     | `pip install black`            |
| pytest    | Testing            | `pip install pytest`           |

## Verification Steps

1. **Verify Environment**:
   ```bash
   # Should show path to virtual environment Python
   python -c "import sys; print(sys.executable)"
   ```

2. **Verify Dependencies**:
   ```python
   python
   >>> import pandas as pd
   >>> import chardet
   >>> import openpyxl
   >>> import xlrd
   >>> print(f"pandas: {pd.__version__}")
   >>> exit()
   ```

3. **Test Run**:
   ```bash
   python file_search.py
   ```

## Common Issues

### 1. Python/Pip Not Found

#### Windows:
```batch
# Add Python to PATH manually
setx PATH "%PATH%;C:\Python3x\Scripts\;C:\Python3x\"
# Replace Python3x with your version
```

#### Unix-like:
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="/usr/local/opt/python/libexec/bin:$PATH"
```

### 2. Virtual Environment Issues

```bash
# If venv fails, try virtualenv
python -m pip install --user virtualenv
python -m virtualenv venv

# OR create without pip cache
python -m venv venv --no-pip --clear
```

### 3. Permission Issues

#### Windows:
- Run Command Prompt/PowerShell as Administrator

#### Unix-like:
```bash
# Fix permissions
chmod +x venv/bin/activate
sudo chown -R $USER venv/
```

## Development Setup

For contributing to the project:

1. **Install Development Dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Setup Pre-commit Hooks**:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

3. **Setup Testing Environment**:
   ```bash
   pip install pytest pytest-cov
   pytest
   ```

## Project Structure After Installation

```
csv_string_search/
│
├── venv/                      # Virtual environment (created during installation)
│   ├── Lib/                  # Windows
│   └── lib/                  # Unix
│
├── Documentation/            # Documentation files
├── file_search.py           # Main script
├── config.py                # Configuration
├── requirements.txt         # Core dependencies
├── requirements-dev.txt     # Development dependencies
└── README.md               # Project overview
```

## Next Steps

1. Review the [Configuration Guide](Config.md)
2. Consult the [Performance Guide](performance.md) for optimization

## Updating

To update an existing installation:

```bash
# Activate virtual environment
source venv/bin/activate  # Unix
# OR
venv\Scripts\activate     # Windows

# Pull latest changes (if using Git)
git pull

# Update dependencies
pip install -r requirements.txt --upgrade
```