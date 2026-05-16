# ChronicleMCP Public Roadmap

Welcome to the ChronicleMCP public roadmap. This document outlines the planned development direction, upcoming features, and areas of focus for the project.

## Project Vision

ChronicleMCP aims to provide AI agents with secure, privacy-first access to local browser history through a well-architected MCP (Model Context Protocol) server. We prioritize local data processing, minimal dependencies, and comprehensive browser support.

---

## In Progress

### Real-time History Updates
- **Type:** Feature
- **Status:** Planned for v1.5.0
- **Description:** Add WebSocket/SSE-based subscription system for real-time history change notifications
- **Milestone:** [Issue #XX](https://github.com/nikolasil/chronicle-mcp/issues)

### Advanced Analytics Dashboard
- **Type:** Feature
- **Status:** Planning
- **Description:** Web-based dashboard for visualizing browsing patterns, productivity metrics, and history insights
- **Milestone:** [Issue #XX](https://github.com/nikolasil/chronicle-mcp/issues)

---

## Planned for v1.5.0

### History Deduplication Tool
- **Type:** Feature
- **Priority:** Medium
- **Description:** Detect and merge duplicate/very similar history entries based on URL and visit timing patterns
- **Effort:** 2-3 days

### PDF Report Export
- **Type:** Enhancement
- **Priority:** Low
- **Description:** Generate formatted PDF reports of browsing history for sharing or archival
- **Effort:** 2 days

### Safari Full Support
- **Type:** Browser Support
- **Priority:** Medium
- **Description:** Complete Safari support including iCloud-synced history, proper plist parsing for bookmarks
- **Effort:** 3-5 days

---

## Backlog

### Browser Extension
- **Type:** Feature
- **Priority:** Medium
- **Description:** Chrome/Firefox extension for quick history lookup and status indicators
- **Effort:** 1-2 weeks

### Multi-Profile Support
- **Type:** Feature
- **Priority:** Low
- **Description:** Support for browser profiles beyond Default (e.g., Chrome Profile 1, Profile 2)
- **Effort:** 3-4 days

### Firefox Containers Support
- **Type:** Feature
- **Priority:** Low
- **Description:** Integration with Firefox Multi-Account Containers extension
- **Effort:** 3-4 days

### Import/Export to Other Formats
- **Type:** Enhancement
- **Priority:** Low
- **Description:** Add support for HTML bookmarks export, Netscape bookmark file import
- **Effort:** 2-3 days

### History Search Enhancement
- **Type:** Enhancement
- **Priority:** Medium
- **Description:** ML-based search ranking and semantic search capabilities
- **Effort:** 1+ week

---

## Completed

### v1.4.0 - Advanced Analytics (Current)
- Advanced search with regex and fuzzy matching
- Productivity analysis and category suggestions
- Time period comparison
- Visualization data export (Chart.js compatible)
- Comprehensive insights report generation
- Duplicate detection and cleanup

### v1.3.0 - Bookmarks & Downloads
- Bookmarks retrieval for all supported browsers
- Downloads history access
- Enhanced search across bookmarks

### v1.2.0 - Cross-Browser Sync
- History synchronization between browsers
- Multiple merge strategies (latest, combine, dedupe)
- Dry-run mode for safe syncing

### v1.1.0 - Multi-Browser Support
- Added Edge, Brave, Vivaldi, Opera support
- Firefox improvements
- Safari basic support

### v1.0.0 - Initial Release
- Core history search functionality
- MCP protocol server
- HTTP REST API
- Chrome history access

---

## Version History

| Version | Status | Release Date | Key Features |
|---------|--------|-------------|--------------|
| 1.4.0 | Current | 2025-01-XX | Advanced search, analytics, insights |
| 1.3.0 | Released | 2024-11-XX | Bookmarks, downloads |
| 1.2.0 | Released | 2024-09-XX | Cross-browser sync |
| 1.1.0 | Released | 2024-07-XX | Multi-browser support |
| 1.0.0 | Released | 2024-05-XX | Initial release |

---

## Contributing to the Roadmap

1. **Open an Issue** - Suggest features using the [Feature Request template](../../.github/ISSUE_TEMPLATE/feature_request.md)
2. **Join Discussions** - Participate in GitHub Discussions
3. **Code Contribution** - See [CONTRIBUTING.md](../../CONTRIBUTING.md) for development guidelines
4. **Security** - For security-related concerns, see [SECURITY.md](../../SECURITY.md)

---

## Last Updated

This roadmap was last updated: **May 2026**

*Note: Dates and timelines are estimates and may change based on contributor availability and project priorities.*