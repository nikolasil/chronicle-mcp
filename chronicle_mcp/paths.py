import glob
import os
import platform

BROWSER_PATHS: dict[str, dict[str, str]] = {
    "chrome": {
        "Windows": r"%LocalAppData%\Google\Chrome\User Data\Default\History",
        "Darwin": "~/Library/Application Support/Google/Chrome/Default/History",
        "Linux": "~/.config/google-chrome/Default/History",
    },
    "edge": {
        "Windows": r"%LocalAppData%\Microsoft\Edge\User Data\Default\History",
        "Darwin": "~/Library/Application Support/Microsoft Edge/Default/History",
        "Linux": "~/.config/microsoft-edge/Default/History",
    },
    "firefox": {
        "Windows": r"%AppData%\Mozilla\Firefox\Profiles\*.default\places.sqlite",
        "Darwin": "~/Library/Mozilla/Firefox/Profiles/*.default/places.sqlite",
        "Linux": "~/.mozilla/firefox/*.default/places.sqlite",
    },
    "brave": {
        "Windows": r"%LocalAppData%\BraveSoftware\Brave-Default\History",
        "Darwin": "~/Library/Application Support/BraveSoftware/Brave-Default/History",
        "Linux": "~/.config/BraveSoftware/Brave-Default/History",
    },
    "safari": {
        "Darwin": "~/Library/Safari/History.db",
    },
    "vivaldi": {
        "Windows": r"%LocalAppData%\Vivaldi\Default\History",
        "Darwin": "~/Library/Application Support/Vivaldi/Default/History",
        "Linux": "~/.config/vivaldi/Default/History",
    },
    "opera": {
        "Windows": r"%AppData%\Opera Software\Opera Stable\History",
        "Darwin": "~/Library/Application Support/com.operasoftware.Opera/History",
        "Linux": "~/.config/opera/History",
    },
}

BROWSER_SCHEMAS: dict[str, str] = {
    "chrome": "chrome",
    "edge": "chrome",
    "brave": "chrome",
    "vivaldi": "chrome",
    "opera": "chrome",
    "firefox": "firefox",
    "safari": "safari",
}


def get_browser_schema(browser: str) -> str:
    """
    Returns the schema type for the specified browser.

    Args:
        browser: Browser name (case insensitive)

    Returns:
        Schema type: 'chrome', 'firefox', or 'safari'
    """
    return BROWSER_SCHEMAS.get(browser.lower(), "chrome")


def get_os_name() -> str:
    """Returns the current operating system name."""
    return platform.system()


def expand_path(path: str) -> str:
    """Expands environment variables and home directory in path."""
    return os.path.expandvars(os.path.expanduser(path))


def find_glob_path(pattern: str) -> str | None:
    """Finds a file matching the glob pattern, returns first match or None."""
    matches = glob.glob(expand_path(pattern))
    return matches[0] if matches else None


def get_browser_path(browser: str) -> str | None:
    """
    Gets the history database path for the specified browser.

    Args:
        browser: Browser name (chrome, edge, firefox) - case insensitive

    Returns:
        Path to history database or None if not found
    """
    browser_lower = browser.lower()

    if browser_lower not in BROWSER_PATHS:
        return None

    os_name = get_os_name()
    path_pattern = BROWSER_PATHS[browser_lower].get(os_name)

    if not path_pattern:
        return None

    if "*" in path_pattern:
        return find_glob_path(path_pattern)
    else:
        expanded = expand_path(path_pattern)
        return expanded if os.path.exists(expanded) else None


def get_available_browsers() -> list[str]:
    """
    Returns a list of browsers with detected history databases.
    """
    available = []
    for browser in BROWSER_PATHS:
        if get_browser_path(browser):
            available.append(browser)
    return available


def get_all_browser_paths() -> dict[str, str | None]:
    """
    Returns a dictionary of all browser paths (found or not found).
    Useful for debugging.
    """
    result = {}
    for browser in BROWSER_PATHS:
        path = get_browser_path(browser)
        result[browser] = path
    return result
