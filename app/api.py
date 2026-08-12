from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import json
import re
import requests
from dotenv import load_dotenv
from google import genai
from app.db import create_ticket, get_all_tickets, get_ticket_by_id, update_ticket

# Load environment variables
load_dotenv()
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").strip().lower()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3.5-mini")
ANTHROPIC_API_URL = os.getenv("ANTHROPIC_API_URL", "https://api.anthropic.com/v1/complete")

gemini_client = None
if AI_PROVIDER == "gemini":
    try:
        gemini_client = genai.Client()
    except Exception as e:
        gemini_client = None
        print("Warning: Failed to initialize Gemini Client. Make sure GEMINI_API_KEY is set in .env")

if AI_PROVIDER in ["claude", "anthropic"] and not ANTHROPIC_API_KEY:
    print("Warning: ANTHROPIC_API_KEY is not set in .env. Claude will not work until it is configured.")

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
    Real AI endpoint using the configured AI provider.
    """
    try:
        if AI_PROVIDER == "gemini":
            if not gemini_client:
                return {"reply": "System Error: The Gemini API is not configured properly. Please check the .env file."}
            response = gemini_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"You are a helpful IT Support Agent. The user says: '{chat.message}'",
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': AIResponse,
                },
            )
            ai_data = response.parsed

        elif AI_PROVIDER in ["claude", "anthropic"]:
            if not ANTHROPIC_API_KEY:
                return {"reply": "System Error: The Claude API key is not configured. Please check the .env file."}

            anthropic_request = {
                "model": ANTHROPIC_MODEL,
                "instructions": (
                    "You are a helpful IT Support Agent. "
                    "The user says: '" + chat.message + "'"
                ),
                "temperature": 0.2,
                "max_tokens_to_sample": 1000,
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "type": "object",
                        "properties": {
                            "should_create_ticket": {"type": "boolean"},
                            "ticket_title": {"type": ["string", "null"]},
                            "ticket_priority": {"type": ["string", "null"]},
                            "reply_to_user": {"type": "string"}
                        },
                        "required": ["should_create_ticket", "reply_to_user"]
                    }
                }
            }

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-API-Key": ANTHROPIC_API_KEY,
            }
            claude_url = ANTHROPIC_API_URL
            response = requests.post(claude_url, headers=headers, json=anthropic_request, timeout=30)
            response.raise_for_status()
            json_response = response.json()
            text = json_response.get("completion") or ""

            # Extract JSON body from Claude response text.
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                raise ValueError("Unable to parse Claude JSON response")
            parsed_json = json.loads(match.group(0))

            class ParsedResponse:
                pass
            ai_data = ParsedResponse()
            ai_data.should_create_ticket = parsed_json.get("should_create_ticket")
            ai_data.ticket_title = parsed_json.get("ticket_title")
            ai_data.ticket_priority = parsed_json.get("ticket_priority")
            ai_data.reply_to_user = parsed_json.get("reply_to_user")

        else:
            return {"reply": "System Error: Unknown AI_PROVIDER setting. Use 'gemini' or 'claude'."}

        if ai_data.should_create_ticket:
            title = ai_data.ticket_title or "AI Logged Issue"
            priority = ai_data.ticket_priority or "Unassigned"
            if priority not in ["Low", "Medium", "High", "Unassigned"]:
                priority = "Unassigned"
            t_id = create_ticket(title=title, priority=priority)
            reply = f"{ai_data.reply_to_user}\n\n*(Ticket #{t_id} automatically created with {priority} priority)*"
        else:
            reply = ai_data.reply_to_user

        return {"reply": reply}

    except Exception as e:
        print(f"AI Error: {e}")
        return {"reply": "Sorry, I ran into an error connecting to my AI brain! Make sure your API key is valid."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
