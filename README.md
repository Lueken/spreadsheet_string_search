# File Search Utility

A Python utility for searching through Excel (.xlsx, .xls) and CSV files in a directory for specific strings. The tool provides detailed location information including row numbers, column names, and sheet names (for Excel files).

## 📖 Documentation Quick Links

- [Installation Guide](Documentation/installation.md) - Detailed setup instructions
- [Configuration Guide](Documentation/Config.md) - Configuration options and settings
- [API Reference](Documentation/api_reference.md) - Function documentation and usage
- [Performance Guide](Documentation/performance.md) - Optimization and best practices

## ⚡ Quick Start

1. **Clone or Download**:
   ```bash
   git clone [your-repository-url]
   cd csv_string_search
   ```

2. **Set Up Virtual Environment** (Recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Unix/MacOS
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

For detailed installation instructions, see the [Installation Guide](Documentation/installation.md).

## 🔍 Basic Usage

```python
from file_search import search_files, print_results

# Using default settings from config.py
results = search_files()
print_results(results)
```


## 🗂️ Project Structure
```
csv_string_search/
│
├── Documentation/               # Comprehensive documentation
│   ├── Config.md               # Configuration guide
│   ├── installation.md         # Detailed installation steps
│   ├── api_reference.md        # Function documentation
│   ├── performance.md          # Performance optimization
│
├── file_search.py              # Main script
├── config.py                   # Configuration settings
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## ⚙️ Configuration

Basic configuration can be done through `config.py`. Common settings include:

```python
# In config.py
DEFAULT_SEARCH_PATH = r'path/to/your/files'
DEFAULT_SEARCH_TERMS = ['term1', 'term2']
```

For detailed configuration options:
- [Configuration Guide](Documentation/Config.md)
- [Performance Optimization Guide](Documentation/performance.md)

## 🔧 Features

- Support for Excel (.xlsx, .xls) and CSV files
- Recursive directory searching
- Case-insensitive search (configurable)
- Automatic encoding detection
- Detailed location reporting
- Robust error handling
- Word boundary matching

## 🚀 Performance Optimization

For large datasets or performance-critical applications, see our [Performance Guide](Documentation/performance.md) for:
- Memory optimization
- Search algorithm tuning
- Parallel processing options
- Caching strategies

## ❗ Troubleshooting

Common issues and solutions:

1. **Excel Dependencies**:
   ```bash
   pip install openpyxl  # For .xlsx
   pip install xlrd==2.0.1  # For .xls
   ```

2. **Encoding Issues**:
    - Check the [Installation Guide](Documentation/installation.md#common-installation-issues)
    - Adjust encoding settings in `config.py`

3. **Performance Issues**:
    - See [Performance Guide](Documentation/performance.md)
    - Adjust chunk size and memory settings

For more troubleshooting help, check the [Installation Guide](Documentation/installation.md#troubleshooting).

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See our [Contributing Guide](Documentation/contributing.md) for more details.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📚 Additional Resources

- [API Reference](Documentation/api_reference.md) - Complete function documentation
- [Performance Tips](Documentation/performance.md) - Optimization strategies