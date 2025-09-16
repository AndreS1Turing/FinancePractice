import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, fund_id: str, amount: float,
               due_date: str, compliance_officer_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        commitments = data.get("commitments", {})
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance officer approval is required"})
        
        commitment_id = generate_id(commitments)
        timestamp = "2025-10-01T00:00:00"
        
        new_commitment = {
            "commitment_id": commitment_id,
            "investor_id": investor_id,
            "fund_id": fund_id,
            "commitment_amount": amount,
            "due_date": due_date,
            "status": "pending",
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        commitments[commitment_id] = new_commitment
        return json.dumps({"commitment_id": commitment_id, "success": True, "status": "pending"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_commitment",
                "description": "Records a new legally binding commitment from an investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "The ID of the investor making the commitment"},
                        "fund_id": {"type": "string", "description": "The ID of the fund receiving the commitment"},
                        "amount": {"type": "number", "description": "The committed capital amount"},
                        "due_date": {"type": "string", "description": "The due date for the capital contribution"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Approval from a Compliance Officer (True/False)"}
                    },
                    "required": ["investor_id", "fund_id", "amount", "due_date", "compliance_officer_approval"]
                }
            }
        }
