## REPLACE YOURAWSPROFILE with your AWS cli profile name
"""
Multi Agent Orchestration using Amazon Strands - Customer Support System

This script demonstrates a multi-agent customer support system using Strands Swarm architecture.
Specialized agents handle: Technical Support, Billing, Product Information, and Order Status.
"""

import os
from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands.multiagent import Swarm


# Mock tools for specialized agents
@tool
def check_order_status(days_since_order: int = 3) -> dict:
    """Check the status of recent orders.
    
    Args:
        days_since_order: Number of days since the order was placed (default: 3)
    """
    return {
        "order_id": "ORD-2024-12345",
        "product": "Laptop - Model X Pro",
        "order_date": f"{days_since_order} days ago",
        "status": "Processing",
        "shipping_status": "Label created, awaiting carrier pickup",
        "estimated_delivery": "2-3 business days from pickup",
        "tracking_number": "1Z999AA10123456784"
    }


@tool
def investigate_charge(amount: float = 0.0) -> dict:
    """Investigate a billing charge on customer's account.
    
    Args:
        amount: The charge amount to investigate (optional)
    """
    return {
        "charge_type": "Express shipping upgrade",
        "amount": 15.99 if amount == 0.0 else amount,
        "description": "Expedited 2-day delivery service automatically applied",
        "valid": True,
        "can_refund": True,
        "note": "This charge can be removed if standard shipping is preferred"
    }


@tool
def get_product_info(product_type: str = "laptop") -> dict:
    """Get product information and recommendations.
    
    Args:
        product_type: Type of product (e.g., laptop, phone)
    """
    return {
        "product": product_type,
        "current_model": "Model X Pro",
        "alternatives": [
            {"name": "Model Y Ultra", "price": "$1299", "availability": "In stock", "delivery": "1-2 days"},
            {"name": "Model Z Elite", "price": "$1499", "availability": "In stock", "delivery": "Next day"}
        ],
        "features": "High performance, 16GB RAM, 512GB SSD, long battery life",
        "recommendation": "Model Y Ultra offers better value with faster delivery"
    }


@tool
def diagnose_technical_issue(issue_description: str) -> dict:
    """Diagnose a technical issue.
    
    Args:
        issue_description: Description of the technical problem
    """
    return {
        "issue": issue_description,
        "diagnosis": "Common connectivity issue",
        "steps": ["Restart device", "Check network settings", "Update firmware"]
    }


if __name__ == "__main__":
    print("Multi-Agent Orchestrator Demo")
    print("=" * 50)
    
    # Set AWS profile
    os.environ["AWS_PROFILE"] = "YOURAWSPROFILE"
    
    # Initialize model
    model = BedrockModel()
    
    # Create specialized agents
    orchestrator = Agent(
        name="orchestrator",
        model=model,
        system_prompt="""You are the central coordinator for customer support.
        
        Analyze customer requests and route to specialized agents:
        - technical_support: For technical issues and troubleshooting
        - billing_support: For billing inquiries and charges
        - product_info: For product details and recommendations
        - order_status: For order tracking and shipping
        
        Synthesize responses from multiple agents into a coherent answer.""",
        description="Central coordinator that routes requests and synthesizes responses"
    )
    
    technical_agent = Agent(
        name="technical_support",
        model=model,
        tools=[diagnose_technical_issue],
        system_prompt="""You are a technical support specialist.
        
        Diagnose technical issues and provide troubleshooting steps.
        Use the diagnose_technical_issue tool for problem analysis.
        Hand back to orchestrator when done.""",
        description="Handles technical issues and troubleshooting"
    )
    
    billing_agent = Agent(
        name="billing_support",
        model=model,
        tools=[investigate_charge],
        system_prompt="""You are a billing support specialist.
        
        Handle billing inquiries and investigate charges.
        Use the investigate_charge tool to check charges.
        Hand back to orchestrator when done.""",
        description="Handles billing inquiries and charge investigations"
    )
    
    product_agent = Agent(
        name="product_info",
        model=model,
        tools=[get_product_info],
        system_prompt="""You are a product information specialist.
        
        Provide product details and recommendations.
        Use the get_product_info tool for product data.
        Hand back to orchestrator when done.""",
        description="Provides product details and recommendations"
    )
    
    order_agent = Agent(
        name="order_status",
        model=model,
        tools=[check_order_status],
        system_prompt="""You are an order status specialist.
        
        Track orders and provide shipping updates.
        Use the check_order_status tool to check recent orders.
        Provide clear information about order status and shipping.
        Hand back to orchestrator when done.""",
        description="Tracks orders and provides shipping updates"
    )
    
    # Create swarm with all agents
    swarm = Swarm(
        [orchestrator, technical_agent, billing_agent, product_agent, order_agent],
        entry_point=orchestrator,
        max_handoffs=10,
        max_iterations=15,
        execution_timeout=300.0,
        node_timeout=120.0,
    )
    
    print("\nStrands Swarm Architecture Initialized!")
    print("\nSpecialized Agents:")
    print("  1. Orchestrator - Central coordinator")
    print("  2. Technical Support - Problem solver")
    print("  3. Billing Support - Financial specialist")
    print("  4. Product Information - Product expert")
    print("  5. Order Status - Logistics coordinator")
    
    print("\n" + "=" * 50)
    print("Sample Customer Query:")
    print("=" * 50)
    
    sample_query = """Hi, I ordered a laptop 3 days ago but haven't received any shipping 
confirmation. Also, I noticed an extra charge on my credit card that I 
don't understand. Can you help me figure out what's going on and maybe 
suggest a better laptop if this one is delayed?"""
    
    print(sample_query)
    
    print("\n" + "=" * 50)
    print("Processing with Strands Swarm...")
    print("=" * 50)
    
    # Execute swarm
    result = swarm(sample_query)
    
    print(f"\nExecution Status: {result.status}")
    print(f"\nAgent Collaboration Path:")
    for i, node in enumerate(result.node_history, 1):
        print(f"  {i}. {node.node_id}")
    
    print("\n" + "=" * 50)
    print("Final Response:")
    print("=" * 50)
    
    # Get final response from orchestrator or last agent
    final_agent = result.node_history[-1].node_id
    print(f"\n{result.results[final_agent].result}")
    
    print("\n" + "=" * 50)
    print("Architecture Benefits:")
    print("=" * 50)
    print("✓ Specialized expertise per domain")
    print("✓ Autonomous agent collaboration")
    print("✓ Scalable and maintainable design")
    print("✓ Dynamic routing based on query")
    print("✓ Clear separation of concerns")
    
    print("\n" + "=" * 50)
    print("Script completed successfully!")
    print("=" * 50)
