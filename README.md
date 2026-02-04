# 🏛️ ChronicleMCP: Local Browser History for AI Agents

**ChronicleMCP** is a secure, local-first [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that allows AI agents (like Claude Desktop, Cursor, and IDEs) to search your local browser history.

Instead of the AI "hallucinating" or guessing which documentation you were reading, it can now reference the exact pages you’ve visited—**without your data ever leaving your machine.**

---

## ✨ Features

* **Privacy-First:** Your browser history is read directly from your local SQLite database. No cloud syncing, no data collection.
* **Documentation Focus:** Specifically tuned to help AI agents find technical docs, GitHub repos, and StackOverflow threads you've recently accessed.
* **Universal Compatibility:** Works with any AI client that supports the MCP standard.
* **Blazing Fast:** Built with Python and SQLite for near-instant retrieval.

---

## 🛠️ Installation

### 1. Prerequisites
- Python 3.10+
- [FastMCP](https://github.com/jlowin/fastmcp)
- Google Chrome or Microsoft Edge (Support for Firefox/Safari coming soon)

### 2. Clone and Setup
```bash
git clone [https://github.com/nikolasil/chronicle-mcp.git](https://github.com/nikolasil/chronicle-mcp.git)
cd ChronicleMCP
pip install fastmcp
```

---

## 🔌 Connecting to AI Clients
To use ChronicleMCP, you need to tell your AI client where the server script and the Python environment are located.

* Claude Desktop
Open your Claude Desktop configuration file:
Windows: %APPDATA%\Claude\claude_desktop_config.json
macOS: ~/Library/Application Support/Claude/claude_desktop_config.json

Add the following to the mcpServers section (replace YOUR_USERNAME and the paths with your actual project location):

```JSON
{
  "mcpServers": {
    "chronicle": {
      "command": "C:\\Users\\YOUR_USERNAME\\path\\to\\chronicle-mcp\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YOUR_USERNAME\\path\\to\\chronicle-mcp\\server.py"
      ]
    }
  }
}
```

* Cursor / IDEs
Go to Settings > Cursor Settings > Features > MCP.
Click + Add New MCP Server.
Name: Chronicle
Type: command
Command: bash /path/to/chronicle-mcp/venv/Scripts/python server.py

## 💡 Pro Tip for Contributors
If you want to test the connection without opening Claude, run this command in your terminal:

```Bash
python server.py dev
```
This will launch the MCP Inspector, a web-based debugger where you can manually run the search_history tool to see what the AI will see.