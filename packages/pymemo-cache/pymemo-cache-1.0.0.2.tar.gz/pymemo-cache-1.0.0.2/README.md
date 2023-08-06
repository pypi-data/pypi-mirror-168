# PyMemo

Simple Python memoization library.

## Installation

```sh
pip install pymemo-cache
```

## Simple Usage

```python
from pymemo import PyMemo


memo = PyMemo()

# Creates collections with optional expiration interval
articles_cache = memo.create_collection('articles', expiration_interval=15)
comments_cache = memo.create_collection('comments', expiration_interval=60)

articles_cache.set_item('article-1', {'id': 1, 'title': 'Article Example'}) # Any data type
articles_cache.get_item('article-1') # -> {'id': 1, 'title': 'Article Example'}

# After 15 seconds
articles_cache.get_item('article-1') # -> None
```
