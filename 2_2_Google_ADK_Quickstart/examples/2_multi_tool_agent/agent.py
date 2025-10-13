"""
Agent with multiple tools for different tasks
Run with: adk run 2_multi_tool_agent
"""

from google.adk.agents.llm_agent import Agent
import random

def search_products(query: str, max_results: int = 5) -> dict:
    """Search for products in the catalog."""
    # Mock product search
    products = [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Mouse", "price": 29.99},
        {"id": 3, "name": "Keyboard", "price": 79.99},
        {"id": 4, "name": "Monitor", "price": 299.99},
        {"id": 5, "name": "Headphones", "price": 149.99},
    ]

    # Simple matching
    results = [p for p in products if query.lower() in p["name"].lower()]
    return {
        "query": query,
        "results": results[:max_results],
        "count": len(results)
    }

def check_inventory(product_id: int) -> dict:
    """Check inventory status for a product."""
    # Mock inventory check
    in_stock = random.choice([True, False])
    quantity = random.randint(0, 50) if in_stock else 0

    return {
        "product_id": product_id,
        "in_stock": in_stock,
        "quantity": quantity,
        "warehouse": "Main Warehouse" if in_stock else "None"
    }

def create_order(product_id: int, quantity: int, customer_email: str) -> dict:
    """Create a new order."""
    order_id = f"ORD-{random.randint(10000, 99999)}"

    return {
        "order_id": order_id,
        "product_id": product_id,
        "quantity": quantity,
        "customer_email": customer_email,
        "status": "pending",
        "estimated_delivery": "3-5 business days"
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='shopping_assistant',
    description="E-commerce assistant that helps with product search and orders.",
    instruction="""You are a helpful shopping assistant. You can:
    1. Search for products
    2. Check inventory status
    3. Create orders for customers

    Always be helpful and provide clear information. When creating orders,
    make sure to confirm the details with the customer first.""",
    tools=[search_products, check_inventory, create_order],
)
