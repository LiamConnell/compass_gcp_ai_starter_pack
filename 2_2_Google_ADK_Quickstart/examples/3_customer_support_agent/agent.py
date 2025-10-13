"""
Customer support agent with knowledge base and ticketing
Run with: adk run 3_customer_support_agent
"""

from google.adk.agents.llm_agent import Agent
from datetime import datetime
import random

# Knowledge base
KNOWLEDGE_BASE = {
    "shipping": "Standard shipping takes 5-7 business days. Express shipping is 2-3 days.",
    "returns": "You can return items within 30 days for a full refund.",
    "warranty": "All products come with a 1-year manufacturer warranty.",
    "payment": "We accept credit cards, PayPal, and Apple Pay.",
}

def search_knowledge_base(topic: str) -> dict:
    """Search the knowledge base for information."""
    topic_lower = topic.lower()

    # Find matching topics
    results = []
    for key, value in KNOWLEDGE_BASE.items():
        if topic_lower in key or topic_lower in value.lower():
            results.append({"topic": key, "answer": value})

    return {
        "query": topic,
        "results": results if results else [{"topic": "general", "answer": "I don't have specific information on that. Let me create a ticket for you."}]
    }

def lookup_order(order_id: str) -> dict:
    """Look up order details."""
    # Mock order lookup
    statuses = ["processing", "shipped", "delivered", "cancelled"]

    return {
        "order_id": order_id,
        "status": random.choice(statuses),
        "items": ["Product A", "Product B"],
        "total": 149.99,
        "tracking_number": f"TRK{random.randint(100000, 999999)}" if random.random() > 0.5 else None,
        "estimated_delivery": "Dec 25, 2025"
    }

def create_support_ticket(customer_email: str, issue_type: str, description: str) -> dict:
    """Create a support ticket."""
    ticket_id = f"TKT-{random.randint(10000, 99999)}"

    return {
        "ticket_id": ticket_id,
        "customer_email": customer_email,
        "issue_type": issue_type,
        "description": description,
        "status": "open",
        "created_at": datetime.now().isoformat(),
        "assigned_to": "Support Team"
    }

def check_refund_status(order_id: str) -> dict:
    """Check refund status for an order."""
    statuses = ["processing", "approved", "completed"]

    return {
        "order_id": order_id,
        "refund_status": random.choice(statuses),
        "refund_amount": 149.99,
        "expected_date": "7-10 business days"
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='support_agent',
    description="Customer support agent for e-commerce",
    instruction="""You are a friendly and helpful customer support agent. Your goal is to:

    1. Answer customer questions using the knowledge base
    2. Look up order information when requested
    3. Create support tickets for issues that need escalation
    4. Check refund statuses

    Guidelines:
    - Always be polite and empathetic
    - Use the tools to get accurate information
    - If you can't help directly, create a support ticket
    - Confirm important details with customers
    - Provide order IDs and ticket IDs clearly

    Start by greeting the customer and asking how you can help.""",
    tools=[
        search_knowledge_base,
        lookup_order,
        create_support_ticket,
        check_refund_status
    ],
)
