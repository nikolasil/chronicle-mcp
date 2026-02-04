import os
import sqlite3
import shutil
import tempfile
import platform
from fastmcp import FastMCP

# Initialize MCP Server
mcp = FastMCP("Chronicle")

def get_history_path():
    """Detects OS and returns the default Chrome history path."""
    system = platform.system()
    if system == "Windows":
        return os.path.expandvars(r"%LocalAppData%\Google\Chrome\User Data\Default\History")
    elif system == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/History")
    else:
        # Default/Linux
        return os.path.expanduser("~/.config/google-chrome/Default/History")

def get_history_connection():
    """Creates a temporary copy of the history DB to avoid 'Database Locked' errors."""
    history_path = get_history_path()
    
    if not os.path.exists(history_path):
        raise FileNotFoundError(f"Could not find browser history at {history_path}")
    
    # Create a unique temp file
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, "chronicle_temp_history.db")
    
    # Copy the file (even if it's open in Chrome)
    shutil.copy2(history_path, temp_path)
    return sqlite3.connect(temp_path)

@mcp.tool()
def search_history(query: str, limit: int = 5) -> str:
    """
    Searches browser history for keywords in titles or URLs.
    """
    try:
        conn = get_history_connection()
        cursor = conn.cursor()
        
        search_query = f"%{query}%"
        cursor.execute(
            "SELECT title, url, last_visit_time FROM urls WHERE title LIKE ? OR url LIKE ? ORDER BY last_visit_time DESC LIMIT ?",
            (search_query, search_query, limit)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return f"No history found for: {query}"
        
        results = [f"- **{title}**\n  URL: {url}" for title, url, _ in rows]
        return "\n\n".join(results)
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()