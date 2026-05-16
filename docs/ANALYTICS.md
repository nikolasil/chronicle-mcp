# Analytics Guide

ChronicleMCP provides advanced analytics features for understanding browsing patterns, productivity, and generating insights reports.

## Table of Contents

1. [Productivity Analysis](#productivity-analysis)
2. [Time Period Comparison](#time-period-comparison)
3. [Category Suggestions](#category-suggestions)
4. [Visualization Export](#visualization-export)
5. [Insights Report](#insights-report)
6. [Duplicate Detection](#duplicate-detection)

---

## Productivity Analysis

Analyze your browsing productivity with a calculated score and category breakdown.

```python
def analyze_productivity(
    start_date: str | None = None,
    end_date: str | None = None,
    browser: str = "chrome",
) -> dict[str, Any]
```

**Example:**

```python
result = HistoryService.analyze_productivity(browser="chrome")
# Returns: {
#     "productivity_score": 72,
#     "grade": "B+",
#     "category_breakdown": {...},
#     "recommendations": [...],
#     "browser": "chrome"
# }
```

### Productivity Grades

| Score | Grade | Description |
|-------|-------|-------------|
| 80-100 | A | Highly productive browsing |
| 60-79 | B | Good balance |
| 40-59 | C | Needs improvement |
| 0-39 | D | Low productivity |

### Categories

Browsing is categorized into:

- **Development** - Programming, documentation, code hosting
- **Search** - Search engines and portals
- **Social** - Social media platforms
- **Video** - Video streaming and content
- **News** - News and media sites
- **Shopping** - E-commerce and retail
- **Entertainment** - Games, humor, leisure
- **Education** - Online courses, tutorials
- **Other** - Uncategorized

---

## Time Period Comparison

Compare browsing statistics between two time periods.

```python
def compare_time_periods(
    start_date1: str,
    end_date1: str,
    start_date2: str,
    end_date2: str,
    browser: str = "chrome",
) -> dict[str, Any]
```

**Example:**

```python
result = HistoryService.compare_time_periods(
    start_date1="2024-01-01",
    end_date1="2024-01-31",
    start_date2="2024-02-01",
    end_date2="2024-02-29",
    browser="chrome"
)
```

**Returns:**

```python
{
    "period1": {
        "start": "2024-01-01",
        "end": "2024-01-31",
        "total_visits": 1500,
        "unique_urls": 400,
        "top_domains": [["github.com", 200], ...]
    },
    "period2": {
        "start": "2024-02-01",
        "end": "2024-02-29",
        "total_visits": 1800,
        "unique_urls": 450,
        "top_domains": [["github.com", 250], ...]
    },
    "changes": {
        "total_visits_delta": 300,
        "unique_urls_delta": 50,
        "top_domains_gained": ["newsite.com"],
        "top_domains_lost": ["oldsite.com"]
    },
    "category_breakdown": {...}
}
```

---

## Category Suggestions

Suggest categories for uncategorized URLs based on URL patterns.

```python
def suggest_categories(
    browser: str = "chrome",
    limit: int = 20,
) -> dict[str, Any]
```

**Example:**

```python
result = HistoryService.suggest_categories(browser="chrome", limit=20)
# Returns: {
#     "uncategorized": [
#         {
#             "title": "Repo Issues",
#             "url": "https://github.com/user/repo/issues",
#             "visit_count": 15,
#             "suggested_category": "Development"
#         }
#     ],
#     "count": 1,
#     "browser": "chrome"
# }
```

---

## Visualization Export

Export browsing data formatted for Chart.js visualization.

```python
def export_visualization(
    format_type: str = "chart_json",
    period: str = "month",
    browser: str = "chrome",
) -> dict[str, Any]
```

**Parameters:**

| Parameter | Values | Description |
|-----------|--------|-------------|
| `format_type` | `chart_json`, `csv` | Output format |
| `period` | `day`, `week`, `month` | Time period |
| `browser` | Browser name | Browser to analyze |

**Example:**

```python
result = HistoryService.export_visualization(
    format_type="chart_json",
    period="month",
    browser="chrome"
)
# Returns Chart.js compatible data:
# {
#     "charts": [
#         {
#             "type": "doughnut",
#             "title": "Time by Category",
#             "data": {
#                 "labels": ["Development", "Search", ...],
#                 "datasets": [{
#                     "data": [45, 20, ...],
#                     "backgroundColor": ["#4CAF50", "#2196F3", ...]
#                 }]
#             }
#         },
#         {
#             "type": "bar",
#             "title": "Top 10 Domains",
#             "data": {...}
#         },
#         {
#             "type": "bar",
#             "title": "Activity by Hour",
#             "data": {...}
#         }
#     ],
#     "period": "month",
#     "category_breakdown": {...}
# }
```

### CSV Export

```python
result = HistoryService.export_visualization(
    format_type="csv",
    period="week",
    browser="firefox"
)
# Returns: {
#     "content": "Category,Count,Percentage,Weight\nDevelopment,150,45.0,45\n...",
#     "format": "csv",
#     "period": "week"
# }
```

---

## Insights Report

Generate a comprehensive browsing insights report.

```python
def generate_insights_report(
    period: str = "week",
    browser: str = "chrome",
    format_type: str = "markdown",
) -> dict[str, Any]
```

**Parameters:**

| Parameter | Values | Description |
|-----------|--------|-------------|
| `period` | `day`, `week`, `month` | Time period |
| `browser` | Browser name | Browser to analyze |
| `format_type` | `markdown`, `json` | Output format |

**Example:**

```python
result = HistoryService.generate_insights_report(
    period="week",
    browser="chrome",
    format_type="markdown"
)
# Returns:
# {
#     "summary_markdown": "# Browsing Insights Report (week)\n\n**Browser:** chrome\n...",
#     "browser": "chrome",
#     "period": "week"
# }
```

### Markdown Report Format

```markdown
# Browsing Insights Report (week)

**Browser:** chrome

**Total Visits:** 1500

**Unique URLs:** 400

## Productivity

**Score:** 72/100 (B+)

## Categories
- **Development** (Code & Documentation): 450 visits (30%)
- **Search** (Search Engines): 300 visits (20%)
...

## Top Domains
- github.com: 200 visits
- stackoverflow.com: 150 visits
...

## Recommendations
- Consider limiting time on social media
- Great focus on development resources!
```

---

## Duplicate Detection

Find and remove duplicate history entries based on URL similarity.

```python
def find_duplicate_entries(
    browser: str,
    similarity_threshold: float = 0.9,
    limit: int = 100,
) -> dict[str, Any]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `browser` | String | Required | Browser to analyze |
| `similarity_threshold` | Float | 0.9 | URL similarity threshold (0.0-1.0) |
| `limit` | Integer | 100 | Maximum groups to return |

**Example:**

```python
result = HistoryService.find_duplicate_entries(
    browser="chrome",
    similarity_threshold=0.9,
    limit=50
)
# Returns:
# {
#     "browser": "chrome",
#     "similarity_threshold": 0.9,
#     "duplicate_groups": [
#         {
#             "url": "https://example.com/page",
#             "title": "Example Page",
#             "visit_count": 10,
#             "similar_to": [
#                 {
#                     "url": "https://example.com/page/",
#                     "title": "Example Page",
#                     "visit_count": 5,
#                     "similarity": 0.96
#                 }
#             ]
#         }
#     ],
#     "total_duplicates": 5,
#     "total_entries_analyzed": 500
# }
```

### Deleting Duplicates

```python
def delete_duplicates(
    browser: str,
    similarity_threshold: float = 0.9,
    keep_strategy: str = "most_visits",
    confirm: bool = False,
) -> dict[str, Any]
```

**Parameters:**

| Parameter | Values | Description |
|-----------|--------|-------------|
| `keep_strategy` | `most_visits`, `most_recent`, `first` | Which entry to keep |
| `confirm` | Boolean | Must be `True` to actually delete |

**Example:**

```python
# Preview what would be deleted
result = HistoryService.delete_duplicates(
    browser="chrome",
    confirm=False
)
# Returns preview

# Actually delete
result = HistoryService.delete_duplicates(
    browser="chrome",
    keep_strategy="most_visits",
    confirm=True
)
# Returns deletion summary
```

---

## MCP Tools

These features are available as MCP tools:

| Tool | Description |
|------|-------------|
| `analyze_productivity` | Get productivity score and recommendations |
| `compare_time_periods` | Compare browsing between two date ranges |
| `suggest_categories` | Suggest categories for uncategorized URLs |
| `export_visualization` | Export Chart.js compatible data |
| `generate_insights_report` | Create comprehensive browsing report |
| `find_duplicate_entries` | Find potential duplicate URLs |
| `delete_duplicates` | Remove duplicate history entries |

---

## See Also

- [Advanced Search](advanced_search.md)
- [Architecture](architecture.md)
- [CLI Reference](cli.md)