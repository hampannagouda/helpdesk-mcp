from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from dotenv import load_dotenv
from google import genai
from db.db import create_ticket, get_all_tickets, get_ticket_by_id, update_ticket

# Load environment variables
load_dotenv()
try:
    gemini_client = genai.Client()
except Exception as e:
    gemini_client = None
    print("Warning: Failed to initialize Gemini Client. Make sure GEMINI_API_KEY is set in .env")

app = FastAPI(title="Help Desk Ticket API", description="API for managing Help Desk Tickets")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

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

class AIResponse(BaseModel):
    should_create_ticket: bool = Field(description="Set to true if the user's message is reporting an issue or problem that requires a support ticket. Set to false if they are just asking a general question, saying hello, or asking who you are.")
    ticket_title: Optional[str] = Field(description="If creating a ticket, summarize the user's issue into a short, descriptive title (e.g. 'Laptop will not turn on')")
    ticket_priority: Optional[str] = Field(description="If creating a ticket, determine the priority: 'Low', 'Medium', or 'High'")
    reply_to_user: str = Field(description="A polite, helpful conversational reply to the user. If a ticket is being created, mention the issue and priority. If no ticket is created, just answer their question.")

@app.post("/chat", response_model=ChatResponse)
def api_chat(chat: ChatMessage):
    """
    Real AI endpoint using Google Gemini to process natural language requests.
    """
    if not gemini_client:
        return {"reply": "System Error: The Gemini API is not configured properly. Please check the .env file."}
        
    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"You are a helpful IT Support Agent. The user says: '{chat.message}'",
            config={
                'response_mime_type': 'application/json',
                'response_schema': AIResponse,
            },
        )
        
        # Parse the structured response
        ai_data = response.parsed
        
        # If the AI decided this requires a ticket, create it!
        if ai_data.should_create_ticket:
            title = ai_data.ticket_title or "AI Logged Issue"
            priority = ai_data.ticket_priority or "Unassigned"
            # Ensure priority is valid
            if priority not in ["Low", "Medium", "High", "Unassigned"]:
                priority = "Unassigned"
                
            t_id = create_ticket(title=title, priority=priority)
            reply = f"{ai_data.reply_to_user}\n\n*(Ticket #{t_id} automatically created with {priority} priority)*"
        else:
            reply = ai_data.reply_to_user
            
        return {"reply": reply}
        
    except Exception as e:
        print(f"Gemini Error: {e}")
        return {"reply": "Sorry, I ran into an error connecting to my AI brain! Make sure your API key is valid."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
