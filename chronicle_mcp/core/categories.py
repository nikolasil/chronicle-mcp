"""Category system for URL classification and browsing analysis.

This module provides category-based classification of URLs for
productivity and browsing habit analysis.
"""

from typing import Any

CATEGORY_PATTERNS: dict[str, list[str]] = {
    "work": [
        "github.com",
        "gitlab.com",
        "bitbucket.org",
        "stackoverflow.com",
        "stackexchange.com",
        "jira.atlassian.com",
        "confluence.atlassian.com",
        "linear.app",
        "notion.so",
        "evernote.com",
        "slack.com",
        "zoom.us",
        "teams.microsoft.com",
        "discourse.org",
        "discuss.codeium.com",
        "sourcegraph.com",
    ],
    "social": [
        "twitter.com",
        "x.com",
        "facebook.com",
        "reddit.com",
        "linkedin.com",
        "instagram.com",
        "threads.net",
        "mastodon.social",
        "blueskyweb.org",
        "tumblr.com",
        "pinterest.com",
        "snapchat.com",
        "tiktok.com",
        "bereal.io",
    ],
    "news": [
        "news.ycombinator.com",
        "bbc.com",
        "cnn.com",
        "reuters.com",
        "apnews.com",
        "nytimes.com",
        "theguardian.com",
        "washingtonpost.com",
        "wsj.com",
        "bloomberg.com",
        "techcrunch.com",
        "arstechnica.com",
        "theverge.com",
        "wired.com",
        "engadget.com",
    ],
    "learning": [
        "coursera.org",
        "udemy.com",
        "edx.org",
        "khanacademy.org",
        "udacity.com",
        "pluralsight.com",
        "linkedin.com/learning",
        "skillshare.com",
        "codecademy.com",
        "freecodecamp.org",
        "developer.mozilla.org",
        "docs.python.org",
        "docs.rs",
        "swift.org",
        "docs.microsoft.com",
        "learn.microsoft.com",
        "google.dev",
        "developers.google.com",
        "cloud.google.com",
        "docs.aws.amazon.com",
        "atlassian.com/docs",
        "guides.github.com",
    ],
    "shopping": [
        "amazon.com",
        "ebay.com",
        "etsy.com",
        "walmart.com",
        "target.com",
        "bestbuy.com",
        "newegg.com",
        "aliexpress.com",
        "shopify.com",
    ],
    "entertainment": [
        "youtube.com",
        "netflix.com",
        "twitch.tv",
        "hulu.com",
        "disneyplus.com",
        "hbomax.com",
        "primevideo.com",
        "spotify.com",
        "soundcloud.com",
        "bandcamp.com",
        "imbd.com",
        "rottentomatoes.com",
        "goodreads.com",
        "audible.com",
    ],
    "health": [
        "webmd.com",
        "healthline.com",
        "mayoclinic.org",
        "nih.gov",
        "who.int",
        "fitbit.com",
        "myfitnesspal.com",
        "strava.com",
        "sleepcycle.com",
        "headspace.com",
        "calm.com",
    ],
}

CATEGORY_DESCRIPTIONS: dict[str, str] = {
    "work": "Software development, documentation, project management",
    "social": "Social media platforms and networking",
    "news": "News outlets and journalism",
    "learning": "Educational platforms and documentation",
    "shopping": "E-commerce and online shopping",
    "entertainment": "Video, audio, and general entertainment",
    "health": "Health, fitness, and wellness",
}

CATEGORY_WEIGHTS: dict[str, float] = {
    "work": 1.0,
    "learning": 0.8,
    "health": 0.7,
    "social": -0.5,
    "entertainment": -0.3,
    "shopping": -0.2,
    "news": 0.0,
}

DEFAULT_CATEGORIES = list(CATEGORY_PATTERNS.keys())


def categorize_url(url: str) -> str | None:
    """
    Categorize a URL based on domain matching.

    Args:
        url: The URL to categorize

    Returns:
        Category name if matched, None if no category found
    """
    if not url:
        return None

    url_lower = url.lower()

    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if pattern in url_lower:
                start_idx = url_lower.find(pattern)
                end_idx = start_idx + len(pattern)
                before = url_lower[:start_idx]
                after = url_lower[end_idx:]

                if (before == "https://" or before == "http://" or before == "//") and (
                    end_idx == len(url_lower) or after[0] in "/."
                ):
                    return category

    return None


