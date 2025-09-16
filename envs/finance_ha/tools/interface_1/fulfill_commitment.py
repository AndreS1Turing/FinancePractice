import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FulfillCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str, payment_amount: float, payment_date: str) -> str:
        
        commitments = data.get("commitments", {})
        
        if str(commitment_id) not in commitments:
            return json.dumps({"error": f"Commitment {commitment_id} not found"})
        
        commitment = commitments[str(commitment_id)]
        
        if commitment.get("status") == "fulfilled":
            return json.dumps({"error": "Commitment is already fulfilled"})
        
        timestamp = "2025-10-01T00:00:00"
        commitment["status"] = "fulfilled"
        commitment["updated_at"] = timestamp
        
        return json.dumps(commitment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fulfill_commitment",
                "description": "Updates the status of a commitment to 'fulfilled' upon receipt of payment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "The ID of the commitment to fulfill"},
                        "payment_amount": {"type": "number", "description": "The amount received from the investor"},
                        "payment_date": {"type": "string", "description": "The date the payment was received"}
                    },
                    "required": ["commitment_id", "payment_amount", "payment_date"]
                }
            }
        }
