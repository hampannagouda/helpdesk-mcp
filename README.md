# Help Desk Ticket MCP Server

A Model Context Protocol (MCP) server and RESTful API for managing IT support tickets. This project exposes essential help desk operations as MCP tools and HTTP endpoints, allowing AI assistants and web clients to interact with the ticket database programmatically.

## Architecture

This project is built using a modern, lightweight Python stack designed for fast iteration and compatibility with the Model Context Protocol.

- **Database Layer**: SQLite (`tickets.db`). All CRUD operations are abstracted through `db/db.py`.
- **MCP Server Layer**: Powered by `FastMCP`. Exposes database functions directly as AI-consumable tools over `stdio`.
- **API Layer**: Powered by `FastAPI`. Exposes the same database functions as standard RESTful endpoints (`POST`, `PATCH`, `GET`), allowing easy frontend integration and manual testing via Swagger UI.

## Setup Steps

1. **Prerequisites**: Ensure you have Python 3.8+ installed on your machine.
2. **Install Dependencies**:
   Install the required Python packages (FastAPI, Uvicorn, and MCP):
   ```bash
   pip install mcp fastapi uvicorn pydantic
   ```
3. **Initialize the Database**:
   Run the database script once to generate `tickets.db` and the corresponding tables.
   ```bash
   python db/db.py
   ```

### Running the Services

**To run the API Server (Swagger UI)**:
```bash
uvicorn api:app --reload
```
Once running, navigate to `http://127.0.0.1:8000/docs` in your browser to interact with the API visually.

**To run the MCP Server**:
```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```
*(This starts the interactive MCP Inspector, allowing you to test the AI tools directly in your browser)*

---

## Tools & Endpoints

### 🤖 MCP Tools
These tools are exposed via `mcp_server.py` for direct AI consumption:
- `create_ticket(title: str)`: Creates a new support ticket and returns the ID.
- `assign_priority(ticket_id: int, priority: str)`: Updates a ticket's priority level.
- `resolve_ticket(ticket_id: int)`: Marks a ticket's status as "Resolved".
- `list_open_tickets()`: Retrieves all active tickets with an "Open" status.

### 🌐 REST API Endpoints
These endpoints are exposed via `api.py`:
- `POST /tickets`: Create a new ticket (accepts title, optional priority and status).
- `GET /tickets`: Retrieve a list of all tickets.
- `PATCH /tickets/{id}`: Update an existing ticket's attributes (title, priority, status).

---

