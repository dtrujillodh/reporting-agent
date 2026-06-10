# Reporting Agent

The Reporting Agent is a specialized system for automating data extraction and report generation from Google Workspace assets using the ADK framework and MCP.

## Overview

This agent streamlines the creation of reports by leveraging:
- **ADK Agent**: Orchestrates data synthesis.
- **MCP Server**: Provides secure, tool-based access to Google Drive, Docs, and Slides.

## Quick Start

### Prerequisites
- Google Cloud Project with Drive and Docs APIs enabled.
- A service account configured for the workspace.

### Local Development
1. Install dependencies:
   ```bash
   uv sync
   ```
2. Run the services:
   ```bash
   # Run the MCP server
   uv run mcp-server/server.py
   # Run the agent
   uv run agent/agent.py
   ```

## Development
- Build the frontend: `cd frontend && npm install && npm run build`
- Run the backend: `uv run python backend/main.py`

## Deployment
This project is containerized for easy deployment to Cloud Run. See `RUNNING_LOCALLY.md` for local Docker instructions.

## Contributing
Please refer to `CONTRIBUTING.md` for guidelines.

## License
Confidential - Internal Use Only.
