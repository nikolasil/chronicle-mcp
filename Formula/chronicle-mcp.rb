class ChronicleMcp < Formula
  desc "MCP server for secure local browser history access"
  homepage "https://github.com/nikolasil/chronicle-mcp"
  url "https://github.com/nikolasil/chronicle-mcp/archive/refs/tags/v1.3.3.tar.gz"
  sha256 "a943887efb6eebdfd5f1df746d77289bb1569aa257638c0038e49f348d8d519a"
  license "MIT"
  head "https://github.com/nikolasil/chronicle-mcp.git", branch: "main"

  depends_on "python@3.10"
  depends_on "python@3.11"
  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "ChronicleMCP", shell_output("#{bin}/chronicle-mcp version")
  end
end