def get_url_category_score(url: str) -> tuple[str | None, float]:
    """
    Get category and productivity score for a URL.

    Args:
        url: The URL to score

    Returns:
        Tuple of (category, productivity_score)
    """
    category = categorize_url(url)
    if category:
        score = CATEGORY_WEIGHTS.get(category, 0.0)
        return category, score
    return None, 0.0


def categorize_urls(urls: list[str]) -> dict[str, list[str]]:
    """
    Categorize multiple URLs.

    Args:
        urls: List of URLs to categorize

    Returns:
        Dict mapping category to list of URLs in that category
    """
    categorized: dict[str, list[str]] = {cat: [] for cat in DEFAULT_CATEGORIES}
    uncategorized: list[str] = []

    for url in urls:
        category = categorize_url(url)
        if category:
            categorized[category].append(url)
        else:
            uncategorized.append(url)

    categorized["uncategorized"] = uncategorized
    return categorized


def get_category_breakdown(category_counts: dict[str, int]) -> dict[str, dict[str, Any]]:
    """
    Calculate category breakdown with percentages and scores.

    Args:
        category_counts: Dict mapping category to visit count

    Returns:
        Dict with category stats including percentages
    """
    total = sum(category_counts.values()) if category_counts else 0

    breakdown = {}
    for category, count in category_counts.items():
        if count > 0:
            percentage = (count / total * 100) if total > 0 else 0
            weight = CATEGORY_WEIGHTS.get(category, 0.0)
            breakdown[category] = {
                "count": count,
                "percentage": round(percentage, 1),
                "weight": weight,
                "score_contribution": round(weight * count, 2),
            }

    return breakdown


def calculate_productivity_score(category_counts: dict[str, int]) -> tuple[int, str]:
    """
    Calculate overall productivity score from category counts.

    Args:
        category_counts: Dict mapping category to visit count

    Returns:
        Tuple of (score 0-100, grade letter)
    """
    total = sum(category_counts.values()) if category_counts else 0
    if total == 0:
        return 0, "N/A"

    positive_score = 0.0
    negative_score = 0.0

    for category, count in category_counts.items():
        weight = CATEGORY_WEIGHTS.get(category, 0.0)
        if weight > 0:
            positive_score += weight * count
        elif weight < 0:
            negative_score += abs(weight) * count

    net_score = positive_score - (negative_score * 0.5)
    max_possible = sum(abs(CATEGORY_WEIGHTS.get(c, 0)) * cnt for c, cnt in category_counts.items())

    if max_possible > 0:
        normalized_score = int((net_score / max_possible) * 100)
        normalized_score = max(0, min(100, normalized_score))
    else:
        normalized_score = 50

    grade = _score_to_grade(normalized_score)
    return normalized_score, grade


def _score_to_grade(score: int) -> str:
    """Convert numeric score to letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def generate_recommendations(
    category_counts: dict[str, int],
    top_domains: list[tuple[str, int]],
) -> list[str]:
    """
    Generate productivity recommendations based on browsing data.

    Args:
        category_counts: Category visit counts
        top_domains: List of (domain, count) tuples

    Returns:
        List of recommendation strings
    """
    recommendations = []

    if category_counts.get("social", 0) > 50:
        recommendations.append("Consider reducing social media usage - it's your top distraction")

    if category_counts.get("entertainment", 0) > 30:
        recommendations.append(
            "Entertainment consumption is high - balance with focused work sessions"
        )

    if category_counts.get("work", 0) > 100:
        recommendations.append("Great focus on work-related sites! Keep up the productive browsing")

    if category_counts.get("learning", 0) > 20:
        recommendations.append(
            "Good learning engagement! Consider tracking what topics interest you most"
        )

    if category_counts.get("uncategorized", 0) > category_counts.get("work", 0):
        recommendations.append(
            "Many visits to uncategorized sites. Consider adding work domains to improve tracking"
        )

    if not recommendations:
        recommendations.append("Your browsing appears balanced. Keep monitoring your habits")

    return recommendations
