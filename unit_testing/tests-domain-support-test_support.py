# Test Support 

import unittest
from datetime import datetime
from domain.support.support_service import SupportTicket, SupportService, SupportTicketStatus

class TestSupportService(unittest.TestCase):
    def setUp(self):
        self.service = SupportService()
        self.ticket_data = {
            "ticket_id": "ticket123",
            "user_id": "user456",
            "issue_type": "payment",
            "description": "Payment not reflected",
            "priority": 2
        }

    def test_ticket_creation(self):
        ticket = SupportTicket(**self.ticket_data)
        self.assertEqual(ticket.status, SupportTicketStatus.OPEN)
        self.assertEqual(ticket.priority, 2)
        self.assertIsNone(ticket.assigned_to)

    def test_ticket_lifecycle(self):
        ticket = SupportTicket(**self.ticket_data)
        
        # Add comment
        ticket.add_comment("Looking into this", "agent1")
        self.assertEqual(len(ticket.comments), 1)
        
        # Update status
        ticket.update_status(SupportTicketStatus.IN_PROGRESS)
        self.assertEqual(ticket.status, SupportTicketStatus.IN_PROGRESS)

    def test_service_operations(self):
        # Create ticket through service
        ticket = self.service.create_ticket(
            self.ticket_data["user_id"],
            self.ticket_data["issue_type"],
            self.ticket_data["description"]
        )
        self.assertIn(ticket.ticket_id, self.service.tickets)
        
        # Assign ticket
        self.service.assign_ticket(ticket.ticket_id, "agent1")
        self.assertEqual(
            self.service.tickets[ticket.ticket_id].assigned_to,
            "agent1"
        )
        self.assertEqual(
            self.service.tickets[ticket.ticket_id].status,
            SupportTicketStatus.IN_PROGRESS
        )

    def test_nonexistent_ticket(self):
        with self.assertRaises(ValueError):
            self.service.assign_ticket("nonexistent", "agent1")

if __name__ == '__main__':
    unittest.main()