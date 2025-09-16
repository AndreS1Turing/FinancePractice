import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, fund_id: str, amount: float,
               payment_details: Dict[str, Any], compliance_officer_approval: bool = False) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        subscriptions = data.get("subscriptions", {})
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        subscription_id = generate_id(subscriptions)
        timestamp = "2025-10-01T00:00:00"
        status = "approved" if compliance_officer_approval else "pending"
        
        new_subscription = {
            "subscription_id": subscription_id,
            "investor_id": investor_id,
            "fund_id": fund_id,
            "amount": amount,
            "status": status,
            "request_date": timestamp,
            "updated_at": timestamp
        }
        
        subscriptions[subscription_id] = new_subscription
        return json.dumps({"subscription_id": subscription_id, "success": True, "status": status})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_subscription",
                "description": "Processes an investor's request to subscribe to a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "The ID of the subscribing investor"},
                        "fund_id": {"type": "string", "description": "The ID of the fund to subscribe to"},
                        "amount": {"type": "number", "description": "The subscription amount"},
                        "payment_details": {"type": "object", "description": "Object containing payment information"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Optional approval from a Compliance Officer. If false, status is 'pending' (True/False)"}
                    },
                    "required": ["investor_id", "fund_id", "amount", "payment_details"]
                }
            }
        }
