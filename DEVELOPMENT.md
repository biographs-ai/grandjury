# GrandJury Python Client - Development

This is the development repository for the GrandJury Python API client.

## 📁 Repository Structure

```
grandjury/
├── grandjury/               # Main package
│   ├── __init__.py
│   └── api_client.py
├── tests/                   # Test files
│   ├── test_api_client.ipynb
│   └── test_server.ipynb
├── scripts/                 # Development scripts
│   ├── build_with_uv.py     # Build script
│   └── quick_test.py        # Quick verification
├── docs/                    # Documentation
│   └── PYPI_GUIDE.md
├── README.md               # Main package README
├── pyproject.toml          # Package configuration
└── uv.lock                 # Lock file
```

## 🚀 Quick Start (Users)

Install the package:
```bash
pip install grandjury
```

See the main [README.md](README.md) for usage examples.

## 🛠 Development Setup

This project uses `uv` for package management:

```bash
# Clone the repository
git clone https://github.com/your-org/grandjury-python.git
cd grandjury-python

# Install dependencies
uv sync

# Run tests
jupyter notebook tests/test_api_client.ipynb

# Build package
python scripts/build_with_uv.py

# Quick verification
python scripts/quick_test.py
```

## 📦 Building & Publishing

```bash
# Build the package
python scripts/build_with_uv.py

# Test upload
cd dist
uv run twine upload --repository testpypi *

# Production upload
uv run twine upload *
```

## 🧪 Testing

The comprehensive test suite is in `tests/test_api_client.ipynb`. It covers:
- All API endpoints
- Multiple data formats (pandas, polars, CSV, parquet)
- Error handling
- Performance optimizations
- Backward compatibility

## 📚 Documentation

- [PyPI Publishing Guide](docs/PYPI_GUIDE.md)
- [API Documentation](README.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run the test notebook
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.
