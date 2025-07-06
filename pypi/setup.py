from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="grandjury",
    version="0.2.0",
    description="Python client for GrandJury ML evaluation and verdict analysis API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/grandjury",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "pandas": ["pandas>=1.3.0"],
        "polars": ["polars>=0.15.0"],
        "parquet": ["pyarrow>=5.0.0"],
        "performance": ["msgspec>=0.18.0", "pyarrow>=5.0.0", "polars>=0.15.0"],
        "all": ["pandas>=1.3.0", "polars>=0.15.0", "pyarrow>=5.0.0", "msgspec>=0.18.0"]
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
