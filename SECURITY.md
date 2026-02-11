# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | :white_check_mark: |
| 0.0.x   | :x: |

## Reporting a Vulnerability

ChronicleMCP is a local-only application that reads browser history from your machine.
No data is sent to any external servers. However, we take security seriously.

If you believe you have found a security vulnerability in ChronicleMCP, please
report it responsibly by emailing: **iliopoulos.info@gmail.com**

Do **not** open public issues or pull requests for security vulnerabilities.

## What to Include in Your Report

When reporting a vulnerability, please include:

1. A description of the vulnerability
2. Steps to reproduce the issue
3. Any relevant code snippets or configurations
4. Your assessment of the potential impact

## What to Expect

After submitting your report, you can expect:

1. **Acknowledgement**: Within 24-48 hours, you will receive an acknowledgment
   of your report.

2. **Investigation**: We will investigate the issue and determine its validity
   and severity.

3. **Response**: You will receive a response with:
   - Whether the issue is confirmed
   - Our assessment of the impact
   - A timeline for when we expect to address it

4. **Resolution**: Once fixed, you will be notified when the fix is released.

## Security Best Practices

ChronicleMCP implements the following security measures:

- **Local-only data access**: All browser history stays on your machine
- **URL sanitization**: Sensitive query parameters (tokens, sessions, keys) are
  automatically removed from URLs before display
- **Temporary file handling**: Browser history is copied to temporary files
  that are cleaned up after each query
- **Error message sanitization**: No sensitive file paths are exposed in error
  messages

## Additional Information

For questions about security in ChronicleMCP, please contact: iliopoulos.info@gmail.com
