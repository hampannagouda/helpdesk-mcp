from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional, List
from db.db import create_ticket, get_all_tickets, get_ticket_by_id, update_ticket

app = FastAPI(title="Help Desk Ticket API", description="API for managing Help Desk Tickets")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# Pydantic Models
class TicketCreate(BaseModel):
    title: str
    priority: Optional[str] = "Unassigned"
    status: Optional[str] = "Open"

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class TicketResponse(BaseModel):
    id: int
    title: str
    priority: Optional[str] = None
    status: Optional[str] = None

@app.post("/tickets", response_model=TicketResponse, status_code=201)
def api_create_ticket(ticket: TicketCreate):
    """
    Create a new support ticket.
    """
    ticket_id = create_ticket(title=ticket.title, priority=ticket.priority, status=ticket.status)
    return get_ticket_by_id(ticket_id)

@app.get("/tickets", response_model=List[TicketResponse])
def api_get_tickets():
    """
    Get a list of all tickets.
    """
    return get_all_tickets()

@app.patch("/tickets/{ticket_id}", response_model=TicketResponse)
def api_update_ticket(ticket_id: int, ticket: TicketUpdate):
    """
    Update an existing ticket by its ID.
    """
    existing_ticket = get_ticket_by_id(ticket_id)
    if not existing_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    update_data = ticket.model_dump(exclude_unset=True)
    if update_data:
        update_ticket(ticket_id, update_data)
        
    return get_ticket_by_id(ticket_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
