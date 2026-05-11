from mcp.server.fastmcp import FastMCP
from db.db import create_ticket as db_create_ticket

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

if __name__ == "__main__":
    mcp.run()
