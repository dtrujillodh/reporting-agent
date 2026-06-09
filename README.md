# 📊 Reporting Agent (ADK + MCP)

This agent automates the creation of monthly reports by extracting data from Google Drive files (Docs and Slides) and generating a formatted Google Doc report.

## Architecture

- **ADK Agent**: Orchestrates the reporting logic and data synthesis.
- **MCP Server**: Provides tools to interact with Google Drive, Docs, and Slides.
- **Google Workspace APIs**: The underlying data source.

## Setup

1. **Google Cloud Project**: Ensure you have a project with Drive and Docs APIs enabled.
2. **Authentication**: Use a Service Account and share your Drive folder with its email.
3. **Environment Variables**:
   ```env
   GOOGLE_CLOUD_PROJECT=dh-imd
   GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
   ```

## Development

### Install Dependencies
```bash
uv sync
```

### Run MCP Server
```bash
uv run mcp-server/server.py
```

### Run ADK Agent
```bash
uv run agent/agent.py
```
