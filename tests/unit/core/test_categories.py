"""Tests for category system."""

from chronicle_mcp.core.categories import (
    calculate_productivity_score,
    categorize_url,
    categorize_urls,
    generate_recommendations,
    get_category_breakdown,
    get_url_category_score,
)


class TestCategorizeUrl:
    """Tests for categorize_url function."""

    def test_github_categorized_as_work(self):
        """GitHub should be categorized as work."""
        assert categorize_url("https://github.com/user/repo") == "work"

    def test_stackoverflow_categorized_as_work(self):
        """Stack Overflow should be categorized as work."""
        assert categorize_url("https://stackoverflow.com/questions/123") == "work"

    def test_twitter_categorized_as_social(self):
        """Twitter should be categorized as social."""
        assert categorize_url("https://twitter.com/user/status/123") == "social"

    def test_reddit_categorized_as_social(self):
        """Reddit should be categorized as social."""
        assert categorize_url("https://reddit.com/r/python") == "social"

    def test_youtube_categorized_as_entertainment(self):
        """YouTube should be categorized as entertainment."""
        assert categorize_url("https://youtube.com/watch?v=abc") == "entertainment"

    def test_netflix_categorized_as_entertainment(self):
        """Netflix should be categorized as entertainment."""
        assert categorize_url("https://netflix.com/title/123") == "entertainment"

    def test_amazon_categorized_as_shopping(self):
        """Amazon should be categorized as shopping."""
        assert categorize_url("https://amazon.com/product/123") == "shopping"

    def test_coursera_categorized_as_learning(self):
        """Coursera should be categorized as learning."""
        assert categorize_url("https://coursera.org/course/123") == "learning"

    def test_unkown_url_returns_none(self):
        """Unknown URL should return None."""
        assert categorize_url("https://example.com/unknown") is None

    def test_empty_url_returns_none(self):
        """Empty URL should return None."""
        assert categorize_url("") is None
        assert categorize_url(None) is None


class TestGetUrlCategoryScore:
    """Tests for get_url_category_score function."""

    def test_work_score_is_positive(self):
        """Work category should have positive score."""
        category, score = get_url_category_score("https://github.com/user/repo")
        assert category == "work"
        assert score > 0

    def test_social_score_is_negative(self):
        """Social category should have negative score."""
        category, score = get_url_category_score("https://twitter.com/user")
        assert category == "social"
        assert score < 0

    def test_unkown_url_returns_zero_score(self):
        """Unknown URL should return zero score."""
        _, score = get_url_category_score("https://example.com")
        assert score == 0


class TestCalculateProductivityScore:
    """Tests for calculate_productivity_score function."""

    def test_all_work_returns_high_score(self):
        """100% work should return high score."""
        category_counts = {"work": 100}
        score, grade = calculate_productivity_score(category_counts)
        assert score >= 80
        assert grade in ["A", "B"]

    def test_all_social_returns_low_score(self):
        """100% social should return low score."""
        category_counts = {"social": 100}
        score, grade = calculate_productivity_score(category_counts)
        assert score < 50
        assert grade in ["D", "F"]

    def test_mixed_category_returns_middle_score(self):
        """Mixed browsing should return middle score."""
        category_counts = {"work": 50, "social": 50}
        score, grade = calculate_productivity_score(category_counts)
        assert 40 <= score <= 70

    def test_empty_counts_returns_zero(self):
        """Empty counts should return 0."""
        category_counts = {}
        score, grade = calculate_productivity_score(category_counts)
        assert score == 0
        assert grade == "N/A"


class TestGenerateRecommendations:
    """Tests for generate_recommendations function."""

    def test_high_social_generates_recommendation(self):
        """High social usage should generate recommendation."""
        category_counts = {"social": 100, "work": 10}
        top_domains = [("reddit.com", 50)]
        recommendations = generate_recommendations(category_counts, top_domains)
        assert any("social media" in r.lower() for r in recommendations)

    def test_high_work_generates_positive_recommendation(self):
        """High work usage should generate positive recommendation."""
        category_counts = {"work": 200, "social": 10}
        top_domains = [("github.com", 100)]
        recommendations = generate_recommendations(category_counts, top_domains)
        assert any("great" in r.lower() or "productive" in r.lower() for r in recommendations)

    def test_empty_recommendations_returns_default(self):
        """Empty counts should return default recommendation."""
        category_counts = {}
        top_domains = []
        recommendations = generate_recommendations(category_counts, top_domains)
        assert len(recommendations) > 0


class TestGetCategoryBreakdown:
    """Tests for get_category_breakdown function."""

    def test_breakdown_includes_percentages(self):
        """Breakdown should include percentage for each category."""
        category_counts = {"work": 50, "social": 50}
        breakdown = get_category_breakdown(category_counts)

        assert "work" in breakdown
        assert "social" in breakdown
        assert "percentage" in breakdown["work"]
        assert "percentage" in breakdown["social"]

    def test_breakdown_percentages_sum_to_100(self):
        """Percentages should sum to approximately 100."""
        category_counts = {"work": 50, "social": 50}
        breakdown = get_category_breakdown(category_counts)

        total_percentage = sum(b.get("percentage", 0) for b in breakdown.values())
        assert 99 <= total_percentage <= 101


class TestCategorizeUrls:
    """Tests for categorize_urls function."""

    def test_categorize_multiple_urls(self):
        """Multiple URLs should be categorized correctly."""
        urls = [
            "https://github.com/user/repo",
            "https://twitter.com/user",
            "https://example.com/unknown",
        ]
        result = categorize_urls(urls)

        assert len(result["work"]) == 1
        assert len(result["social"]) == 1
        assert len(result["uncategorized"]) == 1

    def test_uncategorized_key_always_present(self):
        """uncategorized key should always be present."""
        urls = ["https://github.com/repo"]
        result = categorize_urls(urls)
        assert "uncategorized" in result
