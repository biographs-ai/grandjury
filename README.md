# grandjury

Python client for the GrandJury ML evaluation and verdict analysis API.

This package provides comprehensive access to the GrandJury server for ML model evaluation and voting analysis, supporting:

- **Model scoring** with decay-adjusted algorithms
- **Vote analysis** across multiple dimensions (time, completeness, confidence)
- **Multiple data formats** (pandas, polars, CSV, parquet, dict/list)
- **Performance optimizations** with optional dependencies
- **Backward compatibility** with existing code

**Patent Pending.**

## Installation

```bash
pip install grandjury
```

Optional performance dependencies:
```bash
pip install grandjury[performance]  # Installs msgspec, pyarrow, polars
```

## Quick Start

### Basic Model Evaluation
```python
from grandjury import GrandJuryClient

# Initialize client
client = GrandJuryClient(api_key="your-api-key")

# Evaluate model performance
result = client.evaluate_model(
    previous_score=0.7,
    votes=[0.9, 0.8, 0.6],
    reputations=[1.0, 1.0, 0.8]
)
print(f"Score: {result['score']:.4f}")
```

### Vote Analysis with Multiple Data Formats

```python
import pandas as pd
import polars as pl

# Your vote data
vote_data = [
    {
        "inference_id": 1,
        "vote": True,
        "voter_id": 101,
        "vote_time": "2024-07-07T19:22:30",
        # ... other fields
    }
    # ... more votes
]

# No authentication needed for analysis endpoints  
client = GrandJuryClient()

# Use with different data formats
histogram = client.vote_histogram(vote_data)  # dict/list
histogram = client.vote_histogram(pd.DataFrame(vote_data))  # pandas
histogram = client.vote_histogram(pl.DataFrame(vote_data))  # polars
histogram = client.vote_histogram("votes.csv")  # CSV file
histogram = client.vote_histogram("votes.parquet")  # Parquet file

# Vote completeness analysis
completeness = client.vote_completeness(
    data=vote_data,
    voter_list=[101, 102, 103]
)

# Population confidence
confidence = client.population_confidence(
    data=vote_data,
    voter_list=[101, 102, 103]
)

# Majority vote analysis
majority = client.majority_good_votes(
    data=vote_data,
    good_vote=True,
    threshold=0.5
)

# Vote distribution per inference
distribution = client.votes_distribution(vote_data)
```

### Backward Compatibility

```python
# Original function still works
from grandjury import evaluate_model

result = evaluate_model(
    predictions=["Model output 1", "Model output 2"],
    references=["Expected 1", "Expected 2"],
    api_key="your-api-key"
)
```

## API Endpoints

| Method | Description | Authentication |
|--------|-------------|----------------|
| `evaluate_model()` | Model scoring with decay algorithms | Required |
| `vote_histogram()` | Vote time distribution analysis | Optional |
| `vote_completeness()` | Voting completeness metrics | Optional |
| `population_confidence()` | Population confidence analysis | Optional |
| `majority_good_votes()` | Majority vote counting | Optional |
| `votes_distribution()` | Vote distribution per inference | Optional |

## Performance Features

The client automatically uses performance optimizations when available:

- **msgspec**: Faster JSON serialization
- **PyArrow**: Efficient Parquet file reading  
- **Polars**: Native DataFrame support

Install with: `pip install msgspec pyarrow polars`

## Error Handling

```python
try:
    result = client.vote_histogram(invalid_data)
except Exception as e:
    print(f"API Error: {e}")
```

## Server URL Configuration

```python
# Default: https://grandjury-server.onrender.com/api/v1
client = GrandJuryClient()

# Custom server
client = GrandJuryClient(base_url="https://your-server.com")
# Automatically appends /api/v1 if missing
```

```bash
pip install grandjury
```

Optional performance dependencies:
```bash
pip install grandjury[performance]  # Installs msgspec, pyarrow, polars
```

## Quick Start

### Basic Model Evaluation
```python
from grandjury import GrandJuryClient

# Initialize client
client = GrandJuryClient(api_key="your-api-key")

# Evaluate model performance
result = client.evaluate_model(
    previous_score=0.7,
    votes=[0.9, 0.8, 0.6],
    reputations=[1.0, 1.0, 0.8]
)
print(f"Score: {result['score']:.4f}")
```

### Vote Analysis with Multiple Data Formats

```python
import pandas as pd
import polars as pl

# Your vote data
vote_data = [
    {
        "inference_id": 1,
        "vote": True,
        "voter_id": 101,
        "vote_time": "2024-07-07T19:22:30",
        # ... other fields
    }
    # ... more votes
]

# No authentication needed for analysis endpoints  
client = GrandJuryClient()

# Use with different data formats
histogram = client.vote_histogram(vote_data)  # dict/list
histogram = client.vote_histogram(pd.DataFrame(vote_data))  # pandas
histogram = client.vote_histogram(pl.DataFrame(vote_data))  # polars
histogram = client.vote_histogram("votes.csv")  # CSV file
histogram = client.vote_histogram("votes.parquet")  # Parquet file

# Vote completeness analysis
completeness = client.vote_completeness(
    data=vote_data,
    voter_list=[101, 102, 103]
)

# Population confidence
confidence = client.population_confidence(
    data=vote_data,
    voter_list=[101, 102, 103]
)

# Majority vote analysis
majority = client.majority_good_votes(
    data=vote_data,
    good_vote=True,
    threshold=0.5
)

# Vote distribution per inference
distribution = client.votes_distribution(vote_data)
```

### Backward Compatibility

```python
# Original function still works
from grandjury import evaluate_model

result = evaluate_model(
    predictions=["Model output 1", "Model output 2"],
    references=["Expected 1", "Expected 2"],
    api_key="your-api-key"
)
```

## API Endpoints

| Method | Description | Authentication |
|--------|-------------|----------------|
| `evaluate_model()` | Model scoring with decay algorithms | Required |
| `vote_histogram()` | Vote time distribution analysis | Optional |
| `vote_completeness()` | Voting completeness metrics | Optional |
| `population_confidence()` | Population confidence analysis | Optional |
| `majority_good_votes()` | Majority vote counting | Optional |
| `votes_distribution()` | Vote distribution per inference | Optional |

## Performance Features

The client automatically uses performance optimizations when available:

- **msgspec**: Faster JSON serialization
- **PyArrow**: Efficient Parquet file reading  
- **Polars**: Native DataFrame support

Install with: `pip install msgspec pyarrow polars`

## Error Handling

```python
try:
    result = client.vote_histogram(invalid_data)
except Exception as e:
    print(f"API Error: {e}")
```

## Server URL Configuration

```python
# Default: https://grandjury-server.onrender.com/api/v1
client = GrandJuryClient()

# Custom server
client = GrandJuryClient(base_url="https://your-server.com")
# Automatically appends /api/v1 if missing
```
