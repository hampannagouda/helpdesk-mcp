# Help Desk Ticket MCP Server

A Model Context Protocol (MCP) server for managing IT support tickets. This project exposes essential help desk operations as MCP tools, allowing AI assistants to interact with the ticket database programmatically.

## Overview

The Help Desk Ticket MCP Server is built using Python, SQLite, and the FastMCP library. It provides a structured database schema for tickets and will eventually expose both REST APIs and MCP tools for various help desk workflows.

### Core Features

- **Create support tickets** (Currently available via MCP tool)
- **Assign priority** (Planned)
- **Update ticket status** (Planned)
- **View open tickets** (Planned)
- **Assign tickets to support staff** (Planned)

## Project Structure

- `db/db.py`: Contains the SQLite database connection and operations (CRUD).
- `mcp_server.py`: The FastMCP server implementation that registers tools.
- `main.py`: A script to test basic database operations.
- `tickets.db`: The local SQLite database file.
- `requirements.md`, `disign.md`, `tasks.md`: Project documentation and specifications.

## Prerequisites

- Python 3.8+
- [mcp](https://pypi.org/project/mcp/) library (FastMCP)

Install dependencies using:
```bash
pip install mcp
```

## Running the Server

To start the MCP server:

```bash
python mcp_server.py
```

## Available MCP Tools

### `create_ticket(title: str) -> int`
Creates a new support ticket in the database.
- **Inputs**: `title` (String) - The issue description or title.
- **Outputs**: Returns the generated `ticket_id` (Integer).

## Development Phases

This project is being developed in phases:
1. **Phase 1-2**: Setup project structure and SQLite database.
2. **Phase 3-4**: MCP Server Development & Tools Layer (Current).
3. **Phase 5+**: API Endpoints, Business Logic, and Deployment.

Check `tasks.md` for a comprehensive list of tasks.
