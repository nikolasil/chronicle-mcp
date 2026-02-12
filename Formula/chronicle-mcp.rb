class ChronicleMcp < Formula
  desc "MCP server for secure local browser history access"
  homepage "https://github.com/nikolasil/chronicle-mcp"
  url "https://github.com/nikolasil/chronicle-mcp/archive/refs/tags/v1.2.12.tar.gz"
  sha256 "da21ab5ec5aafb244ef4a475582207319483f8de80adae8981fd23e8ac222427"
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
