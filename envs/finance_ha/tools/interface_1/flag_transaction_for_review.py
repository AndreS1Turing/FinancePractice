import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FlagTransactionForReview(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], transaction_id: str, reason: str, compliance_officer_id: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        audit_trails = data.get("audit_trails", {})
        
        if str(compliance_officer_id) not in users:
            return json.dumps({"error": f"Compliance officer {compliance_officer_id} not found"})
        
        # Check if user has compliance officer role
        user = users[str(compliance_officer_id)]
        if user.get("role") != "compliance_officer":
            return json.dumps({"error": "Only compliance officers can flag transactions"})
        
        # Create audit trail entry
        audit_id = generate_id(audit_trails)
        timestamp = "2025-10-01T00:00:00"
        
        new_audit_entry = {
            "audit_trail_id": audit_id,
            "user_id": compliance_officer_id,
            "action": "flag_for_review",
            "target_entity": "transaction",
            "target_id": transaction_id,
            "details": f"Transaction flagged for review. Reason: {reason}",
            "created_at": timestamp
        }
        
        audit_trails[audit_id] = new_audit_entry
        return json.dumps(new_audit_entry)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "flag_transaction_for_review",
                "description": "Allows a Compliance Officer to flag a transaction for further investigation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "transaction_id": {"type": "string", "description": "The ID of the transaction (e.g., trade_id, subscription_id)"},
                        "reason": {"type": "string", "description": "The reason for flagging the transaction"},
                        "compliance_officer_id": {"type": "string", "description": "The ID of the officer flagging the transaction"}
                    },
                    "required": ["transaction_id", "reason", "compliance_officer_id"]
                }
            }
        }
