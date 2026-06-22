const API_BASE = 'http://127.0.0.1:8001';

// Elements
const board = document.getElementById('ticket-board');
const modal = document.getElementById('ticket-modal');
const btnNewTicket = document.getElementById('btn-new-ticket');
const btnCloseModal = document.getElementById('btn-close-modal');
const ticketForm = document.getElementById('ticket-form');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatHistory = document.getElementById('chat-history');

// Initialization
document.addEventListener('DOMContentLoaded', fetchTickets);

// --- TICKET API ---

async function fetchTickets() {
    try {
        const res = await fetch(`${API_BASE}/tickets`);
        const tickets = await res.json();
        renderTickets(tickets);
    } catch (e) {
        console.error('Failed to fetch tickets:', e);
    }
}

async function createTicket(title, priority, status) {
    try {
        await fetch(`${API_BASE}/tickets`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, priority, status })
        });
        fetchTickets();
    } catch (e) {
        console.error('Failed to create ticket:', e);
    }
}

async function updateTicket(id, field, value) {
    try {
        await fetch(`${API_BASE}/tickets/${id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ [field]: value })
        });
        // We don't necessarily need to re-fetch all tickets, UI is optimistic
    } catch (e) {
        console.error('Failed to update ticket:', e);
    }
}

// --- UI RENDERING ---

function renderTickets(tickets) {
    board.innerHTML = '';
    // Reverse to show newest first
    tickets.reverse().forEach(t => {
        const card = document.createElement('div');
        card.className = 'ticket-card';
        
        card.innerHTML = `
            <div class="ticket-header">
                <span class="badge ${t.priority.toLowerCase()}">${t.priority}</span>
                <span class="ticket-id">#${t.id}</span>
            </div>
            <div class="ticket-title">${t.title}</div>
            <div class="ticket-controls">
                <select onchange="handleUpdate(${t.id}, 'status', this.value)">
                    <option value="Open" ${t.status === 'Open' ? 'selected' : ''}>Open</option>
                    <option value="In Progress" ${t.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
                    <option value="Resolved" ${t.status === 'Resolved' ? 'selected' : ''}>Resolved</option>
                    <option value="Closed" ${t.status === 'Closed' ? 'selected' : ''}>Closed</option>
                </select>
                <select onchange="handleUpdate(${t.id}, 'priority', this.value)">
                    <option value="Low" ${t.priority === 'Low' ? 'selected' : ''}>Low</option>
                    <option value="Medium" ${t.priority === 'Medium' ? 'selected' : ''}>Medium</option>
                    <option value="High" ${t.priority === 'High' ? 'selected' : ''}>High</option>
                    <option value="Unassigned" ${t.priority === 'Unassigned' ? 'selected' : ''}>Unassigned</option>
                </select>
            </div>
        `;
        board.appendChild(card);
    });
}

// Global handler for inline onChange
window.handleUpdate = (id, field, value) => {
    updateTicket(id, field, value);
};

// --- MODAL LOGIC ---

btnNewTicket.onclick = () => modal.classList.add('active');
btnCloseModal.onclick = () => modal.classList.remove('active');
modal.onclick = (e) => {
    if(e.target === modal) modal.classList.remove('active');
};

ticketForm.onsubmit = async (e) => {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const priority = document.getElementById('priority').value;
    const status = document.getElementById('status').value;
    
    await createTicket(title, priority, status);
    
    modal.classList.remove('active');
    ticketForm.reset();
};

// --- AI CHAT LOGIC ---

function appendMessage(msg, sender) {
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender}`;
    bubble.textContent = msg;
    chatHistory.appendChild(bubble);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

chatForm.onsubmit = async (e) => {
    e.preventDefault();
    const msg = chatInput.value.trim();
    if (!msg) return;

    // Display user message
    appendMessage(msg, 'user');
    chatInput.value = '';

    // Show typing indicator or something simple
    const typingBubble = document.createElement('div');
    typingBubble.className = 'chat-bubble ai';
    typingBubble.innerHTML = '<span style="opacity: 0.5;">...</span>';
    chatHistory.appendChild(typingBubble);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        const data = await res.json();
        
        // Remove typing indicator
        chatHistory.removeChild(typingBubble);
        
        // Display AI response
        appendMessage(data.reply, 'ai');
        
        // Automatically refresh board as the AI might have created a ticket!
        fetchTickets();
        
    } catch (err) {
        chatHistory.removeChild(typingBubble);
        appendMessage("System Error: Could not reach the Help Desk MCP.", "ai");
    }
};
