# Help Desk Ticket MCP Server - Design Document

## 1. System Overview

The Help Desk Ticket MCP Server is designed to manage support tickets through MCP tools and REST APIs.

Main features:
- Create support tickets
- Assign priority
- Update ticket status
- View open tickets
- Assign tickets to support staff

---

# 2. Database Schema

## Table: tickets

| Column Name   | Data Type     | Description |
|----------------|---------------|-------------|
| id             | INTEGER       | Primary Key |
| title          | TEXT          | Ticket title |
| description    | TEXT          | Issue description |
| priority       | TEXT          | Low / Medium / High |
| status         | TEXT          | Open / In Progress / Resolved / Closed |
| assigned_to    | TEXT          | Support staff name |
| created_at     | TIMESTAMP     | Ticket creation time |
| updated_at     | TIMESTAMP     | Last update time |

---

# 3. API Endpoints

## Create Ticket

POST /tickets

### Request Body

```json
{
  "title": "Laptop not working",
  "description": "System not booting"
}

### Response
{
  "id": 1,
  "status": "Open",
  "priority": "High"
}

Get All Tickets

GET /tickets

### Response
[
  {
    "id": 1,
    "title": "Laptop not working",
    "status": "Open"
  }
]

Update Ticket Status

PUT /tickets/{id}/status

### Request Body
{
  "status": "Resolved"
}

Assign Ticket

PUT /tickets/{id}/assign

### Request Body
{
  "assigned_to": "Support Team A"
}

MCP Tools
create_ticket()

Creates a new support ticket.

### Input
{
  "title": "Laptop issue",
  "description": "Screen is blank"
}

### Output
{
  "ticket_id": 1,
  "status": "Open"
}

assign_priority()

Assigns priority based on issue severity.

### Input
{
  "ticket_id": 1
}

### Output
{
  "priority": "High"
}

update_status()

Updates ticket status.

### Input
{
  "ticket_id": 1,
  "status": "Resolved"
}

list_open_tickets()

Returns all open tickets.

### Output
[
  {
    "ticket_id": 1,
    "title": "Laptop issue"
  }
]

5. System Flow
    1. User creates a ticket.
    2. System generates ticket ID.
    3. MCP server assigns priority.
    4. Ticket is stored in database.
    5. Support team updates status.
    6. Users can list and track tickets.

6. Future Improvements
    1. Authentication system
    2. Email notifications
    3. Dashboard UI
    4. AI-based priority prediction
    5. Ticket analytics