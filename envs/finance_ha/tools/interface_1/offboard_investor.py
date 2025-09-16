import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class OffboardInvestor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, compliance_officer_approval: bool) -> str:
        
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        redemptions = data.get("redemptions", {})
        
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance officer approval is required"})
        
        # Check for pending transactions
        pending_transactions = []
        for sub in subscriptions.values():
            if sub.get("investor_id") == investor_id and sub.get("status") == "pending":
                pending_transactions.append("subscription")
                
        for red in redemptions.values():
            if red.get("investor_id") == investor_id and red.get("status") == "pending":
                pending_transactions.append("redemption")
        
        if pending_transactions:
            return json.dumps({"error": "Cannot offboard investor with pending transactions"})
        
        timestamp = "2025-10-01T00:00:00"
        investors[str(investor_id)]["status"] = "archived"
        investors[str(investor_id)]["updated_at"] = timestamp
        
        return json.dumps(investors[str(investor_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "offboard_investor",
                "description": "Changes an investor's status to inactive and archives their data. This action cannot proceed if there are pending transactions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "The ID of the investor to offboard"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Flag indicating approval from a Compliance Officer (True/False)"}
                    },
                    "required": ["investor_id", "compliance_officer_approval"]
                }
            }
        }
