/* MkDocs JavaScript configuration */
document$.addEventListener("DOMContentLoaded", function () {
  /* Add copy buttons to code blocks */
  const copyButton = `<button class="md-clipboard" title="Copy to clipboard"></button>`;
  document.querySelectorAll(".highlight > pre, .codehilite pre").forEach(function (pre) {
    pre.insertAdjacentHTML("afterend", copyButton);
  });
});