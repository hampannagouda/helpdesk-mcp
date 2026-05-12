from mcp.server.fastmcp import FastMCP
from app.db import (
    create_ticket as db_create_ticket,
    update_ticket_priority as db_update_priority,
    update_ticket_status as db_update_status,
    get_open_tickets as db_get_open_tickets
)

# Initialize FastMCP server
mcp = FastMCP("HelpDesk")

@mcp.tool()
def create_ticket(title: str) -> int:
    """
    Create a new support ticket.
    
    Args:
        title: The title or description of the ticket.
    
    Returns:
        The ID of the newly created ticket.
    """
    ticket_id = db_create_ticket(title=title)
    return ticket_id

@mcp.tool()
def assign_priority(ticket_id: int, priority: str) -> str:
    """
    Assign a priority to a specific ticket.
    
    Args:
        ticket_id: The ID of the ticket.
        priority: The priority level (e.g. Low, Medium, High).
    """
    db_update_priority(ticket_id, priority)
    return f"Priority '{priority}' assigned to ticket {ticket_id}."

@mcp.tool()
def resolve_ticket(ticket_id: int) -> str:
    """
    Resolve a specific ticket by changing its status to 'Resolved'.
    
    Args:
        ticket_id: The ID of the ticket.
    """
    db_update_status(ticket_id, "Resolved")
    return f"Ticket {ticket_id} has been marked as Resolved."

@mcp.tool()
def list_open_tickets() -> list:
    """
    List all tickets that have a status of 'Open'.
    
    Returns:
        A list of dictionaries representing the open tickets.
    """
    return db_get_open_tickets()

if __name__ == "__main__":
    mcp.run()
