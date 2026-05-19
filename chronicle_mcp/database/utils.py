"""Utility functions for database operations."""

from difflib import SequenceMatcher
from urllib.parse import urlparse


def sanitize_url(url: str) -> str:
    """Removes sensitive query parameters from URLs."""
    parsed = urlparse(url)
    sensitive_params = {
        "token",
        "session",
        "key",
        "password",
        "auth",
        "sid",
        "access_token",
        "api_key",
        "apikey",
        "api-secret",
        "secret",
        "api_token",
        "apitoken",
        "bearer",
        "jwt",
        "csrf",
        "xsrf",
        "nonce",
        "salt",
        "hash",
    }

    query_parts = []
    for part in parsed.query.split("&"):
        param = part.split("=")[0] if "=" in part else part
        if param.lower() not in sensitive_params:
            query_parts.append(part)

    safe_query = "&".join(query_parts)
    reconstructed = parsed._replace(query=safe_query)
    return reconstructed.geturl()


def fuzzy_match_score(s1: str, s2: str) -> float:
    """
    Calculates fuzzy match similarity score between two strings.

    Args:
        s1: First string
        s2: Second string

    Returns:
        Similarity score between 0 and 1
    """
    if not s1 or not s2:
        return 0.0

    s1_lower = s1.lower()
    s2_lower = s2.lower()

    if s1_lower == s2_lower:
        return 1.0

    score1 = SequenceMatcher(None, s1_lower, s2_lower).ratio()
    score2 = SequenceMatcher(None, s2_lower, s1_lower).ratio()

    return max(score1, score2)
