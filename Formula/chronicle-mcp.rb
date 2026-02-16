class ChronicleMcp < Formula
  desc "MCP server for secure local browser history access"
  homepage "https://github.com/nikolasil/chronicle-mcp"
  url "https://github.com/nikolasil/chronicle-mcp/archive/refs/tags/v1.4.0.tar.gz"
  sha256 "d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed"
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
