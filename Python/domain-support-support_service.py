# Customer Support

from enum import Enum
from datetime import datetime

class SupportTicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class SupportTicket:
    def __init__(self, ticket_id: str, user_id: str, issue_type: str, description: str, priority: int = 3):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.issue_type = issue_type
        self.description = description
        self.priority = priority
        self.status = SupportTicketStatus.OPEN
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.assigned_to = None
        self.comments = []

    def add_comment(self, comment: str, author: str):
        self.comments.append({
            'timestamp': datetime.utcnow(),
            'author': author,
            'comment': comment
        })
        self.updated_at = datetime.utcnow()

    def update_status(self, new_status: SupportTicketStatus):
        self.status = new_status
        self.updated_at = datetime.utcnow()

class SupportService:
    def __init__(self):
        self.tickets = {}
        self.agents = {}

    def create_ticket(self, user_id: str, issue_type: str, 
                     description: str) -> SupportTicket:
        ticket_id = f"ticket_{len(self.tickets) + 1}"
        ticket = SupportTicket(ticket_id, user_id, issue_type, description)
        self.tickets[ticket_id] = ticket
        return ticket

    def assign_ticket(self, ticket_id: str, agent_id: str):
        if ticket_id not in self.tickets:
            raise ValueError("Ticket not found")
            
        self.tickets[ticket_id].assigned_to = agent_id
        self.tickets[ticket_id].update_status(SupportTicketStatus.IN_PROGRESS)