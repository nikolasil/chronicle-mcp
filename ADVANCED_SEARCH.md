# Advanced Search Guide

## Table of Contents

1. [Basic Search](#basic-search)
2. [Advanced Search Tool](#advanced-search-tool)
3. [Regex Support](#regex-support)
4. [Fuzzy Matching](#fuzzy-matching)
5. [Domain Filtering](#domain-filtering)
6. [Excluding Domains](#excluding-domains)
7. [Sorting Results](#sorting-results)

---

## Basic Search

### Simple Query

```python
search_history("python tutorial")
```

### With Limit

```python
search_history("github", limit=10)
```

### Specific Browser

```python
search_history("documentation", browser="firefox")
```

---

## Advanced Search Tool

The `search_history_advanced` tool provides additional options for more control over your searches.

```python
search_history_advanced(
    query: str,
    limit: int = 20,
    browser: str = "chrome",
    format_type: str = "markdown",
    exclude_domains: list[str] = None,
    sort_by: str = "date",
    use_regex: bool = False,
    use_fuzzy: bool = False,
    fuzzy_threshold: float = 0.6
)
```

---

## Regex Support

Use regular expressions for powerful pattern matching.

```python
# Search for URLs ending with specific patterns
search_history_advanced(
    query=r"github\.com/.*/issues",
    use_regex=True
)

# Find pages with ticket numbers
search_history_advanced(
    query=r"#\d+",
    use_regex=True
)

# Match multiple patterns
search_history_advanced(
    query=r"(python|javascript|ruby)",
    use_regex=True
)
```

### Common Regex Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| `github\.com` | Literal domain | `github\.com` |
| `\d+` | One or more digits | `#\d+` |
| `.*` | Any characters | `python.*` |
| `^http` | Starts with http | `^http` |
| `$` | Ends with | `\.pdf$` |
| `\|` | OR operator | `python\|javascript` |

---

## Fuzzy Matching

Fuzzy matching helps find results even with typos.

```python
# Standard fuzzy search
search_history_advanced(
    query="pythom tutorial",  # Typo!
    use_fuzzy=True
)

# With custom threshold
search_history_advanced(
    query="javscript",  # Typo!
    use_fuzzy=True,
    fuzzy_threshold=0.5  # Lower threshold for more matches
)
```

### Threshold Guide

| Threshold | Behavior |
|-----------|----------|
| 0.9 | Very strict, only close matches |
| 0.7 | Balanced (recommended) |
| 0.5 | More permissive, may include irrelevant results |

---

## Domain Filtering

Search only within specific domains.

```python
# Search within GitHub
search_by_domain("github.com", query="python")

# Search within documentation sites
search_by_domain("docs.python.org", query="tutorial")
```

---

## Excluding Domains

Filter out specific domains from your results.

```python
# Exclude YouTube from results
search_history_advanced(
    query="tutorial",
    exclude_domains=["youtube.com", "vimeo.com"]
)

# Exclude social media
search_history_advanced(
    query="news",
    exclude_domains=["twitter.com", "facebook.com", "instagram.com"]
)
```

---

## Sorting Results

Control how your results are ordered.

### By Date (Default)

```python
search_history_advanced(
    query="python",
    sort_by="date"
)
```

### By Visit Count

```python
search_history_advanced(
    query="documentation",
    sort_by="visit_count"  # Most visited first
)
```

### By Title

```python
search_history_advanced(
    query="python",
    sort_by="title"  # Alphabetical
)
```

---

## Combining Options

Combine multiple options for powerful searches.

```python
# Find Python tutorials, exclude social media, most visited first
search_history_advanced(
    query="python tutorial",
    sort_by="visit_count",
    exclude_domains=["twitter.com", "facebook.com"],
    limit=20
)

# Regex search with domain filter
search_history_advanced(
    query=r"https://docs\..*",
    use_regex=True,
    sort_by="date"
)
```

---

## Examples

### Finding Recent Documentation

```python
search_history_advanced(
    query="api documentation",
    sort_by="date",
    limit=10
)
```

### Finding Unvisited Bookmarks

```python
search_history_advanced(
    query="bookmark",
    sort_by="visit_count",
    limit=5
)
```

### Finding Specific URL Patterns

```python
search_history_advanced(
    query=r"github\.com/.*/pull/\d+",
    use_regex=True,
    limit=20
)
```

### Fixing Typos

```python
search_history_advanced(
    query="intersting",  # Intended: "interesting"
    use_fuzzy=True,
    fuzzy_threshold=0.6
)
```
